"""2026 臺北市長卡片，族群傾向不用 2026 選舉民調。

族群：台灣民意基金會 2024/1 大選後全國調查（柯, 賴, 侯）與全體的差距，加到臺北各區 2024 實際得票。
2026 換算：蔣 = 侯 + k·柯，沈 = 賴 + (1−k)·柯；k 只用一個數字定（TVBS 10/31 全體蔣／沈）。
ponytail: k 全族群同一個值，年輕人柯票流向若和長輩不同會失真；要升級需柯票流向分齡資料。
"""
import csv
import re
import os
import sys

sys.path.insert(0, "/tmp/tpe2026")
sys.path.insert(0, "/tmp/tw_map_project")
from tpe2026 import card, estimate, norm, OUT
from taipei import GROUPS as TPOF

CANDS = [("KMT", "蔣萬安"), ("DPP", "沈伯洋")]
from polls import average

# 民調偏差校正：2014/2018/2022 臺北市長選前民調低估藍營兩人比 +2.98/+2.85/+2.21，平均 +2.7（見 poll_bias.csv）
BLUE_BIAS = 0.027
_t = average()[0] + BLUE_BIAS
TVBS_TOTAL = {"KMT": _t, "DPP": 1 - _t}  # 多家民調加權平均（名稱沿用，見 polls.py）
AGES = ["20-29", "30-39", "40-49", "50-59", "60-69", "70+"]
DEMO_CARDS = [("男性", "性別", lambda g: g == "男"), ("女性", "性別", lambda g: g == "女")]
DEMO_CARDS += [(f"{a.replace('-', '–')} 歲的人" if a != "70+" else "70 歲以上的人", "年齡", lambda g, a=a: g == a)
               for a in AGES]
DEMO_CARDS += [("國中以下學歷的人", "教育", lambda g: g in ("國中以下", "國小以下", "國初中")),
               ("高中職學歷的人", "教育", lambda g: g in ("高中職", "高中高職")),
               ("專科學歷的人", "教育", lambda g: g == "專科"),
               ("大學學歷的人", "教育", lambda g: g == "大學"),
               ("研究所以上學歷的人", "教育", lambda g: g == "研究所以上")]
POLL_CARDS = [("看過辯論的人", "是否看辯論", lambda g: g == "有"),
              ("沒看辯論的人", "是否看辯論", lambda g: g == "沒有"),
              ("2022 投黃珊珊的人", "2022市長投票", lambda g: "黃珊珊" in g),
              ("民眾黨支持者", "政黨傾向", lambda g: "民眾" in g)]
RENAME = {"河洛人": "本省閩南人", "客家人": "本省客家人", "基層白領": "基層上班族",
          "小學及以下": "小學以下學歷", "國中": "國中學歷", "高中職": "高中職學歷",
          "專科": "專科學歷", "大學以上": "大學以上學歷", "2022 投黃珊珊的人": "2022 投黃珊珊的人"}
# 資策會 2024Q4 社群使用率：18–24、25–34、全體；35 歲以上由全體反推（臺北 20 歲以上人口加權）
PLATFORM = {"Dcard": (0.459, 0.309, 0.176), "Threads": (0.44, 0.284, 0.175)}
# 內政部 112 年底臺北市 20 歲以上人口，5 歲一級
POP5 = {"20-24": 114734, "25-29": 138893, "30-34": 151299, "35-39": 170982, "40-49": 212778 + 199146,
        "50-59": 185797 + 186324, "60-69": 188813 + 184266,
        "70+": 158497 + 87937 + 62389 + 35454 + 17835 + 5686 + 1091}
BIN = {"20-24": "20-29", "25-29": "20-29", "30-34": "30-39", "35-39": "30-39"}
SRC_TPOF = "族群傾向：台灣民意基金會 2024/1 大選後調查"
SRC_DIST = "各區：中選會 2024 總統開票"
SRC_K = "柯 2024 選票流向按上述全體蔣沈比例分配"


def to2026(v, k):
    ko, lai, hou = v
    return {"KMT": hou + k * ko, "DPP": lai + (1 - k) * ko}


def district_votes():
    rows = [r for r in csv.DictReader(open("/tmp/tw_map_project/data/township_2024.csv"))
            if r["county"] == "臺北市"]
    return {r["township"]: [int(r[c]) for c in ("ko", "lai", "hou")] for r in rows}


def share(v):
    s = sum(v)
    return [x / s for x in v]


def solve_k(votes):
    ko, lai, hou = share([sum(v[i] for v in votes.values()) for i in range(3)])
    target = norm(TVBS_TOTAL)["KMT"]
    return (target - hou) / ko


def swing3(votes, g, t, k):
    """各區三人得票率 + (族群 − 全體)，再換成 2026 兩人；回傳 (各區, 全市)。"""
    g, t = share(g), share(t)
    shift = lambda v: [max(v[i] + g[i] - t[i], 0) for i in range(3)]
    dist = {d: norm(to2026(shift(share(v)), k)) for d, v in votes.items()}
    city = share([sum(v[i] for v in votes.values()) for i in range(3)])
    return dist, norm(to2026(shift(city), k))


def platform_gap(rates):
    """平台使用者相對全體的蔣兩人比差距：2026 民調各年齡差距 × (臺北人口 × 使用率)。"""
    r1824, r2534, overall = rates
    adult = sum(POP5.values())
    young = POP5["20-24"] * r1824 + (POP5["25-29"] + POP5["30-34"]) * r2534
    rest = adult - POP5["20-24"] - POP5["25-29"] - POP5["30-34"]
    r35 = (overall * adult - young) / rest
    rate = lambda b: r1824 if b == "20-24" else r2534 if b in ("25-29", "30-34") else r35
    gaps = {a: average("年齡", lambda g, a=a: g == a)[0] for a in AGES}
    w = {b: POP5[b] * rate(b) for b in POP5}
    return sum(w[b] * gaps[BIN.get(b, b)] for b in w) / sum(w.values()), r35


def main():
    votes = district_votes()
    k = solve_k(votes)
    assert 0 < k < 1, k
    print(f"k={k:.3f}（柯票給蔣的比例）")
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))
    sub = "2026 臺北市長選舉｜推估"

    base = {d: norm(to2026(share(v), k)) for d, v in votes.items()}
    city = norm(to2026(share([sum(v[i] for v in votes.values()) for i in range(3)]), k))
    assert abs(city["KMT"] - norm(TVBS_TOTAL)["KMT"]) < 1e-9
    cards = [("全體選民", base, city, ["全體：8 份民調加權平均，再加歷屆民調低估藍營的 2.7 點", SRC_DIST, SRC_K])]

    def poll_card(label, dim, match, extra=""):
        gap, used = average(dim, match)
        grp = {"KMT": _t + gap, "DPP": 1 - _t - gap}
        houses = "、".join(dict.fromkeys(re.sub(r"民調中心|民調雲|協會|[(/（].*", "", u[0]) for u in used))
        return (f"如果只有{label}投票", estimate(base, grp, TVBS_TOTAL), grp,
                [f"{extra}族群傾向：{len(used)} 份民調加權平均（{houses}）", SRC_DIST,
                 "全體：8 份民調加權平均，再加歷屆民調低估藍營的 2.7 點"])

    for label, dim, match in DEMO_CARDS:
        cards.append(poll_card(label, dim, match))

    for dim, total, items in TPOF:
        if dim not in ("族群", "職業"):
            continue
        for label, n, g in items:
            name = RENAME.get(label, label)
            d, c = swing3(votes, g, total, k)
            cards.append((f"如果只有{name.replace(' 歲', '歲')}的人投票" if "歲" in name or name.endswith("學歷") else f"如果只有{name}投票", d, c, [f"{SRC_TPOF}（{name} {n} 人）", SRC_DIST, SRC_K]))

    for plat, rates in PLATFORM.items():
        gap, r35 = platform_gap(rates)
        grp = {"KMT": _t + gap, "DPP": 1 - _t - gap}
        print(f"{plat} 35+ 使用率反推 {r35:.1%}")
        cards.append((f"如果只有{plat}上的臺北人投票", estimate(base, grp, TVBS_TOTAL), grp,
                      [f"兩層推估：資策會 2024 各年齡 {plat} 使用率 × 2026 民調各年齡傾向", SRC_DIST,
                       "全體：8 份民調加權平均，再加歷屆民調低估藍營的 2.7 點"]))

    for label, dim, match in POLL_CARDS:
        cards.append(poll_card(label, dim, match))

    for i, (title, d, c, note) in enumerate(cards):
        card(f"{OUT}/{i:02d}.png", title, sub, d, c, CANDS, note)
        blue = sum(v["KMT"] > v["DPP"] for v in d.values())
        print(f"{i:02d} {title} 蔣{c['KMT']:.1%} 沈{c['DPP']:.1%} 藍{blue}區")
    close = sum(abs(c["KMT"] - c["DPP"]) < 0.06 for _, _, c, _ in cards)
    end_card(f"{OUT}/{len(cards):02d}.png", len(cards), close)
    print(f"{len(cards):02d} 結尾卡：{len(cards)} 張裡 {close} 張差距不到 6 點")


def end_card(path, n, close):
    from PIL import Image, ImageDraw, ImageFont
    from taipei import FONT, BG, INK, GREY
    img = Image.new("RGB", (1080, 1920), BG)
    dr = ImageDraw.Draw(img)
    f = lambda k: ImageFont.truetype(FONT, k)
    dr.text((540, 640), "決定結果的是投票率", font=f(80), fill=INK, anchor="mm")
    dr.text((540, 780), f"{n} 張圖裡，{close} 張兩人差距不到 6 個百分點", font=f(40), fill=GREY, anchor="mm")
    dr.text((540, 1080), "不管你支持誰", font=f(64), fill=INK, anchor="mm")
    dr.text((540, 1180), "11 月 28 日，為自己", font=f(64), fill=INK, anchor="mm")
    dr.text((540, 1280), "也為公民社會去投票", font=f(64), fill=INK, anchor="mm")
    img.save(path)


if __name__ == "__main__":
    main()
