"""series_feed：照表序取第一個沒核准檔的題；已排過（任何狀態）不重排；排完不寫檔。"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "scripts"))
import series_feed  # noqa: E402

TABLE = """| 序 | slug | 議題 | 國際案例方向 |
|---|---|---|---|
| 1 | pedestrian-hell | 行人地獄 | 已發布 |
| 2 | taipei-bus | 公車 | 盧森堡 |
| 3 | taipei-flood | 防災治水 | 哥本哈根 |
"""

assert [r[1] for r in series_feed.rows(TABLE)] == ["pedestrian-hell", "taipei-bus", "taipei-flood"]
assert series_feed.next_topic(TABLE, {"pedestrian-hell"})[1] == "taipei-bus"
assert series_feed.next_topic(TABLE, {"pedestrian-hell", "taipei-bus", "taipei-flood"}) is None

with tempfile.TemporaryDirectory() as d:
    Path(d, "2026-10-29-pedestrian-hell.md").write_text("---\nslug: pedestrian-hell\nstatus: published\n---\n")
    assert series_feed.queued(Path(d)) == {"pedestrian-hell"}
    env = {**os.environ, "AUTOLOOP_DIR": d}
    run = lambda: subprocess.run([sys.executable, str(HERE / "scripts/series_feed.py")], env=env, capture_output=True, text=True)
    r = run()
    assert r.returncode == 0, r.stderr
    made = sorted(p.name for p in Path(d).glob("*.md"))
    assert len(made) == 2, made  # 真表第一個沒排的題，一次只排一題
    new = [p for p in Path(d).glob("*.md") if "pedestrian" not in p.name][0].read_text()
    assert "status: approved" in new and "proposal: " in new
print("OK test_series_feed")
