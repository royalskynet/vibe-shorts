#!/usr/bin/env python3
"""meta_publish.py 的最小自檢。不連網。

測三件會讓發片出事的事：
  1. 已經發過的平台要擋下（IG 刪不掉，重發就是兩篇一樣的公開貼文）
  2. 說明超過平台上限要在建 container 前擋下
  3. 兩個平台的狀態欄位名不同（status_code／status），收成同一個詞不能弄錯
"""
import json
import os
import sys
import tempfile
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts", "publish"))

import meta_publish as mp  # noqa: E402

fails = []
film = Path(tempfile.mkdtemp(prefix="vibe-meta-test-")) / "f"
(film / "meta").mkdir(parents=True)


def rejects(p, text):
    (film / "meta" / mp.PLAT[p]["caption"]).write_text(text)
    try:
        mp.caption(film, p)
    except SystemExit:
        return True
    return False


if mp.already(film, ["ig", "threads"]):
    fails.append("沒發過卻說發過")
mp.record(film, "ig", {"id": "1"})
if mp.already(film, ["ig", "threads"]) != ["ig"]:
    fails.append("發過 ig 沒擋")
if json.loads((film / "meta" / "published.json").read_text())["ig"]["id"] != "1":
    fails.append("published.json 沒寫對")

if not rejects("threads", "字" * 501):
    fails.append("Threads 501 字沒擋")
if rejects("threads", "字" * 500):
    fails.append("Threads 500 字被誤擋")
if not rejects("ig", "#a " * 31):
    fails.append("IG 31 個 hashtag 沒擋")
if not rejects("ig", "  \n"):
    fails.append("空說明沒擋")

if mp.state_of("ig", {"status_code": "FINISHED", "status": "Finished: ok"}) != "FINISHED":
    fails.append("IG FINISHED 判錯")
if mp.state_of("threads", {"status": "ERROR", "error_message": "x"}) != "ERROR":
    fails.append("Threads ERROR 判錯")
if mp.state_of("threads", {}) != "IN_PROGRESS":
    fails.append("沒狀態時沒當處理中")

if mp.create_params("ig", "u", "t")["media_type"] != "REELS":
    fails.append("IG 不是 REELS")
if "text" not in mp.create_params("threads", "u", "t"):
    fails.append("Threads 沒帶 text")

# IG 自訂封面：funnel 輸出有 cover 行就帶 cover_url；Threads 沒封面參數，不能帶
up_out = "reels\thttps://h:10000/t/f-reels.mp4\nthreads\thttps://h:10000/t/f-threads.mp4\ncover\thttps://h:10000/t/f-cover.jpg\n"
urls = mp.funnel_urls(up_out)
ig = mp.create_params("ig", urls["reels"], "t", urls.get("cover"))
if ig.get("cover_url") != "https://h:10000/t/f-cover.jpg":
    fails.append("IG 沒帶 cover_url")
if ig.get("video_url") != "https://h:10000/t/f-reels.mp4":
    fails.append("IG video_url 拿錯")
if "cover_url" in mp.create_params("threads", urls["threads"], "t", urls.get("cover")):
    fails.append("Threads 不該帶 cover_url")
no_cover = mp.funnel_urls("reels\tu1\nthreads\tu2\n# 30 分鐘後自動關\n")
if "cover_url" in mp.create_params("ig", no_cover["reels"], "t", no_cover.get("cover")):
    fails.append("沒封面檔卻帶了 cover_url")

if mp.has_ip(";; communications error to 1.1.1.1#53: timed out\n"):
    fails.append("dig 錯誤訊息被當成解析成功")
if mp.has_ip(""):
    fails.append("空輸出被當成解析成功")
if not mp.has_ip("208.111.34.45\n"):
    fails.append("IPv4 沒認出來")

# 輪播：影片發過不能擋輪播，輪播發過要擋輪播
if mp.already(film, [mp.record_key("ig", True)]):
    fails.append("ig 影片發過卻擋了輪播")
mp.record(film, mp.record_key("ig", True), {"id": "2"})
if mp.already(film, [mp.record_key("ig", True)]) != ["ig-carousel"]:
    fails.append("ig 輪播發過沒擋")
if mp.item_params("ig", "u").get("media_type") is not None:
    fails.append("IG 輪播子項不該帶 media_type")
if mp.item_params("threads", "u") != {"image_url": "u", "is_carousel_item": "true", "media_type": "IMAGE"}:
    fails.append("Threads 輪播子項參數錯")
cp = mp.carousel_params("ig", ["1", "2"], "t")
if cp != {"media_type": "CAROUSEL", "children": "1,2", "caption": "t"}:
    fails.append("IG 輪播容器參數錯")
if mp.carousel_params("threads", ["1", "2"], "t").get("text") != "t":
    fails.append("Threads 輪播容器要用 text 不是 caption")
(film / "meta" / mp.CAROUSEL_CAPTION).write_text("字" * 501)
try:
    mp.caption(film, "threads", True)
    fails.append("輪播說明 501 字沒擋")
except SystemExit:
    pass

if fails:
    sys.exit("\n".join(fails))
print("meta_publish: 全部通過")
