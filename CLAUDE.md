# CLAUDE.md — vibe-shorts

專案導覽見 README.md；進度正本是 PLAN.md。本檔只放 agent 在這個 repo 做事會做錯的規則。

## 接手順序

1. 讀 PLAN.md「流程」表與編號步驟，找到目前的第 N 步。
2. 讀 DECISIONS.md 相關段落，已裁決的不重議。
3. 要資訊（選題、鉤子、節奏、畫面）→ 用 skill `viral-scout`，先查 `refs/VIRAL-LEDGER.md`、`refs/BENCHMARKS.md`、`refs/BREAKDOWN.md`，命中就引用，不從頭抓。

## 規則

- **爆款第一**：每個決定附爆款證據（平台、播放數、連結）；抓不到數字寫「無數字」。工具開源輪子優先，不寫爬蟲。每支片的 `TREATMENT.md` 要有「爆款證據：」行，`precheck.py` 機械檢查。
- **經驗入帳**：每次查完爆款，證據 append 到 `refs/VIRAL-LEDGER.md`；新驗證成功或失敗的命令更新到 `skills/viral-scout/SKILL.md` 第 1 節。
- **對外發布、刪除平台貼文要人點頭**：發布不可收回；IG 貼文 API 刪不掉，要走網頁（見 `docs/HANDOFF-threads-delete.md`）。
- **建置不併發**：`films/*/build.sh` 一次只跑一支，兩個建置同時寫 `out/` 會壞片。
- **Python 環境**：配音、拆解用 `.venv/bin/python`；`scripts/publish/cdp.py` 用系統 `python3`（`.venv` 沒裝 playwright）。
- **源頭先對，閘門只驗收**（使用者 2026-10-20 定）：問題修在產生它的地方（寫稿、index.html、build／deliver 腳本），不靠閘門擋下再退回重做。閘門的假設不符片型就改閘門，不扭曲片子去過門。第 0 幀是預覽圖，大標要在第 0 幀就完整顯示（`docs/WRITING.md` §6.3）。
- **閘門基準改動要使用者目視核准**（`rhythm_check.py` 的 map 基準就是這樣放寬的）。
- **衛星底圖授權**：EOX `s2cloudless` 只有 2016 版可商用（CC BY 4.0），出處寫進片子的 `SOURCES.md` 與說明欄。
- **稿子禁止防衛性中立語言**（使用者 2026-10-14 定，最高嚴重度）：旁白、字幕、說明欄不准出現「問法不同」「不能直接比較」「不代表全部」「不能說成同一個原因」這類沒資訊的自我辯護句。範圍限定寫進事實本身（年份、地點、對象）。稿子只呈現數據傾向，不替論點背書，結論交給聽眾。細則 `docs/WRITING.md` §4。
- **新片格式是單人旁白科普**（使用者 2026-10-29 定，取代 10-16 起的深夜對談：「對話根本沒有邏輯」）：m3 男聲、一支只講一個機制，對標 IG @boundless__explorer 與我們的 france／scam-map。寫法照 `docs/WRITING.md` §7 與 `docs/寫稿原則.md`（無邊探索口吻，使用者 2026-11-01 定：一句講完一個因果、≤35 字、空話換具體事實或動作；precheck「旁白稿結構」門擋單行超長與一行兩個句號）；新片以 `films/taipei-silence` 為範本建目錄（使用者 11-04 定：米色插畫風、插畫庫 `assets/illust/`、只封面有大標；elected-dictator 是 11-01 深色舊範本，france 是 10-20 舊引擎）。對談格式（§5）只在使用者點名時用。
- **稿子一定要過 humanize**（使用者 2026-10-29 定）：每支稿寫完、每次改稿後都照 genie-humanizer 改成台灣口語，戳記寫 `audit/humanize.md`，precheck「口語化」門機械核對（`docs/WRITING.md` §7 第 10 條）。
- **對談片的角色**（只在使用者點名對談時適用）：女主＋Clawd Bot（BRAND.md「吉祥物與視覺風格」）；角色進片用 `scripts/mascot_install.sh` 複製進片目錄，動畫一律走 `clawd-bot-shot.mjs` 的 `poseAt(t)`，不要用上游 `clawd-bot-rig.js`（累積狀態會讓 `seek_check.mjs` 不過）。用法與理由 `docs/MASCOT.md`。
- **稿子從爆款改編，台詞不能照抄**（使用者 2026-10-18 定，10-29 起適用於旁白稿：從爆款抽鉤子與機制重寫，數字重新查證）。對談稿的做法：從 `refs/dialogue-corpus/` 給爆款原稿＋直譯當參考，只借結構（節拍、三段加碼、回扣）；成片台詞要重寫，precheck「台詞非照抄」門比對直譯句（相似度 >0.6 擋，圈內梗白名單）。改編稿要使用者核過才建置。原創稿 nerf、clawd-notes 與翻譯試作 not-human 都被否決並刪除；直譯版 sixty-one 因抄襲不發。
- 參考片（別人的內容）不進版控，只留我們做的分析；規則見 `.gitignore`。

## 改完要跑

```bash
for t in tests/test_*.py; do python3 "$t" || echo "FAIL $t"; done
for t in tests/test_*.mjs; do node "$t" || echo "FAIL $t"; done
```
改到閘門或發布腳本，對應的 `tests/test_*.py` 要能在邏輯改錯時失敗。
