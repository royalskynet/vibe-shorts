#!/usr/bin/env python3
"""cover.sh 自檢：IG 網格 3:4 中央裁切要看到完整的第 0 幀。

假片 1080x1920：第 0 幀是藍底、頂端 y 40–240 一條白帶（模擬系列標籤／大標頂端，原本會被裁掉），
之後幾幀換成黑底（確認取的是第 0 幀）。
  1. 輸出 1080x1920
  2. 3:4 中央裁切（y 240–1680）裡看得到白帶 → 縮到高 1440 置中才成立；沒縮就被裁掉
  3. 上下補邊是第 0 幀左上角的藍，不是黑
"""
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COVER = os.path.join(ROOT, "scripts", "cover.sh")
fails = []


def px(img, x, y):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", img, "-vf", f"format=rgb24,crop=1:1:{x}:{y}",
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return tuple(raw[:3])


def near(a, b, tol=24):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


BLUE, WHITE = (0x30, 0x50, 0xa0), (255, 255, 255)

with tempfile.TemporaryDirectory() as d:
    film = os.path.join(d, "demo")
    os.makedirs(film)
    src = os.path.join(film, "demo.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y",
                    "-f", "lavfi", "-i", "color=0x3050a0:s=1080x1920:d=0.1:r=30",
                    "-f", "lavfi", "-i", "color=black:s=1080x1920:d=0.3:r=30",
                    "-filter_complex", "[0]drawbox=x=100:y=40:w=880:h=200:color=white:t=fill[a];[a][1]concat=n=2:v=1",
                    "-pix_fmt", "yuv420p", src], check=True)
    r = subprocess.run(["bash", COVER, src], capture_output=True, text=True)
    out = os.path.join(film, "dist", "demo-cover.jpg")
    if r.returncode != 0 or not os.path.isfile(out):
        sys.exit(f"cover.sh 失敗：{r.stdout}{r.stderr}")
    wh = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-of", "csv=p=0", out],
                        capture_output=True, text=True, check=True).stdout.strip()
    if wh != "1080,1920":
        fails.append(f"尺寸 {wh} 不是 1080x1920")
    crop = os.path.join(d, "c34.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-vf", "crop=1080:1440:0:240", crop], check=True)
    # 白帶縮成 0.75 倍＝y 30–180，3:4 裁切後也是 y 30–180；取 y=100 正中
    if not near(px(crop, 540, 100), WHITE):
        fails.append(f"3:4 裁切後頂端白帶不見了：{px(crop, 540, 100)}")
    # 白帶之下是第 0 幀的藍底，不是後面幀的黑
    if not near(px(crop, 540, 700), BLUE):
        fails.append(f"中間不是第 0 幀的藍底：{px(crop, 540, 700)}")
    # 補邊：最上 240px 與左右 135px 要是取樣出的藍
    for x, y in ((540, 100), (20, 1000), (1060, 1800)):
        if not near(px(out, x, y), BLUE):
            fails.append(f"({x},{y}) 補邊不是第 0 幀底色：{px(out, x, y)}")

if fails:
    sys.exit("\n".join(fails))
print("cover: 全部通過")
