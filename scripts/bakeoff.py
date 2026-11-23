#!/usr/bin/env python3
"""寫稿擂台（使用者 2026-11-06：「稿子看誰比較會寫」）：同一份事實表給多個模型寫旁白稿，匿名兩兩盲評。

用法：
  scripts/bakeoff.py write films/<片>   # 讀 FACTS.md → bakeoff/<寫手>.md
  scripts/bakeoff.py judge films/<片>   # 兩兩比、每對 AB／BA 各評一次 → bakeoff/RESULT.md＋TOP.json（機器讀）

評法借 MT-Bench pairwise（arXiv 2306.05685）：同一評審換位置後結論不同＝和局，抵銷位置偏誤。
寫手只比文筆：事實一律來自 FACTS.md，寫手不上網。結構門（precheck.story_problems）不過的稿照評，結果標出來。
BAKEOFF_WRITERS／BAKEOFF_JUDGES 用空白分隔覆寫名單；名字要在 ENGINES 裡。
評審預設 codex＋deepseek（使用者 11-06 定：省 Claude token）。兩個評審都是寫手，各有自評偏誤（兩題實測都偏自己）；
結果分評審列，兩人都判贏的才算可靠。
"""
import itertools
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import precheck  # noqa: E402

CLAUDE = "~/.local/bin/claude"
OC_MODEL = "opencode-go/deepseek-v4.1-flash"
ENGINES = {
    "opus": ["claude", "claude-opus-5-5"],
    "fable": ["claude", "claude-fable-5-1"],
    "codex": ["codex", None],
    "deepseek": ["opencode", OC_MODEL],
}
WRITERS = os.environ.get("BAKEOFF_WRITERS", "opus fable codex deepseek").split()
JUDGES = os.environ.get("BAKEOFF_JUDGES", "codex deepseek").split()  # 使用者 11-06：評審外移，不花 Claude
TIMEOUT = int(os.environ.get("BAKEOFF_TIMEOUT", 900))

WRITE_PROMPT = """你是台灣短影音科普帳號的旁白寫手。這是寫稿比賽：好幾個寫手拿同一份事實表各寫一份，評審盲評哪份讓人看到最後、後段有爆點。

只輸出 narration.md 全文，不要任何說明、不要 code fence。格式：
## 鉤子
（念的字，一行一句）
## 機制
…
## 轉折
…
## 落點
…

硬規則：
- 全文 300–420 字（不含段名），每行一句、≤35 字，一行只有一個句末標點（。？！擇一，問句後面接別的話就換行）。
- 段名只用 鉤子／機制／轉折／落點，順序固定；中間可加段，落點最後。
- 鉤子第一句 ≤25 字，要有「你」或是問句。轉折段第一句要有轉折連詞（但／可是／不過／其實／原來／問題是…）。
- 事實與數字只能用下面事實表「已查證」的內容，不准自己補數字。
- 台灣口語，一句講完一個因果。

寫法規則（repo 正本節錄）：
{rules}

# 事實表
{facts}
"""

JUDGE_PROMPT = """你是短影音主編。下面是同一題的兩份 60–90 秒旁白稿 A、B，事實都來自同一份事實表。
判斷哪一份讓滑到的人看到最後、後段有爆點。看：第一句能不能讓人停下；有沒有懸念留到最後才揭曉；中段有沒有再鉤一次；
最反直覺的事實是不是壓在後段；結尾有沒有回扣開頭而不是總結；念起來像不像台灣人講話；有沒有誇大或用了事實表沒有的數字（有就重扣）。

先用 3–5 行講理由，最後一行只寫 `WINNER: A`、`WINNER: B` 或 `WINNER: TIE`。

# 事實表
{facts}

# 稿 A
{a}

# 稿 B
{b}
"""


BUSY = re.compile(r"overloaded|capacity|rate.?limit|retry shortly", re.I)  # 上游暫時忙：等一下再試
RETRIES, RETRY_WAIT = 3, 45


def run(engine, prompt, cwd):
    """跑一個引擎；上游忙（BUSY）最多重試 RETRIES 次，其他錯誤直接丟。"""
    for i in range(RETRIES + 1):
        try:
            return run_once(engine, prompt, cwd)
        except RuntimeError as e:
            if i == RETRIES or not BUSY.search(str(e)):
                raise
            time.sleep(RETRY_WAIT * (i + 1))


def run_once(engine, prompt, cwd):
    """跑一個引擎一次，回傳最後一則回覆文字；失敗丟 RuntimeError（含一行原因）。"""
    kind, model = ENGINES[engine]
    out = Path(cwd) / f"last-{os.getpid()}-{abs(hash(prompt))}.md"
    if kind == "claude":
        # --tools 是可變長度旗標，prompt 放參數會被吃進去 → 走 stdin。
        # --setting-sources project：跳過 user 層 hook／plugin 注入，輸入從約 9 萬降到約 2.5 萬（11-06 實測）；
        # 寫手 --tools "" 沒有工具，不需要 user 層安全 hook。
        cmd = [CLAUDE, "-p", "--model", model, "--tools", "", "--setting-sources", "project"]
    elif kind == "codex":
        # prompt 走參數、stdin 給 /dev/null：不然 codex exec 卡在讀 stdin（coldread.sh 同一個坑）
        cmd = ["codex", "exec", "--skip-git-repo-check", "-s", "read-only", "-o", str(out), prompt]
    else:
        cmd = ["opencode", "run", "-m", model, "--", prompt]
    stdin = {"input": prompt} if kind == "claude" else {"stdin": subprocess.DEVNULL}
    r = subprocess.run(cmd, cwd=cwd, **stdin, capture_output=True, text=True, timeout=TIMEOUT)
    text = out.read_text(encoding="utf-8") if kind == "codex" and out.exists() else r.stdout
    out.unlink(missing_ok=True)
    if r.returncode != 0 or not text.strip():
        tail = [l for l in r.stderr.splitlines() if not re.search(r"token|key", l, re.I)][-1:]
        raise RuntimeError(f"{engine} rc={r.returncode} {tail[0] if tail else '無輸出'}")
    return text


def clean(text):
    """去掉 code fence 與段名前的閒聊，只留從第一個「## 」開始的稿。"""
    text = re.sub(r"^```\w*\n|```\s*$", "", text.strip(), flags=re.M)
    i = text.find("## ")
    return text[i:].strip() + "\n" if i >= 0 else text.strip() + "\n"


def rules():
    w = (ROOT / "docs/WRITING.md").read_text(encoding="utf-8")
    return w[w.index("## 7."):]


def write(film):
    facts = (film / "FACTS.md").read_text(encoding="utf-8")
    d = film / "bakeoff"
    d.mkdir(exist_ok=True)
    prompt = WRITE_PROMPT.format(rules=rules(), facts=facts)

    def one(name):
        with tempfile.TemporaryDirectory() as cwd:
            try:
                (d / f"{name}.md").write_text(clean(run(name, prompt, cwd)), encoding="utf-8")
                return f"OK   {name}"
            except Exception as e:  # 一個寫手掛掉不拖垮其他人
                return f"FAIL {name}：{e}"

    with ThreadPoolExecutor(len(WRITERS)) as ex:
        lines = list(ex.map(one, WRITERS))
    print("\n".join(lines))
    return 0 if any(l.startswith("OK") for l in lines) else 3


def verdict(text):
    m = re.findall(r"WINNER:\s*(A|B|TIE)", text)
    return m[-1] if m else None


def pair_result(first, second):
    """同一評審、同一對稿的兩次結果 → 勝者或 None（和局）。

    first：x 放 A、y 放 B 的判決；second：y 放 A、x 放 B 的判決。換位後一致才算贏。
    """
    if first == "A" and second == "B":
        return "x"
    if first == "B" and second == "A":
        return "y"
    return None


def tally(names, results):
    """results：[(judge, x, y, first, second)] → {name: 分數}，贏 1、和 0.5、輸 0。"""
    score = {n: 0.0 for n in names}
    for _, x, y, first, second in results:
        w = pair_result(first, second)
        if w == "x":
            score[x] += 1
        elif w == "y":
            score[y] += 1
        else:
            score[x] += 0.5
            score[y] += 0.5
    return score


def write_top(d, names, results, missing, pairs):
    """寫 bakeoff/TOP.json：總分、各評審分、缺票數、前兩名（同分照 codex 評審分，再照名字）。

    呼叫端（autoloop）只讀這個檔，不解析 RESULT.md 的中文行。
    """
    total = tally(names, results)
    per = {n: {j: tally(names, [r for r in results if r[0] == j])[n] for j in JUDGES} for n in names}
    order = sorted(names, key=lambda n: (-total[n], -per[n].get("codex", 0.0), n))
    top = {"tiebreak": "同分照 codex 評審分，再照名字",
           "writers": names, "judges": JUDGES, "missing": missing, "pairs": pairs,
           "top2": order[:2],
           "rank": [{"name": n, "total": total[n], "codex": per[n].get("codex", 0.0),
                     "per_judge": per[n]} for n in order]}
    (d / "TOP.json").write_text(json.dumps(top, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return top


def judge(film):
    facts = (film / "FACTS.md").read_text(encoding="utf-8")
    d = film / "bakeoff"
    names = sorted(p.stem for p in d.glob("*.md") if p.stem in ENGINES)
    if len(names) < 2:
        print(f"bakeoff/ 只有 {len(names)} 份稿，至少 2 份才能比", file=sys.stderr)
        if names:  # 只有一份也寫 TOP.json：呼叫端照用那一份，不必解析 RESULT.md
            write_top(d, names, [], 0, 0)
        return 2
    body = {n: (d / f"{n}.md").read_text(encoding="utf-8") for n in names}
    jobs = [(j, x, y, a, b) for j in JUDGES for x, y in itertools.combinations(names, 2)
            for a, b in ((x, y), (y, x))]

    def one(job):
        j, x, y, a, b = job
        with tempfile.TemporaryDirectory() as cwd:
            try:
                return job, verdict(run(j, JUDGE_PROMPT.format(facts=facts, a=body[a], b=body[b]), cwd))
            except Exception as e:
                print(f"評審失敗 {j} {a}vs{b}：{e}", file=sys.stderr)
                return job, None

    got = {}
    with ThreadPoolExecutor(4) as ex:
        for (j, x, y, a, b), v in ex.map(one, jobs):
            got[(j, x, y, a == x)] = v
    results = [(j, x, y, got.get((j, x, y, True)), got.get((j, x, y, False)))
               for j in JUDGES for x, y in itertools.combinations(names, 2)]
    missing = sum(v is None for v in got.values())
    top = write_top(d, names, results, missing, len(jobs))
    lines = ["# 寫稿擂台結果", "", f"寫手：{'、'.join(names)}　評審：{'、'.join(JUDGES)}（每對 AB／BA 各一次，換位不一致＝和局）", ""]
    if missing:
        lines += [f"**缺票 {missing}／{len(jobs)}**（評審失敗或沒給 WINNER，缺票算和局，結果不可靠）", ""]
    total = {r["name"]: r["total"] for r in top["rank"]}
    for n in [r["name"] for r in top["rank"]]:
        per = "　".join(f"{j} {tally(names, [r for r in results if r[0] == j])[n]:g}" for j in JUDGES)
        probs = precheck.story_problems(precheck.parse_narration(body[n]))
        lines.append(f"- {n}：{total[n]:g} 分（{per}）{'　結構門：' + '；'.join(probs) if probs else ''}")
    lines += ["", "## 逐對", ""]
    for j, x, y, f, s in results:
        w = pair_result(f, s)
        lines.append(f"- {j}：{x} vs {y} → {'和' if w is None else (x if w == 'x' else y)}（{f}/{s}）")
    (d / "RESULT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 3 if missing else 0  # 缺票 exit 3：呼叫端（autoloop）要知道結果不完整


def main(argv):
    if len(argv) != 3 or argv[1] not in ("write", "judge"):
        print(__doc__.split("\n\n")[1], file=sys.stderr)
        return 2
    film = Path(argv[2]).resolve()
    if not (film / "FACTS.md").is_file():
        print(f"缺 {film}/FACTS.md", file=sys.stderr)
        return 2
    return write(film) if argv[1] == "write" else judge(film)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
