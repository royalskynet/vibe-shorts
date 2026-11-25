#!/usr/bin/env python3
"""outlier 公式自檢：邊界倍數 5.0 算離群、2.0 算偏強、1.99 算一般；中位數不被單支爆款拉高。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from outlier import score  # noqa: E402

base = [{"url": f"b{i}", "view_count": 100} for i in range(5)]
cases = {500: "離群", 200: "偏強", 199: "一般"}
for v, want in cases.items():
    med, out = score(base + [{"url": "t", "view_count": v}])
    got = next(l for _, l, e in out if e["url"] == "t")
    assert med == 100 and got == want, (v, med, got, want)
med, out = score(base + [{"url": "huge", "view_count": 10**9}])
assert med == 100 and out[0][2]["url"] == "huge", med
print("ok")
