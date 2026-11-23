import csv
import os
import sys

sys.path.insert(0, "/tmp/tpe2026")
from tpe2026 import card, estimate, norm, OUT

CANDS = [("KMT", "蔣萬安"), ("DPP", "沈伯洋")]
# TVBS 民調中心 2026/10/31 辯論後調查（n=1,747，投票意向基數 1,666），蔣／沈，未決定不計
TOTAL = {"KMT": 46, "DPP": 42}
GROUPS = [
    ("男性", (49, 43)), ("女性", (44, 41)),
    ("20 多歲", (40, 48)), ("30 多歲", (51, 42)), ("40 多歲", (46, 43)),
    ("50 多歲", (50, 42)), ("60 多歲", (48, 42)), ("70 歲以上", (40, 39)),
    ("國中以下", (31, 43)), ("高中職", (38, 47)), ("專科", (58, 33)),
    ("大學", (50, 41)), ("研究所以上", (50, 44)),
    ("2022 投黃珊珊的人", (39, 53)), ("2022 沒去投票的人", (21, 45)),
    ("民眾黨支持者", (80, 14)), ("中立選民", (37, 36)),
    ("看過辯論的人", (41, 52)), ("沒看辯論的人", (54, 27)),
]
SRC = "資料：TVBS 2026/10/31 民調（1,747 人）；各區傾向取 2024 總統大選藍綠得票"


def baseline():
    """2024 總統大選臺北各區侯／賴兩黨比，整體平移到 TVBS 全體。"""
    rows = [r for r in csv.DictReader(open("/tmp/tw_map_project/data/township_2024.csv"))
            if r["county"] == "臺北市"]
    raw = {r["township"]: norm({"KMT": int(r["hou"]), "DPP": int(r["lai"])}) for r in rows}
    w = {r["township"]: int(r["hou"]) + int(r["lai"]) for r in rows}
    city = sum(raw[d]["KMT"] * w[d] for d in raw) / sum(w.values())
    shift = norm(TOTAL)["KMT"] - city
    return {d: {"KMT": v["KMT"] + shift, "DPP": v["DPP"] - shift} for d, v in raw.items()}


if __name__ == "__main__":
    base = baseline()
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))
    card(f"{OUT}/00.png", "全體選民", "2026 臺北市長選舉｜民調推估", base, norm(TOTAL), CANDS,
         ["估計：各區傾向平移到民調全體數字", SRC])
    print("00 全體", sum(v["KMT"] > v["DPP"] for v in base.values()), "區藍")
    for k, (label, (kmt, dpp)) in enumerate(GROUPS, 1):
        g = {"KMT": kmt, "DPP": dpp}
        est = estimate(base, g, TOTAL)
        card(f"{OUT}/{k:02d}.png", f"如果只有{label}投票", "2026 臺北市長選舉｜民調推估", est, norm(g), CANDS,
             [f"估計：各區傾向加上{label}與全體的差距", SRC])
        print(f"{k:02d} {label} 蔣{norm(g)['KMT']:.0%}", sum(v["KMT"] > v["DPP"] for v in est.values()), "區藍")
