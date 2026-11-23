#!/usr/bin/env python3
"""⑨ 回饋：三平台每支影片的播放與互動，一支一行。

  stats.py [--limit 15]

欄位用 tab 分開：平台、發布日、已上架小時、播放、讚、留言、分享、ID、前 40 字。
播放欄在 YT 是 viewCount，IG／Threads 是 insights 的 views。
YT 只列公開片；刪掉的片在 uploads 清單留空殼（Deleted video），一併略過。
IG／Threads 的 insights 要 *_manage_insights scope，缺了會回 403，重跑 tokens.py login。
"""
import os
import sys
import time
import urllib.parse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import social  # noqa: E402

META = {
    "ig": ("https://graph.instagram.com/v23.0", "views,likes,comments,shares"),
    "threads": ("https://graph.threads.net/v1.0", "views,likes,replies,shares"),
}
VIDEO_TYPES = ("VIDEO", "REELS")


# ---------- 純函數（測試只測這幾個）----------

def insight_values(data):
    """insights 回應 → {名稱: 數字}。Meta 有兩種形狀：values[0].value 或 total_value.value。"""
    out = {}
    for m in data:
        vals = m.get("values") or []
        v = vals[0].get("value") if vals else m.get("total_value", {}).get("value")
        out[m["name"]] = int(v or 0)
    return out


def yt_keep(row):
    return row["type"] == "PUBLIC"


def age_hours(iso, now=None):
    t = datetime.fromisoformat(iso.replace("Z", "+00:00").replace("+0000", "+00:00")).timestamp()
    return int(((now or time.time()) - t) / 3600)


def line(platform, row, views, likes, comments, shares, now=None):
    return "\t".join([platform, row["date"][:10], f"{age_hours(row['date'], now)}h",
                      str(views), str(likes), str(comments), str(shares),
                      row["id"], social.one_line(row["text"])])


# ---------- 抓數 ----------

def yt_lines(limit):
    rows = [r for r in social.yt_list(limit, "all") if yt_keep(r)]
    if not rows:
        return []
    d = social.api("https://www.googleapis.com/youtube/v3/videos?" + urllib.parse.urlencode(
        {"part": "statistics", "id": ",".join(r["id"] for r in rows)}), bearer=social.yt_bearer())
    st = {it["id"]: it["statistics"] for it in d.get("items", [])}
    return [line("yt", r, st[r["id"]].get("viewCount", 0), st[r["id"]].get("likeCount", 0),
                 st[r["id"]].get("commentCount", 0), "-") for r in rows if r["id"] in st]


def meta_lines(platform, limit):
    base, metric = META[platform]
    tok = social.need(platform, f"{platform.upper()}_ACCESS_TOKEN")
    out = []
    for r in social.meta_list(platform, limit, "all"):
        if r["type"] not in VIDEO_TYPES:
            continue
        d = social.api(f"{base}/{r['id']}/insights?"
                       + urllib.parse.urlencode({"metric": metric, "access_token": tok}))
        v = insight_values(d.get("data", []))
        r = dict(r, id=r["url"].rstrip("/").split("/")[-1])  # 短碼比數字 ID 好對照網址
        out.append(line(platform, r, v.get("views", 0), v.get("likes", 0),
                        v.get("comments", v.get("replies", 0)), v.get("shares", 0)))
    return out


def main():
    args = sys.argv[1:]
    if args and args[0] in ("-h", "--help"):
        print(__doc__)
        return
    limit = social.intflag(args, "--limit", 15)
    print("平台\t日期\t上架\t播放\t讚\t留言\t分享\tID\t標題")
    for lines in (yt_lines(limit), meta_lines("ig", limit), meta_lines("threads", limit)):
        for ln in lines:
            print(ln)


if __name__ == "__main__":
    main()
