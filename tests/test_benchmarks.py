#!/usr/bin/env python3
"""benchmarks.py 主題歸屬與中文比例的最小自檢。判準改錯這支要 fail。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import benchmarks as b  # noqa: E402

fails = []
ai = ["ChatGPT 新功能", "AI 會取代你嗎", "今天吃什麼", "貓咪日常", "Gemini 實測"]
s = b.topic_shares(ai)
if abs(s["AI"] - 0.6) > 1e-9:
    fails.append(f"AI 佔比應 0.6，得 {s['AI']}")
if s["區塊鏈"] != 0:
    fails.append("區塊鏈不該有")
# 大小寫：ai 小寫也要算
if b.topic_shares(["ai 繪圖"])["AI"] != 1:
    fails.append("小寫 ai 沒算到")
# 英文詞整詞比對：taiwan 不是 AI
if b.topic_shares(["#taiwan 國慶", "Chill 一下"])["AI"] != 0:
    fails.append("taiwan／chill 被當成 AI")
en = ["Predicting what", "FREE FIRE VLOG", "新西兰"]
if not b.cjk_share(en) < b.CJK_SHARE_MIN:
    fails.append("英文頻道沒被擋")
if b.cjk_share(["日本一無駄なAIの使い方", "【地獄】マジで会話", "新宿"]) >= b.CJK_SHARE_MIN:
    fails.append("日文頻道沒被擋")
if b.cjk_share(ai) != 1:
    fails.append("中文頻道比例應 1")

# 離群值：單支 ÷ 中位數；中位數 0 不炸
if b.outlier(500_000, 50_000) != 10:
    fails.append("離群值算錯")
if b.outlier(1, 0) != 0:
    fails.append("中位數 0 應回 0")

# 上一輪 tsv 累加：舊格式（無 seed 欄）與新格式都要讀得到
import tempfile  # noqa: E402
from pathlib import Path  # noqa: E402
with tempfile.TemporaryDirectory() as d:
    f = Path(d) / "t.tsv"
    f.write_text("median\tname\turl\n1\t甲\thttps://www.youtube.com/channel/UCa/shorts\n", encoding="utf-8")
    old = b.previous(f)
    f.write_text("median\tname\turl\tseed_views\tseed_title\tseed_url\n"
                 "1\t乙\thttps://www.youtube.com/channel/UCb/shorts\t500\t標題\tu\n", encoding="utf-8")
    new = b.previous(f)
if list(old) != ["UCa"] or old["UCa"]["seed"][0] != 0:
    fails.append(f"舊格式 tsv 讀錯：{old}")
if new.get("UCb", {}).get("seed") != (500, "標題", "u"):
    fails.append(f"新格式 tsv 讀錯：{new}")

# 不限主題：時間切段要首尾相接、不重疊、新的在前
import datetime as dt  # noqa: E402
now = dt.datetime(2026, 10, 14, tzinfo=dt.timezone.utc)
w = b.windows(now, 90, 6)
if len(w) != 6 or w[0][1] != "2026-10-14T00:00:00Z" or w[-1][0] != "2026-07-16T00:00:00Z":
    fails.append(f"切段頭尾錯：{w[0]} … {w[-1]}")
if any(w[i][0] != w[i + 1][1] for i in range(5)):
    fails.append("切段沒有首尾相接")
# 不限主題取全部頻道；有主題的只取該主題
rows = [{"name": "甲", "topics": set()}, {"name": "乙", "topics": {"AI"}}, {"name": "丙", "topics": set()}]
if [r["name"] for r in b.ranked(rows, b.FREE, 10)] != ["甲", "乙", "丙"]:
    fails.append("不限主題漏頻道")
if [r["name"] for r in b.ranked(rows, "AI", 10)] != ["乙"]:
    fails.append("AI 主題篩錯")
if len(b.ranked(rows, b.FREE, 2)) != 2:
    fails.append("top n 沒截")

if fails:
    print("FAIL\n  " + "\n  ".join(fails))
    sys.exit(1)
print("OK benchmarks 自檢 16/16")
