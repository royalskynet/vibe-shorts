"""autoloop 狀態機：狀態只依檔案與閘門結果推進，不信模型自述；slug 擋路徑注入；已存在的片不覆蓋。

全程假 claude、假 facts、假 bakeoff、假 dcq、假 precheck、假 yt_upload，不連網、不叫模型。
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
AUTOLOOP = HERE / "scripts" / "autoloop.py"


def setup(tmp, precheck_rc=0):
    root, appr = tmp / "repo", tmp / "approved"
    (root / "scripts/publish").mkdir(parents=True)
    (root / "films").mkdir()
    (root / "refs").mkdir()
    appr.mkdir()
    (root / "scripts/precheck.py").write_text(f"import sys; sys.exit({precheck_rc})\n")
    (root / "scripts/publish/yt_upload.py").write_text(
        "import sys\nif sys.argv[1]=='public': sys.exit(0)\nprint('  已上傳：https://youtube.com/shorts/AbC_123-xyz（private）')\n")
    (root / "scripts/publish/public_path.py").write_text("pass\n")
    (root / "scripts/publish/meta_publish.py").write_text("import sys; assert '--yes' in sys.argv\n")
    # 假 facts：task 印工單路徑；check 依 FACTS_FAIL；過的時候把（slug）補進 VIRAL-LEDGER（模擬派o 完工）
    (root / "scripts/facts.py").write_text(r'''import os, sys
from pathlib import Path
a = sys.argv
if a[1] == "task":
    Path("docs/workorders").mkdir(parents=True, exist_ok=True)
    p = Path("docs/workorders") / f"facts-{a[2]}.md"
    p.write_text("task\n", encoding="utf-8")
    print(p)
    sys.exit(0)
slug = a[2].split("/")[-1]
if os.environ.get("FACTS_FAIL"):
    print("FAIL 已查證事實只有 2 條（要 8）")
    sys.exit(1)
Path("refs").mkdir(exist_ok=True)
led = Path("refs/VIRAL-LEDGER.md")
old = led.read_text(encoding="utf-8") if led.is_file() else ""
if not os.environ.get("LEDGER_SKIP") and f"（{slug}）" not in old:
    led.write_text(old + f"## x （{slug}）\n", encoding="utf-8")
sys.exit(0)
''')
    # 假 bakeoff：write 產稿、judge 依 JUDGE_RC 寫 TOP.json；刻意用反序排名，證明 autoloop 照 json
    (root / "scripts/bakeoff.py").write_text(r'''import json, os, sys
from pathlib import Path
film = Path(sys.argv[2]); d = film / "bakeoff"; d.mkdir(parents=True, exist_ok=True)
mark = Path(os.environ["BAKE_MARKER"])
with mark.open("a") as f: f.write(sys.argv[1] + "\n")
if sys.argv[1] == "write":
    if os.environ.get("WRITE_RC"):
        sys.exit(int(os.environ["WRITE_RC"]))
    for n in os.environ.get("WRITERS", "opus codex").split():
        (d / f"{n}.md").write_text(f"## 鉤子\n{n} 第一句？\n## 機制\n{n} 第二句。\n## 轉折\n但 {n}。\n## 落點\n{n}。\n", encoding="utf-8")
    sys.exit(0)
rc = int(os.environ.get("JUDGE_RC", "0"))
names = sorted(p.stem for p in d.glob("*.md"))
if rc == 2:
    names = names[:1]
order = sorted(names, key=lambda n: (n != "codex", n))  # codex 第一，其餘照名字：證明 autoloop 照 json
top = {"missing": 2 if rc == 3 else 0, "pairs": 8, "top2": order[:2],
       "rank": [{"name": n, "total": len(order) - i, "codex": 1.5} for i, n in enumerate(order)]}
(d / "TOP.json").write_text(json.dumps(top), encoding="utf-8")
(d / "RESULT.md").write_text("x", encoding="utf-8")
sys.exit(rc)
''')
    # 假 dcq：記下每個子命令，add 印 job id，wait 依 DCQ_WAIT_RC
    fake_dcq = tmp / "fake_dcq.py"
    fake_dcq.write_text(r'''import os, sys
from pathlib import Path
with Path(os.environ["DCQ_MARKER"]).open("a") as f:
    f.write(sys.argv[1] + "\n")
if sys.argv[1] == "add":
    print("job-123"); sys.exit(0)
if sys.argv[1] == "wait":
    sys.exit(int(os.environ.get("DCQ_WAIT_RC", "0")))
sys.exit(0)
''')
    # 假 claude：讀 prompt 裡的片名，寫稿或建片產物；BLOCK=1 時只寫 BLOCKED.md
    fake = tmp / "fake_claude.py"
    fake.write_text(r'''import os, re, sys
from pathlib import Path
p = sys.stdin.read()
slug = re.search(r"films/([a-z0-9-]+)", p).group(1)
film = Path("films") / slug
film.mkdir(parents=True, exist_ok=True)
if os.environ.get("BLOCK"):
    (film / "BLOCKED.md").write_text("缺爆款證據")
elif "只寫稿" in p:
    if (film / "narration.md").is_file():
        (film / "seen.md").write_text((film / "narration.md").read_text())
    (film / "narration.md").write_text("## 鉤子\n")
    (film / "TREATMENT.md").write_text("爆款證據：https://x 12萬\n")
else:
    (film / "dist").mkdir(exist_ok=True)
    (film / "dist" / f"{slug}-shorts.mp4").write_bytes(b"x")
''')
    fleet = tmp / "fleet"  # 假 notify_send：記下收件 bot，不打真 webhook；POST_FAIL=1 模擬送失敗
    fleet.mkdir()
    (fleet / "notify_send.py").write_text(
        "import os\n"
        "def post(bot, key, text, timeout=15):\n"
        "    with open(os.environ['POST_MARKER'], 'a') as f: f.write(bot + '|' + text + '\\n')\n"
        "    return (False, 'post failed: test') if os.environ.get('POST_FAIL') else (True, 'http 200')\n")
    env = dict(os.environ, AUTOLOOP_ROOT=str(root), AUTOLOOP_DIR=str(appr), AUTOLOOP_LOG=str(tmp / "log"),
               AUTOLOOP_CLAUDE=f"{sys.executable} {fake}", AUTOLOOP_PY=sys.executable,
               AUTOLOOP_DCQ=f"{sys.executable} {fake_dcq}",
               AUTOLOOP_ALERTS=str(tmp / "alerts"), AUTOLOOP_FLEET=str(fleet), POST_MARKER=str(tmp / "posts.log"),
               DCQ_MARKER=str(tmp / "dcq.log"), BAKE_MARKER=str(tmp / "bake.log"),
               AUTOLOOP_CUTOFF="9e12")  # 預設不延後；延後另測
    return root, appr, env


def approve(appr, name, slug, status="approved", now=None, **extra):
    f = appr / f"{name}.md"
    nowline = f'now: {now}\n' if now is not None else ""
    lines = "".join(f"{k}: {v}\n" for k, v in extra.items())
    f.write_text(f"---\nslug: {slug}\ntitle: 測試題\nproposal: /x/proposal.md\ntopic_no: 1\nstatus: {status}\n{nowline}{lines}---\n內文\n")
    return f


def status(f):
    return dict(l.split(": ", 1) for l in f.read_text().split("---")[1].strip().splitlines() if ": " in l)


def run(mode, env, **extra):
    r = subprocess.run([sys.executable, str(AUTOLOOP), mode], env=dict(env, **extra), capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return r


def mark(tmp, name):
    p = Path(tmp) / name
    return p.read_text(encoding="utf-8") if p.is_file() else ""


# ---- 主流程：查證 → 擂台 → 選稿 → 建片 → 私人上傳 → 發布 ----
with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    f = approve(appr, "2026-10-29-love-tax", "love-tax")
    run("night", env, CLAUDE_CODE_SUBPROCESS_ENV_SCRUB="1")  # 從 Claude Code session 手動觸發
    s = status(f)
    assert s["status"] == "script_ready", s
    assert s["film"] == "films/love-tax"
    assert s["script_a"].endswith("bakeoff/codex.md") and s["script_b"].endswith("bakeoff/opus.md"), s
    assert "內文" in f.read_text(), "body 被吃掉"
    # 使用者選 A → 建片 → 私人上傳
    f.write_text(f.read_text().replace("status: script_ready", "status: script_ok")
                 .replace("---\n內文", "pick: A\n---\n內文", 1))
    run("night", env)
    s = status(f)
    assert s["status"] == "built", s
    assert (root / "films/love-tax/narration.md").read_text().startswith("## 鉤子\ncodex"), "建的片不是選的 A"
    assert s["yt_id"] == "AbC_123-xyz" and s["yt_private"].endswith("AbC_123-xyz"), s
    # night 不發布；publish 只吃 publish_ok
    run("publish", env)
    assert status(f)["status"] == "built"
    f.write_text(f.read_text().replace("status: built", "status: publish_ok"))
    run("publish", env)
    assert status(f)["status"] == "published", status(f)

# ---- slug 不合法、片已存在 ----
with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    bad = approve(appr, "a-bad", "../../etc")
    run("night", env)
    assert status(bad)["status"] == "failed" and "slug" in status(bad)["error"]

with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    (root / "films/old-film").mkdir()
    old = approve(appr, "b-old", "old-film")
    run("night", env)
    assert status(old)["status"] == "failed" and "已存在" in status(old)["error"]
    assert not (root / "films/old-film/narration.md").exists(), "覆蓋了既有片"

# ---- 查證閘門 ----
with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    # check 不過 → dcq 派工、wait 過了仍不過 → failed，不跑擂台；error 是 check 的 FAIL 行
    f = approve(appr, "c-facts", "facts-fail")
    run("night", env, FACTS_FAIL="1")
    s = status(f)
    assert s["status"] == "failed" and s["error"].startswith("FAIL"), s
    assert "add" in mark(t, "dcq.log") and "wait" in mark(t, "dcq.log"), mark(t, "dcq.log")
    assert not (root / "films/facts-fail/bakeoff").exists(), "查證沒過還跑擂台"
    assert "facts-fail 查證卡住" in mark(t, "alerts/" + __import__("time").strftime("%F") + ".txt")

with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    # FACTS.md 已過（ledger 也有）→ 跳過 dcq，不再花 60 分
    (root / "refs/VIRAL-LEDGER.md").write_text("## x （skip-film）\n")
    f = approve(appr, "d-skip", "skip-film")
    run("night", env)
    assert status(f)["status"] == "script_ready", status(f)
    assert "add" not in mark(t, "dcq.log"), "已過還派 dcq"

with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    # 工單驗收的另一半：VIRAL-LEDGER 沒有（slug）→ failed
    f = approve(appr, "e-ledger", "ledger-miss")
    run("night", env, LEDGER_SKIP="1")
    s = status(f)
    assert s["status"] == "failed" and "VIRAL-LEDGER" in s["error"], s

with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    # wait 逾時 → failed、先 cancel、鎖有放掉（下一次跑得動下一張）
    a = approve(appr, "f-timeout", "slow")
    run("night", env, FACTS_FAIL="1", DCQ_WAIT_RC="124")
    s = status(a)
    assert s["status"] == "failed" and "逾時" in s["error"], s
    assert "cancel" in mark(t, "dcq.log"), mark(t, "dcq.log")
    b = approve(appr, "g-next", "next-film")
    run("night", env)
    assert status(b)["status"] == "script_ready", status(b)

with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    f = approve(appr, "h-norunner", "no-runner", now='"true"')
    original = f.read_bytes()
    run("night", env, FACTS_FAIL="1", DCQ_WAIT_RC="3")
    s = status(f)
    assert s["status"] == "approved" and "error" not in s, s
    assert f.read_bytes() == original, "沒有 runner 不得改核准檔或 now"
    assert "沒有 runner" in mark(t, "log")
    assert not mark(t, "bake.log")
    # worker 晚到，只產查證表，下一輪仍可接擂台；不覆蓋既有影片。
    (root / "films/no-runner").mkdir()
    (root / "films/no-runner/FACTS.md").write_text("fake verified facts")
    run("night", env)
    assert status(f)["status"] == "script_ready", status(f)

# ---- 擂台回傳碼 ----
with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    f = approve(appr, "i-write3", "write3")
    run("night", env, WRITE_RC="3")
    s = status(f)
    assert s["status"] == "failed" and "沒有稿" in s["error"], s
    assert "judge" not in mark(t, "bake.log"), mark(t, "bake.log")

with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    f = approve(appr, "j-judge2", "judge2")
    run("night", env, JUDGE_RC="2")
    s = status(f)
    assert s["status"] == "script_ready" and s["script_a"].endswith("codex.md") and s.get("script_b", "") == "", s

with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    f = approve(appr, "k-judge3", "judge3")
    run("night", env, JUDGE_RC="3")
    assert status(f)["status"] == "script_ready", status(f)
    out = subprocess.run([sys.executable, str(AUTOLOOP), "digest"], env=env, capture_output=True, text=True).stdout
    assert "缺票 2／8" in out, out

# ---- 建片：沒選稿／選 B ----
with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    (root / "films/no-pick").mkdir()
    (root / "films/no-pick/bakeoff").mkdir()
    (root / "films/no-pick/bakeoff/opus.md").write_text("B 稿\n")
    f = approve(appr, "l-nopick", "no-pick", status="script_ok", script_a=str(root / "films/no-pick/bakeoff/opus.md"))
    run("night", env)
    assert status(f)["status"] == "failed" and "沒選稿" in status(f)["error"], status(f)

with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    (root / "films/pick-b/bakeoff").mkdir(parents=True)
    (root / "films/pick-b/bakeoff/a.md").write_text("A 稿\n")
    (root / "films/pick-b/bakeoff/b.md").write_text("B 稿\n")
    f = approve(appr, "m-pickb", "pick-b", status="script_ok", pick="B",
                script_a=str(root / "films/pick-b/bakeoff/a.md"), script_b=str(root / "films/pick-b/bakeoff/b.md"))
    run("night", env)
    assert status(f)["status"] == "built", status(f)
    assert (root / "films/pick-b/narration.md").read_text() == "B 稿\n"

# 改稿後 script: 指 narration.md：建片照改好的稿，不被 pick 原稿蓋回
with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    (root / "films/revised/bakeoff").mkdir(parents=True)
    (root / "films/revised/bakeoff/b.md").write_text("B 稿\n")
    (root / "films/revised/narration.md").write_text("改好的 B 稿\n")
    f = approve(appr, "m2-revised", "revised", status="script_ok", pick="B",
                script_b=str(root / "films/revised/bakeoff/b.md"), script=str(root / "films/revised/narration.md"))
    run("night", env)
    assert status(f)["status"] == "built", status(f)
    assert (root / "films/revised/narration.md").read_text() == "改好的 B 稿\n", "改稿被 pick 原稿蓋回"

# ---- 改稿：沒 pick 擋下；有 pick 先複製再改 ----
with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    (root / "films/rev/bakeoff").mkdir(parents=True)
    (root / "films/rev/bakeoff/opus.md").write_text("A 稿\n")
    f = approve(appr, "n-rev", "rev", status="script_revise", script_a=str(root / "films/rev/bakeoff/opus.md"))
    run("night", env)
    s = status(f)
    assert s["status"] == "failed" and "選稿" in s["error"], s
    assert not (root / "films/rev/narration.md").exists()

with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    (root / "films/rev2/bakeoff").mkdir(parents=True)
    (root / "films/rev2/bakeoff/a.md").write_text("A 稿\n")
    (root / "films/rev2/bakeoff/b.md").write_text("B 稿\n")
    f = approve(appr, "o-rev", "rev2", status="script_revise", pick="B",
                script_a=str(root / "films/rev2/bakeoff/a.md"), script_b=str(root / "films/rev2/bakeoff/b.md"))
    run("night", env)
    assert status(f)["status"] == "script_ready", status(f)
    assert (root / "films/rev2/seen.md").read_text() == "B 稿\n", "改稿前沒先複製選的稿"

# ---- 其他既有行為 ----
with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t), precheck_rc=1)
    # precheck 不過＝不上傳
    built = approve(appr, "d-build", "pc-fail", status="script_ok")
    (root / "films/pc-fail").mkdir()
    (root / "films/pc-fail/narration.md").write_text("x")
    run("night", env)
    s = status(built)
    assert s["status"] == "failed" and "precheck" in s["error"] and "yt_id" not in s, s
    # 模型寫 BLOCKED.md＝失敗並帶原因
    blk = approve(appr, "e-blk", "blk", status="script_ok")
    (root / "films/blk").mkdir()
    (root / "films/blk/narration.md").write_text("x")
    run("night", env, BLOCK="1")
    assert status(blk)["status"] == "failed" and "缺爆款證據" in status(blk)["error"]
    # 沒 yt_id 不准發布
    nopub = approve(appr, "f-nopub", "nopub", status="publish_ok")
    run("publish", env)
    assert status(nopub)["status"] == "failed"

with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    # 每晚只建 1 支、只寫 1 題（試點期 MAX_SCRIPTS=1）
    fs = []
    for n in ("x1", "x2"):
        (root / f"films/{n}").mkdir()
        (root / f"films/{n}/narration.md").write_text("x")
        fs.append(approve(appr, n, n, status="script_ok"))
    run("night", env)
    assert [status(f)["status"] for f in fs] == ["built", "script_ok"], [status(f)["status"] for f in fs]
    a = approve(appr, "y1", "y1")
    b = approve(appr, "y2", "y2")
    run("night", env)
    assert status(a)["status"] == "script_ready" and status(b)["status"] == "approved", [status(a), status(b)]

with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    # 21:00 後才核准的留到下一晚：mtime 晚於 cutoff 不動
    early = approve(appr, "g-early", "early")
    late = approve(appr, "h-late", "late")
    os.utime(early, (1000, 1000))
    os.utime(late, (3000, 3000))
    run("night", env, AUTOLOOP_CUTOFF="2000")
    assert status(early)["status"] == "script_ready", status(early)
    assert status(late)["status"] == "approved", status(late)

# cutoff：22:00 跑 → 當天 21:00；02:00 跑 → 前一天 21:00
sys.path.insert(0, str(HERE / "scripts"))
import autoloop  # noqa: E402
import time  # noqa: E402
d22 = time.mktime((2026, 10, 29, 22, 0, 0, 0, 0, -1))
d02 = time.mktime((2026, 10, 30, 2, 0, 0, 0, 0, -1))
c21 = time.mktime((2026, 10, 29, 21, 0, 0, 0, 0, -1))
assert autoloop.cutoff(d22) == c21 and autoloop.cutoff(d02) == c21

# digest：A／B 各前 3 句＋評審分＋bakeoff 連結＋FACTS 連結；已選的題不再列；播放數取最高
prop = "# x\n\n## 題 1：甲題\n\n- 同題爆款：a · 39,174 播放（10-22）/ 88,160 播放（10-23）\n\n## 題 2：乙題\n\n- 同題爆款：b · 500 播放\n"
assert autoloop.topics(prop) == [(1, "甲題", 88160, ""), (2, "乙題", 500, "")], autoloop.topics(prop)
with tempfile.TemporaryDirectory() as t:
    shared = Path(t)
    appr = shared / "approved"
    appr.mkdir()
    (shared / "marketer-topics-2026-10-28").mkdir()
    pp = shared / "marketer-topics-2026-10-28/proposal.md"
    pp.write_text(prop, encoding="utf-8")
    (shared / "a.md").write_text("## 鉤子\n輪盤不記得妳贏過？\n## 機制\n甲句。\n## 轉折\n但乙句。\n## 落點\n丙句。\n", encoding="utf-8")
    (shared / "b.md").write_text("## 鉤子\n另一份開頭。\n", encoding="utf-8")
    (appr / "a.md").write_text(f"---\nslug: odds\ntitle: 賭\nproposal: {pp}\ntopic_no: 2\nstatus: script_ready\n"
                               f"script_a: {shared / 'a.md'}\nscript_b: {shared / 'b.md'}\n"
                               f"score_a: 2.5\nscore_b: 1\nbakeoff_missing: 3/8\n---\n", encoding="utf-8")
    autoloop.APPROVED = appr
    out = autoloop.digest()
    assert "「輪盤不記得妳贏過？」" in out and "「甲句。」" in out and "「但乙句。」" in out, out
    assert "丙句" not in out, out  # 只列前 3 句
    assert "A：【a】評審 2.5 分" in out and "B：【b】評審 1 分" in out, out
    assert f"{autoloop.GH_BLOB}/films/odds/bakeoff/a.md" in out, out
    assert f"{autoloop.GH_BLOB}/films/odds/FACTS.md" in out, out
    assert "稿過 odds A" in out and "稿過 odds B" in out and "缺票 3／8" in out, out
    assert "1. 甲題（同題爆款 8.8 萬 播放）" in out and "乙題" not in out, out
    assert t not in out and "/Users" not in out, out  # 給 GitHub 連結，不給本機路徑
    assert "⚠️ B 稿結構門沒過" in out and "沒有「你」也沒有問句" in out, out  # fix 12159：送核前就標結構門

# 提案已帶「## 卡片」完稿：旁白逐字進 narration.md，不叫 facts／bakeoff／claude
with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    f = approve(appr, "fx", "fixed-film", script_a="/x/a.md", score_a="0")
    f.write_text(f.read_text() + "\n## 卡片\n\n卡1｜第一句，有逗號。｜畫面甲\n卡2｜第二句？｜畫面乙｜多餘\n\n## 備註\n卡3｜不算。｜x\n")
    run("night", env)
    s = status(f)
    assert s["status"] == "script_ready" and s["script"].endswith("films/fixed-film/narration.md"), s
    assert "script_a" not in s and "score_a" not in s, s
    assert (root / "films/fixed-film/narration.md").read_text(encoding="utf-8") == "## 卡1\n第一句，有逗號。\n\n## 卡2\n第二句？\n", "旁白不是逐字"
    assert "write" not in mark(t, "bake.log") and "add" not in mark(t, "dcq.log"), "完稿不該叫 AI 寫稿"

print("AUTOLOOP_OK")

# ---- now 立即開工（CHG-20261106-04）----
def alerts_text(tmp):
    p = tmp / "alerts" / f"{time.strftime('%F')}.txt"
    return p.read_text(encoding="utf-8") if p.is_file() else ""


with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    # now＋approved：publish 就叫 do_script 一次，到 script_ready 後 now 被刪，且絕不變 publish_ok／不發布
    f = approve(appr, "n-now", "now-film", now='"true"')
    r = run("publish", env)
    s = status(f)
    assert s["status"] == "script_ready" and "now" not in s, s
    assert (Path(t) / "log").read_text().count("now 立即開工") == 1
    assert "已上傳" not in r.stdout and "已上傳" not in r.stderr
    # 無 now：publish 不寫稿
    g = approve(appr, "n-plain", "plain-film")
    run("publish", env)
    assert status(g)["status"] == "approved" and not (root / "films/plain-film").exists()
    # now: false 不觸發
    h = approve(appr, "n-false", "false-film", now="false")
    run("publish", env)
    assert status(h)["status"] == "approved" and not (root / "films/false-film").exists()

with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    # night 跑到 script_ready 時 now 也被刪（night 也清 now）
    f = approve(appr, "n-night", "night-film", now='"true"')
    run("night", env)
    s = status(f)
    assert s["status"] == "script_ready" and "now" not in s, s

with tempfile.TemporaryDirectory() as t:
    import fcntl
    root, appr, env = setup(Path(t))
    # 鎖被占：now 阻塞等鎖逾時（1 秒）→ now 留著＋alerts 一行
    f = approve(appr, "n-lock", "lock-film", now='"true"')
    lk = open(appr / ".autoloop.lock", "w")
    fcntl.flock(lk, fcntl.LOCK_EX)
    run("publish", dict(env, AUTOLOOP_NOW_WAIT="1"))
    s = status(f)
    assert s["status"] == "approved" and s["now"] == '"true"', s
    assert "lock-film 立即開工排到今晚 02:00" in alerts_text(Path(t)), alerts_text(Path(t))
    assert not (root / "films/lock-film").exists()
    fcntl.flock(lk, fcntl.LOCK_UN)
    lk.close()

with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    # now 沒有每日次數上限：當日已跑過多次照樣開工
    day = time.strftime("%F")
    (Path(t) / "log").write_text("".join(f"{day} 09:0{i}:00 x: now 立即開工\n" for i in range(5)))
    f = approve(appr, "n-cap", "cap-film", now='"true"')
    run("publish", env)
    s = status(f)
    assert s["status"] == "script_ready" and "now" not in s, s
    assert (root / "films/cap-film").exists()

with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    # alerts 子命令：沒事不寫；有可行動行才寫；同日同行不重複
    run("alerts", env)
    adir = Path(t) / "alerts"
    assert not adir.exists() or not any(adir.iterdir()), list(adir.iterdir()) if adir.exists() else None
    approve(appr, "s-ready", "ready-film", status="script_ready")
    run("alerts", env)
    assert "ready-film 等核稿" in alerts_text(Path(t)), alerts_text(Path(t))
    run("alerts", env)
    assert alerts_text(Path(t)).count("ready-film 等核稿") == 1
    # 建好的片：告警行帶私人連結（session 封存後只靠 Scribe 轉這行給使用者）
    approve(appr, "s-built", "built-film", status="built", yt_private="https://youtube.com/shorts/abc123XYZ")
    run("alerts", env)
    assert "built-film 等看片" in alerts_text(Path(t)) and "shorts/abc123XYZ" in alerts_text(Path(t)), alerts_text(Path(t))
    # 營銷號事件只發 Marketer（使用者 11-07），同日同行只發一次
    posts = mark(t, "posts.log")
    assert posts and all(ln.startswith(("Marketer|", "・")) for ln in posts.splitlines()), posts
    assert posts.count("Marketer|") == 2, posts  # 每次 alerts 合併成一則
    assert posts.count("built-film 等看片") == 1 and "shorts/abc123XYZ" in posts, posts
    # 送失敗不記去重，下個整點重發
    approve(appr, "s-fail", "fail-film", status="script_ready")
    run("alerts", dict(env, POST_FAIL="1"))
    assert "fail-film" not in alerts_text(Path(t)), alerts_text(Path(t))
    run("alerts", env)
    assert "fail-film 等核稿" in alerts_text(Path(t)) and mark(t, "posts.log").count("fail-film 等核稿") == 2

with tempfile.TemporaryDirectory() as t:
    root, appr, env = setup(Path(t))
    # 已到終點還帶著陳舊 now：任何一次 publish 都清掉，不會被當成待開工
    f = approve(appr, "n-stale", "stale-film", status="script_ready", now='"true"')
    run("publish", env)
    assert "now" not in status(f), status(f)
    assert "add" not in mark(t, "dcq.log") and "write" not in mark(t, "bake.log")

# G4：鎖檔位於 WatchPaths 目錄，重複 publish 不能修改它或洗 log。
with tempfile.TemporaryDirectory() as t:
    import fcntl
    root, appr, env = setup(Path(t))
    lockpath = appr / ".autoloop.lock"
    lockpath.write_text("sentinel")
    before = lockpath.stat().st_mtime_ns
    with lockpath.open("a") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        for _ in range(5):
            run("publish", env)
    assert lockpath.read_text() == "sentinel"
    assert lockpath.stat().st_mtime_ns == before
    assert mark(t, "log").count("另一個 autoloop") == 0

# G7：優先卡在哪段第一句；移除標題，保持單行與 160 字上限。
def test_error_summary(monkeypatch):
    reason = "# BLOCKED — taipei-childcare 卡在旁白核稿\n\n## 卡在哪\n\n第 16 句核稿未過。第二句不用帶。\n\n## 下一步\n重做"
    assert autoloop.error_summary(reason) == "第 16 句核稿未過。"
    assert autoloop.error_summary("## 單純錯誤\n缺少旁白") == "單純錯誤 缺少旁白"
    assert len(autoloop.error_summary("字" * 200)) == 160
    with tempfile.TemporaryDirectory() as t:
        appr = Path(t)
        monkeypatch.setattr(autoloop, "APPROVED", appr)
        approve(appr, "blocked", "childcare", status="failed", error=reason.replace("\n", " "))
        assert "#" not in autoloop.actionable()[0]
