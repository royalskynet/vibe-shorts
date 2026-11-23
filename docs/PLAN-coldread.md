# PLAN：冷讀審核＋黑白對比（借 Eian「Claude+Codex+Seedance」流程）

來源：https://x.com/EianLu/status/2118317430665613741 （2026-11-05）。
Eian 流程多數不適用（我們全程式渲染，不用 AI 生圖／Seedance，無抽卡成本）。採用三點：
1. **冷讀審核**：另開一個不知道意圖的 agent，只給成品，先寫「我看懂的故事」再挑錯。主 agent 聊久了會腦補。
   我們現有 `qa/review_log.md` 是主 session 自評、`scripts/devils.sh` 只查事實，兩者都不是冷讀。
2. **稿子階段就冷讀**：錯擋在建置（8–10 分鐘渲染＋TTS）之前。
3. **黑白對比**：畫面轉灰階，主體跟背景分不開＝明暗對比不夠（米色插畫風風險高）。

不採用：38%／62% 構圖、每鏡換機位（版面固定、片型 calm）、四線程（已有閘門＋approve.py）。

## 任務

工作目錄 `REPO_ROOT`。先讀 `CLAUDE.md`、`scripts/devils.sh`、`scripts/precheck.py`（`check()`、`review_problems()`、`humanize_problems()` 的 sha 比對寫法）、`scripts/qa_sheet.sh`、`films/democracy-noise/qa/review_log.md`，照既有寫法。

### 1. `scripts/coldread.sh films/<片> script|film`

- 第二模型：`codex exec --skip-git-repo-check -s read-only`，stdin 關掉（`</dev/null` 或 `- < prompt檔`，見 devils.sh 註解）。codex 不可用 → exit 3 並印一行原因，不靜默成功。
- **只給成品，不給 TREATMENT.md、SOURCES.md、verdicts、review_log、對話紀錄**。
- `script` 模式：輸入只有 `narration.md` 全文。輸出 `audit/coldread-script.md`，首行 `narration_sha: <sha256 of narration.md>`。prompt 要求依序寫：
  1. 你看懂的內容（3 句內）
  2. 一句話主旨；說不出來就寫「說不出」
  3. 前 3 秒（第一段）會不會讓人停下來滑；理由
  4. 逐句追問：哪句看不懂、哪個轉折沒理由、哪個數字沒說是什麼
  5. 每條格式 `- [硬傷|小問題] 第N句：問題 → 建議改法`；沒把握寫「可能」
  6. 最後一行 `VERDICT: 通過` 或 `VERDICT: 不通過`
- `film` 模式：輸入 `qa/sheet.jpg`、`qa/cards.jpg`（用 `-i`）＋ `out/narration-report.json` 抽出的逐句字幕文字（只文字）。缺 sheet/cards → exit 2 提示先跑 `scripts/qa_sheet.sh`。輸出 `qa/coldread-film.md`，首行 `video_sha: <sha256 of films/<片>/<片>.mp4>`（跟 review_log.md 同算法）。prompt：先寫看懂的故事、再列看不懂處、逐卡查（字太小、字被擋、數字與字幕不一致、構圖重複、主體看不清），每條 `- [硬傷|小問題] 卡NN：…`；明寫「看不到動態與聲音，這兩項未查」；末行 `VERDICT:`。
- prompt 全用正向白名單寫法，放在 `scripts/coldread/` 兩個 txt 檔，腳本讀檔組合。

### 2. `scripts/gray_contrast.py films/<片>`（系統 `python3`）

- 讀每卡尾幀（`qa_sheet.sh` 產的單張幀；找不到就用 ffmpeg 從成片按 `out/` 時間表抽，照 qa_sheet.sh 的取幀法）。
- 轉灰階，算每張 RMS 對比（灰階標準差/255）與 5–95 百分位亮度差。輸出 `qa/gray.json`（每卡數值）＋ `qa/gray-sheet.jpg`（灰階拼圖，給人看）。
- **只回報不判死**：stdout 列最低 3 張，exit 0。不設門檻（新增閘門基準要使用者目視核准，CLAUDE.md 規則）。
- 只用已安裝套件（先查 `python3 -c "import PIL, numpy"`；沒有就用 ffmpeg `signalstats` 的 YAVG/YMIN/YMAX 等，不 pip install）。

### 3. precheck 接線（**只警告，不擋**）

- 新增兩項「冷讀（稿）」「冷讀（片）」：檔案缺、sha 不符、或 VERDICT 不通過 → 印 `WARN` 行，**不計入 FAIL、不改 exit code、不改通過分母**。在程式碼註解寫 `ponytail: 使用者核准後改硬門`。
- 不改任何既有門的邏輯與基準。

### 4. 文件

- `skills/vibe-shorts/SKILL.md`「做一支片」表（repo 內那份，若 `~/.claude/skills/vibe-shorts/SKILL.md` 是同一份 symlink 或同步副本則一起改）：在 3 反方稽核後加一列「3b 稿冷讀 `scripts/coldread.sh films/<片> script`」，5 目視自評後加「5b 片冷讀 `… film`＋`scripts/gray_contrast.py`」。改原表，不另開段。
- `references/gates.md` 加兩行說明 WARN 項。

### 5. 測試 `tests/test_coldread.py`

- 不打真模型：用假 `codex`（PATH 前置一個 stub 腳本）驗：(a) script 模式產物首行 sha 正確 (b) 輸入 prompt 不含 TREATMENT/SOURCES 內容（stub 把收到的 stdin 存檔，斷言不含 TREATMENT.md 裡的一個獨特字串）(c) codex 不存在時 exit 3。
- precheck 的 WARN 解析：對假的 coldread 檔（sha 錯／VERDICT 不通過／正常）各斷言一次，並斷言 precheck exit code 不因 WARN 改變。改錯邏輯測試要 fail。

### 6. 實跑一次

對 `films/democracy-noise`（已發布片，只新增 audit/qa 下的檔）跑 `script`、`film`、`gray_contrast.py` 各一次（真 codex）。把三份產出的 VERDICT 與硬傷條數寫進 `PLAN.md` 末段一行。commit（git identity 用 repo 既有設定），不 push 到公開 repo、不跑 publish-sync。

### 7. 引擎備援（使用者 11-05 追加，第一輪 deep 收件後補）

- 冷讀引擎順序 `COLDREAD_ENGINES`（預設 `codex opencode`），照 `~/.claude/skills/research/scripts/devils_advocate.sh` 的寫法：codex 失敗（未登入、額度用完、到期）自動換下一個。
- opencode 走 deep 同一條 OpenCode Go 訂閱：`opencode run -m opencode-go/deepseek-v4.1-flash`（`COLDREAD_OPENCODE_MODEL` 可覆寫），film 模式圖片用 `-f` 附檔。
- 產物第二行寫 `engine: <codex|opencode/模型>`；film 模式若引擎看不到圖，輸出要寫「畫面未查」。
- 兩個都失敗才 exit 3。測試加一條：假 codex exit 1 → 換假 opencode 成功。

## 驗收

```bash
cd REPO_ROOT && python3 tests/test_coldread.py
cd REPO_ROOT && for t in tests/test_*.py; do python3 "$t" >/dev/null || exit 1; done
cd REPO_ROOT && head -1 films/democracy-noise/audit/coldread-script.md | grep -q "^narration_sha: $(shasum -a 256 films/democracy-noise/narration.md | cut -d' ' -f1)$"
cd REPO_ROOT && grep -q '^VERDICT: ' films/democracy-noise/audit/coldread-script.md
cd REPO_ROOT && head -1 films/democracy-noise/qa/coldread-film.md | grep -q '^video_sha: '
cd REPO_ROOT && grep -q '^VERDICT: ' films/democracy-noise/qa/coldread-film.md
cd REPO_ROOT && python3 scripts/gray_contrast.py films/democracy-noise && test -s films/democracy-noise/qa/gray.json
cd REPO_ROOT && python3 scripts/precheck.py films/democracy-noise > /tmp/pc-cold.txt; grep -q '冷讀' /tmp/pc-cold.txt
cd REPO_ROOT && grep -q 'coldread.sh' skills/vibe-shorts/SKILL.md
cd REPO_ROOT && git diff --quiet ffe5f58 -- scripts/rhythm_check.py scripts/publish
```

預期：每行 exit 0；precheck 通過數與改前相同（46/47 那一項仍只差公開路徑）。

## 不動

- `scripts/rhythm_check.py`、既有 precheck 門的判定與基準、`films/*/index.html`、`narration.md`、`meta/published.json`、`scripts/publish/**`。
- 不發布、不上傳 YT、不刪任何檔。

## 禁止

1. `launchctl bootout/bootstrap/kickstart` 必帶完整 service target `gui/$(id -u)/<label>`；裸 domain 與 `launchctl reboot` 禁止；載入回 141/125 立即停手回報。本任務不需要動 launchd。
2. 無頭機：禁止回報「請使用者手動貼 token／授權／執行指令」；codex 不可用＝停手回報阻斷點。
3. 禁 `pip install`／`brew install`；禁 `set -x`、禁印憑證值。
4. 不建置任何片（`build.sh` 不跑）；precheck 不得把新增項計入 FAIL。
