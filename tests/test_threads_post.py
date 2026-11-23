#!/usr/bin/env python3
"""threads_post 佇列邏輯自檢：不連網。"""
import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "publish"))
import threads_post as tp  # noqa: E402

fails = []


def check(name, ok):
    if not ok:
        fails.append(name)


tmp = Path(tempfile.mkdtemp())
tp.QUEUE = tmp / "queue"
tp.ROOT = tmp
tp.QUEUE.mkdir()


def q(name, at, approved="yes", quote=None, text="內文"):
    head = f"at: {at}\napproved: {approved}\n" + (f"quote: {quote}\n" if quote else "")
    (tp.QUEUE / name).write_text(head + "---\n" + text + "\n", encoding="utf-8")


q("a.md", "2026-10-21 20:00")
q("b.md", "2026-10-21 19:00")
q("c.md", "2026-10-21 18:00", approved="no")
q("d.md", "2026-10-22 09:00")
now = datetime(2026, 10, 21, 20, 30)
names = [f.name for f, _ in tp.due(now)]
check("只發到點且核准的，照時間排", names == ["b.md", "a.md"])

q("e.md", "2026-10-21 10:00", text="字" * 501)
try:
    tp.parse(tp.QUEUE / "e.md")
    fails.append("501 字沒擋")
except ValueError:
    pass
(tp.QUEUE / "e.md").unlink()

(tp.QUEUE / "f.md").write_text("at: 2026-10-21 10:00\napproved: yes\n內文沒分隔線\n", encoding="utf-8")
try:
    tp.due(now)
    fails.append("缺分隔線沒報錯")
except ValueError:
    pass
(tp.QUEUE / "f.md").unlink()

meta = tmp / "films" / "codex" / "meta"
meta.mkdir(parents=True)
(meta / "published.json").write_text(json.dumps({"threads": {"id": "18099"}}))
check("片名/鍵 解成 ID", tp.resolve_quote("codex/threads") == "18099")
check("純數字照用", tp.resolve_quote("123") == "123")
check("沒引用回 None", tp.resolve_quote(None) is None)
try:
    tp.resolve_quote("codex/ig")
    fails.append("不存在的鍵沒擋")
except ValueError:
    pass

if fails:
    sys.exit("FAIL\n  " + "\n  ".join(fails))
print("OK threads_post 自檢")
