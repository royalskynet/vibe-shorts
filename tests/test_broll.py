#!/usr/bin/env python3
"""broll.py license_ok/rank 最小自檢。不連網。"""
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
from pathlib import Path
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import broll  # noqa: E402

fails = []

for name in ("CC0", "Public domain", "CC BY 4.0", "cc by  2.0", "Pexels"):
    if not broll.license_ok(name):
        fails.append(f"應允許：{name}")

# 未知或附加條款的授權也要擋，不只 SA／NC／ND
for name in ("CC BY-SA 4.0", "CC BY-NC 4.0", "CC BY-ND 3.0", "cc by-sa 4.0", "CC BY mystery",
             "CC BY 4.0 + custom restriction", "not public domain", "CC0-custom", "", None):
    if broll.license_ok(name):
        fails.append(f"應擋下：{name}")

items = [
    {"id": "short", "duration": 2.0, "width": 1080, "height": 1920},
    {"id": "land", "duration": 5.0, "width": 1920, "height": 1080},
    {"id": "port", "duration": 5.0, "width": 1080, "height": 1920},
]
ranked = broll.rank(items, min_sec=3)
ids = [x["id"] for x in ranked]
if "short" in ids:
    fails.append(f"短於 min_sec 應被濾掉：{ids}")
if ids[:2] != ["port", "land"]:
    fails.append(f"直式應排在橫式前：{ids}")

# 同是直式，越接近 9:16 越前面
ids = [x["id"] for x in broll.rank([{"id": "4:5", "duration": 5, "width": 1080, "height": 1350},
                                    {"id": "9:16", "duration": 5, "width": 1080, "height": 1920}], min_sec=3)]
if ids != ["9:16", "4:5"]:
    fails.append(f"直式間應依比例接近 9:16 排序：{ids}")

# 直式優先要先於比例：極瘦長直式（1:10）比例差大於近正方形橫式，仍要排前面
ids = [x["id"] for x in broll.rank([{"id": "sq-land", "duration": 5, "width": 1001, "height": 1000},
                                    {"id": "thin", "duration": 5, "width": 100, "height": 1000}], min_sec=3)]
if ids != ["thin", "sq-land"]:
    fails.append(f"直式應先於橫式，不論比例：{ids}")

# HTTP 錯誤回顯 key 時要遮掉
KEY = "fake-key-1234567890"
err = urllib.error.HTTPError("https://x", 401, "Unauthorized", {}, io.BytesIO(f"bad key {KEY}".encode()))
with mock.patch.object(broll.urllib.request, "urlopen", side_effect=err):
    try:
        broll._request_json("https://x", headers={"Authorization": KEY})
        fails.append("HTTP 401 應丟 RuntimeError")
    except RuntimeError as e:
        if KEY in str(e) or "***" not in str(e):
            fails.append(f"錯誤訊息沒遮 key：{e}")

# fetch：舊幀不算進 count；抽 0 張要失敗
def fake_ffmpeg(n, rc=0):
    def run(cmd, **kw):
        for i in range(1, n + 1):
            Path(cmd[-1] % i).write_bytes(b"x")
        return subprocess.CompletedProcess(cmd, rc, "", "boom" if rc else "")
    return run

with tempfile.TemporaryDirectory() as d:
    (Path(d) / "9999.jpg").write_bytes(b"stale")
    with mock.patch.object(broll.subprocess, "run", fake_ffmpeg(3)):
        rc = broll.main(["fetch", "x.mp4", "--out", d])
    count = json.loads((Path(d) / "clip.json").read_text())["count"] if rc == 0 else None
    jpgs = sorted(p.name for p in Path(d).glob("*.jpg"))
    if rc != 0 or count != 3 or jpgs != ["0001.jpg", "0002.jpg", "0003.jpg"]:
        fails.append(f"fetch 應只留新抽的 3 張：rc={rc} count={count} jpgs={jpgs}")
with tempfile.TemporaryDirectory() as d:
    with mock.patch.object(broll.subprocess, "run", fake_ffmpeg(0)), \
         contextlib.redirect_stderr(io.StringIO()):
        rc = broll.main(["fetch", "x.mp4", "--out", d])
    if rc != 1 or (Path(d) / "clip.json").exists():
        fails.append(f"抽 0 張應回 1 且不寫 clip.json：rc={rc}")

# 重抽失敗（ffmpeg 非零、或 0 張）時既有素材與 clip.json 原樣保留，暫存目錄不殘留
for label, fake in (("ffmpeg 失敗", fake_ffmpeg(2, rc=1)), ("0 張", fake_ffmpeg(0))):
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "0001.jpg").write_bytes(b"old")
        (Path(d) / "clip.json").write_text('{"count": 1}')
        with mock.patch.object(broll.subprocess, "run", fake), contextlib.redirect_stderr(io.StringIO()):
            rc = broll.main(["fetch", "x.mp4", "--out", d])
        left = sorted(p.name for p in Path(d).iterdir())
        if rc != 1 or left != ["0001.jpg", "clip.json"] or (Path(d) / "0001.jpg").read_bytes() != b"old" \
                or (Path(d) / "clip.json").read_text() != '{"count": 1}':
            fails.append(f"{label}重抽應保留舊素材與 clip.json：rc={rc} 剩 {left}")

# --sources 寫不進去（指到目錄）時，既有素材與 clip.json 不動
with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as srcdir:
    (Path(d) / "0001.jpg").write_bytes(b"old")
    (Path(d) / "clip.json").write_text('{"count": 1}')
    with mock.patch.object(broll.subprocess, "run", fake_ffmpeg(2)), contextlib.redirect_stderr(io.StringIO()):
        rc = broll.main(["fetch", "new.mp4", "--out", d, "--sources", srcdir])
    if rc != 1 or (Path(d) / "0001.jpg").read_bytes() != b"old" or (Path(d) / "clip.json").read_text() != '{"count": 1}':
        fails.append(f"--sources 失敗應不動既有素材：rc={rc}")

if fails:
    print("FAIL\n  " + "\n  ".join(fails))
    sys.exit(1)
print("OK broll 自檢")
