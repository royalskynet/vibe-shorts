"""launchd 跑的腳本 PATH 要含 ~/.local/bin（hpush、yt-dlp）與 /opt/homebrew/bin（ffmpeg）。

launchd 預設 PATH 只有 /usr/bin:/bin:/usr/sbin:/sbin：10-16 hpush rc=127、10-20 viral_text 找不到 ffmpeg 10 支全敗。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ["scripts/daily-trends.sh","scripts/threads-queue.sh", "scripts/autoloop.sh"]

for rel in SCRIPTS:
    text = (ROOT / rel).read_text(encoding="utf-8")
    m = re.search(r'^PATH="([^"]+)"', text, re.M)
    assert m, "%s 沒設 PATH" % rel
    for need in ("$HOME/.local/bin", "/opt/homebrew/bin"):
        assert need in m.group(1).split(":"), "%s 的 PATH 缺 %s" % (rel, need)
print("LAUNCHD_PATH_OK")
