#!/usr/bin/env python3
"""postmortem_refresh.refresh：只更新「初記」且滿 120h 的段，教訓不動、已滿的段不動、缺數字不動。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "publish"))
from postmortem_refresh import parse_stats, refresh  # noqa: E402

MD = """快照 2026-10-19（stats-20261019.tsv）

## a
- 上架：50h 初記
- yt：播放 1／讚 0／留言 0
- ig：播放 2／讚 0／留言 0
- threads：播放 3／讚 0／留言 0
- 下次要改：教訓 A 不准動。

## b
- 上架：109h 初記
- yt：播放 1／讚 0／留言 0
- ig：播放 1／讚 0／留言 0
- threads：播放 1／讚 0／留言 0
- 下次要改：教訓 B。

## c
- 上架：125h
- yt：播放 9／讚 0／留言 0
- ig：播放 9／讚 0／留言 0
- threads：播放 9／讚 0／留言 0
- 下次要改：教訓 C。
"""
H = "平台\t日期\t上架\t播放\t讚\t留言\t分享\tID\t標題\n"
ROWS = [("yt", "121h", "700", "6", "1", "YA"), ("ig", "121h", "170", "2", "0", "IA"), ("threads", "121h", "30", "1", "1", "TA"),
        ("yt", "180h", "150", "3", "0", "YB"), ("ig", "180h", "8", "0", "0", "IB"),   # b 缺 threads
        ("yt", "196h", "99", "0", "0", "YC"), ("ig", "196h", "99", "0", "0", "IC"), ("threads", "196h", "99", "0", "0", "TC")]
TSV = H + "".join(f"{p}\t2026-10-17\t{h}\t{v}\t{l}\t{c}\t-\t{i}\tx\n" for p, h, v, l, c, i in ROWS)
IDS = {"a": {"yt": "YA", "ig": "IA", "threads": "TA"}, "b": {"yt": "YB", "ig": "IB", "threads": "TB"},
       "c": {"yt": "YC", "ig": "IC", "threads": "TC"}}

new, done = refresh(MD, parse_stats(TSV), IDS, "10-22")
assert done == ["a"], done                                         # b 缺 threads 不動；c 已非初記不動
seg_a = new.split("## a\n")[1].split("## b")[0]
assert "- 上架：121h（10-22 更新）" in seg_a and "初記" not in seg_a
assert "- yt：播放 700／讚 6／留言 1" in seg_a and "- threads：播放 30／讚 1／留言 1" in seg_a
assert "- 下次要改：教訓 A 不准動。" in seg_a and "- 重看：" in seg_a
assert "109h 初記" in new and "播放 9／讚 0／留言 0" in new           # b、c 原樣
assert new.count("## ") == 3

# 未滿 120h 不動
young = TSV.replace("121h", "100h")
assert refresh(MD, parse_stats(young), IDS, "10-22")[1] == []
print("test_postmortem_refresh ok")
