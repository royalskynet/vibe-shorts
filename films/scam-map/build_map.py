#!/usr/bin/env python3
"""縣市地圖與人均數字 → map.js（window.MAP），給 index.html 畫。

  python3 build_map.py

地圖：data/tw-counties-10t.json（taiwan-atlas 2021.9.20，MIT；底層是內政部國土測繪中心縣市界）。
數字：data/165-monthly-city-fraud-2025.json ÷ data/moi-population-2025-12.json，算法見 SOURCES.md。
預先投影成畫面座標，頁面不用載 d3／topojson，也沒有外部請求。
金門、連江在本島框外，搬到左上角小框（離島插圖）。
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE / "data"

W, H = 1080, 1920
LAT0 = 23.7
COS0 = math.cos(math.radians(LAT0))
# 本島＋澎湖的框：經度 119.3–122.1、緯度 21.85–25.35，放進畫面 y 360–1560
LON_MIN, LON_MAX, LAT_MIN, LAT_MAX = 119.3, 122.1, 21.85, 25.35
BOX = (60, 360, 1020, 1560)
K = min((BOX[2] - BOX[0]) / ((LON_MAX - LON_MIN) * COS0), (BOX[3] - BOX[1]) / (LAT_MAX - LAT_MIN))
OX = (BOX[0] + BOX[2]) / 2 - (LON_MIN + LON_MAX) / 2 * COS0 * K
OY = (BOX[1] + BOX[3]) / 2 + (LAT_MIN + LAT_MAX) / 2 * K
# 離島搬家：畫面位移（像素），讓金門、連江落在左上小框裡，放大倍率 INSET_Z
INSETS = {"金門縣": {"box": (70, 400, 330, 600), "z": 2.2},
          "連江縣": {"box": (70, 640, 330, 840), "z": 2.2}}
INSET_REACH = 200  # 像素（投影後、搬家前）
MIN_STEP = 2.0  # 簡化：跟上一個保留點距離不到 2px 的點丟掉


def proj(lon, lat):
    return lon * COS0 * K + OX, -lat * K + OY


def decode_arcs(topo):
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    out = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        out.append(pts)
    return out


def ring(arcs, idx):
    pts = []
    for i in idx:
        a = arcs[i] if i >= 0 else arcs[~i][::-1]
        pts.extend(a if not pts else a[1:])
    return pts


def polygons(geom):
    if geom["type"] == "Polygon":
        return [geom["arcs"]]
    if geom["type"] == "MultiPolygon":
        return geom["arcs"]
    return []


def simplify(pts):
    keep = [pts[0]]
    for p in pts[1:]:
        if math.dist(p, keep[-1]) >= MIN_STEP:
            keep.append(p)
    return keep


def area(pts):
    return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1])) / 2


def centroid(pts):
    a = area(pts) or 1e-9
    cx = sum((x0 + x1) * (x0 * y1 - x1 * y0) for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]))
    cy = sum((y0 + y1) * (x0 * y1 - x1 * y0) for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]))
    return cx / (6 * a), cy / (6 * a)


def fit_inset(rings, box, z):
    """離島：縮放到塞進 box（最多 z 倍），搬到 box 中心。
    離最大島超過 INSET_REACH 像素的小島不畫：金門縣含烏坵，在金門東北約 130 公里，
    算進外框的話整個縣會縮成一個點。"""
    big = max(rings, key=lambda r: abs(area(r)))
    bx0, by0 = centroid(big)
    rings = [r for r in rings if math.dist(centroid(r) if abs(area(r)) > 1 else r[0], (bx0, by0)) <= INSET_REACH]
    xs = [x for r in rings for x, _ in r]
    ys = [y for r in rings for _, y in r]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    z = min(z, 0.85 * (box[2] - box[0]) / (max(xs) - min(xs)), 0.85 * (box[3] - box[1]) / (max(ys) - min(ys)))
    bx, by = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    # 搬家參數一併回傳：衛星底圖要照同一個變換貼進小框（index.html basemap()）
    return [[(bx + (x - cx) * z, by + (y - cy) * z) for x, y in r] for r in rings], [cx, cy, z, bx, by]


def rates():
    fraud = json.loads((D / "165-monthly-city-fraud-2025.json").read_text(encoding="utf-8"))
    pop = json.loads((D / "moi-population-2025-12.json").read_text(encoding="utf-8"))
    cases = {}
    for b in fraud.values():
        for c in b["Cities"]:
            cases[c["Name"]] = cases.get(c["Name"], 0) + c["Cases"]
    return {k: {"cases": v, "pop": pop[k], "per100k": round(v / pop[k] * 1e5)} for k, v in cases.items()}


def months():
    """2025-01～2026-09 每月「每十萬人件數」第一名（165 CasePopulationRatio）。"""
    st = json.loads((D / "165-monthly-city-stats.json").read_text(encoding="utf-8"))
    return [{"m": k, "name": v["CasePopulationRatio"]["Name"]} for k, v in sorted(st.items())]


def methods():
    """2025 全年手法：件數佔比、財損佔比。只有每月前五名有名字，其餘併成「其他」。"""
    raw = json.loads((D / "165-fraud-method-2025.json").read_text(encoding="utf-8"))
    out, top = {}, None
    # 全國先算，新竹沿用全國的前四名與順序，兩條堆疊長條才能逐段對照
    for label, by_month in sorted(raw.items(), key=lambda kv: kv[0] != "全國"):
        cases, loss, tc, tl = {}, {}, 0, 0
        for b in by_month.values():
            tc += b["TotalCases"]
            tl += b["TotalLosses"]
            for t in b["TopFive"]:
                cases[t["Name"]] = cases.get(t["Name"], 0) + t["Cases"]
                loss[t["Name"]] = loss.get(t["Name"], 0) + t["Losses"]
        top = top or sorted(cases, key=lambda k: -cases[k])[:4]
        rows = [{"name": k.replace("詐騙", ""), "cases": round(cases[k] / tc, 3), "loss": round(loss[k] / tl, 3)}
                for k in top]
        rows.append({"name": "其他", "cases": round(1 - sum(r["cases"] for r in rows), 3),
                     "loss": round(1 - sum(r["loss"] for r in rows), 3)})
        out[label] = rows
    return out


def build():
    topo = json.loads((D / "tw-counties-10t.json").read_text(encoding="utf-8"))
    arcs = decode_arcs(topo)
    stats = rates()
    counties, xf = [], {}
    for g in topo["objects"]["counties"]["geometries"]:
        name = g["properties"]["COUNTYNAME"].replace("台", "臺")  # 地圖寫台，165／內政部寫臺
        rings = [simplify([proj(*p) for p in ring(arcs, poly[0])]) for poly in polygons(g)]
        rings = [r for r in rings if len(r) >= 3]
        if name in INSETS:
            rings, t = fit_inset(rings, INSETS[name]["box"], INSETS[name]["z"])
            xf[name] = [round(v, 3) for v in t]
        big = max(rings, key=lambda r: abs(area(r)))
        cx, cy = centroid(big)
        counties.append({"name": name, "cx": round(cx, 1), "cy": round(cy, 1),
                         "rings": [[round(v, 1) for p in r for v in p] for r in rings],
                         **stats[name]})
    counties.sort(key=lambda c: -c["per100k"])
    for i, c in enumerate(counties):
        c["rank"] = i + 1
    total_cases = sum(s["cases"] for s in stats.values())
    total_pop = sum(s["pop"] for s in stats.values())
    return {"counties": counties, "insets": {k: v["box"] for k, v in INSETS.items()}, "insetXf": xf,
            "months": months(), "methods": methods(),
            "national": {"cases": total_cases, "pop": total_pop,
                         "per100k": round(total_cases / total_pop * 1e5)}}


if __name__ == "__main__":
    m = build()
    (HERE / "map.js").write_text("// build_map.py 產生，不要手改。\nwindow.MAP = "
                                 + json.dumps(m, ensure_ascii=False, separators=(",", ":")) + ";\n",
                                 encoding="utf-8")
    pts = sum(len(r) // 2 for c in m["counties"] for r in c["rings"])
    print(f"{len(m['counties'])} 縣市、{pts} 點；全國每十萬 {m['national']['per100k']}；"
          f"第一 {m['counties'][0]['name']} {m['counties'][0]['per100k']}、最後 {m['counties'][-1]['name']} {m['counties'][-1]['per100k']}")
