#!/usr/bin/env python3
"""precheck 語速門與吉祥物接線門的最小自檢。

語速：只管單人旁白片（cast.json 有 host、clawd 空陣列）；字數÷（TL.dur − pace.json tail）> PACE_CPS_MAX 擋。
吉祥物：有 mascot/ 目錄時 index.html 要同時有 poseAt 與 drawImage(。
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


def film_with(d, chars, dur, tail=None, cast=None):
    f = Path(d)
    # 兩句，標點不算字；「AI」「2024」算字
    half = chars // 2
    lines = [{"text": "你" * (half - 2) + "AI，"}, {"text": "好" * (chars - half - 4) + "2024。"}]
    (f / "timeline.js").write_text("// gen\nwindow.TL = " + json.dumps({"dur": dur, "lines": lines}) + ";\n",
                                   encoding="utf-8")
    (f / "cast.json").write_text(json.dumps(cast if cast is not None else {"host": {"ref": "x"}, "clawd": []}))
    pace = {"tempo": 1.0}
    if tail is not None:
        pace["tail"] = tail
    (f / "pace.json").write_text(json.dumps(pace))
    return f


with tempfile.TemporaryDirectory() as d:
    # 字數：300 字（含英數、不含標點）
    f = film_with(d, 300, 55.0, tail=3.5)
    cps, n, denom = pc.pace_cps(f)
    check("字數只算中英數", n == 300)
    check("分母扣 tail", abs(denom - 51.5) < 1e-9)
    check("5.83 字／秒要擋", pc.pace_problems(f) != [])
    check("訊息有實際值與對標", "5.83" in pc.pace_problems(f)[0] and "4.85–5.53" in pc.pace_problems(f)[0])
    # 沒有 tail 當 0：300 / 55 = 5.45 過
    f = film_with(d, 300, 55.0)
    check("沒 tail 當 0", abs(pc.pace_cps(f)[2] - 55.0) < 1e-9)
    check("5.45 字／秒要過", pc.pace_problems(f) == [])
    # 剛好在門檻：5.6 不擋（> 才擋）
    f = film_with(d, 280, 50.0)
    check("等於門檻不擋", pc.pace_problems(f) == [])
    f = film_with(d, 281, 50.0)
    check("超過門檻一點就擋", pc.pace_problems(f) != [])
    # 不是單人旁白片：有 clawd 或沒 host 都不管
    f = film_with(d, 400, 50.0, cast={"host": {"ref": "x"}, "clawd": [{"ref": "y"}]})
    check("對談片不適用", pc.pace_cps(f) is None and pc.pace_problems(f) == [])
    f = film_with(d, 400, 50.0, cast={"clawd": []})
    check("沒 host 不適用", pc.pace_cps(f) is None)
    os.remove(os.path.join(d, "cast.json"))
    check("沒 cast.json 不適用", pc.pace_cps(Path(d)) is None)

with tempfile.TemporaryDirectory() as d:
    f = Path(d)
    (f / "index.html").write_text("<script>ctx.drawImage(img,0,0)</script>")
    check("沒 mascot 目錄不管", pc.mascot_problems(f) == [])
    (f / "mascot").mkdir()
    check("有 mascot 沒 poseAt 要擋", pc.mascot_problems(f) != [])
    check("訊息寫 mascot 沒畫", "mascot 已安裝但 index.html 沒畫" in pc.mascot_problems(f)[0])
    (f / "index.html").write_text("import { poseAt } from './mascot/clawd-bot-shot.mjs';")
    check("有 poseAt 沒 drawImage 要擋", pc.mascot_problems(f) != [])
    (f / "index.html").write_text("import { poseAt } from './mascot/clawd-bot-shot.mjs';\nctx.drawImage(img,0,0)")
    check("兩個都有才過", pc.mascot_problems(f) == [])
    (f / "index.html").unlink()
    check("沒 index.html 要擋", pc.mascot_problems(f) != [])

if fails:
    sys.exit("FAIL\n  " + "\n  ".join(fails))
print("precheck 語速／吉祥物: 全部通過")
