#!/usr/bin/env python3
"""營銷號閉環：approved 檔的 status 推進。本程式零 token，只在要寫稿／建片時叫 Claude headless。

  autoloop.py night     02:00 launchd：建 1 支已核稿的片＋寫最多 2 份稿（建置不併發）
  autoloop.py publish   launchd 監看 approved/：status=publish_ok 的片發三平台；now: "true" 立即開工
  autoloop.py status    列出每個 approved 檔的狀態
  autoloop.py digest    印 08:30 待核准清單的營銷號段（白話全文，Emperor 原文轉貼）
  autoloop.py alerts    可行動行（等核稿／等看片／卡住）用 Marketer 的 post webhook 發給使用者，同日不重複

approved 檔＝state/approved/<日期>-<slug>.md，開頭 frontmatter：
  ---
  slug: kebab-case 片名（= films/<slug>）
  title: 題目
  proposal: proposal.md 絕對路徑
  topic_no: 第幾題
  status: approved
  ---
status 誰寫：
  approved／script_revise／script_ok／publish_ok  ← Emperor（使用者回話後寫入）
  script_ready／built／published／failed          ← 本程式（依檔案與閘門結果判定，不信模型自述）

now（立即開工）只認字串 "true"，由使用者說「現在做 <slug>」寫入；移除一律 del meta["now"]，
不准寫 false。publish 觸發時不等 21:00 cutoff；該階段到終點（script_ready／built／failed／
published／dropped）就自動移除，night 也一樣。不會把 now 改成 publish_ok、不會因 now 呼叫 do_publish。
"""
import fcntl
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import precheck  # noqa: E402

ROOT =Path(os.environ.get("AUTOLOOP_ROOT", Path(__file__).resolve().parent.parent))
APPROVED = Path(os.environ.get("AUTOLOOP_DIR", ROOT / "state/approved"))
LOG = Path(os.environ.get("AUTOLOOP_LOG", ROOT / "logs/autoloop.log"))
# 不載 user 層設定：它的 CLAUDE_CODE_SUBPROCESS_ENV_SCRUB 會把 -p 的權限打回 default（fixindex 10029），
# 使用者層 hook（delegate-guard）也會在無人值守時要求改派。訂閱 OAuth 照常。skill 改由 prompt 指檔讀。
CLAUDE = shlex.split(os.environ.get(
    "AUTOLOOP_CLAUDE", "/Users/51mini/.local/bin/claude -p --model claude-opus-5-5"
    " --setting-sources project,local --permission-mode bypassPermissions"))
PY = os.environ.get("AUTOLOOP_PY", "/usr/bin/python3")
DCQ = shlex.split(os.environ.get("AUTOLOOP_DCQ", "dcq"))
DCQ_TIMEOUT = int(os.environ.get("AUTOLOOP_DCQ_TIMEOUT", 3600))  # 查證工單最長 60 分（review 設計 3）
CLAUDE_TIMEOUT = int(os.environ.get("AUTOLOOP_TIMEOUT", 4 * 3600))
MAX_SCRIPTS = 1  # 試點期（review 設計 3）：一晚一題擂台，03:00 前收工；順一晚再回 2
CUTOFF_HOUR = 21  # 使用者 10-29 定：21:00 前核准的當晚做，之後的排隔晚（凌晨跑不佔白天 usage）
NOW_WAIT = int(os.environ.get("AUTOLOOP_NOW_WAIT", 1800))  # now 立即開工最多阻塞等鎖 30 分鐘
NOW_START = ("approved", "script_revise", "script_ok")  # now 只從這三個狀態開工
NOW_END = ("script_ready", "built", "failed", "published", "dropped")  # 到終點一律刪 now
# 營銷號事件歸 Marketer（使用者 11-07「要發Marketer才對」），不進 fleet/alerts（那是 Scribe 的系統告警）；這裡只留同日去重記錄
ALERTS = Path(os.environ.get("AUTOLOOP_ALERTS", ROOT / "state/vibe-alerts"))
FLEET = os.environ.get("AUTOLOOP_FLEET", str(Path(__file__).resolve().parent))  # notify_send.py 所在
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,40}$")
GH_BLOB = "https://github.com/royalskynet/vibe-shorts-pipeline/blob/main"  # 私人 repo；稿子寫好就 push，清單給連結不給本機路徑

SCRIPT_PROMPT = """你在 /Users/51mini/dev/vibe-shorts-pipeline，先讀 /Users/51mini/.claude/skills/vibe-shorts/SKILL.md（vibe-shorts skill，查表段的 references 需要時再讀），照它與 repo CLAUDE.md 做事。這是無人值守的夜間批次，沒有人會回答問題。

任務：替使用者已選的題目寫單人旁白科普稿（docs/WRITING.md §7；不寫對談），只寫稿，不建置。
- 核准檔：{path}（題目、proposal 路徑、第幾題都在 frontmatter）
- 片名：{slug}，片目錄 films/{slug}
{revise}
要做：
1. 片目錄不存在就照 skill「做一支片」步 1 建，但範本改用 films/france（複製後清舊產物、改 build.sh 的 OUT=、rhythm-profile 寫 card、pace.json 與 m3 男聲照 france）。
2. 照 docs/WRITING.md §7＋§8（爆點結構：懸念留到最後、40–60% 再鉤、爆點壓後 20%、結尾回扣第一句）從同題爆款抽鉤子與機制寫旁白稿：寫 TREATMENT.md（要有「爆款證據：」行，連結＋播放數）、narration.md、SOURCES.md、meta/facts.md。台詞不照抄，禁防衛性中立語言。
3. 寫完照 /Users/51mini/.claude/plugins/cache/genie-harness/genie-harness/0.5.5/skills/genie-humanizer/SKILL.md 逐句過一遍 narration.md：念出來要像台灣人口語（「輸得越準」這類翻譯腔、硬湊的文法改掉），一句一件事，同一個東西同一個叫法，不用格言收尾。改完寫 films/{slug}/audit/humanize.md：首行 `narration_sha: <narration.md 的 sha256>`，下面列改了哪些句（原句 → 新句），precheck「口語化」門會核。
4. 不跑 build.sh、不渲染、不上傳、不發布、不 commit，不動其他片目錄。
完成就結束；做不到就在 films/{slug}/BLOCKED.md 寫原因。"""

BUILD_PROMPT = """你在 /Users/51mini/dev/vibe-shorts-pipeline，先讀 /Users/51mini/.claude/skills/vibe-shorts/SKILL.md（vibe-shorts skill，查表段的 references 需要時再讀），照它與 repo CLAUDE.md 做事。這是無人值守的夜間批次，沒有人會回答問題。

任務：films/{slug} 的改編稿使用者已核過（核准檔 {path}），接著建片到可發布。
- 先讀核准檔全文：內文的「## 建片注意」「## 修改意見」優先於 skill 預設。
- 不改 narration.md 台詞（使用者核過的稿）；畫面、動畫、混音、說明文字照 skill 寫。
- 片目錄只有 FACTS.md／bakeoff／narration.md 時，先以 films/taipei-silence 為範本補齊，TREATMENT／SOURCES／meta/facts.md 一律取自 FACTS.md；humanize 只蓋戳記不改台詞。
- 照 skill「做一支片」步 2 剩下的檔（index.html、mix.py、cast.json、三份 caption）→ 步 3 反方稽核 → 步 4 build.sh → 步 5 qa_sheet 目視自評 → 步 6 precheck → 步 7 deliver.sh。
- 問題修在源頭（稿以外的檔、index.html、build），不放寬任何閘門基準。
- 不上傳、不發布、不 commit，不動其他片目錄。
完成條件：`python3 scripts/precheck.py films/{slug}` exit 0，且 films/{slug}/dist/ 有三平台檔。做不到就在 films/{slug}/BLOCKED.md 寫卡在哪。"""


def log(msg):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%F %T')} {msg}\n")
    print(msg)


def parse(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n?", text, re.S)
    if not m:
        return None, text
    meta = {}
    for line in m.group(1).splitlines():
        k, sep, v = line.partition(":")
        if sep:
            meta[k.strip()] = v.strip()
    return meta, text[m.end():]


def save(path, meta, body):
    head = "\n".join(f"{k}: {v}" for k, v in meta.items())
    tmp = path.with_suffix(".tmp")
    tmp.write_text(f"---\n{head}\n---\n{body}", encoding="utf-8")
    tmp.replace(path)


def set_status(path, meta, body, status, **extra):
    meta["status"] = status
    if status in NOW_END:
        meta.pop("now", None)  # 到終點就清掉立即開工旗標，避免下次「稿改」帶著陳舊 now 直接開工
    meta.update({k: str(v).replace("\n", " ") for k, v in extra.items()})
    meta["updated"] = time.strftime("%F %T")
    save(path, meta, body)
    log(f"{path.name}: status={status} {extra or ''}")


def cutoff(now=None):
    """最近一個 ≤ now 的 21:00（epoch 秒）。檔案 mtime 晚於它＝核准太晚，留到下一晚。"""
    now = now or time.time()
    t = time.localtime(now)
    c = time.mktime((t.tm_year, t.tm_mon, t.tm_mday, CUTOFF_HOUR, 0, 0, 0, 0, -1))
    return c if c <= now else c - 86400


def items():
    out = []
    for p in sorted(APPROVED.glob("*.md")):
        meta, body = parse(p)
        if meta is None or "status" not in meta:
            log(f"{p.name}: 沒有 frontmatter／status，跳過")
            continue
        out.append((p, meta, body))
    return out


def now_flag(meta):
    """frontmatter now 只認字串 true（含 SKILL 教使用者寫的 now: "true"）；false 一律不算。"""
    return str(meta.get("now", "")).strip().strip('"').strip("'") == "true"


def alert(*lines):
    """新行合併成一則，用 Marketer 的 post webhook 發（不叫模型）；同一行同日只發一次，發成功才記進 <日>.txt。
    一次一則：逐行發會撞 webhook 429（11-07 實測 12 行掉 2 行）。"""
    ALERTS.mkdir(parents=True, exist_ok=True)
    p = ALERTS / f"{time.strftime('%F')}.txt"
    old = p.read_text(encoding="utf-8").splitlines() if p.is_file() else []
    new = [ln for ln in dict.fromkeys(" ".join(l.split())[:160] for l in lines) if ln not in old]
    if not new:
        return
    if FLEET not in sys.path:
        sys.path.insert(0, FLEET)
    from notify_send import post
    body = "營銷號待你處理：\n" + "\n".join(f"・{ln}" for ln in new)
    ok, info = post("Marketer", f"vibe-alert:{time.strftime('%F')}:" + "|".join(new), body)
    log(f"alert → Marketer {info}: {len(new)} 行")
    if ok:  # 失敗不記，下個整點 alerts 會再發；失敗不寫 outbox，下個整點重發
        with p.open("a", encoding="utf-8") as f:
            f.write("".join(ln + "\n" for ln in new))


def error_summary(error):
    """告警只帶卡點第一句，避免整份 BLOCKED Markdown 淹沒訊息。"""
    section = re.split(r"#{1,6}\s*卡在哪\s*", error, maxsplit=1)
    text = section[-1]
    text = re.split(r"\s*#{1,6}\s+", text, maxsplit=1)[0] if len(section) > 1 else text
    text = re.sub(r"(?m)^\s*#{1,6}\s*", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return re.split(r"(?<=[。！？])", text, maxsplit=1)[0][:160]


def actionable():
    """可行動行：等核稿／等看片／卡住。沒有就回空清單。"""
    out = []
    for _, meta, _ in items():
        st, slug = meta["status"], meta.get("slug", "?")
        if st == "script_ready":
            out.append(f"{slug} 等核稿：{meta.get('title', '')}".rstrip("："))
        elif st == "built":
            out.append(f"{slug} 等看片：{meta.get('title', '')} {meta.get('yt_private', '')}".rstrip("： "))
        elif st == "failed":
            out.append(f"{slug} 卡住：{error_summary(meta.get('error', ''))}".rstrip("："))
    return out


def run_now():
    """now 立即開工：approved／script_revise 寫稿、script_ok 建片；不看 21:00 cutoff。"""
    for p, meta, body in items():
        if not now_flag(meta) or meta["status"] not in NOW_START:
            continue
        log(f"{p.name}: now 立即開工")
        if meta["status"] == "script_ok":
            do_build(p, meta, body)
        else:
            do_script(p, meta, body)


def acquire(lock, wait):
    """取排他鎖；wait=0 不阻塞，>0 最多等這麼多秒。"""
    end = time.time() + wait
    while True:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except BlockingIOError:
            if time.time() >= end:
                return False
            time.sleep(0.2)


def check_slug(p, meta, body):
    slug = meta.get("slug", "")
    if SLUG_RE.match(slug):
        return slug
    set_status(p, meta, body, "failed", error=f"slug 不合法：{slug!r}（要 kebab-case 英數）")
    return None


def run_claude(prompt):
    try:
        # 從 Claude Code session 裡手動觸發時會繼承這個變數，子 claude 會把 bypassPermissions 降成 default、寫不了檔（10-29 實測）
        env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CODE_SUBPROCESS_ENV_SCRUB"}
        r = subprocess.run(CLAUDE, input=prompt, text=True, cwd=ROOT, capture_output=True, timeout=CLAUDE_TIMEOUT, env=env)
        return r.returncode, (r.stdout + r.stderr)[-2000:]
    except subprocess.TimeoutExpired:
        return 124, f"逾時 {CLAUDE_TIMEOUT}s"


def blocked(film):
    b = film / "BLOCKED.md"
    return b.read_text(encoding="utf-8")[:300] if b.is_file() else ""


def push_script(film):
    """稿子與事實表推上 GitHub 給使用者點連結看。push 失敗只記 log，不擋流程（清單連結會 404，log 查得到）。"""
    files = [str(f.relative_to(ROOT)) for f in
             [film / "narration.md", film / "TREATMENT.md", film / "SOURCES.md", film / "FACTS.md",
              *(sorted((film / "bakeoff").glob("*.md")) if (film / "bakeoff").is_dir() else [])]
             if f.is_file()]
    if not files:
        return
    for cmd in (["git", "add", "--", *files], ["git", "commit", "-q", "-m", f"{film.name}：夜間寫稿", "--", *files],
                ["git", "push", "-q", "origin", "HEAD:main"]):
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            log(f"{film.name}: {' '.join(cmd[:2])} rc={r.returncode} {(r.stdout + r.stderr)[-200:]!r}")
            return


def facts_check(slug):
    """工單驗收的兩半：facts.py check 全過，且 refs/VIRAL-LEDGER.md 有（slug）。回 (ok, 說明)。"""
    r = subprocess.run([PY, "scripts/facts.py", "check", f"films/{slug}"],
                       cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        fails = [l.strip() for l in (r.stdout + r.stderr).splitlines() if l.strip().startswith("FAIL")]
        return False, (fails[0] if fails else f"facts check rc={r.returncode}")
    ledger = ROOT / "refs/VIRAL-LEDGER.md"
    if not ledger.is_file() or f"（{slug}）" not in ledger.read_text(encoding="utf-8"):
        return False, f"refs/VIRAL-LEDGER.md 沒有（{slug}）"
    return True, ""


def facts_run(slug, title):
    """產工單 → dcq add（派o 預設序）→ dcq wait；逾時先 cancel，免得晚到的 worker 覆寫 FACTS.md。"""
    t = subprocess.run([PY, "scripts/facts.py", "task", slug, title], cwd=ROOT, capture_output=True, text=True)
    tasks = [l.strip() for l in t.stdout.splitlines() if l.strip().endswith(".md")]
    if t.returncode != 0 or not tasks:
        return False, f"facts task rc={t.returncode} {(t.stdout + t.stderr)[-200:]}".strip()
    add = subprocess.run([*DCQ, "add", tasks[-1], str(ROOT), "mid"], cwd=ROOT, capture_output=True, text=True,
                         env=dict(os.environ, DCQ_ORDER="default"))
    ids = [l.strip() for l in add.stdout.splitlines() if l.strip()]
    if add.returncode != 0 or not ids:
        return False, f"dcq add rc={add.returncode} {(add.stdout + add.stderr)[-200:]}".strip()
    jid = ids[-1]
    log(f"{slug}: facts dcq job {jid}")
    w = subprocess.run([*DCQ, "wait", jid, "--timeout", str(DCQ_TIMEOUT)], cwd=ROOT, capture_output=True, text=True)
    if w.returncode == 124:
        subprocess.run([*DCQ, "cancel", jid], cwd=ROOT, capture_output=True, text=True)
        return False, f"查證逾時（{DCQ_TIMEOUT}s），已 dcq cancel {jid}"
    if w.returncode == 3:
        return None, "沒有 runner（dcq wait rc=3），留待下一輪重試"
    if w.returncode != 0:
        tail = [l for l in (w.stdout + w.stderr).splitlines() if l.strip()][-1:]
        return False, f"查證失敗（dcq wait rc={w.returncode}）{tail[0] if tail else ''}".strip()
    return facts_check(slug)


def bake(slug, mode):
    """bakeoff.py write／judge；回傳碼意義見 bakeoff.py（write 3＝0 份稿，judge 2＝只有 1 份，judge 3＝缺票）。"""
    r = subprocess.run([PY, "scripts/bakeoff.py", mode, f"films/{slug}"], cwd=ROOT, capture_output=True, text=True)
    log(f"{slug}: bakeoff {mode} rc={r.returncode} {(r.stdout + r.stderr)[-300:]!r}")
    return r.returncode


def read_top(film):
    f = film / "bakeoff/TOP.json"
    try:
        return json.loads(f.read_text(encoding="utf-8")) if f.is_file() else {}
    except (OSError, ValueError):
        return {}


def fixed_cards(body):
    """提案「## 卡片」段的「卡N｜旁白｜畫面」逐行取旁白；沒有該段回空串列。"""
    m = re.search(r"^## 卡片[ \t]*\n(.*?)(?=^## |\Z)", body, re.S | re.M)
    if not m:
        return []
    return [c.strip() for c in re.findall(r"^卡\d+｜([^｜\n]+)｜", m.group(1), re.M) if c.strip()]


def do_fixed_script(p, meta, body, slug, film, cards):
    """提案已帶使用者核過的完稿：旁白逐字進 narration.md，不查證、不擂台、不改稿。"""
    if film.exists() and not {f.name for f in film.iterdir()} <= {"narration.md"}:
        set_status(p, meta, body, "failed", error=f"films/{slug} 已存在，換 slug 再核准")
        return
    film.mkdir(parents=True, exist_ok=True)
    (film / "narration.md").write_text(
        "".join(f"## 卡{i}\n{c}\n\n" for i, c in enumerate(cards, 1)).rstrip() + "\n", encoding="utf-8")
    push_script(film)
    for k in ("film", "script_a", "script_b", "score_a", "score_b", "bakeoff_missing"):
        meta.pop(k, None)
    set_status(p, meta, body, "script_ready", script=str(film / "narration.md"), fixed="卡片原文")


def do_script(p, meta, body):
    slug = check_slug(p, meta, body)
    if not slug:
        return
    film = ROOT / "films" / slug
    if meta["status"] == "script_revise":
        do_revise(p, meta, body, slug, film)
        return
    cards = fixed_cards(body)
    if cards:
        do_fixed_script(p, meta, body, slug, film, cards)
        return
    facts_only = film.is_dir() and {f.name for f in film.iterdir()} == {"FACTS.md"}
    if film.exists() and not facts_only:  # 查證可能在沒 runner 返回後才完工，只有事實表可安全續接
        set_status(p, meta, body, "failed", error=f"films/{slug} 已存在，換 slug 再核准")
        return
    title = meta.get("title", slug)
    ok, why = facts_check(slug)  # 已過就跳過 dcq：重跑別再花 60 分
    if not ok:
        ok, why = facts_run(slug, title)
        if ok is None:  # 暫時沒有執行程序，不是查證失敗；核准檔原樣保留
            log(f"{slug}: {why}")
            return
        if not ok:
            set_status(p, meta, body, "failed", error=why)
            alert(f"{slug} 查證卡住：{why}")
            return
    rc = bake(slug, "write")
    if rc != 0:  # 3＝一份稿都沒寫成
        set_status(p, meta, body, "failed", error=f"擂台沒有稿（bakeoff write rc={rc}）")
        alert(f"{slug} 擂台沒有稿：bakeoff write rc={rc}")
        return
    rc = bake(slug, "judge")
    top = read_top(film)
    rank = [r for r in (top.get("rank") or []) if (film / "bakeoff" / f"{r.get('name')}.md").is_file()]
    if rc not in (0, 2, 3) or not rank:  # 2＝只有一份稿照用；3＝缺票照用但 digest 標示
        set_status(p, meta, body, "failed", error=f"擂台評審失敗（bakeoff judge rc={rc}，可用稿 {len(rank)}）")
        alert(f"{slug} 擂台評審失敗：bakeoff judge rc={rc}")
        return
    a = film / "bakeoff" / f"{rank[0]['name']}.md"
    b = film / "bakeoff" / f"{rank[1]['name']}.md" if len(rank) > 1 else None
    push_script(film)
    set_status(p, meta, body, "script_ready", film=f"films/{slug}",
               script_a=str(a), script_b=str(b) if b else "",
               score_a=f"{rank[0].get('total', 0):g}", score_b=f"{rank[1].get('total', 0):g}" if b else "",
               bakeoff_missing=f"{top.get('missing', 0)}/{top.get('pairs', 0)}")


def do_revise(p, meta, body, slug, film):
    """改稿：照使用者選的 A／B 先複製成 narration.md，再叫 Opus 照修改意見改。"""
    pick = meta.get("pick", "").strip().upper()
    src = Path(meta.get(f"script_{pick.lower()}", "")) if pick in ("A", "B") else None
    if not src or not src.is_file():
        set_status(p, meta, body, "failed", error="稿改沒選稿：先回「稿過 <slug> A」或「B」")
        alert(f"{slug} 稿改缺選稿：先選 A 或 B")
        return
    shutil.copyfile(src, film / "narration.md")
    (film / "BLOCKED.md").unlink(missing_ok=True)
    revise = "- 這是改稿：照核准檔內文「修改意見」改 films/%s/narration.md（已從使用者選的 %s 稿複製過來），其餘不動。\n" % (slug, pick)
    rc, tail = run_claude(SCRIPT_PROMPT.format(path=p, slug=slug, revise=revise))
    log(f"{p.name}: claude revise rc={rc} tail={tail[-300:]!r}")
    if (film / "narration.md").is_file() and not blocked(film):
        push_script(film)
        set_status(p, meta, body, "script_ready", script=str(film / "narration.md"))
    else:
        set_status(p, meta, body, "failed", error=blocked(film) or f"改稿沒成（claude rc={rc}）")


def do_build(p, meta, body):
    slug = check_slug(p, meta, body)
    if not slug:
        return
    film = ROOT / "films" / slug
    pick = meta.get("pick", "").strip().upper()
    src = Path(meta.get(f"script_{pick.lower()}", "")) if pick in ("A", "B") else None
    # 改稿過（script: 指 narration.md）就照改好的稿建，不能再用 pick 的原稿蓋回去
    if pick and not meta.get("script"):
        if not src or not src.is_file():
            set_status(p, meta, body, "failed", error=f"選稿 {pick} 的稿子檔不見了")
            return
        shutil.copyfile(src, film / "narration.md")  # 使用者選的那份才是要念的
    elif meta.get("script_a") and not (film / "narration.md").is_file():
        set_status(p, meta, body, "failed", error="沒選稿：先回「稿過 <slug> A」或「B」")
        alert(f"{slug} 沒選稿，建片略過")
        return
    if not (film / "narration.md").is_file():
        set_status(p, meta, body, "failed", error=f"films/{slug}/narration.md 不存在，先寫稿")
        return
    (film / "BLOCKED.md").unlink(missing_ok=True)
    rc, tail = run_claude(BUILD_PROMPT.format(path=p, slug=slug))
    log(f"{p.name}: claude build rc={rc} tail={tail[-300:]!r}")
    pc = subprocess.run([PY, "scripts/precheck.py", f"films/{slug}"], cwd=ROOT, capture_output=True, text=True)
    shorts = film / "dist" / f"{slug}-shorts.mp4"
    if pc.returncode != 0 or not shorts.is_file():
        why = blocked(film) or f"precheck rc={pc.returncode} {pc.stdout[-200:]}"
        set_status(p, meta, body, "failed", error=why)
        return
    up = subprocess.run([PY, "scripts/publish/yt_upload.py", f"films/{slug}"], cwd=ROOT, capture_output=True, text=True)
    m = re.search(r"youtube\.com/shorts/([\w-]{6,})", up.stdout)
    if up.returncode != 0 or not m:
        set_status(p, meta, body, "failed", error=f"YT 私人上傳失敗 rc={up.returncode} {(up.stdout + up.stderr)[-200:]}")
        return
    set_status(p, meta, body, "built", yt_private=f"https://youtube.com/shorts/{m.group(1)}", yt_id=m.group(1))


def do_publish(p, meta, body):
    slug = check_slug(p, meta, body)
    if not slug:
        return
    vid = meta.get("yt_id", "")
    if not vid:
        set_status(p, meta, body, "failed", error="publish_ok 但沒有 yt_id，先建片")
        return
    # Meta 先發：yt_upload public 會檢查 published.json 已有 ig、threads
    steps = [
        [PY, "scripts/publish/public_path.py", f"films/{slug}"],
        [PY, "scripts/publish/meta_publish.py", f"films/{slug}", "--yes"],
        [PY, "scripts/publish/yt_upload.py", "public", f"films/{slug}", vid],
    ]
    for cmd in steps:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        log(f"{p.name}: {' '.join(cmd[1:3])} rc={r.returncode} {r.stdout[-300:]!r}")
        if r.returncode != 0:
            set_status(p, meta, body, "failed", error=f"發布卡在 {cmd[1]} rc={r.returncode} {(r.stdout + r.stderr)[-200:]}")
            return
    set_status(p, meta, body, "published", published=f"films/{slug}/meta/published.json")


def topics(proposal):
    """proposal.md → [(題號, 題目, 爆款最高播放數, 鉤子)]；格式見 Marketer 每週選題。"""
    out = []
    for no, title, sec in re.findall(r"^## 題 ?(\d+)[：:]\s*(.+?)\n(.*?)(?=^## |\Z)", proposal, re.S | re.M):
        views = [int(v.replace(",", "")) for v in re.findall(r"([\d,]+) ?播放", sec)]
        hook = re.search(r"鉤子[：:]\s*「?(.+?)」?\s*$", sec, re.M)
        out.append((int(no), title.strip(), max(views, default=0), hook.group(1) if hook else ""))
    return out


def wan(n):
    return f"{n / 10000:.1f} 萬" if n >= 10000 else f"{n:,}"


def script_ready_block(meta, slug, title):
    """擂台稿：A／B 各列前 3 句＋評審分＋GitHub 連結；不貼全文（review 設計 2）。"""
    if not meta.get("script_a") and meta.get("script"):
        meta = dict(meta, script_a=meta["script"])  # 舊路徑留下的單稿 script_ready
    out = [f"📝 新稿子等你看：{title}"]
    for letter in ("A", "B"):
        raw = meta.get(f"script_{letter.lower()}", "").strip()
        if not raw:
            continue
        path = Path(raw)
        lines = [l.strip() for l in path.read_text(encoding="utf-8").splitlines()] if path.is_file() else []
        lines = [l for l in lines if l and not l.startswith("#")]
        head = "\n".join(f"「{l}」" for l in lines[:3]) or "（稿子檔不見了）"
        try:
            rel = path.relative_to(ROOT)
        except ValueError:
            rel = Path("films") / slug / "bakeoff" / path.name
        score = meta.get(f"score_{letter.lower()}", "").strip()
        out.append(f"{letter}：【{path.stem}】{f'評審 {score} 分' if score else ''}\n{head}\n全文：{GH_BLOB}/{rel}")
        probs = precheck.story_problems(precheck.parse_narration(path.read_text(encoding="utf-8"))) if path.is_file() else []
        if probs:  # 結構門不過的稿核了也建不了片（fix 12159）
            out.append(f"⚠️ {letter} 稿結構門沒過，核前先改：" + "；".join(probs))
    missing, _, pairs = meta.get("bakeoff_missing", "0/0").partition("/")
    try:
        if int(missing) > 0:
            out.append(f"⚠️ 缺票 {missing}／{pairs}，結果不完整（缺票算和局）")
    except ValueError:
        pass
    out.append(f"事實表：{GH_BLOB}/films/{slug}/FACTS.md")
    out.append(f"👉 OK 就回「稿過 {slug} A」或「稿過 {slug} B」，今晚做成片\n"
               f"👉 要改就回「稿改 {slug}：你的意見」")
    return "\n\n".join(out)


def digest():
    """08:30 待核准清單的營銷號段：白話全文，Emperor 原文轉貼。沒事就印空字串。"""
    todo = items()
    parts, busy = [], []
    for p, meta, body in todo:
        st, slug, title = meta["status"], meta.get("slug", "?"), meta.get("title", meta.get("slug", "?"))
        if st == "script_ready":
            parts.append(script_ready_block(meta, slug, title))
        elif st == "built":
            parts.append(f"🎬 片做好了：{title}\n私人連結（只有你看得到）：{meta.get('yt_private', '（沒有連結）')}\n\n"
                         f"👉 看完要公開就回「發 {slug}」，會發到 YouTube、IG、Threads，發了收不回")
        elif st == "failed":
            parts.append(f"⚠️ 卡住了：{title}\n原因：{meta.get('error', '（沒寫原因）')}")
        elif st in ("approved", "script_revise", "script_ok", "publish_ok"):
            busy.append(f"・{title}（{ {'approved': '今晚寫稿', 'script_revise': '今晚照你的意見改稿', 'script_ok': '今晚做成片', 'publish_ok': '發布中'}[st]}）")
    props = sorted(Path(APPROVED).parent.glob("marketer-topics-*/proposal.md"))
    if props:
        chosen = {m.get("topic_no") for _, m, _ in todo if m.get("proposal") == str(props[-1])}
        left = [t for t in topics(props[-1].read_text(encoding="utf-8")) if str(t[0]) not in chosen]
        if left:
            lines = [f"{no}. {title}（同題爆款 {wan(v)} 播放）" for no, title, v, _ in left]
            parts.append(f"💡 本週選題還有 {len(left)} 題可挑：\n" + "\n".join(lines) + "\n\n👉 想做哪題就回「做題 N」")
    if busy:
        parts.append("⏳ 進行中，不用你動：\n" + "\n".join(busy))
    return "\n\n────────\n\n".join(parts)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode not in ("night", "publish", "status", "digest", "alerts"):
        print(__doc__)
        sys.exit(2)
    APPROVED.mkdir(parents=True, exist_ok=True)
    if mode == "status":
        for p, meta, _ in items():
            print(f"{meta['status']:14} {p.name}  {meta.get('yt_private') or meta.get('error', '')}")
        return
    if mode == "digest":
        print(digest())
        return
    if mode == "alerts":
        alert(*actionable())  # 沒事不發；同日同行 alert() 去重
        return
    # 夜間與發布共用一把鎖：建置不併發、發布中不換片
    # now 立即開工不受 21:00 cutoff，但 WatchPaths 只觸發一次，所以阻塞等鎖（最多 NOW_WAIT 秒）
    nows = [it for it in items() if now_flag(it[1]) and it[1]["status"] in NOW_START]
    wait = NOW_WAIT if (mode == "publish" and nows) else 0
    lock = open(APPROVED / ".autoloop.lock", "a")  # 不截斷鎖檔，避免自觸發 WatchPaths
    if not acquire(lock, wait):
        if wait:
            for _, m, _ in nows:
                alert(f"{m.get('slug', '?')} 立即開工排到今晚 02:00")
            log(f"publish: 等鎖逾時 {wait}s，now 排到今晚 02:00")
        # 一般鎖競爭靜默，WatchPaths 重複觸發不洗版。
        return
    todo = items()
    for p, meta, body in todo:  # 已到終點卻還帶著 now 的陳舊旗標一律清掉（含 night）
        if "now" in meta and meta["status"] in NOW_END:
            meta.pop("now")
            save(p, meta, body)
            log(f"{p.name}: status={meta['status']}，移除 now")
    if mode == "publish":
        for it in todo:
            if it[1]["status"] == "publish_ok":
                do_publish(*it)
        run_now()
        return
    cut = float(os.environ.get("AUTOLOOP_CUTOFF") or cutoff())
    late = [it for it in todo if it[0].stat().st_mtime > cut
            and it[1]["status"] in ("approved", "script_revise", "script_ok")]
    for it in late:
        log(f"{it[0].name}: {CUTOFF_HOUR}:00 後才核准，排到下一晚")
    todo = [it for it in todo if it not in late]
    builds = [it for it in todo if it[1]["status"] == "script_ok"]
    if builds:
        do_build(*builds[0])
    scripts = [it for it in todo if it[1]["status"] in ("approved", "script_revise")]
    for it in scripts[:MAX_SCRIPTS]:
        do_script(*it)
    if not builds and not scripts:
        log("night: 沒有待辦")


if __name__ == "__main__":
    main()
