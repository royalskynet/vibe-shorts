# 交接：營銷號寫稿（10-29 更新）

## 現況

- gamble-odds 是測試稿，只確認寫稿流程，狀態 `dropped`，不建片。star-income 也是 `dropped`：同題只有 8.8 萬播放，太冷門。
- 新的選題清單是 `~/OpenBot/Shared/marketer-topics-2026-10-29/proposal.md`，題目是台北市民痛點對照國際共鳴：
  1. 行人地獄
  2. 鼠患
  3. 垃圾桶
- 爆款證據記在 `refs/VIRAL-LEDGER.md`「台北市民痛點 × 國際共鳴」。國際同題片破百萬的都是長片，同題 Shorts 沒有一支破 100 萬。
- 10-29 下午手動觸發寫題 1 的稿，核准檔是 `~/OpenBot/Shared/approved/2026-10-29-pedestrian-hell.md`，片目錄是 `films/pedestrian-hell`。執行紀錄寫在 `/tmp/autoloop-now.out` 和 `logs/autoloop.log`。
- 10-29 定的規則：稿子一定要過 humanize。precheck 的「口語化（humanize）」門會核對 `audit/humanize.md` 的 `narration_sha:` 戳記，稿子改過就要重過（`docs/WRITING.md` §7 第 10 條）。

## 接手步驟

1. 確認寫完：`pgrep -f "autoloop.py night"` 沒有輸出就是寫完了。接著跑 `grep '^status:\|^error:' ~/OpenBot/Shared/approved/2026-10-29-pedestrian-hell.md`。
2. 驗稿：
   - 單人旁白，`rhythm-profile` 是 `card`。
   - 跑 `.venv/bin/python scripts/precheck.py films/pedestrian-hell`，下面四個門要 OK：爆款證據、禁止清單、旁白稿結構、口語化（humanize）。
   - 自己念一遍，確認是台灣口語。
   - 「霍博肯零死亡」這類數字要對得上 `meta/facts.md` 和 `SOURCES.md` 的來源。
   - 稿子不比較政治人物。
3. 確認 push 了：`git log -1 origin/main -- films/pedestrian-hell`。
4. 跑 `/usr/bin/python3 scripts/autoloop.py digest`，原文貼給使用者，等他回「稿過」或「稿改 pedestrian-hell」。
5. 使用者回「稿過」，就把狀態改成 `script_ok`，當晚 02:00 建片；他說「現在」就照上面的方式立即觸發。

## 待辦（使用者已同意方向，還沒做）

- Marketer 選題改成同題要有 ≥10 萬（最好 100 萬級）的爆款證據。Marketer 沒開 Local scripts，要請 Emperor 代改。
- 08:30 的 digest 不列同題爆款低於 10 萬的題（改 `autoloop.py digest`，加測試）。
- 反方稽核（`scripts/devils.sh`）可以排進夜間寫稿流程。
