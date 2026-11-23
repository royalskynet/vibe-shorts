#!/usr/bin/env python3
"""oc_headless.sh 的自檢：假 opencode 驗參數、模型覆寫、exit code、空 prompt 與網路錯誤重試一次。"""
import os
import stat
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = str(ROOT / "scripts" / "oc_headless.sh")
DEFAULT_MODEL = "opencode-go/deepseek-v4.1-flash"


def make_fake(bin_dir: Path, name: str, code: int) -> Path:
    p = bin_dir / name
    p.write_text(
        "#!/usr/bin/env bash\n"
        ': > "$ARGS_FILE"\n'
        'for a in "$@"; do printf \'%s\\0\' "$a" >> "$ARGS_FILE"; done\n'
        "printf 'FAKE-OK\\n'\n"
        f"exit {code}\n",
        encoding="utf-8",
    )
    p.chmod(p.stat().st_mode | stat.S_IXUSR)
    return p


def make_counted(bin_dir: Path, name: str, counter: Path, code: int, first_msg: str) -> Path:
    """計數型假 opencode：first_msg 非空時第一次印它並 exit 1，之後印 FAKE-OK 並 exit code。"""
    p = bin_dir / name
    p.write_text(
        "#!/usr/bin/env bash\n"
        f'n=$(cat "{counter}" 2>/dev/null || echo 0); echo $((n+1)) > "{counter}"\n'
        + (f'if [ "$n" = 0 ]; then printf \'{first_msg}\\n\' >&2; exit 1; fi\n' if first_msg else "")
        + "printf 'FAKE-OK\\n'\n"
        f"exit {code}\n",
        encoding="utf-8",
    )
    p.chmod(p.stat().st_mode | stat.S_IXUSR)
    return p


def read_args(path: Path):
    raw = path.read_bytes()
    return [x.decode("utf-8") for x in raw.split(b"\0")[:-1]]


def run(fake: Path, args_file: Path, data: bytes, extra=None):
    # log 寫暫存目錄：寫進 repo 的 logs/oc 會把 latest.log 從正在跑的 od 搶走（11-15 監看斷線）
    env = {**os.environ, "OC_BIN": str(fake), "ARGS_FILE": str(args_file),
           "OC_LOGDIR": str(args_file.parent / "oclogs"), **(extra or {})}
    return subprocess.run(["bash", SCRIPT], input=data, capture_output=True, cwd=str(ROOT), env=env)


with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    args_file = d / "args.bin"
    prompt = "第一行\n第二行 with ASCII"
    ok = make_fake(d, "opencode-ok", 0)
    bad = make_fake(d, "opencode-bad", 7)

    r = run(ok, args_file, prompt.encode("utf-8"))
    assert r.returncode == 0, r.stderr
    assert b"FAKE-OK" in r.stdout, r.stdout
    args = read_args(args_file)
    assert args[0] == "run", args
    assert "-m" in args and args[args.index("-m") + 1] == DEFAULT_MODEL, args
    assert "--dir" in args and args[args.index("--dir") + 1] == str(ROOT), args
    assert "--" in args, args
    assert args[-1] == prompt, repr(args[-1])

    r = run(ok, args_file, prompt.encode("utf-8"), {"OC_MODEL": "x/y"})
    assert r.returncode == 0, r.stderr
    args = read_args(args_file)
    assert args[args.index("-m") + 1] == "x/y", args
    assert DEFAULT_MODEL not in args, args

    r = run(bad, args_file, prompt.encode("utf-8"))
    assert r.returncode == 7, r.returncode

    r = run(ok, args_file, b"")
    assert r.returncode == 2, r.returncode
    assert b"oc_headless: empty prompt" in r.stderr, r.stderr

    # 暫時性網路錯誤（ENOTFOUND）只重試一次：第一次失敗、第二次成功 → rc=0、被叫 2 次
    counter = d / "count"
    flaky = make_counted(d, "opencode-flaky", counter, 0, "getaddrinfo ENOTFOUND opencode.ai")
    r = run(flaky, args_file, prompt.encode("utf-8"), {"OC_RETRY_SLEEP": "0"})
    assert r.returncode == 0, (r.returncode, r.stderr)
    assert counter.read_text().strip() == "2", counter.read_text()
    logs = [f.read_text() for f in (d / "oclogs").glob("*.log")]
    assert any("oc_headless: retry after ENOTFOUND" in t for t in logs), logs

    # 非網路錯誤（exit 7、無網路字串）：不重試，被叫 1 次、rc 原樣回傳
    counter = d / "count2"
    once = make_counted(d, "opencode-once", counter, 7, "")
    r = run(once, args_file, prompt.encode("utf-8"), {"OC_RETRY_SLEEP": "0"})
    assert r.returncode == 7, r.returncode
    assert counter.read_text().strip() == "1", counter.read_text()

    # 成功但 log 含網路字串（中途瞬斷已自行恢復）：不重試，被叫 1 次
    counter = d / "count4"
    recovered = make_counted(d, "opencode-recovered", counter, 0, "")
    recovered.write_text(recovered.read_text(encoding="utf-8").replace(
        "printf 'FAKE-OK\\n'\n", "printf 'ECONNRESET retried\\nFAKE-OK\\n'\n"), encoding="utf-8")
    r = run(recovered, args_file, prompt.encode("utf-8"), {"OC_RETRY_SLEEP": "0"})
    assert r.returncode == 0, r.returncode
    assert counter.read_text().strip() == "1", counter.read_text()

    # 重試只重試一次：兩次都 ENOTFOUND → rc=1、被叫 2 次
    counter = d / "count3"
    always = make_counted(d, "opencode-always", counter, 1, "getaddrinfo ENOTFOUND opencode.ai")
    always.write_text(always.read_text(encoding="utf-8").replace(
        "printf 'FAKE-OK\\n'\n", "printf 'getaddrinfo ENOTFOUND opencode.ai\\n' >&2\n"), encoding="utf-8")
    r = run(always, args_file, prompt.encode("utf-8"), {"OC_RETRY_SLEEP": "0"})
    assert r.returncode == 1, r.returncode
    assert counter.read_text().strip() == "2", counter.read_text()

print("ALL PASS")
