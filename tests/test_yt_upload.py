#!/usr/bin/env python3
"""yt_upload.py 的最小自檢。不連網。

測兩件會讓發片出事的事：
  1. 預設必須是 private；只有明確 --public 才公開（反了就是未確認就對外發布）
  2. 標題超長或含 < > 要在送出前擋下（YouTube 會拒收，但那時已經燒掉配額）
  3. 公開成功要記進 published.json，私人不記
  4. 標籤讀 meta/tags.txt，合計超過 500 字元要擋
"""
import os
import sys
import tempfile
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts", "publish"))

import yt_upload  # noqa: E402

fails = []
film = Path(tempfile.mkdtemp(prefix="vibe-yt-test-")) / "f"
(film / "meta").mkdir(parents=True)
(film / "meta" / "caption-shorts.txt").write_text("說明")


def title(t):
    (film / "meta" / "title-shorts.txt").write_text(t)


def rejects(t):
    title(t)
    try:
        yt_upload.build_body(film, False)
    except SystemExit:
        return True
    return False


title("正常標題")
if yt_upload.build_body(film, False)["status"]["privacyStatus"] != "private":
    fails.append("預設不是 private")
if yt_upload.build_body(film, True)["status"]["privacyStatus"] != "public":
    fails.append("--public 沒變 public")
if not rejects("字" * 101):
    fails.append("101 字標題沒擋")
if not rejects("a<b"):
    fails.append("含 < 的標題沒擋")
if not rejects("\n"):
    fails.append("空標題沒擋")
if rejects("字" * 100):
    fails.append("100 字標題被誤擋")

title("正常標題")
(film / "meta" / "tags.txt").write_text("#行人地獄\n\n台北\n")
if yt_upload.build_body(film, False)["snippet"]["tags"] != ["行人地獄", "台北"]:
    fails.append("tags.txt 沒讀成 [行人地獄, 台北]（要去 # 去空行）")
(film / "meta" / "tags.txt").write_text("字" * 499)
try:
    yt_upload.build_body(film, False)
    fails.append("超過 500 字元的標籤沒擋")
except SystemExit:
    pass
(film / "meta" / "tags.txt").unlink()
if yt_upload.build_body(film, False)["snippet"]["tags"] != []:
    fails.append("沒有 tags.txt 時不是空清單")

pub = film / "meta" / "published.json"
for content, ok in [(None, False), ('{"ig": {}}', False), ('{"ig": {}, "threads": {}}', True)]:
    pub.unlink(missing_ok=True)
    if content:
        pub.write_text(content)
    try:
        yt_upload.meta_done(film)
        passed = True
    except SystemExit:
        passed = False
    if passed != ok:
        fails.append(f"published.json={content} 時三平台檢查應{'放行' if ok else '擋下'}")

pub.write_text('{"ig": {"id": "1"}}')
yt_upload.record_public(film, {"id": "PRIV", "status": {"privacyStatus": "private"}})
if "youtube" in pub.read_text():
    fails.append("私人上傳不該記進 published.json")
yt_upload.record_public(film, {"id": "PUB1", "status": {"privacyStatus": "public"}})
got = __import__("json").loads(pub.read_text())
if got.get("youtube", {}).get("url") != "https://youtube.com/shorts/PUB1" or "ig" not in got:
    fails.append(f"公開後 published.json 沒記 youtube 或洗掉其他平台：{got}")

if fails:
    sys.exit("\n".join(fails))
print("yt_upload: 全部通過")
