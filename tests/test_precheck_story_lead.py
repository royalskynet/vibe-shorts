#!/usr/bin/env python3
"""precheck 開場門：開頭 STORY_LEAD_CHARS 字內要有「你」或問句。問句的「？」不能被 norm() 刪掉。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from precheck import STORY_LEAD_CHARS, story_problems  # noqa: E402

TAIL = "\n".join(f"第{i}句講一件事。" for i in range(3))
MSG = "開場沒點到觀眾"


def lead_flagged(opening):
    sections = [("開場", opening), ("中段", TAIL), ("結尾", "回到第一句。")]
    return any(MSG in p for p in story_problems(sections))


fails = 0


def check(name, cond):
    global fails
    print(("ok - " if cond else "not ok - ") + name)
    fails += 0 if cond else 1


check("問句（全形？）開場放行", not lead_flagged("天天排隊的那家店，為什麼突然關了？"))
check("問句（半形?）開場放行", not lead_flagged("天天排隊的那家店，為什麼突然關了?"))
check("有「你」放行（回歸）", not lead_flagged("你有沒有發現那家店關了。"))
check("無「你」無問句要擋（回歸）", lead_flagged("那家店上週突然關了，沒有人說明原因。"))
# 問號落在 60 個正文字之後不算開場：前 60 字都是陳述，問句在後面
late = "那家店上週關了。" * 9 + "為什麼關了？"
check(f"問號在開頭 {STORY_LEAD_CHARS} 字之外要擋", lead_flagged(late))
sys.exit(1 if fails else 0)
