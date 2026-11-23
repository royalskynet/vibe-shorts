#!/usr/bin/env python3
"""precheck.storyboard_rows：TREATMENT.md 有多張表時只取分鏡表。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from precheck import storyboard_rows  # noqa: E402

DOC = """# x

| 節拍 | 爆款 | 本片 |
|---|---|---|
| 鉤子 | a | b |

## 分鏡

| 段 | 卡 | 內容 | 動作（畫面） | 衝擊事件 | 來源 |
|---|---|---|---|---|---|
| 鉤子 | 01 | 句 | 點陣落下 | — | [1] |

| 另一張 | 表 |
|---|---|
"""
rows = storyboard_rows(DOC)
assert rows[0].startswith("| 段 | 卡"), rows[0]
assert len(rows) == 3, rows            # 表頭、分隔線、一張卡；不吃前後兩張表
assert storyboard_rows("| a | b |\n|---|---|\n")[0] == "| a | b |"   # 沒有分鏡表 → 第一張表，交給呼叫端報缺欄
assert storyboard_rows("沒有表") == []
print("ok")
