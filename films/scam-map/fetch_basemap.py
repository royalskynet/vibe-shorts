"""衛星底圖：EOxCloudless 2016（Sentinel-2，CC BY 4.0，可商用）。
2018 之後的年份是 CC BY-NC-SA，不能用在會營利的頻道，所以固定拿 2016 的 `s2cloudless` 圖層。
授權條件：畫面上與說明欄要清楚標出處（ATTRIB），index.html 底部有一行小字。
來源：https://cloudless.eox.at/license-non-commercial（2026-10-14 查）。

輸出 data/basemap/*.jpg 與 basemap.js（每張圖在地圖座標裡的矩形）。已存在的圖不重抓。
"""
import json
import urllib.parse
import urllib.request
from pathlib import Path

from build_map import HERE, proj

OUT = HERE / "data" / "basemap"
WMS = "https://tiles.maps.eox.at/wms"
LAYER = "s2cloudless"  # 2016 版；別換成 s2cloudless-20xx，授權不同
ATTRIB = "EOxCloudless https://cloudless.eox.at by EOX IT Services GmbH (Contains modified Copernicus Sentinel data 2016 & 2017)"
MAX_PX = 4096  # EOX 單次請求上限

# name: (lon0, lat0, lon1, lat1, 長邊像素)。大圖墊底，細圖疊在會推近的地方。
# ponytail: 新竹市推近到約 4 倍時 wide 會糊，所以北部另抓一張；要更清楚就再切細圖。
TILES = {
    "wide": (116.0, 19.5, 124.5, 27.8, 4096),
    "north": (120.55, 24.2, 122.05, 25.35, 4096),
    "kinmen": (118.15, 24.35, 118.55, 24.56, 2048),
    "matsu": (119.85, 25.92, 120.55, 26.42, 2048),
}


def size(lon0, lat0, lon1, lat1, long_px):
    x0, y0 = proj(lon0, lat1)
    x1, y1 = proj(lon1, lat0)
    w, h = x1 - x0, y1 - y0
    k = long_px / max(w, h)
    return (x0, y0, w, h), round(w * k), round(h * k)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tiles = []
    for name, (lon0, lat0, lon1, lat1, px) in TILES.items():
        assert px <= MAX_PX
        rect, w, h = size(lon0, lat0, lon1, lat1, px)
        f = OUT / f"{name}.jpg"
        if not f.exists():
            q = {"service": "WMS", "version": "1.1.1", "request": "GetMap", "layers": LAYER, "styles": "",
                 "srs": "EPSG:4326", "bbox": f"{lon0},{lat0},{lon1},{lat1}", "width": w, "height": h,
                 "format": "image/jpeg"}
            with urllib.request.urlopen(f"{WMS}?{urllib.parse.urlencode(q)}", timeout=120) as r:
                ct, body = r.headers.get("Content-Type", ""), r.read()
            if not ct.startswith("image/"):
                raise SystemExit(f"{name}: WMS 回的不是圖（{ct}）：{body[:300]!r}")
            f.write_bytes(body)
        tiles.append({"name": name, "src": f"data/basemap/{name}.jpg", "rect": [round(v, 2) for v in rect]})
        print(f"{name}: {w}x{h}  {f.stat().st_size // 1024}KB")
    (HERE / "basemap.js").write_text("// fetch_basemap.py 產生，不要手改。\nwindow.BASEMAP = "
                                     + json.dumps({"attrib": ATTRIB, "tiles": tiles}, ensure_ascii=False) + ";\n",
                                     encoding="utf-8")


if __name__ == "__main__":
    main()
