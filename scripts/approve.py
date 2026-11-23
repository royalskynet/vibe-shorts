#!/usr/bin/env python3
"""使用者審過稿子後寫核准戳記：audit/approved.md（綁現在 narration.md 的 sha256）。

用法：python3 scripts/approve.py films/<片> "<使用者原話，例：稿子通過>"
只在使用者明說通過後跑；改稿後戳記自動失效，voice.py 與 precheck「稿子已核准」會擋。
"""
import hashlib
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from precheck import gate_waived, parse_narration, story_problems  # noqa: E402


def main():
    if len(sys.argv) != 3 or not sys.argv[2].strip():
        print(__doc__)
        return 2
    film = Path(sys.argv[1]).resolve()
    narr = film / "narration.md"
    if not narr.is_file():
        print(f"找不到 {narr}")
        return 1
    # 結構門不過的稿蓋了戳也建不了片（voice.py 照樣擋），先擋在核准這步（fix 12159，free-speech-line 11-15）
    prof = film / "rhythm-profile"
    dialogue = prof.is_file() and prof.read_text(encoding="utf-8").strip() == "dialogue"
    probs = [] if gate_waived(film) else story_problems(parse_narration(narr.read_text(encoding="utf-8")), dialogue)
    if probs:
        print("旁白稿結構門沒過，改完稿再給人核：\n- " + "\n- ".join(probs))
        return 1
    sha = hashlib.sha256(narr.read_bytes()).hexdigest()
    (film / "audit").mkdir(exist_ok=True)
    (film / "audit" / "approved.md").write_text(
        f"narration_sha: {sha}\n核准：{sys.argv[2].strip()}\n時間：{datetime.now():%Y-%m-%d %H:%M}\n", encoding="utf-8")
    print(f"已核准 {film.name} 稿 {sha[:12]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
