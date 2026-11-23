"""card_sheet 拼圖的未用格要填片子底色，不是黑（冷讀會把黑格當片尾全黑硬傷）。"""
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import card_sheet as cs  # noqa: E402

BG = (245, 239, 230)


def pixel(path: Path, x: int, y: int):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"scale=iw*40:ih*40:flags=neighbor,crop=1:1:{x * 40 + 20}:{y * 40 + 20}",
                          "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    return tuple(out[:3])


with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    cards = []
    for i in range(3):
        p = d / f"{i:03d}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=0xF5EFE6:s=108x192:d=3",
                        "-frames:v", "1", str(p)], check=True)
        cards.append(str(p))
    sheet = d / "cards.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "1", "-i", str(d / "%03d.jpg"),
                    "-vf", cs.tile_cmd(cards, 2), "-frames:v", "1", str(sheet)], check=True)
    # 3 張卡 2×2：右下格未用，取該格中心
    got = pixel(sheet, 108 + 54, 192 + 96)
    assert all(abs(g - b) <= 12 for g, b in zip(got, BG)), f"補位格 {got} 不是底色 {BG}：{cs.tile_cmd(cards, 2)}"
print("ALL PASS")
