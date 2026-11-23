import csv
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from render import area_centroid, frame

FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
BG = (244, 237, 225)
INK = (37, 36, 34)
GREY = (110, 105, 98)
PARTY = [("民眾黨", (79, 179, 176)), ("民進黨", (74, 140, 92)), ("國民黨", (52, 92, 160))]
OUT = "/tmp/tw_map_project/taipei_cards"
# 小區塊的質心會壓到邊界，手動放（像素，畫布 1080x1920）
LABEL_AT = {"大同區": (343, 1060), "中山區": (422, 1075), "中正區": (365, 1165), "萬華區": (282, 1215)}

# 台灣民意基金會 2024-01-15~17 投票後調查，橫%（柯, 賴, 侯）；每組附該題全體列
GROUPS = [
    ("性別", (23.7, 38.8, 27.2), [("男性", 451, (28.4, 42.8, 21.3)), ("女性", 473, (19.3, 35.1, 32.8))]),
    ("年齡", (23.8, 38.9, 27.2), [
        ("20–24 歲", 49, (47.4, 25.2, 21.1)), ("25–34 歲", 147, (56.1, 26.6, 11.0)),
        ("35–44 歲", 160, (38.8, 33.2, 17.6)), ("45–54 歲", 171, (18.8, 38.3, 33.3)),
        ("55–64 歲", 175, (7.6, 42.7, 41.8)), ("65 歲以上", 221, (2.8, 51.7, 30.0))]),
    ("族群", (23.8, 38.9, 27.2), [
        ("河洛人", 697, (23.2, 44.3, 23.5)), ("客家人", 105, (24.2, 29.5, 29.0)),
        ("外省人", 100, (25.2, 16.7, 47.1))]),
    ("教育", (23.8, 38.8, 27.2), [
        ("小學及以下", 107, (2.5, 50.0, 23.9)), ("國中", 98, (1.5, 67.4, 26.3)),
        ("高中職", 247, (24.4, 34.6, 29.2)), ("專科", 105, (21.7, 34.5, 37.2)),
        ("大學以上", 365, (36.3, 31.9, 24.1))]),
    ("職業", (23.9, 39.0, 27.2), [
        ("自營商／老闆", 123, (26.6, 40.5, 25.0)), ("高階白領", 132, (37.1, 34.7, 23.2)),
        ("基層白領", 200, (39.1, 32.4, 19.8)), ("勞工", 100, (23.4, 44.6, 25.1)),
        ("家庭主婦", 133, (6.4, 37.9, 40.3)), ("退休人員", 127, (2.9, 47.9, 33.9))]),
]


def share(v):
    s = sum(v)
    return [x / s for x in v]


def load_votes():
    rows = [r for r in csv.DictReader(open("/tmp/tw_map_project/data/township_2024.csv"))
            if r["county"] == "臺北市"]
    return {r["township"]: [int(r["ko"]), int(r["lai"]), int(r["hou"])] for r in rows}


def load_shapes():
    from render import decode
    topo = json.load(open("/tmp/tw_map_project/towns.json"))
    topo["objects"]["counties"] = {"geometries": [
        {**g, "properties": {"COUNTYNAME": g["properties"]["TOWNNAME"]}}
        for g in topo["objects"]["towns"]["geometries"]
        if g["properties"]["COUNTYNAME"] in ("台北市", "臺北市")]}
    return decode(topo)


def swing(district_votes, group, total):
    d = share(district_votes)
    g, t = share(group), share(total)
    return [d[i] + g[i] - t[i] for i in range(3)]


def card(path, title, sub, winners, note):
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H), BG)
    dr = ImageDraw.Draw(img)
    f = lambda n: ImageFont.truetype(FONT, n)
    dr.text((W / 2, 230), title, font=f(84), fill=INK, anchor="mm")
    dr.text((W / 2, 330), sub, font=f(36), fill=GREY, anchor="mm")

    allpts = [p for polys in SHAPES.values() for poly in polys for p in poly[0]]
    lons, lats = [p[0] for p in allpts], [p[1] for p in allpts]
    proj = frame(min(lons), max(lons), min(lats), max(lats), (90, 420, 990, 1500))
    for name, polys in SHAPES.items():
        color = PARTY[winners[name]][1]
        best = (0, None)
        for poly in polys:
            ring = [proj(*p) for p in poly[0]]
            dr.polygon(ring, fill=color, outline=BG, width=4)
            a, c = area_centroid(ring)
            if a > best[0]:
                best = (a, c)
        pos = LABEL_AT.get(name, best[1])
        dr.text(pos, name[:2], font=f(26 if name in LABEL_AT else 30), fill=(255, 255, 255), anchor="mm")

    counts = [sum(1 for w in winners.values() if w == i) for i in range(3)]
    x = 140
    for i in (1, 2, 0):
        label, color = PARTY[i]
        dr.rounded_rectangle([x, 1580, x + 44, 1624], radius=8, fill=color)
        dr.text((x + 60, 1602), f"{label} {counts[i]} 區", font=f(38), fill=INK, anchor="lm")
        x += 290
    for k, line in enumerate(note):
        dr.text((W / 2, 1720 + k * 40), line, font=f(26), fill=GREY, anchor="mm")
    img.save(path)


SHAPES = load_shapes()

if __name__ == "__main__":
    votes = load_votes()
    assert set(votes) == set(SHAPES), (set(votes) ^ set(SHAPES))
    os.makedirs(OUT, exist_ok=True)
    tot = [sum(v[i] for v in votes.values()) for i in range(3)]
    print("臺北市合計 柯 賴 侯", tot, "賴−侯", tot[1] - tot[2])
    src = "資料：中選會開票；台灣民意基金會 2024/1/15–17 投票後調查（1,083 人）"
    actual = {n: max(range(3), key=lambda i: v[i]) for n, v in votes.items()}
    card(f"{OUT}/00.png", "全體選民", "2024 總統大選｜臺北市各區最高票", actual,
         ["實際開票結果", "資料：中選會"])
    k = 1
    for _, total, items in GROUPS:
        for label, n, g in items:
            est = {d: max(range(3), key=lambda i: swing(v, g, total)[i]) for d, v in votes.items()}
            card(f"{OUT}/{k:02d}.png", f"如果只有{label}投票", "2024 總統大選｜臺北市各區", est,
                 [f"估計：各區實際得票率加上{label}與全體的全國差距（樣本 {n} 人）", src])
            print(f"{k:02d} {label}", [sum(1 for w in est.values() if w == i) for i in range(3)])
            k += 1
