#!/usr/bin/env python3
"""對標清單：找中文 Shorts 頻道，按「最近 30 支 Shorts 的播放中位數」排名。零 token。

  python3 scripts/benchmarks.py            # 搜尋＋量測，寫 refs/benchmarks.tsv 與 refs/BENCHMARKS.md
  python3 scripts/benchmarks.py --top 15   # 報告每題取前幾名

為什麼用中位數不用總觀看：要找「每支流量都高」的帳號（格式本身有效），
不是靠一兩支爆款撐起來的帳號。中位數不受單支爆款影響。

兩步：
1. 發現：每個主題幾組關鍵字打 YouTube Data API search.list（order=viewCount、videoDuration=short、
   近 SEARCH_DAYS 天），videos.list 補播放數，留下有一支 ≥ MIN_SEED_VIEWS 的頻道。
   權杖沿用 publish/tokens.py 的 YouTube OAuth。配額：search 每次 100 單位、videos 每 50 支 1 單位，日上限 1 萬。
   初版用 yt-dlp 搜尋只能相關度排序，撈不到近期爆款（AI 類第一名中位數才 7.8 萬）。
2. 量測：抓每個頻道 /shorts 頁最近 N 支的播放數。沒有 Shorts 頁的頻道丟掉。

離群值＝發現階段那支的播放 ÷ 頻道中位數：高代表那支是內容本身爆，不是頻道底盤大，② 拆解優先挑這種。

ponytail: 只量 YouTube。IG／抖音沒有免費的播放數介面（見 2026-10-13 輪子卡），要擴就接 agent-reach。
"""
import argparse
import concurrent.futures as cf
import datetime as dt
import html
import json
import re
import statistics
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "publish"))
import tokens  # noqa: E402
# 爆款第一（2026-10-14）：主題只用來分組，「不限」才是主榜。
# 「不限」不帶關鍵字，把近 SEARCH_DAYS 天切成 FREE_WINDOWS 段各撈一頁，題型由結果決定，不由我們先猜。
FREE = "不限"
FREE_WINDOWS = 6
TOPICS = {
    FREE: [""],
    "AI": ["AI 冷知識", "ChatGPT 技巧", "AI 工具 推薦", "人工智慧 科普", "AI 新聞 shorts",
           "AI", "ChatGPT", "AI 教學", "AI 繪圖", "AI 影片", "Gemini", "Claude AI"],
    "區塊鏈": ["比特幣", "幣圈 新手", "加密貨幣 科普", "區塊鏈 是什麼", "虛擬貨幣 shorts"],
    "金融": ["理財 知識", "投資 冷知識", "存錢 方法", "經濟學 冷知識", "股票 新手 shorts"],
    "防詐": ["詐騙 手法", "防詐騙", "詐騙集團 揭密", "投資詐騙"],
    "台灣": ["台灣 冷知識", "台灣人 不知道", "台灣 歷史 shorts"],
    "品牌原型": ["反直覺 冷知識", "悖論", "機率 反直覺", "心理學 冷知識"],
}
# 主題歸屬看頻道自己最近的標題，不看是被哪組搜尋字找到的：
# 搜尋只是撈候選，一個遊戲頻道剛好有一支標題含 AI 不代表它是 AI 頻道（初版就把 JJJacksfilms 排進 AI 第一）。
TOPIC_WORDS = {
    "AI": ["AI", "ChatGPT", "GPT", "人工智慧", "人工智能", "Claude", "Gemini", "機器人", "机器人", "演算法", "算法"],
    "區塊鏈": ["比特幣", "比特币", "BTC", "幣圈", "币圈", "區塊鏈", "区块链", "加密貨幣", "加密货币", "以太", "ETH",
             "虛擬貨幣", "虚拟货币", "NFT", "交易所", "幣安", "币安"],
    "金融": ["理財", "理财", "投資", "投资", "股票", "股市", "台股", "美股", "ETF", "0050", "存錢", "存钱",
           "經濟", "经济", "利率", "通膨", "通胀", "退休", "財富", "财富"],
    "防詐": ["詐騙", "诈骗", "騙", "骗", "165", "釣魚", "钓鱼", "盜刷", "盗刷", "詐", "诈"],
    "台灣": ["台灣", "台湾", "臺灣", "台北", "高雄", "台中", "台南", "新竹"],
    "品牌原型": ["冷知識", "冷知识", "為什麼", "为什么", "悖論", "悖论", "機率", "概率", "心理", "數學", "数学",
             "科學", "科学", "反直覺", "反直觉"],
}
TOPIC_SHARE_MIN = 0.2   # 最近標題至少兩成含主題詞，才算這個主題的頻道
CJK_SHARE_MIN = 0.5     # 中文標題不到一半的頻道不收（我們做中文）
SEARCH_N = 50          # search.list 單頁上限
SEARCH_DAYS = 90
MIN_SEED_VIEWS = 10_000
HOT_MEDIAN_MIN = 1_000  # 離群榜的頻道中位數下限：中位數幾十的多是搬運或死頻道，除出來的倍數沒意義
SHORTS_N = 30
# 預設介面 YouTube 會把標題自動翻成英文，主題詞比不到；
# 換 zh-TW 介面標題對了，但「萬次觀看」yt-dlp 解析不了、播放數變 NA。所以頻道頁抓兩次再用網址合併。
ZH = ["--extractor-args", "youtube:lang=zh-TW"]


def _hit(word, title):
    # 英文詞要整詞比對：子字串的話「AI」會比到 taiwan、chill 裡的 a-i（第二輪實測誤判）
    if word.isascii():
        return re.search(rf"(?<![A-Za-z]){re.escape(word)}(?![A-Za-z])", title, re.I) is not None
    return word in title


def topic_shares(titles):
    return {t: sum(any(_hit(w, s) for w in ws) for s in titles) / len(titles)
            for t, ws in TOPIC_WORDS.items()}


def cjk_share(titles):
    # 有假名就是日文：漢字也落在 CJK 區段，只看漢字會把日本頻道當中文（10-14 實測 AI、金融第一名都是日本頻道）
    return sum(bool(re.search(r"[㐀-鿿]", s)) and not re.search(r"[ぁ-ゟ゠-ヿ]", s) for s in titles) / len(titles)


def ytdlp_json(url, n, extra=()):
    r = subprocess.run(["yt-dlp", url, "--flat-playlist", "--no-warnings", *extra, "-I", f"1:{n}", "-J"],
                       capture_output=True, text=True, timeout=180)
    if r.returncode != 0 or not r.stdout.strip():
        return None
    return json.loads(r.stdout)


def yt_api(path, **params):
    req = urllib.request.Request(f"https://www.googleapis.com/youtube/v3/{path}?" + urllib.parse.urlencode(params),
                                 headers={"Authorization": "Bearer " + tokens.read("YT_ACCESS_TOKEN")})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:   # 配額用完是 403 quotaExceeded，原文丟出來
        raise RuntimeError(f"HTTP {e.code} {path}\n{e.read().decode(errors='replace')}") from None


def search(q, after, before=None):
    """search.list 依觀看排序 → videos.list 補播放數。回 [(channel_id, channel, views, title, url)]"""
    p = dict(part="snippet", type="video", order="viewCount", videoDuration="short",
             publishedAfter=after, regionCode="TW", relevanceLanguage="zh-Hant", maxResults=SEARCH_N)
    if q:
        p["q"] = q
    if before:
        p["publishedBefore"] = before
    d = yt_api("search", **p)
    ids = [i["id"]["videoId"] for i in d.get("items", [])]
    if not ids:
        return []
    v = yt_api("videos", part="snippet,statistics", id=",".join(ids))
    return [(i["snippet"]["channelId"], i["snippet"]["channelTitle"], int(i["statistics"].get("viewCount", 0)),
             html.unescape(i["snippet"]["title"]), f"https://www.youtube.com/shorts/{i['id']}")
            for i in v.get("items", [])]


def discover():
    """回 {channel_id: {"name", "topics": set, "seed": (views, title, url)}}"""
    if tokens.yt_refresh() == "未登入":
        sys.exit("YouTube 未登入，先跑 scripts/publish/tokens.py login yt")
    now = dt.datetime.now(dt.timezone.utc)
    jobs = []
    for t, qs in TOPICS.items():
        spans = windows(now, SEARCH_DAYS, FREE_WINDOWS) if t == FREE else [(_iso(now - dt.timedelta(days=SEARCH_DAYS)), None)]
        jobs += [(t, q, a, b) for q in qs for a, b in spans]
    print(f"  search.list {len(jobs)} 次，約 {len(jobs) * 101} 配額單位", file=sys.stderr)
    found = {}
    with cf.ThreadPoolExecutor(4) as ex:
        for (topic, q, _, _), hits in zip(jobs, ex.map(lambda j: search(j[1], j[2], j[3]), jobs)):
            for cid, name, v, title, url in hits:
                if v < MIN_SEED_VIEWS:
                    continue
                c = found.setdefault(cid, {"name": name, "topics": set(), "seed": (0, "", "")})
                c["topics"].add(topic)
                if v > c["seed"][0]:
                    c["seed"] = (v, title, url)
            print(f"  搜尋 {topic}/{q}：累計 {len(found)} 個頻道", file=sys.stderr)
    return found


def _iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def windows(now, days, k):
    """把近 days 天切成 k 段不重疊的 (after, before)，新的在前。"""
    step = dt.timedelta(days=days) / k
    return [(_iso(now - step * (i + 1)), _iso(now - step * i)) for i in range(k)]


def ranked(rows, topic, n):
    """rows 已依中位數排好；「不限」取全部，其餘只取該主題的頻道。"""
    return (rows if topic == FREE else [r for r in rows if topic in r["topics"]])[:n]


def previous(tsv):
    """上一輪 benchmarks.tsv 的頻道 → discover() 同形狀。tsv 有版控，raw.json 沒有。"""
    if not tsv.exists():
        return {}
    lines = tsv.read_text(encoding="utf-8").splitlines()
    head = lines[0].split("\t")
    out = {}
    for line in lines[1:]:
        r = dict(zip(head, line.split("\t")))
        cid = r["url"].split("/channel/")[1].split("/")[0]
        seed = (int(r["seed_views"]), r["seed_title"], r["seed_url"]) if r.get("seed_views") else (0, "", "")
        out[cid] = {"name": r["name"], "topics": set(), "seed": seed}
    return out


def outlier(seed_views, median):
    return seed_views / median if median else 0.0


def measure(cid):
    d = ytdlp_json(f"https://www.youtube.com/channel/{cid}/shorts", SHORTS_N)
    entries = [e for e in (d or {}).get("entries") or [] if e and e.get("view_count")]
    views = [e["view_count"] for e in entries]
    if len(views) < 5:   # 太少支算不出中位數的意義
        return None
    zh = ytdlp_json(f"https://www.youtube.com/channel/{cid}/shorts", SHORTS_N, ZH)
    zh_title = {e.get("url"): e.get("title") for e in (zh or {}).get("entries") or [] if e}
    for e in entries:
        e["title"] = zh_title.get(e.get("url")) or e.get("title") or ""
    titles = [e["title"] for e in entries]
    if cjk_share(titles) < CJK_SHARE_MIN:
        return None
    top = max(entries, key=lambda e: e["view_count"])
    return {
        "titles": titles,
        "median": int(statistics.median(views)),
        "hit100k": sum(v >= 100_000 for v in views) / len(views),
        "n": len(views),
        "subs": d.get("channel_follower_count"),
        "handle": d.get("uploader_id") or "",
        "top": (top["view_count"], top.get("title") or "", top.get("url") or ""),
    }


def fmt(n):
    if n is None:
        return "—"
    return f"{n / 10_000:.1f} 萬" if n >= 10_000 else str(n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--cached", action="store_true", help="用 refs/benchmarks-raw.json，不重抓")
    a = ap.parse_args()

    raw = ROOT / "refs" / "benchmarks-raw.json"
    if a.cached:   # 只改判準時不用重抓（全量一次約 15 分鐘）
        found_n, rows = json.loads(raw.read_text(encoding="utf-8"))
    else:
        found = discover()
        # 累加不覆蓋：上一輪的頻道也重量一次。search.list 只看近 90 天，
        # 只靠它的話舊的頭部（四處觀察、cheap）會掉出清單。
        for cid, c in previous(ROOT / "refs" / "benchmarks.tsv").items():
            found.setdefault(cid, c)
        found_n = len(found)
        print(f"量測 {found_n} 個頻道的 Shorts 頁…", file=sys.stderr)
        with cf.ThreadPoolExecutor(4) as ex:
            stats = dict(zip(found, ex.map(measure, found)))
        rows = [{"id": cid, "name": found[cid]["name"], "seed": found[cid]["seed"], **s}
                for cid, s in stats.items() if s]
        raw.write_text(json.dumps([found_n, rows], ensure_ascii=False), encoding="utf-8")
    for r in rows:   # 主題看頻道自己的標題，不看搜尋階段的猜測
        r["shares"] = topic_shares(r["titles"])
        r["topics"] = {t for t, v in r["shares"].items() if v >= TOPIC_SHARE_MIN}
        r["seed"] = r.get("seed") or (0, "", "")   # 舊版 raw 沒存發現那支
        r["outlier"] = outlier(r["seed"][0], r["median"])
    rows.sort(key=lambda r: r["median"], reverse=True)

    tsv = ROOT / "refs" / "benchmarks.tsv"
    with tsv.open("w", encoding="utf-8") as f:
        f.write("median\thit100k\tn\tsubs\ttopics\tname\turl\ttop_views\ttop_title\t"
                "outlier\tseed_views\tseed_title\tseed_url\n")
        for r in rows:
            f.write(f"{r['median']}\t{r['hit100k']:.2f}\t{r['n']}\t{r['subs'] or ''}\t{','.join(sorted(r['topics']))}\t"
                    f"{r['name']}\thttps://www.youtube.com/channel/{r['id']}/shorts\t{r['top'][0]}\t{r['top'][1]}\t"
                    f"{r['outlier']:.1f}\t{r['seed'][0]}\t{r['seed'][1]}\t{r['seed'][2]}\n")

    md = ["# 對標清單（YouTube Shorts）", "",
          f"`scripts/benchmarks.py` 產生。排名依最近 {SHORTS_N} 支 Shorts 播放中位數。",
          f"發現 {found_n} 個頻道（search.list 近 {SEARCH_DAYS} 天依觀看排序），有 Shorts 頁可量測的 {len(rows)} 個。"
          "全表在 `refs/benchmarks.tsv`。",
          "離群＝發現那支播放 ÷ 頻道中位數。", ""]
    for topic in TOPICS:
        sub = ranked(rows, topic, a.top)
        md += [f"## {topic}", ""]
        if not sub:
            md += ["（沒找到）", ""]
            continue
        for i, r in enumerate(sub, 1):
            share = "" if topic == FREE else f"主題詞佔 {r['shares'][topic]:.0%}，"
            md.append(f"{i}. **{r['name']}**　中位數 {fmt(r['median'])}，{share}"
                      f"破 10 萬比例 {r['hit100k']:.0%}，訂閱 {fmt(r['subs'])}　"
                      f"[頻道](https://www.youtube.com/channel/{r['id']}/shorts)"
                      f"　最高：{fmt(r['top'][0])}〈{r['top'][1][:30]}〉"
                      f"　離群 ×{r['outlier']:.1f}")
        md.append("")
    hot = sorted((r for r in rows if r["seed"][0] >= 100_000 and r["median"] >= HOT_MEDIAN_MIN),
                 key=lambda r: r["outlier"], reverse=True)[: a.top * 2]
    md += [f"## 離群爆款（單支 ≥ 10 萬、頻道中位數 ≥ {HOT_MEDIAN_MIN}，依離群值）", ""]
    md += [f"{i}. ×{r['outlier']:.1f}　{fmt(r['seed'][0])}〈{r['seed'][1][:40]}〉　{r['name']}"
           f"（中位數 {fmt(r['median'])}，{','.join(sorted(r['topics'])) or '無主題'}）　[片]({r['seed'][2]})"
           for i, r in enumerate(hot, 1)] or ["（沒有）"]
    md.append("")
    (ROOT / "refs" / "BENCHMARKS.md").write_text("\n".join(md), encoding="utf-8")
    print(f"寫入 {tsv} 與 refs/BENCHMARKS.md：{len(rows)} 個頻道")
    return 0 if rows else 1


if __name__ == "__main__":
    sys.exit(main())
