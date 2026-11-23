#!/usr/bin/env python3
"""funnel.py 的最小自檢。不連網、不碰 tailscale。

只測四件出錯會曝光不該曝光的東西、或網址一直開著的事：
  1. 只放 reels／threads，不放 shorts（shorts 走 YouTube 上傳，不該公開）
  2. 網址固定 10000 埠（443 上有 tailnet-only 的 4177，見 funnel.py 坑 1、4）；
     直通不剝路徑，只放行 /<token>/<要發的檔名>
  3. 沒有 public-path.txt 或內容是片名時拒開
  4. 逾時守衛只關自己那次，token 對不上不關（不然會關到下一支片）
"""
import json
import os
import sys
import tempfile
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
TMP = Path(tempfile.mkdtemp(prefix="vibe-funnel-test-"))
os.environ["VIBE_PUBLISH_DIR"] = str(TMP / "pub")
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts", "publish"))

import funnel  # noqa: E402

fails = []


def check(name, ok):
    if not ok:
        fails.append(name)


def raises(fn, *a):
    try:
        fn(*a)
    except SystemExit:
        return True
    return False


film = TMP / "demo"
(film / "dist").mkdir(parents=True)
(film / "meta").mkdir()
for label in ("shorts", "reels", "threads"):
    (film / "dist" / f"demo-{label}.mp4").write_bytes(b"x")

# 1
labels = [l for l, _ in funnel.served_files(film)]
check("只放 reels／threads", labels == ["reels", "threads"])
(film / "dist" / "demo-threads.mp4").unlink()
check("缺檔拒開", raises(funnel.served_files, film))
(film / "dist" / "demo-threads.mp4").write_bytes(b"x")

# 1b IG 封面：有 dist/<名稱>-cover.jpg 才多放一張，放在最後，label 叫 cover（meta_publish 靠這個帶 cover_url）
(film / "dist" / "demo-cover.jpg").write_bytes(b"j")
check("有封面多放 cover", [l for l, _ in funnel.served_files(film)] == ["reels", "threads", "cover"])
check("封面放的是 jpg", funnel.served_files(film)[-1][1].name == "demo-cover.jpg")
(film / "dist" / "demo-cover.jpg").unlink()

# 2
check("網址走 10000", funnel.url("ab", "f.mp4").startswith(f"https://{funnel.HOST}:10000/ab/"))
names = {"demo-reels.mp4"}
check("放行 token＋檔名", funnel.allowed("/tok/demo-reels.mp4", "tok", names))
check("放行帶 query", funnel.allowed("/tok/demo-reels.mp4?x=1", "tok", names))
check("根目錄不列", not funnel.allowed("/", "tok", names))
check("token 目錄不列", not funnel.allowed("/tok/", "tok", names))
check("錯 token 擋", not funnel.allowed("/bad/demo-reels.mp4", "tok", names))
check("清單外檔名擋", not funnel.allowed("/tok/demo-shorts.mp4", "tok", names))
check("跳目錄擋", not funnel.allowed("/tok/../tok/demo-reels.mp4", "tok", names))

# 3
check("沒 token 檔拒開", raises(funnel.film_token, film))
(film / "meta" / "public-path.txt").write_text("demo\n")
check("片名當 token 拒開", raises(funnel.film_token, film))
(film / "meta" / "public-path.txt").write_text("0123456789abcdef0123\n")
check("隨機 token 可用", funnel.film_token(film) == "0123456789abcdef0123")

# 4
funnel.HOME.mkdir(parents=True)
closed = []
funnel.down = lambda: closed.append(1)
funnel.STATE.write_text(json.dumps({"token": "new"}))
funnel.expire("old", 0)
check("token 不同不關", closed == [])
funnel.expire("new", 0)
check("token 相同才關", closed == [1])

# 5 Range：Meta 先試 bytes=0-1 要 206
check("bytes=0-1", funnel.parse_range("bytes=0-1", 100) == (0, 1))
check("bytes=90- 到尾", funnel.parse_range("bytes=90-", 100) == (90, 99))
check("bytes=-10 取尾", funnel.parse_range("bytes=-10", 100) == (90, 99))
check("超出範圍不當 Range", funnel.parse_range("bytes=200-300", 100) is None)
check("沒 Range 送整檔", funnel.parse_range(None, 100) is None)

# 6 輪播：只放 out/carousel 的 jpg，照頁碼數字排（p_10 不能排在 p_2 前面），張數 2–10
car = film / "out" / "carousel"
car.mkdir(parents=True)
(car / "p_0.00.jpg").write_bytes(b"j")
check("輪播 1 張拒開", raises(funnel.served_files, film, True))
for i in range(1, 11):
    (car / f"p_{i}.00.jpg").write_bytes(b"j")
check("輪播 11 張拒開", raises(funnel.served_files, film, True))
(car / "p_10.00.jpg").unlink()
for i in range(3, 10):
    (car / f"p_{i}.00.jpg").unlink()
(car / "notes.txt").write_text("x")
labels = [l for l, _ in funnel.served_files(film, True)]
check("輪播只放 jpg 且照頁碼", labels == ["p_0.00.jpg", "p_1.00.jpg", "p_2.00.jpg"])
check("頁碼按數字排", sorted([Path("p_10.00.jpg"), Path("p_2.00.jpg")], key=funnel.page_no)[0].name == "p_2.00.jpg")
check("jpg 回 image/jpeg", funnel.content_type("p_0.00.jpg") == "image/jpeg")
check("mp4 回 video/mp4", funnel.content_type("demo-reels.mp4") == "video/mp4")

if fails:
    print("FAIL\n  " + "\n  ".join(fails))
    sys.exit(1)
print("OK funnel 自檢 28/28")
