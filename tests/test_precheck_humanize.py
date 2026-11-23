#!/usr/bin/env python3
"""precheck 口語門：沒戳記、戳記綁舊稿、沒寫改動都要擋；綁現在的稿才過。"""
import hashlib
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from precheck import humanize_problems  # noqa: E402

with tempfile.TemporaryDirectory() as d:
    film = Path(d)
    (film / "audit").mkdir()
    (film / "narration.md").write_text("## 鉤子\n玩越久，越確定會輸。\n", encoding="utf-8")
    sha = hashlib.sha256((film / "narration.md").read_bytes()).hexdigest()
    stamp = film / "audit" / "humanize.md"
    assert humanize_problems(film), "沒戳記要擋"
    stamp.write_text(f"narration_sha: {sha}\n- 輸得越準 → 越確定會輸\n", encoding="utf-8")
    assert humanize_problems(film) == []
    stamp.write_text(f"narration_sha: {sha}\n\n", encoding="utf-8")
    assert humanize_problems(film), "沒寫改動要擋"
    stamp.write_text(f"narration_sha: {sha}\n無需改\n", encoding="utf-8")
    (film / "narration.md").write_text("## 鉤子\n你玩得越久，輸得越準。\n", encoding="utf-8")
    assert humanize_problems(film), "改稿後舊戳記要擋"
print("ok")
