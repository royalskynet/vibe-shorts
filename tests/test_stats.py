#!/usr/bin/env python3
"""stats.py 的最小自檢。不連網。

只測錯了會讓數據看錯的事：
  1. insights 兩種回應形狀都要讀對，缺值算 0。
  2. YT 只留公開片，私人片和刪掉的空殼不能混進來。
  3. 上架小時要算對（Meta 時間格式是 +0000，不是 +00:00）。
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TMP = tempfile.mkdtemp(prefix="vibe-stats-test-")
os.environ["VIBE_CREDS_DIR"] = os.path.join(TMP, "kv")
os.environ["VIBE_STATE"] = os.path.join(TMP, "state.json")
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts", "publish"))

import stats  # noqa: E402

fails = []


def check(name, got, want):
    if got != want:
        fails.append(f"{name}: 得到 {got!r}，應該是 {want!r}")


check("insights 兩種形狀", stats.insight_values([
    {"name": "views", "values": [{"value": 56}]},
    {"name": "likes", "total_value": {"value": 3}},
    {"name": "shares", "values": [{"value": None}]},
]), {"views": 56, "likes": 3, "shares": 0})

check("YT 公開留", stats.yt_keep({"type": "PUBLIC"}), True)
check("YT 私人略過", stats.yt_keep({"type": "PRIVATE"}), False)
check("YT 空殼略過", stats.yt_keep({"type": "PRIVACYSTATUSUNSPECIFIED"}), False)

now = 1760702400  # 2025-10-17T12:00:00Z
check("小時 Meta 格式", stats.age_hours("2025-10-17T02:00:00+0000", now), 10)
check("小時 YT 格式", stats.age_hours("2025-10-16T12:00:00Z", now), 24)

row = {"date": "2025-10-17T02:00:00+0000", "id": "abc", "text": "標題"}
check("一行欄位", stats.line("ig", row, 56, 1, 0, 1, now),
      "ig\t2025-10-17\t10h\t56\t1\t0\t1\tabc\t標題")

if fails:
    print("\n".join(fails))
    sys.exit(1)
print(f"test_stats 全過")
