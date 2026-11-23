#!/usr/bin/env python3
"""台北議題系列每天排一題（使用者 10-31 定）。零 token。

  series_feed.py            取 docs/SERIES-taipei-issues.md 排程表第一個還沒有核准檔的題，寫核准檔（status approved）
  series_feed.py --dry-run  只印會排哪一題

已排過＝approved/ 裡有同 slug 的檔（不管狀態）。表排完就什麼都不做。
"""
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERIES = ROOT / "docs" / "SERIES-taipei-issues.md"
APPROVED = Path(os.environ.get("AUTOLOOP_DIR", ROOT / "state/approved"))
ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*([a-z0-9][a-z0-9-]{1,40})\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$", re.M)

NOTE = """{date} 使用者 10-31 定：台北議題系列每天一題，照行人地獄／居住／托育的格式做。寫法、順序、禁字、來源規則全照 {series} ；範本稿 films/taipei-rent/narration.md、films/taipei-childcare/narration.md（定稿 bccd752）。
議題：{topic}。國際案例：{intl}。
兩種主張只收兩大陣營都有提出的，各自做法＋代價；片內不出現人名、政黨、候選人、選舉、政見、市長字眼。

## 建片注意

照 films/pedestrian-hell 第三版（commit 6cf2cc3，使用者核准的溫和版）：cast.json／pace.json／rhythm-profile 從那支複製（m4 溫和聲、tempo 1.0、calm 節奏基準）；換卡原地交叉淡化 0.6 秒，不滑入、不交替底色、沒有章名全屏卡、沒有換卡音效、沒有懶人包卡，做法照抄 pedestrian-hell 的 index.html／mix.py。
"""


def rows(text):
    return [(int(n), slug, topic, intl) for n, slug, topic, intl in ROW.findall(text)]


def queued(approved_dir):
    out = set()
    for p in approved_dir.glob("*.md"):
        m = re.search(r"^slug:\s*(\S+)", p.read_text(encoding="utf-8"), re.M)
        if m:
            out.add(m.group(1))
    return out


def next_topic(text, done):
    return next((r for r in rows(text) if r[1] not in done), None)


def main():
    dry = "--dry-run" in sys.argv[1:]
    APPROVED.mkdir(parents=True, exist_ok=True)
    nxt = next_topic(SERIES.read_text(encoding="utf-8"), queued(APPROVED))
    if not nxt:
        print("系列排程表排完了")
        return 0
    no, slug, topic, intl = nxt
    date = time.strftime("%Y-%m-%d")
    path = APPROVED / f"{date}-{slug}.md"
    body = (f"---\nslug: {slug}\ntitle: {topic}\nproposal: {SERIES}\ntopic_no: {no}\nstatus: approved\n---\n"
            + NOTE.format(date=date[5:], series=SERIES, topic=topic, intl=intl))
    if dry:
        print(body)
        return 0
    path.write_text(body, encoding="utf-8")
    print(f"排入 {path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
