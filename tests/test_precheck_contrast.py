#!/usr/bin/env python3
"""precheck 對比句門：genie-humanizer 的二元對比句型要擋，一般否定與「是不是」問句要放。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from precheck import contrast_problems  # noqa: E402

BAD = [
    "半年前他押的，是帳對不上，不是誰跟誰吃飯。",
    "這不是運氣，是算出來的。",
    "他要的不是錢，而是名聲。",
    "這並非偶然。",
    "與其說是失誤，不如說是設計。",
    "看似便宜，實則更貴。",
    "你以為他輸了，其實他早就賺了。",
    "價格不重要，重要的是時機。",
]
GOOD = [
    "特規晶片一片都沒賣給中國客戶。",
    "你知道是不是他先發現的嗎？",
    "外遇被證實了，這筆帳還沒有人證實。",
    "他不是第一個放空輝達的人。",
    "## 不是標題也不算",
]
for s in BAD:
    assert contrast_problems(s), f"要擋：{s}"
for s in GOOD:
    assert contrast_problems(s) == [], f"誤擋：{s} → {contrast_problems(s)}"
print("ok")
