#!/usr/bin/env python3
"""黑白對比（使用者 2026-11-05 定，借 Eian 流程第三點）：每卡尾幀轉灰階，主體跟背景分不開＝明暗對比不夠。
米色插畫風本色偏亮偏近，這支風險最高，所以先量出來給人看。

用法：python3 scripts/gray_contrast.py films/<片>
讀 qa/cards-NNN.jpg（card_sheet.py 逐張留的卡尾幀）；沒有就照 card_sheet.py 的取幀法從成片抽。
輸出 qa/gray.json（每卡 rms＝灰階標準差/255、p5_95＝5–95 百分位亮度差/255）＋ qa/gray-sheet.jpg（灰階拼圖）。
只回報不判死：stdout 列最低 3 張，exit 0。門檻要使用者目視核准後才加（CLAUDE.md）。
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from card_sheet import card_end_times, load_tl  # noqa: E402


def tail_frames(film: Path, master: Path, d: str):
    """每卡尾幀 jpg：有 cards-*.jpg 就用，沒有就從成片按 timeline 抽（同 card_sheet.py）。"""
    kept = sorted((film / "qa").glob("cards-[0-9]*.jpg"))
    if kept:
        return kept
    for i, t in enumerate(card_end_times(load_tl(film / "timeline.js"))):
        p = Path(d) / f"cards-{i:03d}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(master), "-frames:v", "1",
                        "-vf", "scale=320:-2", str(p)], check=True)
        kept.append(p)
    return kept


def stats(p: Path):
    g = np.asarray(Image.open(p).convert("L"), dtype=np.float64)
    lo, hi = np.percentile(g, [5, 95])
    return {"rms": round(float(g.std()) / 255, 4), "p5_95": round(float(hi - lo) / 255, 4)}


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    film = Path(sys.argv[1]).resolve()
    master = film / f"{film.name}.mp4"
    if not master.is_file():
        print(f"缺 {master}")
        return 1
    with tempfile.TemporaryDirectory() as d:
        frames = tail_frames(film, master, d)
        cards = {f"卡{i + 1:02d}": stats(p) for i, p in enumerate(frames)}
        for i, p in enumerate(frames):
            Image.open(p).convert("L").save(Path(d) / f"g-{i:03d}.png")
        rows = -(-len(frames) // 5)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "1", "-i", str(Path(d) / "g-%03d.png"),
                        "-vf", f"tile=5x{rows}", "-frames:v", "1", "-update", "1",
                        str(film / "qa" / "gray-sheet.jpg")], check=True)
    (film / "qa" / "gray.json").write_text(json.dumps(cards, ensure_ascii=False, indent=1) + "\n",
                                           encoding="utf-8")
    low = sorted(cards.items(), key=lambda kv: kv[1]["rms"])[:3]
    print(f"{len(cards)} 卡；對比最低 3 張（rms／p5_95，0–1，越高越好）：")
    for k, v in low:
        print(f"  {k}  rms {v['rms']}  p5_95 {v['p5_95']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
