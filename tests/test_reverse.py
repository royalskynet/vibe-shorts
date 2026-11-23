#!/usr/bin/env python3
"""reverse.py 純函式自檢：python3 tests/test_reverse.py（不跑模型、不連網）。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from reverse import assign_speech, cjk_per_sec, clean_ocr_text, parse_vocr  # noqa: E402

shots = [{"id": "S01", "start": 0, "end": 2}, {"id": "S02", "start": 2, "end": 4}]
# 0.5–2.8：S01 重疊 1.5 秒、S02 0.8 秒 → 歸 S01；2.5–3.5 全在 S02
segs = [{"t0": 0.5, "t1": 2.8, "text": "甲"}, {"t0": 2.5, "t1": 3.5, "text": "乙"}, {"t0": 3.6, "t1": 3.9, "text": "丙"}]
assert assign_speech(shots, segs) == {"S01": "甲", "S02": "乙丙"}, assign_speech(shots, segs)

assert cjk_per_sec("你好123", 2) == 1.0
assert cjk_per_sec("abc", 5) == 0
assert cjk_per_sec("你好", 0) == 0 and cjk_per_sec("你好", -1) == 0

# 只濾字元，不改字：OCR 認錯要原樣留下，不准用對照表把答案改對
assert clean_ocr_text("台灣 伶知識 A1") == "台灣伶知識1", clean_ocr_text("台灣 伶知識 A1")

# vocr 輸出：字裡有換行也不錯位；格數不符要丟錯
assert parse_vocr('["甲\\n續", "", "乙"]', 3) == ["甲\n續", "", "乙"]
for bad, n in (('["甲"]', 2), ('["甲", "乙"]', 1), ('{"a": 1}', 1), ('[1]', 1)):
    try:
        parse_vocr(bad, n)
    except RuntimeError:
        continue
    raise AssertionError(f"parse_vocr 該丟錯：{bad} n={n}")

print("OK reverse 自檢 4/4")
