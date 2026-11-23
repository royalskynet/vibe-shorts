import csv
import os
import sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, "/tmp/tw_map_project")
from render import area_centroid, frame
from taipei import SHAPES, LABEL_AT, FONT, BG, INK, GREY

OUT = "/tmp/tpe2026/cards"
COLOR = {"KMT": (52, 92, 160), "DPP": (74, 140, 92), "TPP": (79, 179, 176), "OTH": (150, 140, 130)}


def norm(v):
    s = sum(v.values())
    return {k: x / s for k, x in v.items()}


def load_baseline(path, colmap):
    """colmap: CSV 欄名 → 2026 政黨代碼；同黨多欄相加。"""
    out = {}
    for r in csv.DictReader(open(path)):
        v = {}
        for col, party in colmap.items():
            v[party] = v.get(party, 0) + int(r[col])
        out[r["district"]] = norm(v)
    return out


def estimate(base, group, total):
    g, t = norm(group), norm(total)
    return {d: {p: b[p] + g[p] - t[p] for p in b} for d, b in base.items()}


def card(path, title, sub, district_share, city_share, cands, note):
    """cands: [(政黨代碼, 候選人名)]，city_share: 政黨代碼 → 全市比例。"""
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H), BG)
    dr = ImageDraw.Draw(img)
    f = lambda n: ImageFont.truetype(FONT, n)
    size = 80
    while dr.textlength(title, font=f(size)) > 980:
        size -= 4
    dr.text((W / 2, 200), title, font=f(size), fill=INK, anchor="mm")
    dr.text((W / 2, 295), sub, font=f(34), fill=GREY, anchor="mm")

    allpts = [p for polys in SHAPES.values() for poly in polys for p in poly[0]]
    lons, lats = [p[0] for p in allpts], [p[1] for p in allpts]
    bounds = (min(lons), max(lons), min(lats), max(lats))
    proj = frame(*bounds, (110, 360, 970, 1360))
    old = frame(*bounds, (90, 420, 990, 1500))  # LABEL_AT 是在 taipei.py 這個框裡量的
    (ox0, oy0), (ox1, oy1) = old(bounds[0], bounds[3]), old(bounds[1], bounds[2])
    (nx0, ny0), (nx1, ny1) = proj(bounds[0], bounds[3]), proj(bounds[1], bounds[2])
    remap = lambda p: (nx0 + (p[0] - ox0) * (nx1 - nx0) / (ox1 - ox0),
                       ny0 + (p[1] - oy0) * (ny1 - ny0) / (oy1 - oy0))
    for name, polys in SHAPES.items():
        sh = district_share[name]
        color = COLOR[max(sh, key=sh.get)]
        best = (0, None)
        for poly in polys:
            ring = [proj(*p) for p in poly[0]]
            dr.polygon(ring, fill=color, outline=BG, width=4)
            a, c = area_centroid(ring)
            if a > best[0]:
                best = (a, c)
        pos = remap(LABEL_AT[name]) if name in LABEL_AT else best[1]
        dr.text(pos, name[:2], font=f(26 if name in LABEL_AT else 30), fill=(255, 255, 255), anchor="mm")

    winner = max(city_share, key=city_share.get)
    y = 1430
    for party, cand in sorted(cands, key=lambda c: -city_share[c[0]]):
        n = sum(1 for s in district_share.values() if max(s, key=s.get) == party)
        bold = party == winner
        dr.rounded_rectangle([150, y - 24, 198, y + 24], radius=8, fill=COLOR[party])
        dr.text((222, y), cand, font=f(46 if bold else 40), fill=INK, anchor="lm")
        dr.text((620, y), f"{city_share[party] * 100:.0f}%", font=f(46 if bold else 40), fill=INK, anchor="lm")
        dr.text((780, y), f"{n} 區", font=f(36), fill=GREY, anchor="lm")
        y += 72
    dr.text((W / 2, y + 20), f"推估當選：{dict(cands)[winner]}", font=f(48), fill=COLOR[winner], anchor="mm")
    for k, line in enumerate(note):
        dr.text((W / 2, 1790 + k * 38), line, font=f(25), fill=GREY, anchor="mm")
    img.save(path)


if __name__ == "__main__":
    # 自測：2022 基準＋零偏差 → 各區顏色必須等於 2022 實際最高票
    base = load_baseline("/tmp/tpe2026/mayor2022.csv",
                         {"kmt_chiang": "KMT", "dpp_chen": "DPP", "ind_huang": "TPP"})
    tot = {"KMT": 42.29, "DPP": 31.93, "TPP": 25.14}
    est = estimate(base, tot, tot)
    assert all(max(est[d], key=est[d].get) == ("DPP" if d == "大同區" else "KMT") for d in est), est
    os.makedirs(OUT, exist_ok=True)
    card(f"{OUT}/selftest.png", "2022 實際結果", "臺北市長選舉｜各區最高票", est, norm(tot),
         [("KMT", "蔣萬安"), ("DPP", "陳時中"), ("TPP", "黃珊珊")], ["自測卡", "資料：中選會"])
    print("selftest ok")
