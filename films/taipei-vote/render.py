import json
import math
import sys
from PIL import Image, ImageDraw, ImageFont

GREEN = (46, 139, 87)
BLUE = (30, 90, 180)
WHITE = (40, 170, 170)
NONE = (222, 218, 205)
BG = (250, 248, 240)
INK = (30, 30, 30)
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"

# 2024 總統選舉各縣市得票率（柯, 賴, 侯），維基百科引中選會
RESULTS = {
    "臺北市": (23.79, 38.13, 38.08), "新北市": (26.24, 38.59, 35.17),
    "基隆市": (26.60, 34.77, 38.63), "宜蘭縣": (26.27, 44.74, 28.99),
    "桃園市": (30.61, 35.27, 34.12), "新竹縣": (35.55, 27.42, 37.03),
    "新竹市": (34.30, 34.79, 30.90), "苗栗縣": (30.01, 28.81, 41.18),
    "臺中市": (30.05, 37.58, 32.37), "彰化縣": (28.96, 38.11, 32.93),
    "南投縣": (26.05, 35.95, 38.00), "雲林縣": (26.13, 44.54, 29.33),
    "嘉義縣": (23.03, 47.69, 29.28), "嘉義市": (25.34, 43.26, 31.40),
    "臺南市": (23.44, 50.95, 25.61), "高雄市": (21.88, 48.89, 29.23),
    "屏東縣": (21.65, 47.51, 30.84), "臺東縣": (23.28, 27.41, 49.32),
    "花蓮縣": (24.72, 24.78, 50.50), "澎湖縣": (24.76, 38.60, 36.63),
    "金門縣": (28.58, 10.02, 61.40), "連江縣": (26.81, 10.52, 62.67),
}


def winner_color(name):
    shares = RESULTS[name]
    return (WHITE, GREEN, BLUE)[max(range(3), key=lambda i: shares[i])]


def decode(topo):
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    arcs = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)

    def ring(idx):
        out = []
        for i in idx:
            pts = arcs[i] if i >= 0 else arcs[~i][::-1]
            out.extend(pts if not out else pts[1:])
        return out

    counties = {}
    for g in topo["objects"]["counties"]["geometries"]:
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        counties[g["properties"]["COUNTYNAME"].replace("台", "臺")] =[[ring(r) for r in p] for p in polys]
    return counties


def area_centroid(r):
    a = cx = cy = 0
    for (x0, y0), (x1, y1) in zip(r, r[1:] + r[:1]):
        c = x0 * y1 - x1 * y0
        a += c
        cx += (x0 + x1) * c
        cy += (y0 + y1) * c
    if a == 0:
        return 0, r[0]
    return abs(a / 2), (cx / (3 * a), cy / (3 * a))


def frame(lon0, lon1, lat0, lat1, box):
    k = math.cos(math.radians(23.7))
    x0, y0, x1, y1 = box
    s = min((x1 - x0) / ((lon1 - lon0) * k), (y1 - y0) / (lat1 - lat0))
    ox = x0 + ((x1 - x0) - (lon1 - lon0) * k * s) / 2
    oy = y0 + ((y1 - y0) - (lat1 - lat0) * s) / 2
    return lambda lon, lat: (ox + (lon - lon0) * k * s, oy + (lat1 - lat) * s)


def render(out_path, title, subtitle, color_of=winner_color,
           source="資料：中選會 2024 總統選舉各縣市開票（經維基百科）；邊界：taiwan-atlas",
           none_label=None):
    counties = decode(json.load(open("/tmp/tw_map_project/counties.json")))
    W, H = 1080, 1350
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f_title = ImageFont.truetype(FONT, 46)
    f_sub = ImageFont.truetype(FONT, 26)
    f_lab = ImageFont.truetype(FONT, 20)
    f_small = ImageFont.truetype(FONT, 18)

    main_proj = frame(119.3, 122.1, 21.85, 25.35, (60, 170, 1020, 1230))
    insets = {
        "連江縣": (50, 190, 270, 360, 119.85, 120.55, 25.9, 26.42),
        "金門縣": (50, 400, 270, 520, 118.18, 118.52, 24.36, 24.54),
    }

    def draw_county(name, proj):
        best = (0, None)
        for poly in counties[name]:
            outer = [proj(*p) for p in poly[0]]
            edge = color_of(name) if name in insets or name == "澎湖縣" else (255, 255, 255)
            d.polygon(outer, fill=color_of(name), outline=edge, width=2)
            area, c = area_centroid(outer)
            if area > best[0]:
                best = (area, c)
        return best[1]

    centers = {}
    # 縣界的洞就是被包住的市（臺北、嘉義市），後畫蓋上去
    for name in sorted(counties, key=lambda n: n in ("臺北市", "嘉義市")):
        if name in insets:
            x0, y0, x1, y1, *bounds = insets[name]
            d.rectangle((x0, y0, x1, y1), outline=(170, 170, 170), width=2)
            draw_county(name, frame(*bounds, (x0 + 10, y0 + 10, x1 - 10, y1 - 35)))
            centers[name] = ((x0 + x1) / 2, y1 - 20)
        else:
            centers[name] = draw_county(name, main_proj)

    nudge = {"臺北市": (-70, -75), "基隆市": (75, -35), "新竹市": (-90, -25),
             "嘉義市": (-110, -10)}
    on_map_shift = {"新北市": (15, 75), "嘉義縣": (30, 15), "澎湖縣": (0, 60)}
    keep_full = ("新竹市", "新竹縣", "嘉義市", "嘉義縣")
    for name, (cx, cy) in centers.items():
        dx, dy = nudge.get(name, (0, 0))
        tx, ty = cx + dx, cy + dy
        if (dx, dy) != (0, 0):
            d.line([(cx, cy), (tx, ty)], fill=INK, width=2)
        sx, sy = on_map_shift.get(name, (0, 0))
        tx, ty = tx + sx, ty + sy
        label = name if name in keep_full else name[:2]
        bb = d.textbbox((0, 0), label, font=f_lab)
        w, h = bb[2] - bb[0], bb[3] - bb[1]
        on_map = (dx, dy) == (0, 0) and name not in insets and name != "澎湖縣"
        if not on_map:
            d.rectangle([tx - w / 2 - 4, ty - h / 2 - 4, tx + w / 2 + 4, ty + h / 2 + 4], fill=BG)
        d.text((tx - w / 2, ty - h / 2 - 4), label, font=f_lab,
               fill=INK if not on_map or color_of(name) == NONE else (255, 255, 255))

    d.text((60, 40), title, font=f_title, fill=INK)
    d.text((60, 105), subtitle, font=f_sub, fill=(90, 90, 90))
    ly = 1250
    for x, color, text in ((60, GREEN, "賴清德（民進黨）"), (360, BLUE, "侯友宜（國民黨）"),
                           (660, WHITE, "柯文哲（民眾黨）")) + (
                           ((60, NONE, none_label),) if none_label else ()):
        if color == NONE:
            ly = 1205
        d.rectangle([x, ly, x + 30, ly + 30], fill=color)
        d.text((x + 40, ly), text, font=f_sub, fill=INK)
    d.text((60, 1300), source, font=f_small, fill=(120, 120, 120))
    img.save(out_path)
    print("saved", out_path)


if __name__ == "__main__":
    render(sys.argv[1] if len(sys.argv) > 1 else "/tmp/tw_map_project/map_national.png",
           "2024 總統大選：全體選民", "各縣市最高票候選人")
