#!/usr/bin/env python3
"""asr_guard 自檢：python3 tests/test_asr_guard.py。靜音上的 whisper 段要丟、有聲的要留。"""
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from asr_guard import silences, voiced  # noqa: E402

inf = float("inf")
seg = lambda a, b: {"start": a, "end": b, "text": f"{a}-{b}"}  # noqa: E731

# 全落在靜音（含檔尾無 silence_end 的 inf）→ 丟
assert voiced([seg(0, 3.98)], [(0.0, inf)]) == []
# 靜音只占一半 → 留
assert voiced([seg(0, 4)], [(0.0, 2.0)]) == [seg(0, 4)]
# 多段靜音加總 ≥ 0.8 → 丟；不足 → 留
assert voiced([seg(0, 10)], [(0, 4), (5, 9)]) == []
assert voiced([seg(0, 10)], [(0, 4), (5, 8)]) == [seg(0, 10)]
# 長度 0 的段不除以零、照留
assert voiced([seg(1, 1)], [(0, inf)]) == [seg(1, 1)]

# silences 實跑 ffmpeg：前 2 秒正弦波、後 2 秒靜音
with tempfile.TemporaryDirectory() as td:
    wav = os.path.join(td, "a.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "sine=f=440:d=2",
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-filter_complex",
                    "[1]atrim=0:2[s];[0][s]concat=n=2:v=0:a=1", wav], check=True)
    sp = silences(wav)
    assert len(sp) == 1 and abs(sp[0][0] - 2.0) < 0.1, sp
    assert voiced([seg(0, 2), seg(2.05, 3.95)], sp) == [seg(0, 2)], sp

print("OK asr_guard 自檢 6/6")
