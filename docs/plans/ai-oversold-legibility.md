# ai-oversold 內頁小字可讀性（L2）

輪子卡：設定（taipei-silence 模板常數調整，無新依賴；借鏡 WCAG 1.4.3 對比 4.5:1）。已登記 `~/.wheel/registry.tsv` 2026-11-18。

## 證據（已量）
- 系列標籤 `plain(SERIES…, 34, DIM)` 與來源行 `plain('來源｜…', 28, DIM, w:500)`，`DIM=#8C7B6B` 疊在奶油底 `#f5efe6`，對比 3.56:1，低於 4.5:1（`films/ai-oversold/index.html:29,322,414`）。
- 同一個 `DIM=#8C7B6B` 出現在 6 支以上成片（ai-oversold、dunning-kruger、mib-lotr、nvidia-founder-return、democracy-noise、free-speech-line）。
- 冷讀報告 5/7 支片重複指出小字偏淡。
- 候選 `#6F5F50` 對比 5.36:1；`#74644F` 4.99:1。選 `#6F5F50`，仍落在色票的棕色系。

## 範圍
只動 ai-oversold（尚未出片）。已出片不重 render、不重發。其他片的 DIM 不動；要不要回補由使用者看過 ai-oversold 審片版後決定。

## 一、根治
1. `films/ai-oversold/index.html:29` `DIM` 改 `#6F5F50`。
2. 同檔 `:414` 來源行字級 28 改 32、字重 500 改 600（仍小於字幕，保持層級）。
3. 同檔 `:322` 系列標籤維持 34，不動。

## 二、預防加固
新增 `tests/test_dim_contrast.py`：讀 `films/ai-oversold/index.html` 的 `DIM` 色與來源行字級，對比 < 4.5 或字級 < 32 就失敗。改回舊值它必須變紅。不新增 gate、不動 precheck 基準（基準變動要使用者看畫面核准）。

## 驗收
`python3 tests/test_dim_contrast.py`：改前 exit 1，改後 exit 0。
`cd films/ai-oversold && bash build.sh` 的 textless_check 與 precheck 不得新增失敗。

## 未驗證
- 變深之後畫面是否更好看：要使用者看審片版才算數，Codex 冷讀只能證明沒回歸。
- 之前冷讀看到的 f4/f5 標籤偏左、數字重複、f5 留白過大：這輪沒有重量到，不進計畫。
- Codex 目前是否仍可用（PLAN 11-05 提過到期）：`codex --version` 回 0.163.0，帳號額度沒驗。
