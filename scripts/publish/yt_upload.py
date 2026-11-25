#!/usr/bin/env python3
"""把 dist/<片名>-shorts.mp4 上傳到 YouTube。預設私人，確認過再公開。

  yt_upload.py films/flt-11days                 私人上傳，印出影片 ID
  yt_upload.py films/flt-11days --public        直接公開（對外發布，跑之前要確認）
  yt_upload.py films/flt-11days --dry-run       只印要送出的 metadata，不連網
  yt_upload.py status <影片ID>                  查處理狀態與公開狀態
  yt_upload.py public films/flt-11days <影片ID> 私人轉公開並更新標題說明（對外發布，跑之前要確認）

預設三平台一起發：轉公開（含 --public）前 meta/published.json 要已有 ig 和 threads，
所以順序是 meta_publish.py --yes → 再轉 YouTube 公開；只發 YouTube 要明說 --yt-only。

標題讀 meta/title-shorts.txt（第一行），說明讀 meta/caption-shorts.txt，
標籤讀 meta/tags.txt（一行一個，可省略；YouTube 上限合計 500 字元）。
上傳走 resumable upload 的單次 PUT：先拿上傳網址，再把整個檔案送過去。
ponytail: 單次 PUT 不續傳。網路中斷就整支重傳；常斷再加 Content-Range 續傳。

AI 揭露（containsSyntheticMedia）填 False：YouTube 只管「觀眾會誤認為真實」的內容，
動畫與明顯不寫實的畫面在豁免清單（見 state 10-12 的查證）。
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokens  # noqa: E402

ENDPOINT = "https://www.googleapis.com/upload/youtube/v3/videos"
CATEGORY_EDUCATION = "27"
TITLE_MAX = 100
TAGS_MAX = 500  # YouTube 標籤合計字元上限，含空白的標籤官方算法另加 2，這裡一律加 2 從嚴
# 悖論小酒館。10-20 refresh token 綁到個人頻道 Eight (Cai)，私人片傳錯頻道使用者找不到；上傳前比對
CHANNEL_ID = os.environ.get("YT_CHANNEL_ID", "UCZkzE-KXwTHZysZmpCfTx_A")


def check_channel(got, want=CHANNEL_ID):
    if got != want:
        raise SystemExit(f"YouTube 授權綁的頻道是 {got}，不是悖論小酒館 {want}；重跑 tokens.py login yt 選對頻道")


def mine_channel(tok):
    req = urllib.request.Request("https://www.googleapis.com/youtube/v3/channels?part=id&mine=true",
                                 headers={"Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        items = json.loads(r.read().decode()).get("items") or [{}]
    return items[0].get("id")


def build_body(film, public):
    film = Path(film).resolve()
    # 橫式片（dist/<名>-youtube.mp4 存在）用 youtube 檔名與 meta
    yt = (film / "dist" / f"{film.name}-youtube.mp4").exists()
    title_p = film / "meta" / ("title-youtube.txt" if yt else "title-shorts.txt")
    desc_p = film / "meta" / ("caption-youtube.txt" if yt else "caption-shorts.txt")
    for p in (title_p, desc_p):
        if not p.is_file():
            raise SystemExit(f"找不到 {p}")
    title = (title_p.read_text().strip().splitlines() or [""])[0].strip()
    if not title or len(title) > TITLE_MAX:
        raise SystemExit(f"標題長度 {len(title)}，必須 1–{TITLE_MAX} 字")
    if "<" in title or ">" in title:
        raise SystemExit("標題不能有 < 或 >，YouTube 會拒收")
    tags_p = film / "meta" / "tags.txt"
    tags = [t.strip().lstrip("#") for t in tags_p.read_text().splitlines()] if tags_p.is_file() else []
    tags = [t for t in tags if t]
    if sum(len(t) + 2 for t in tags) > TAGS_MAX:
        raise SystemExit(f"標籤合計超過 {TAGS_MAX} 字元")
    if any("<" in t or ">" in t for t in tags):
        raise SystemExit("標籤不能有 < 或 >，YouTube 會拒收")
    return {
        "snippet": {
            "title": title,
            "description": desc_p.read_text().strip(),
            "tags": tags,
            "categoryId": CATEGORY_EDUCATION,
            "defaultLanguage": "zh-Hant",
            "defaultAudioLanguage": "zh-Hant",
        },
        "status": {
            "privacyStatus": "public" if public else "private",
            "selfDeclaredMadeForKids": False,
            "containsSyntheticMedia": False,
        },
    }


def upload(video, body):
    tokens.yt_refresh()
    tok = tokens.read("YT_ACCESS_TOKEN")
    if not tok:
        raise SystemExit("YouTube 未登入，先跑 tokens.py login yt")
    check_channel(mine_channel(tok))
    size = video.stat().st_size

    q = urllib.parse.urlencode({"uploadType": "resumable", "part": "snippet,status"})
    req = urllib.request.Request(f"{ENDPOINT}?{q}", data=json.dumps(body).encode(), method="POST", headers={
        "Authorization": f"Bearer {tok}",
        "Content-Type": "application/json; charset=UTF-8",
        "X-Upload-Content-Type": "video/mp4",
        "X-Upload-Content-Length": str(size),
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            loc = r.headers["Location"]
    except urllib.error.HTTPError as e:
        raise SystemExit(f"建立上傳失敗 HTTP {e.code}\n{e.read().decode(errors='replace')}")

    with open(video, "rb") as f:
        put = urllib.request.Request(loc, data=f, method="PUT", headers={
            "Authorization": f"Bearer {tok}",
            "Content-Type": "video/mp4",
            "Content-Length": str(size),
        })
        try:
            with urllib.request.urlopen(put, timeout=1800) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            raise SystemExit(f"上傳失敗 HTTP {e.code}\n{e.read().decode(errors='replace')}")


def status(vid):
    tokens.yt_refresh()
    q = urllib.parse.urlencode({"part": "status,snippet,processingDetails", "id": vid})
    req = urllib.request.Request(f"https://www.googleapis.com/youtube/v3/videos?{q}",
                                 headers={"Authorization": "Bearer " + tokens.read("YT_ACCESS_TOKEN")})
    with urllib.request.urlopen(req, timeout=30) as r:
        items = json.loads(r.read().decode())["items"]
    if not items:
        raise SystemExit(f"查無 {vid}")
    d = items[0]
    print(json.dumps({"channel": d["snippet"]["channelId"], "status": d["status"],
                      "processing": d.get("processingDetails", {}).get("processingStatus")},
                     ensure_ascii=False, indent=1))


def meta_done(film):
    """預設三平台一起發（11-08 使用者定）：IG、Threads 沒發過就不准只公開 YouTube。"""
    p = Path(film) / "meta" / "published.json"
    got = json.loads(p.read_text()) if p.is_file() else {}
    miss = [k for k in ("ig", "threads") if k not in got]
    if miss:
        raise SystemExit(f"{'、'.join(miss)} 還沒發。先跑 meta_publish.py {film} --yes 再轉公開；"
                         "確定只發 YouTube 就加 --yt-only")


def record_public(film, d):
    """公開成功才記進 meta/published.json 的 youtube，跟 IG／Threads 同格式；私人上傳不記。"""
    if d["status"]["privacyStatus"] != "public":
        return
    f = Path(film) / "meta" / "published.json"
    done = json.loads(f.read_text()) if f.is_file() else {}
    done["youtube"] = {"id": d["id"], "url": f"https://youtube.com/shorts/{d['id']}",
                       "at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
    f.write_text(json.dumps(done, ensure_ascii=False, indent=2) + "\n")


def make_public(film, vid):
    """私人上傳確認過畫面後轉公開，標題說明一併換成 meta/ 裡現在的版本。
    part 列到的物件會整個覆蓋，所以用 build_body 帶齊所有欄位，不然會被重設。"""
    tokens.yt_refresh()
    body = {"id": vid, **build_body(film, True)}
    req = urllib.request.Request("https://www.googleapis.com/youtube/v3/videos?part=snippet,status",
                                 data=json.dumps(body).encode(), method="PUT", headers={
                                     "Authorization": "Bearer " + tokens.read("YT_ACCESS_TOKEN"),
                                     "Content-Type": "application/json; charset=UTF-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"轉公開失敗 HTTP {e.code}\n{e.read().decode(errors='replace')}")
    record_public(film, d)
    print(f"  https://youtube.com/shorts/{vid}（{d['status']['privacyStatus']}）")


def main():
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == "status":
        status(args[1])
        return
    yt_only = "--yt-only" in args
    args = [a for a in args if a != "--yt-only"]
    if len(args) == 3 and args[0] == "public":
        if not yt_only:
            meta_done(Path(args[1]).resolve())
        make_public(Path(args[1]).resolve(), args[2])
        return
    if not args or args[0].startswith("-"):
        print(__doc__)
        sys.exit(2)
    film = Path(args[0]).resolve()
    unknown = set(args[1:]) - {"--public", "--dry-run"}
    if unknown:
        raise SystemExit(f"不認得的參數：{' '.join(sorted(unknown))}")
    if "--public" in args and not yt_only:
        meta_done(film)
    body = build_body(film, "--public" in args)
    yt = (film / "dist" / f"{film.name}-youtube.mp4").exists()
    video = film / "dist" / (f"{film.name}-youtube.mp4" if yt else f"{film.name}-shorts.mp4")
    if not video.is_file():
        raise SystemExit(f"找不到 {video}，先跑 scripts/deliver.sh")
    if "--dry-run" in args:
        print(json.dumps(body, ensure_ascii=False, indent=2))
        return
    r = upload(video, body)
    record_public(film, r)
    u = f"https://youtube.com/watch?v={r['id']}" if yt else f"https://youtube.com/shorts/{r['id']}"
    print(f"  已上傳：{u}（{r['status']['privacyStatus']}）")


if __name__ == "__main__":
    main()
