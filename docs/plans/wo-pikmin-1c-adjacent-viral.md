## 任務

工作目錄：`/Users/you/dev/vibe-shorts-pipeline`。只補查「同大題」爆款證據並更新帳本與 `TREATMENT.md` 一行，不寫稿、不 render、不 git commit。

背景：Pikmin Bloom 把台灣寫成「中國台灣」的同題 Shorts 查到 0 筆 ≥10 萬，上一輪連同大題（品牌／遊戲把台灣寫成中國引發抵制）也 0 筆符合「≤180 秒且 ≥10 萬」。使用者已核准「同大題爆款當證據」的例外，所以要放寬範圍再查，仍然不編數字。

用 `yt-dlp --flat-playlist -J "ytsearch40:<q>"`（見 `skills/viral-scout/SKILL.md` 第 1 節），分三輪，每輪都記關鍵字與命中筆數：
1. 同大題放寬到 `duration ≤ 180`、`view_count ≥ 100000`，關鍵字至少含：品牌 把台灣 列為中國 道歉、App 台灣 標示 中國 台灣人 抗議、台灣玩家 抵制 遊戲公司、Taiwan listed as China apology brand、Taiwan labeled China app backlash、台灣人 刪 App 抗議。
2. 第 1 輪仍 0 筆，才放寬到 `duration ≤ 600`（標註「非 Shorts」）。
3. 還是 0 筆，把「無」如實寫進帳本，**不要改 `TREATMENT.md`**，回報後停手。

有結果時：
- append 到 `refs/VIRAL-LEDGER.md` 末尾（既有內容不改），新段標題 `## 皮克敏同大題補查（2026-11-19，使用者核准放寬）`，每筆一行：平台｜播放｜標題（秒數）｜連結，末行「判定：」。
- 把最多 3 筆寫進 `films/pikmin-bloom/TREATMENT.md` 的「爆款證據：」那一行（整行取代），格式：`爆款證據：同題 0 筆 ≥10 萬；同大題（使用者 2026-11-19 核准的例外）：YouTube｜<播放>｜<標題>（<秒>）｜<連結> ；…`。`TREATMENT.md` 其他內容不動。
- 播放數必須是 yt-dlp 回傳的 `view_count`，不可四捨五入成更大的數。

## 驗收

```bash
cd /Users/you/dev/vibe-shorts-pipeline
grep -q '皮克敏同大題補查' refs/VIRAL-LEDGER.md
line=$(grep -E '^爆款證據：' films/pikmin-bloom/TREATMENT.md)
echo "$line" | grep -q '同題 0 筆'
echo "$line" | grep -q '使用者 2026-11-19 核准'
ids=$(echo "$line" | grep -oE '(watch\?v=|youtu\.be/)[A-Za-z0-9_-]{11}' | sed -E 's/.*(=|\/)//')
test -n "$ids"
for id in $ids; do
  v=$(yt-dlp --skip-download --print view_count "https://www.youtube.com/watch?v=$id" 2>/dev/null | head -1)
  test -n "$v"
  test "$v" -ge 100000
done
```
預期整段 exit 0；開工前 `TREATMENT.md` 的爆款證據行是「同題 0 筆（查法…）」，沒有「使用者 2026-11-19 核准」，第三行就會失敗。

## 不動
`films/` 其他資料夾與 `films/pikmin-bloom/` 除 `TREATMENT.md` 爆款證據行以外的檔案、`scripts/`、`tests/`、`PLAN.md`；`refs/VIRAL-LEDGER.md` 只在末尾 append。

## 禁止
1. 不 render、不執行 `build.sh`、不 git commit。
2. 無頭機：禁止回報「請使用者手動貼 token／授權／執行指令」；憑證讀不到＝停手回報阻斷點。
3. 查不到寫「無」，不准憑記憶補片名、播放數或連結。
