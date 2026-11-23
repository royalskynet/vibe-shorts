#!/usr/bin/env python3
"""每張卡「快結束」那一幀拼成 qa/cards.jpg：目視自評看的是動畫跑完的樣子。

qa_sheet.sh 的均勻抽幀常落在卡片中段（value-life 11-01：島名卡六個名字只看到四個），要另外手抽尾幀。
卡的起點＝那句開口前 0.25 秒（各片 index.html 的 T0），所以第 i 卡結束在第 i+1 句 t0−0.25。
用法：python3 scripts/card_sheet.py films/<片>
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LEAD = 0.25    # 同 index.html：卡比句子早 0.25 秒換
BEFORE = 0.2   # 取卡結束前多久那一幀
END_PAD = 0.3  # 同 index.html END0：末句結束後 0.3 秒進片尾系列卡


def card_end_times(tl):
    """timeline 物件 → 每張卡的取樣時間（秒）。"""
    lines, dur = tl["lines"], tl["dur"]
    starts = [0.0] + [l["t0"] - LEAD for l in lines[1:]]
    # 末卡在片尾系列卡前結束（index.html 的 END0＝末句 t1＋0.3）；取到 dur 會拍到片尾卡（democracy-noise 卡22 冷讀誤報）
    last = lines[-1].get("t1")
    ends = starts[1:] + [min(dur, last + END_PAD) if last is not None else dur]
    return [round(max(s, e - BEFORE), 3) for s, e in zip(starts, ends)]


def load_tl(path):
    m = re.search(r"window\.TL\s*=\s*(\{.*\})\s*;?\s*$", path.read_text(encoding="utf-8"), re.S)
    if not m:
        raise SystemExit(f"{path} 不是 window.TL = {{...}} 格式")
    return json.loads(m.group(1))


def pad_color(first_card):
    """拼圖第一張卡的底色（左上 5,5）給 tile 補未用格；冷讀會把黑格當「片尾全黑」硬傷。抽不到回 'black'。"""
    try:
        # crop 在 yuv420 下容不下 1×1 偶數裁切，先放大 40 倍再取中心 1 像素
        rgb = subprocess.run(["ffmpeg", "-v", "error", "-i", first_card, "-vf", "scale=iw*40:ih*40:flags=neighbor,crop=1:1:205:205",
                              "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                             capture_output=True, check=True).stdout
        if len(rgb) == 3:
            return "0x%02X%02X%02X" % tuple(rgb)
    except (OSError, subprocess.CalledProcessError):
        pass
    print("WARN card_sheet: 抽不到底色，補位格填黑", file=sys.stderr)
    return "black"


def tile_cmd(files, cols):
    """files 依序拼成 cols 欄的拼圖檔名（ffmpeg tile 濾鏡；未用格填第一張底色）。"""
    return f"tile={cols}x{-(-len(files) // cols)}:color={pad_color(files[0])}"


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    film = Path(sys.argv[1]).resolve()
    master = film / f"{film.name}.mp4"
    tlf = film / "timeline.js"
    if not (master.is_file() and tlf.is_file()):
        print(f"缺 {master.name} 或 timeline.js")
        return 1
    times = card_end_times(load_tl(tlf))
    (film / "qa").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as d:
        for i, t in enumerate(times):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(master), "-frames:v", "1",
                            "-vf", "scale=320:-2", f"{d}/{i:03d}.jpg"], check=True)
            # 逐張留在 qa/：gray_contrast.py 直接讀，不用從成片再抽一次。
            shutil.copy(f"{d}/{i:03d}.jpg", film / "qa" / f"cards-{i:03d}.jpg")
        vf = tile_cmd([f"{d}/{i:03d}.jpg" for i in range(len(times))], 5)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "1", "-i", f"{d}/%03d.jpg",
                        "-vf", vf, "-frames:v", "1", str(film / "qa" / "cards.jpg")], check=True)
    print(f"卡尾拼圖 {film / 'qa' / 'cards.jpg'}（{len(times)} 張）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
