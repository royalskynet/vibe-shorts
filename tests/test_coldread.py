#!/usr/bin/env python3
"""冷讀審核的自檢：假的 codex 驗 sha 戳記、只餵成品、不可用要 exit 3；precheck 的冷讀 WARN 不影響 exit code。"""
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHA = "a" * 64


def stub_codex(bin_dir: Path, stdin_out: Path, verdict="通過"):
    """假 codex：把收到的 prompt 存檔，-o 寫一份合格式的回答。"""
    only_pattern = verdict == "通過"
    p = bin_dir / "codex"
    p.write_text(f"""#!/usr/bin/env bash
out=""; prompt=""
while [ $# -gt 0 ]; do
  case "$1" in -o) out="$2"; shift 2;; -i) shift 2;; exec|-*) shift;; *) prompt="$1"; shift;; esac
done
printf '%s' "$prompt" > "$STUB_STDIN"
printf '%s\\n' "我看到的故事。" "- [小問題] 第2句：轉折太急 → 加一句過渡" "VERDICT: {'通過' if only_pattern else '不通過'}" > "$out"
""", encoding="utf-8")
    p.chmod(p.stat().st_mode | stat.S_IXUSR)
    return p


def run(args, path_prefix, cwd, extra=None, path=None):
    env = {**os.environ, "PATH": path or f"{path_prefix}:{os.environ.get('PATH', '')}", **(extra or {})}
    return subprocess.run(args, capture_output=True, text=True, env=env, cwd=cwd)


with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    film = d / "films" / "f"
    (film / "audit").mkdir(parents=True)
    (film / "narration.md").write_text("## 鉤子\n玩越久，越確定會輸。\n", encoding="utf-8")
    (film / "TREATMENT.md").write_text("## 爆款證據\n獨特字串ZZTREATMENT\n", encoding="utf-8")
    sha = subprocess.run(["shasum", "-a", "256", str(film / "narration.md")],
                         capture_output=True, text=True).stdout.split()[0]
    bin_dir = d / "bin"
    bin_dir.mkdir()
    stdin_out = d / "stdin.txt"
    stub_codex(bin_dir, stdin_out)
    script = str(ROOT / "scripts" / "coldread.sh")

    # (a)(b) script 模式：戳記對，prompt 只有旁白稿，不含 TREATMENT 內容。
    r = run(["bash", script, str(film), "script"], bin_dir, d, {"STUB_STDIN": str(stdin_out)})
    assert r.returncode == 0, r.stderr
    out = (film / "audit" / "coldread-script.md").read_text(encoding="utf-8").splitlines()
    assert out[0] == f"narration_sha: {sha}", out[0]
    assert out[1] == "engine: codex", out[1]
    assert out[-1] == "VERDICT: 通過", out[-1]
    prompt = stdin_out.read_text(encoding="utf-8")
    assert "玩越久，越確定會輸。" in prompt
    assert "ZZTREATMENT" not in prompt and "TREATMENT" not in prompt, "冷讀只能看到成品"

    # (d) codex 失敗（到期／額度用完）→ 換 opencode，engine 行記實際引擎。
    fb = d / "fbbin"
    fb.mkdir()
    (fb / "codex").write_text("#!/usr/bin/env bash\necho 'quota exceeded' >&2; exit 1\n", encoding="utf-8")
    (fb / "opencode").write_text("#!/usr/bin/env bash\nprintf '%s\\n' '我看到的故事。' 'VERDICT: 通過'\n", encoding="utf-8")
    for f in ("codex", "opencode"):
        (fb / f).chmod(0o755)
    r = run(["bash", script, str(film), "script"], fb, d)
    assert r.returncode == 0, r.stderr
    out = (film / "audit" / "coldread-script.md").read_text(encoding="utf-8").splitlines()
    assert out[1] == "engine: opencode/opencode-go/deepseek-v4.1-flash", out[1]
    # 兩個都失敗 → exit 3。
    (fb / "opencode").write_text("#!/usr/bin/env bash\nexit 1\n", encoding="utf-8")
    (film / "audit" / "coldread-script.md").unlink()
    r = run(["bash", script, str(film), "script"], fb, d)
    assert r.returncode == 3 and "codex" in r.stderr and "opencode" in r.stderr, (r.returncode, r.stderr)

    # (c) codex、opencode 都不存在 → exit 3，不產檔。
    empty = d / "emptybin"   # 只有系統工具、沒有 codex／opencode（真的在 /opt/homebrew/bin）
    empty.mkdir()
    for tool in ("shasum", "sed", "cut", "grep", "mktemp", "rm", "cat", "dirname", "tr", "wc", "basename", "mkdir"):
        (empty / tool).symlink_to(shutil.which(tool))
    r = run(["/bin/bash", script, str(film), "script"], empty, d, path=str(empty))
    assert r.returncode == 3, (r.returncode, r.stderr)
    assert r.stderr.strip(), "要印一行原因"
    assert not (film / "audit" / "coldread-script.md").exists(), "不可用時不靜默產檔"

    # film 模式缺 sheet/cards → exit 2。
    r = run(["bash", script, str(film), "film"], bin_dir, d)
    assert r.returncode == 2, r.returncode

    # precheck 的冷讀 WARN：缺檔／sha 錯／不通過／正常，四種都不改 exit code。
    sys.path.insert(0, str(ROOT / "scripts"))
    from precheck import coldread_warnings  # noqa: E402

    assert len(coldread_warnings(film, SHA)) == 2, "兩個檔都缺要兩條 WARN"
    (film / "audit" / "coldread-script.md").write_text(f"narration_sha: {sha}\nVERDICT: 通過\n", encoding="utf-8")
    (film / "qa").mkdir()
    (film / "qa" / "coldread-film.md").write_text(f"video_sha: {SHA}\nVERDICT: 通過\n", encoding="utf-8")
    assert coldread_warnings(film, SHA) == [], coldread_warnings(film, SHA)
    (film / "audit" / "coldread-script.md").write_text(f"narration_sha: {SHA}\nVERDICT: 通過\n", encoding="utf-8")
    w = coldread_warnings(film, SHA)
    assert len(w) == 1 and "對不上" in w[0][1], w
    stub_codex(bin_dir, stdin_out, verdict="不通過")
    (film / "audit" / "coldread-script.md").write_text(f"narration_sha: {sha}\nVERDICT: 通過\n", encoding="utf-8")
    run(["bash", script, str(film), "script"], bin_dir, d, {"STUB_STDIN": str(stdin_out)})
    w = coldread_warnings(film, SHA)
    assert len(w) == 1 and "不通過" in w[0][1], w

    # exit code 不因 WARN 改變：拿真 precheck 對一個會因別的原因失敗的目錄跑，比有無冷讀檔的 exit 相同。
    empty_film = d / "films" / "e"
    (empty_film / "audit").mkdir(parents=True)
    pre = run([sys.executable, str(ROOT / "scripts" / "precheck.py"), str(empty_film)], bin_dir, ROOT)
    assert "WARN 冷讀" in pre.stdout, pre.stdout
    (empty_film / "audit" / "coldread-script.md").write_text("narration_sha: x\nVERDICT: 不通過\n", encoding="utf-8")
    post = run([sys.executable, str(ROOT / "scripts" / "precheck.py"), str(empty_film)], bin_dir, ROOT)
    assert pre.returncode == post.returncode, (pre.returncode, post.returncode)
    assert "WARN 冷讀（稿）" in post.stdout and "2 項 WARN" in post.stdout, post.stdout

print("ok")
