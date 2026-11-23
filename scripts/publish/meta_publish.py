#!/usr/bin/env python3
"""把成片發到 IG Reels 和 Threads。兩邊共用同一次公開網址，都發完才關。

  meta_publish.py films/flt-11days                 只印計畫與檢查結果，不連 Meta 發片
  meta_publish.py films/flt-11days --yes           真的發（對外公開、IG API 刪不掉只能網頁刪，跑之前要確認）
  meta_publish.py films/flt-11days --only ig --yes 只發一邊
  meta_publish.py films/codex --carousel [--yes]   發輪播圖（out/carousel/p_*.jpg，先跑 scripts/carousel.sh）
                                                   說明讀 meta/caption-carousel.txt（兩平台共用，≤500 字）
                                                   記在 published.json 的 ig-carousel／threads-carousel

流程（官方 content publishing 文件）：
  public_path.py 換 token → funnel.py up → 建 container（Meta 自己來抓 mp4；
  dist/<片名>-cover.jpg 在就一起放上去，IG 帶 cover_url）
  → 輪詢到 FINISHED → publish → 兩邊都結束才 funnel.py down（發失敗也一定關）

說明文字：IG 讀 meta/caption-reels.txt，Threads 讀 meta/caption-threads.txt。
發過的平台記在 meta/published.json，再跑會擋下，防止同一支片重複發。

IG 走 Instagram Login，發出去之後 API 刪不掉（見 social.py caps），只能在 App 裡手動刪。
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tokens  # noqa: E402

ACCOUNT = "paradoxbar.tw"  # 兩個平台都必須是這個帳號，whoami 對不上就不發
POLL_EVERY = 15
# ponytail: 官方建議輪詢 5 分鐘內；給 15 分鐘並把 funnel 逾時守衛（30 分鐘）留在外面。
# 常超時再改成每輪延長 funnel。
POLL_MAX = 15 * 60
# DNS 等待＋輪詢要小於 funnel 的 30 分鐘逾時守衛，不然發到一半網址被關
DNS_WAIT = 12 * 60
PUBLIC_DNS = ("1.1.1.1", "8.8.8.8")

PLAT = {
    "ig": {"graph": "https://graph.instagram.com/v23.0", "label": "reels",
           "caption": "caption-reels.txt", "limit": 2200,
           "create": "media", "publish": "media_publish", "status_field": "status_code,status"},
    "threads": {"graph": "https://graph.threads.net/v1.0", "label": "threads",
                "caption": "caption-threads.txt", "limit": 500,
                "create": "threads", "publish": "threads_publish", "status_field": "status,error_message"},
}
IG_HASHTAG_MAX = 30


# ---------- 純函數（測試只測這幾個）----------

CAROUSEL_CAPTION = "caption-carousel.txt"


def caption(film, p, carousel=False):
    """讀說明文字並在送出前擋超長；Meta 拒收時 container 已經建了，白跑一趟。"""
    f = Path(film) / "meta" / (CAROUSEL_CAPTION if carousel else PLAT[p]["caption"])
    if not f.is_file():
        raise SystemExit(f"找不到 {f}")
    text = f.read_text(encoding="utf-8").strip()
    if not text:
        raise SystemExit(f"{f} 是空的")
    if len(text) > PLAT[p]["limit"]:
        raise SystemExit(f"{p} 說明 {len(text)} 字，上限 {PLAT[p]['limit']}")
    if p == "ig" and text.count("#") > IG_HASHTAG_MAX:
        raise SystemExit(f"IG hashtag 超過 {IG_HASHTAG_MAX} 個")
    return text


def create_params(p, video_url, text, cover_url=None):
    """cover_url：IG Reels 自訂封面（deliver.sh 產的 dist/<片名>-cover.jpg，網格 3:4 裁切不切到大標）。
    Threads 沒有封面參數，給了也不帶。"""
    if p == "ig":
        d = {"media_type": "REELS", "video_url": video_url, "caption": text, "share_to_feed": "true"}
        if cover_url:
            d["cover_url"] = cover_url
        return d
    return {"media_type": "VIDEO", "video_url": video_url, "text": text}


def funnel_urls(out):
    """funnel.py up 的輸出「label<TAB>網址」→ {label: 網址}；有封面時多一個 cover。"""
    return dict(line.split("\t", 1) for line in out.splitlines() if "\t" in line)


def item_params(p, image_url):
    """輪播子項。IG 子項不帶 media_type（預設圖片）；Threads 要寫 IMAGE。"""
    d = {"image_url": image_url, "is_carousel_item": "true"}
    if p == "threads":
        d["media_type"] = "IMAGE"
    return d


def carousel_params(p, children, text):
    key = "caption" if p == "ig" else "text"
    return {"media_type": "CAROUSEL", "children": ",".join(children), key: text}


def record_key(p, carousel):
    return f"{p}-carousel" if carousel else p


def state_of(p, d):
    """把兩個平台不同欄位名的狀態收成一個詞：FINISHED／IN_PROGRESS／ERROR／EXPIRED／PUBLISHED。"""
    s = d.get("status_code") if p == "ig" else d.get("status")
    return (s or "IN_PROGRESS").upper()


def already(film, platforms):
    f = Path(film) / "meta" / "published.json"
    done = json.loads(f.read_text()) if f.is_file() else {}
    return [p for p in platforms if p in done]


def record(film, p, info):
    f = Path(film) / "meta" / "published.json"
    done = json.loads(f.read_text()) if f.is_file() else {}
    done[p] = info
    f.write_text(json.dumps(done, ensure_ascii=False, indent=2) + "\n")


# ---------- 連網 ----------

def tok(p):
    t = tokens.read(f"{p.upper()}_ACCESS_TOKEN")
    if not t:
        raise SystemExit(f"{p} 未登入，先跑 tokens.py login {p}")
    return t


def whoami(p):
    fields = "user_id,username" if p == "ig" else "id,username"
    me = tokens.http(f"{PLAT[p]['graph']}/me?" + urllib.parse.urlencode({"fields": fields, "access_token": tok(p)}))
    return me.get("username")


def call(p, path, data=None):
    if data is None:
        q = urllib.parse.urlencode({"access_token": tok(p)})
        return tokens.http(f"{PLAT[p]['graph']}/{path}{'&' if '?' in path else '?'}{q}")
    return tokens.http(f"{PLAT[p]['graph']}/{path}", data={**data, "access_token": tok(p)})


def run(script, *args):
    r = subprocess.run([sys.executable, str(HERE / script), *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"{script} 失敗：\n{r.stdout}{r.stderr}")
    return r.stdout


def public_dns_ready(host):
    """用公開 DNS 查，不用系統解析：本機有 MagicDNS，自己永遠查得到，Meta 不一定。"""
    for resolver in PUBLIC_DNS:
        r = subprocess.run(["dig", "+short", host, f"@{resolver}"], capture_output=True, text=True)
        if not has_ip(r.stdout):
            return False
    return True


def has_ip(dig_out):
    """dig 連線失敗時 +short 也會印 ';; communications error'，不能只看有沒有輸出。"""
    return bool(re.search(r"^\d{1,3}(\.\d{1,3}){3}$|^[0-9a-f:]+:[0-9a-f:]+$", dig_out, re.M))


def wait_dns(url):
    """Tailscale 官方：Funnel 的公開 DNS 最多 10 分鐘才生效。
    2026-10-13 第一次真發沒等，兩平台 container 都 ERROR，Meta 根本沒來抓檔。"""
    host = urllib.parse.urlparse(url).hostname
    start = time.time()
    while not public_dns_ready(host):
        if time.time() - start > DNS_WAIT:
            raise SystemExit(f"{DNS_WAIT // 60} 分鐘後公開 DNS 仍查不到 {host}")
        time.sleep(20)
    print(f"  公開 DNS 生效（等了 {int(time.time() - start)} 秒）")


def publish(film, platforms):
    run("public_path.py", str(film))
    urls = funnel_urls(run("funnel.py", "up", str(film)))
    results = {}
    try:
        wait_dns(next(iter(urls.values())))
        containers = {}
        for p in platforms:
            r = call(p, f"me/{PLAT[p]['create']}",
                     create_params(p, urls[PLAT[p]["label"]], caption(film, p), urls.get("cover")))
            containers[p] = r["id"]
            print(f"  {p}: container {r['id']}")
        pending, start = dict(containers), time.time()
        while pending and time.time() - start < POLL_MAX:
            time.sleep(POLL_EVERY)
            for p, cid in list(pending.items()):
                d = call(p, f"{cid}?fields={PLAT[p]['status_field']}")
                s = state_of(p, d)
                if s == "FINISHED":
                    m = call(p, f"me/{PLAT[p]['publish']}", {"creation_id": cid})
                    link = call(p, f"{m['id']}?fields=permalink").get("permalink", "-")
                    info = {"id": m["id"], "url": link, "at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
                    record(film, p, info)
                    results[p] = f"已發 {link}"
                    del pending[p]
                elif s in ("ERROR", "EXPIRED"):
                    results[p] = f"{s}：{json.dumps(d, ensure_ascii=False)}"
                    del pending[p]
        for p in pending:
            results[p] = f"逾時 {POLL_MAX // 60} 分鐘仍未處理完（container {pending[p]}）"
    finally:
        print("  " + run("funnel.py", "down").strip())
    return results


def wait_finished(p, ids):
    """輪詢一批 container 直到全部 FINISHED；有任何一個 ERROR／EXPIRED／逾時就丟例外。"""
    pending, start = set(ids), time.time()
    while pending:
        if time.time() - start > POLL_MAX:
            raise RuntimeError(f"{p} 逾時 {POLL_MAX // 60} 分鐘：{sorted(pending)}")
        time.sleep(POLL_EVERY)
        for cid in list(pending):
            d = call(p, f"{cid}?fields={PLAT[p]['status_field']}")
            s = state_of(p, d)
            if s == "FINISHED":
                pending.discard(cid)
            elif s in ("ERROR", "EXPIRED"):
                raise RuntimeError(f"{p} container {cid} {s}：{json.dumps(d, ensure_ascii=False)}")


def publish_carousel(film, platforms):
    run("public_path.py", str(film))
    urls = [line.split("\t", 1)[1] for line in run("funnel.py", "up", str(film), "--carousel").splitlines()
            if "\t" in line]
    results = {}
    try:
        wait_dns(urls[0])
        for p in platforms:
            try:
                kids = [call(p, f"me/{PLAT[p]['create']}", item_params(p, u))["id"] for u in urls]
                wait_finished(p, kids)
                cid = call(p, f"me/{PLAT[p]['create']}", carousel_params(p, kids, caption(film, p, True)))["id"]
                wait_finished(p, [cid])
                m = call(p, f"me/{PLAT[p]['publish']}", {"creation_id": cid})
                link = call(p, f"{m['id']}?fields=permalink").get("permalink", "-")
                record(film, record_key(p, True),
                       {"id": m["id"], "url": link, "at": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
                results[p] = f"已發 {link}"
            except RuntimeError as e:
                results[p] = str(e)
    finally:
        print("  " + run("funnel.py", "down").strip())
    return results


def main():
    a = sys.argv[1:]
    if not a or a[0].startswith("-"):
        print(__doc__)
        return 2
    film = Path(a[0]).resolve()
    yes = "--yes" in a
    carousel = "--carousel" in a
    unknown = [x for x in a[1:] if x not in ("--yes", "--carousel", "--only", *PLAT)]
    if unknown:
        raise SystemExit(f"不認得的參數 {unknown}")
    platforms = list(PLAT)
    if "--only" in a:
        i = a.index("--only")
        if i + 1 >= len(a) or a[i + 1] not in PLAT:
            raise SystemExit("--only 後面接 ig 或 threads")
        platforms = [a[i + 1]]

    dup = already(film, [record_key(p, carousel) for p in platforms])
    if dup:
        raise SystemExit(f"{', '.join(dup)} 已經發過（meta/published.json），不重發")
    if carousel:
        sys.path.insert(0, str(HERE))
        import funnel
        pages = funnel.served_files(film, carousel=True)
        for _, f in pages:
            out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(f)],
                                 capture_output=True, text=True).stdout
            wh = tuple(int(x) for x in re.findall(r"pixel(?:Width|Height): (\d+)", out))
            if wh != (1080, 1350):  # IG 輪播比例要在 4:5～1.91:1 之間，用 4:5 頂格
                raise SystemExit(f"{f.name} 是 {wh}，不是 1080x1350")
        print(f"  輪播 {len(pages)} 張，皆 1080x1350")
    for p in platforms:
        c = caption(film, p, carousel)
        if not carousel:
            v = film / "dist" / f"{film.name}-{PLAT[p]['label']}.mp4"
            if not v.is_file():
                raise SystemExit(f"找不到 {v}，先跑 scripts/deliver.sh")
        who = whoami(p)
        if who != ACCOUNT:
            raise SystemExit(f"{p} 權杖對應 {who}，不是 {ACCOUNT}，不發")
        what = "輪播" if carousel else f"{v.name} {v.stat().st_size // 2**20}MB"
        print(f"  {p}: 帳號 {who}，{what}，說明 {len(c)} 字")
    if not yes:
        print("  以上會公開發布。確定就加 --yes 再跑一次。", file=sys.stderr)
        return 0

    results = publish_carousel(film, platforms) if carousel else publish(film, platforms)
    for p, r in results.items():
        print(f"  {p}: {r}")
    return 0 if all(r.startswith("已發") for r in results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
