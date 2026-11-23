"""多家民調加權平均（借鏡 538）：權重 = sqrt(樣本/1000) × 0.5^(距今天數/14) × 調查方式。

全體：各家蔣／沈兩人比加權平均（未決定不計）。
族群：各家「族群兩人比 − 該家全體兩人比」加權平均，再加回全體平均；機構偏差在差距裡抵消。
ponytail: 無機構偏差校正（家數太少）；要升級需各家歷史誤差。
"""
import csv
import math
import re
from datetime import date

PATH = "/tmp/tpe2026_polls/crosstabs.csv"
TODAY = date(2026, 11, 8)
HALF_LIFE = 14
METHOD = {"網路": 0.5, "AI電話": 0.5}  # 非真人訪問減半
HOUSE = {}  # 例：{"TVBS": 2.0}；11-08 試過加倍後改回，避免和 BLUE_BIAS 重複加成。歷屆臺北市長 TVBS 平均誤差 3.1、聯合報 3.6，紀錄不足以證明較準


def load():
    polls = {}
    for r in csv.DictReader(open(PATH, encoding="utf-8-sig")):
        key = (r["pollster"], r["date"])
        p = polls.setdefault(key, {"n": int(re.match(r"\d+", r["n"]).group()), "rows": {}})
        g = p["rows"].setdefault((r["dimension"], r["group"]), {})
        g[r["candidate"]] = float(r["pct"])
        if (m := re.match(r"\d+", r["group_n"] or "")):
            g["_n"] = int(m.group())
    return polls


def weight(pollster, d, n):
    days = (TODAY - date.fromisoformat(d[:10])).days
    m = next((v for k, v in METHOD.items() if k in pollster), 1.0)
    h = next((v for k, v in HOUSE.items() if k in pollster), 1.0)
    return math.sqrt(n / 1000) * 0.5 ** (days / HALF_LIFE) * m * h


def kmt2(v):
    return v["蔣萬安"] / (v["蔣萬安"] + v["沈伯洋"])


def average(dim=None, match=None):
    """回傳 (蔣兩人比, [(機構, 日期, 權重, 該家值)])；dim=None 為全體。"""
    polls, used = load(), []
    for (who, d), p in polls.items():
        total = p["rows"].get(("整體", "全體"))
        if not total:
            continue
        if dim is None:
            val = kmt2(total)
        else:
            hit = [v for (dm, g), v in p["rows"].items()
                   if dm == dim and match(g) and "蔣萬安" in v and "沈伯洋" in v]  # 報導只給單一候選人的組跳過
            if not hit:
                continue
            # 多組合併（如信民的國小以下＋國初中）：按組樣本數加權，沒有樣本數就平均
            ws = [v.get("_n") or 1 for v in hit]
            val = sum(w * kmt2(v) for w, v in zip(ws, hit)) / sum(ws) - kmt2(total)
        used.append((who, d, weight(who, d, p["n"]), val))
    ws = sum(u[2] for u in used)
    return sum(u[2] * u[3] for u in used) / ws, used


if __name__ == "__main__":
    t, used = average()
    for u in sorted(used, key=lambda u: -u[2]):
        print(f"  {u[0][:12]:12s} {u[1][:10]} 權重{u[2]:.2f} 蔣{u[3]:.1%}")
    print(f"全體平均 蔣 {t:.1%}")
    # 自測：單一民調時平均要等於該家數值
    assert abs(kmt2({"蔣萬安": 46, "沈伯洋": 42}) - 46 / 88) < 1e-12
    for name, dim, m in [("民眾黨支持者", "政黨傾向", lambda g: "民眾" in g),
                         ("2022 投黃珊珊", "2022市長投票", lambda g: "黃珊珊" in g),
                         ("看過辯論", "是否看辯論", lambda g: g == "有"),
                         ("沒看辯論", "是否看辯論", lambda g: g == "沒有")]:
        gap, used = average(dim, m)
        print(f"{name}: 蔣 {t + gap:.1%}（{len(used)} 家：{'、'.join(u[0][:4] for u in used)}）")
