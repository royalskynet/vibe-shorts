#!/usr/bin/env python3
"""precheck「內頁大標」門的最小自檢（純函數部分，不開瀏覽器）。

headline_problems：首卡之後各卡尾幀的文字框，框高 ÷ TEXT_BOX_RATIO ≥ HEADLINE_PX 就列出。
headline_applies：cast.json 有 host 且 index.html 有 window.TEXTS 才適用。
真頁面取樣（headline_check.mjs）由驗收指令 precheck.py films/taipei-silence 覆蓋。
"""
import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import precheck as pc  # noqa: E402

fails = []


def check(name, ok):
    if not ok:
        fails.append(name)


R = pc.TEXT_BOX_RATIO
box = lambda text, px: {"id": text, "text": text, "h": px * R}

# 畫內數字 64px、片尾系列名 68px 要過
check("64px 過", pc.headline_problems([{"card": 2, "t": 6.3, "boxes": [box("差 641 票", 64)]}]) == [])
check("68px 過", pc.headline_problems([{"card": "end", "t": 54.3, "boxes": [box("選前看懂台北", 68)]}]) == [])
check("沒字過", pc.headline_problems([{"card": 3, "t": 8.8, "boxes": []}]) == [])
# 門檻本身與以上擋（等號也擋）
p = pc.headline_problems([{"card": 3, "t": 8.8, "boxes": [box("很難猜準", 170)]}])
check("170px 擋", len(p) == 1 and "很難猜準" in p[0] and "卡 3" in p[0])
check("剛好門檻擋", len(pc.headline_problems([{"card": 4, "t": 1, "boxes": [box("x", pc.HEADLINE_PX)]}])) == 1)
check("門檻下 1px 過", pc.headline_problems([{"card": 4, "t": 1, "boxes": [box("x", pc.HEADLINE_PX - 1)]}]) == [])
# 多卡多框：每個大框都列出，小框不列
p = pc.headline_problems([
    {"card": 2, "t": 1, "boxes": [box("a", 112), box("b", 44)]},
    {"card": 5, "t": 2, "boxes": [box("c", 140)]},
])
check("多卡逐一列", len(p) == 2 and "「a」" in p[0] and "「c」" in p[1])
check("門檻常數合理", 64 < pc.HEADLINE_PX <= 110)

with tempfile.TemporaryDirectory() as d:
    f = Path(d)
    (f / "cast.json").write_text(json.dumps({"host": {"ref": "x"}, "clawd": []}))
    (f / "index.html").write_text("<script>window.TEXTS = t => [];</script>", encoding="utf-8")
    check("單人旁白＋TEXTS 適用", pc.headline_applies(f))
    (f / "index.html").write_text("<script>window.render = t => 0;</script>", encoding="utf-8")
    check("沒 TEXTS 不適用", not pc.headline_applies(f))
    (f / "index.html").write_text("<script>window.TEXTS = t => [];</script>", encoding="utf-8")
    (f / "cast.json").write_text(json.dumps({"clawd": ["a"]}))
    check("沒 host 不適用", not pc.headline_applies(f))
    (f / "cast.json").unlink()
    check("沒 cast.json 不適用", not pc.headline_applies(f))

if fails:
    print("FAIL test_precheck_headline:", "、".join(fails))
    sys.exit(1)
print("ok test_precheck_headline")
