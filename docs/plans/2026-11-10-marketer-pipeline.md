# 讓 OMB Marketer 跑完整 vibe-shorts 流水線

使用者 2026-11-10 定：四項全做（skill 補新工具、修紅燈測試、Marketer skill 同步、Inspector 試跑），執行派od。

## 現況（11-10 查過）

| 項目 | 事實 | 怎麼查的 |
|---|---|---|
| Marketer | bot `e4207ff3`，模型 `opencode-go/deepseek-v4.1-flash`；agent 目錄判定為 `~/OpenBot/Agents/agent-fb607a57-…`（唯一同時有 vibe-shorts、viral-scout、marketer-approval 的目錄） | `m4_list_bots`、`ls Agents/*/.claude/skills` |
| Inspector | bot `19f2273a`，同模型 | `m4_list_bots` |
| skill 副本 | Marketer 的 vibe-shorts、viral-scout 是 10-28 複製檔（`.claude/skills` 與 `.agents/skills` 各一份），與 repo `diff` 不同 | `diff -q` |
| 新工具 | repo `skills/vibe-shorts/SKILL.md` 沒提 reverse、broll（grep 0 筆） | `grep -c` |
| 紅燈測試 | `test_seek_check.py`、`test_textless_check.py`、`test_illust.mjs` 同一根因：`browserType.launch: Executable doesn't exist at …/chromium_headless_shell-1243/…`。lemo-opuscar 的 playwright-core 1.63.0 要 build 1243，快取只有 1254 | 跑測試看 stderr、`ls ~/Library/Caches/ms-playwright` |
| skill 規則 | PERSONA-PRINCIPLES 第 10 條：正本放 `Shared/skills/<名>/`，同一份**複製**到 `Agents/<ID>/.claude/skills/<名>/`；第 11 條：先成功跑過一次才存；改 skill 要寫 CHG 條目交蛋先生 | Read `~/OpenBot/Shared/fleet/PERSONA-PRINCIPLES.md` |

## 根治

### A. SKILL.md 補新工具（派od，工單 `docs/workorders/20261110-skill-tools.md`）
- 「做一支片」表加兩列：拆對標片用 `scripts/reverse.py`；畫面缺實景時用 `scripts/broll.py search/fetch`＋`assets/broll/broll.mjs` 的 `drawBroll`，細節指向 `docs/BROLL.md`。
- 修 `docs/BROLL.md` 第 2 步漏寫的 `--license`、`--credit`（CC BY 要署名）。

### B. skill 同步腳本（同一張工單）
- 新增 `scripts/skill_sync.sh --root <OpenBot 根> --agent <agent 目錄名>…`：把 `skills/vibe-shorts`、`skills/viral-scout` 以 `rsync -a --delete` 複製到 `<根>/Shared/skills/<名>/`，再到每個 agent 的 `.claude/skills/<名>/` 與 `.agents/skills/<名>/`。
- agent 目錄不存在就 exit 2，不建新目錄。`--dry` 只印將做的事。
- 照第 10 條用複製、不用 symlink。

### C. 紅燈測試（主 session，不派）
- `cd ~/dev/lemo-opuscar && npx playwright-core install chromium-headless-shell`，補 build 1243。免費下載，不改程式碼。
- 為什麼不升 playwright-core：渲染器跟著變，成片可能不一樣，要重驗所有片。

### D. 同步與試跑（主 session，od 沙箱寫不到 `~/OpenBot`）
1. 跑 `scripts/skill_sync.sh --root ~/OpenBot --agent agent-fb607a57-b2ea-4d90-a379-f52a9f08073e`，`diff -r` 驗。
2. 用 `m4_send_bot_message` 交辦 Inspector：在 repo 跑 `tests/` 全套＋用 `scripts/reverse.py tests/fixtures/reverse-2shot.mp4` 與 `scripts/broll.py search taipei` 各跑一次，回報 exit code。成功才算第 11 條「跑過一次」。
3. 試跑過了才寫 CHG 條目到 `~/OpenBot/Shared/fleet/WORKFLOW-CHANGES.md`：Marketer 職責從選題擴到建片，逐條寫符合 PERSONA-PRINCIPLES 第幾條，交蛋先生。

## 預防加固
- `skill_sync.sh` 有驗收測試（rsync 刪舊檔、缺 agent 目錄報錯），以後 repo 改 skill 照跑一次就同步，不再靠手動複製。
- 紅燈測試修好後全套綠，往後回歸能分辨是不是自己改壞。

## 不做／待定
- Marketer 人設（OMB 內）怎麼改、routine 加不加建片：要等蛋先生裁 CHG，這份計畫不動人設。
- 發布仍要使用者點頭（SKILL.md 硬規則 3），Marketer 擴權不含發布。
- `skills-lock.json` 記了檔案 sha256，複製新檔後 OMB 會不會報錯：D-2 試跑時看，報錯就停下回報。

## 驗收（全部 exit 0 才算完）
```bash
cd REPO_ROOT
wo-verify docs/workorders/20261110-skill-tools.md
for t in tests/test_*.py; do python3 "$t" >/dev/null 2>&1 || { echo "FAIL $t"; exit 1; }; done
for t in tests/test_*.mjs; do node "$t" >/dev/null 2>&1 || { echo "FAIL $t"; exit 1; }; done
A=~/OpenBot/Agents/agent-fb607a57-b2ea-4d90-a379-f52a9f08073e
diff -r skills/vibe-shorts $A/.claude/skills/vibe-shorts && diff -r skills/viral-scout $A/.agents/skills/viral-scout
grep -q 'reverse.py' $A/.claude/skills/vibe-shorts/SKILL.md
```
