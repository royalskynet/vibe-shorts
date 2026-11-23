#!/usr/bin/env python3
"""一支指令管三個平台的貼文：列出、刪除、批次清轉貼。

  social.py caps                             三個平台各能做什麼
  social.py list threads [--type repost] [--limit 25]
  social.py list ig|yt [--limit 25]
  social.py delete threads|yt <ID>... --yes
  social.py prune threads --reposts [--limit 50] --yes

不帶 --yes 的 delete 與 prune 只印出會動到哪幾筆，不碰任何東西。
每筆一行、欄位用 tab 分開：ID、類型、日期、網址、前 40 字。
行數刻意壓低，是為了讓 agent 讀完整個清單只花一點 token。

三個平台能做的事不一樣，這是平台的限制不是這支程式少寫：
  Threads  列出、刪除（要 threads_delete 權限；官方上限 100 刪/天/帳號）
  IG       只能列出。DELETE 只存在於 Facebook Login for Business 那條路
           （graph.facebook.com + instagram_manage_contents）；我們走
           Instagram Login，官方 media reference 明寫這條路不支援 DELETE。
  YouTube  列出、刪除（現有的 youtube scope 已經含刪除）

ponytail: Threads 官方沒明文說 REPOST_FACADE 能不能 DELETE，第一次用先刪一筆試。
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokens  # noqa: E402

THREADS_DELETE_DAILY = 100
TEXT_WIDTH = 40
DEFAULT_LIST = 25
DEFAULT_PRUNE = 50
PAGE = 100

# 平台能力。delete 為 False 的平台在送出任何請求之前就被擋下來。
CAPS = {
    "threads": {"list": True, "delete": True,
                "note": "刪除要 threads_delete 權限，官方上限 100 刪/天"},
    "ig": {"list": True, "delete": False,
           "note": "Instagram Login 這條路官方不支援 DELETE，只能在 App 裡手動刪"},
    "yt": {"list": True, "delete": True,
           "note": "youtube scope 已含刪除；影片刪掉不可復原"},
}

THREADS_FIELDS = "id,media_type,permalink,timestamp,text"
IG_FIELDS = "id,media_type,permalink,timestamp"  # caption 只在 Facebook Login 那條路給


# ---------- 純函數（測試只測這幾個）----------

def one_line(s):
    """壓成單行再截斷。貼文裡的換行會把 tab 分隔的輸出弄亂。"""
    s = " ".join((s or "").split())
    return s[:TEXT_WIDTH - 1] + "…" if len(s) > TEXT_WIDTH else s


def pick(rows, kind):
    """kind='repost' 只留轉貼。篩錯就會刪到自己寫的貼文，所以單獨測。"""
    if kind == "repost":
        return [r for r in rows if r["type"] == "REPOST_FACADE"]
    return list(rows)


def can(platform, action):
    cap = CAPS.get(platform)
    if not cap:
        raise SystemExit(f"不認得平台 {platform}，只有 {', '.join(CAPS)}")
    if not cap[action]:
        raise SystemExit(f"{platform} 不能 {action}：{cap['note']}")
    return True


def fmt(r):
    return "\t".join([r["id"], r["type"], r["date"][:10], r["url"], one_line(r["text"])])


# ---------- HTTP ----------

def api(url, method="GET", bearer=None):
    req = urllib.request.Request(url, method=method)
    if bearer:
        req.add_header("Authorization", "Bearer " + bearer)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode()
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code} {method} {url.split('?')[0]}\n"
                         f"{e.read().decode(errors='replace')}")


def need(platform, name):
    tok = tokens.read(name)
    if not tok:
        raise SystemExit(f"{platform} 未登入，先跑 tokens.py login {platform}")
    return tok


# ---------- Meta（Threads / IG 同一個形狀）----------

def meta_list(platform, limit, kind):
    cfg = {"threads": ("https://graph.threads.net/v1.0/me/threads", THREADS_FIELDS),
           "ig": ("https://graph.instagram.com/v23.0/me/media", IG_FIELDS)}[platform]
    tok = need(platform, f"{platform.upper()}_ACCESS_TOKEN")
    rows, after = [], None
    while len(rows) < limit:
        q = {"fields": cfg[1], "limit": PAGE, "access_token": tok}
        if after:
            q["after"] = after
        d = api(f"{cfg[0]}?" + urllib.parse.urlencode(q))
        page = d.get("data", [])
        if not page:
            break
        for m in page:
            rows.append({"id": m["id"], "type": m.get("media_type", "?"),
                         "date": m.get("timestamp", ""),
                         "url": m.get("permalink", "-"), "text": m.get("text", "")})
        rows = pick(rows, kind)
        after = d.get("paging", {}).get("cursors", {}).get("after")
        if not after:
            break
    return rows[:limit]


def meta_delete(platform, mid):
    tok = need(platform, f"{platform.upper()}_ACCESS_TOKEN")
    base = {"threads": "https://graph.threads.net/v1.0"}[platform]
    api(f"{base}/{mid}?" + urllib.parse.urlencode({"access_token": tok}), method="DELETE")


# ---------- YouTube ----------

def yt_bearer():
    tokens.yt_refresh()
    return need("yt", "YT_ACCESS_TOKEN")


def yt_list(limit, kind):
    tok = yt_bearer()
    ch = api("https://www.googleapis.com/youtube/v3/channels?"
             + urllib.parse.urlencode({"part": "contentDetails", "mine": "true"}),
             bearer=tok)
    items = ch.get("items") or []
    if not items:
        raise SystemExit("這個權杖沒有對應的 YouTube 頻道")
    pl = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]
    rows, page_token = [], None
    while len(rows) < limit:
        q = {"part": "snippet,status", "playlistId": pl,
             "maxResults": min(50, limit - len(rows))}
        if page_token:
            q["pageToken"] = page_token
        d = api("https://www.googleapis.com/youtube/v3/playlistItems?"
                + urllib.parse.urlencode(q), bearer=tok)
        for it in d.get("items", []):
            vid = it["snippet"]["resourceId"]["videoId"]
            rows.append({"id": vid, "type": it.get("status", {}).get("privacyStatus", "VIDEO").upper(),
                         "date": it["snippet"].get("publishedAt", ""),
                         "url": f"https://youtu.be/{vid}",
                         "text": it["snippet"].get("title", "")})
        page_token = d.get("nextPageToken")
        if not page_token:
            break
    return pick(rows, kind)[:limit]


def yt_delete(vid):
    api("https://www.googleapis.com/youtube/v3/videos?"
        + urllib.parse.urlencode({"id": vid}), method="DELETE", bearer=yt_bearer())


# ---------- 指令 ----------

LISTERS = {"threads": lambda n, k: meta_list("threads", n, k),
           "ig": lambda n, k: meta_list("ig", n, k),
           "yt": yt_list}
DELETERS = {"threads": lambda i: meta_delete("threads", i), "yt": yt_delete}


def cmd_caps():
    for p, c in CAPS.items():
        acts = " ".join(a for a in ("list", "delete") if c[a])
        print(f"  {p:<8} {acts:<12} {c['note']}")


def cmd_list(platform, limit, kind):
    can(platform, "list")
    rows = LISTERS[platform](limit, kind)
    for r in rows:
        print(fmt(r))
    print(f"  共 {len(rows)} 筆", file=sys.stderr)


def delete_many(platform, rows, yes):
    """rows 是 cmd_list 的那種 dict；只有 yes 才真的送 DELETE。"""
    can(platform, "delete")
    if not rows:
        print("  沒有符合的，不用刪", file=sys.stderr)
        return
    for r in rows:
        print(fmt(r))
    if not yes:
        print(f"  以上 {len(rows)} 筆會被刪。確定就加 --yes 再跑一次。", file=sys.stderr)
        return
    if platform == "threads" and len(rows) > THREADS_DELETE_DAILY:
        raise SystemExit(f"{len(rows)} 筆超過 Threads 每天 {THREADS_DELETE_DAILY} 刪的上限，"
                         f"用 --limit {THREADS_DELETE_DAILY} 分幾天跑")
    done, failed = 0, []
    for r in rows:
        try:
            DELETERS[platform](r["id"])
            done += 1
        except SystemExit as e:
            failed.append((r["id"], str(e)))
    print(f"  已刪 {done} 筆", file=sys.stderr)
    if failed:
        for mid, err in failed:
            print(f"  {mid} 刪不掉：{err}", file=sys.stderr)
        raise SystemExit(f"{len(failed)} 筆失敗")


def cmd_delete(platform, ids, yes):
    can(platform, "delete")
    rows = [{"id": i, "type": "-", "date": "-", "url": "-", "text": ""} for i in ids]
    delete_many(platform, rows, yes)


def cmd_prune(platform, limit, yes):
    can(platform, "delete")
    rows = LISTERS[platform](limit, "repost")
    delete_many(platform, rows, yes)


def intflag(args, name, default):
    if name not in args:
        return default
    i = args.index(name)
    if i + 1 >= len(args) or not args[i + 1].isdigit():
        raise SystemExit(f"{name} 後面要接數字")
    v = int(args[i + 1])
    del args[i:i + 2]
    return v


def strflag(args, name, default):
    if name not in args:
        return default
    i = args.index(name)
    if i + 1 >= len(args):
        raise SystemExit(f"{name} 後面要接值")
    v = args[i + 1]
    del args[i:i + 2]
    return v


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd, args = args[0], args[1:]
    if cmd == "caps":
        cmd_caps()
        return
    yes = "--yes" in args
    if yes:
        args.remove("--yes")

    if cmd == "list":
        limit = intflag(args, "--limit", DEFAULT_LIST)
        kind = strflag(args, "--type", "all")
        if kind not in ("all", "repost"):
            raise SystemExit("--type 只有 all 或 repost")
        if len(args) != 1:
            raise SystemExit("list 要帶一個平台：threads、ig 或 yt")
        cmd_list(args[0], limit, kind)
    elif cmd == "prune":
        limit = intflag(args, "--limit", DEFAULT_PRUNE)
        if len(args) != 2 or args[0] != "threads" or args[1] != "--reposts":
            raise SystemExit("目前只有 prune threads --reposts（只有 Threads 有轉貼這種貼文）")
        cmd_prune(args[0], limit, yes)
    elif cmd == "delete":
        if len(args) < 2:
            raise SystemExit("delete 要帶平台和至少一個 ID")
        cmd_delete(args[0], args[1:], yes)
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
