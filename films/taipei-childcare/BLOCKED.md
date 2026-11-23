# BLOCKED — taipei-childcare 卡在旁白核稿（2026-11-01 夜間批次）

## 卡在哪

`build.sh` 第一步 `scripts/voice.py` exit 1。第 25 句連續 6 次重念（兩輪 build × 3 次），Whisper 都聽不到 0.90：

| 次 | 相似度 | Whisper 聽到 |
|---|---|---|
| 1 | 0.73 | 是否估计每周要41万小时零拖 |
| 2 | 0.80 | 是否估计每周要41万小时临拖 |
| 3–6 | 0.73 | 是否估计每周要41万小时零拖 |

稿：「市府估計，每週要四十一萬小時臨托，」（narration.md 轉折段，使用者核過，不能改）。
6 次都把開頭「市府」聽成「是否」，這是固定的錯，再重念大概也一樣；已經到盲試 2 次上限，所以停下來。

最好的一次在 `out/voice/25.wav`（0.80 那次），`timeline.js`／`out/voice/lines.json` 是用這次排的（片長 96.9 秒）。

## 要你決定（三選一）

1. **聽 `out/voice/25.wav`**：如果「市府」「臨托」聽起來是對的，就是 Whisper 聽錯。核准方式：在 `scripts/verify_tts.py` 的 `HOMOPHONE` 加 `"拖": "托"`（同音 tuō；第 1、22 句也被聽成「公拖」「临拖」），第 25 句仍會因為「是否」卡在約 0.87，要再決定是否讓這句手動放行。這是放寬閘門，照規則要你點頭。
2. **改稿**（要你核）：例如「市府估計」→「台北市政府估計」，句首多兩個字，「市府」不會單獨出現在開頭被聽成「是否」。
3. 換音色或調 `pace.json`：不建議，核准檔說 cast.json／pace.json 是溫和版定案，不要改回。

選好後跑 `cd films/taipei-childcare && bash build.sh`（只有第 25 句會重念，其他句沿用），然後 qa_sheet → precheck → deliver。

## 這輪已完成（不用重做）

- `index.html`：照定稿 31 句重做，一句一卡；換卡原地交叉淡化 0.6 秒、沒有滑入、沒有章名全屏卡、沒有懶人包卡、沒有換卡音效（照 pedestrian-hell 第三版）。兩種主張用同一個標籤樣式，「代價是人」兩張是同構圖。
- `mix.py`：從 pedestrian-hell 複製（溫和大調配樂，沒有音效）。`cast.json`／`pace.json`／`rhythm-profile` 照核准檔，沒有動。
- `meta/facts.md`：照定稿數字重寫（起薪 38,011、1:3–1:4、日本 2025 年 2,254、155 人、41 萬／13 萬小時）；precheck「數字都有來源」OK。
- `TREATMENT.md`：分鏡表照定稿 31 句重寫；precheck「寫稿規則」OK。
- 三份說明文字＋`title-shorts.txt`＋`tags.txt`；說明文字相關 precheck 門全部 OK。
- 反方稽核：`audit/verdicts.md` sha 對得上現稿，precheck OK（沒動 SOURCES.md）。
- 渲染前檢查用真的時間軸跑過：字幕閱讀時長全 OK（把 8 個太短卡的副標移進畫面裡）、尋幀一致 OK、藏字檢查沒有 FAIL（8 張偏薄 WARN）。改完 index.html 之後報告已經過期，下次 build.sh 會重跑。
- 修了核稿正規化的 bug（`scripts/verify_tts.py`）：萬位以上的數字沒轉中文、「兩千／兩百」跟「二千」沒對齊。修好後第 12、13 句第一次就 1.00。`tests/test_verify_tts_norm.py` 加了 5 條斷言，全部測試通過。

## 還沒做

build 的渲染、合軌、節奏閘門 → `qa_sheet.sh`＋`qa/review_log.md` → precheck → `deliver.sh`。
precheck「公開路徑是隨機 token」要等發布前跑 `scripts/publish/public_path.py`（發布步驟，這輪沒碰）。

precheck 現在 22/35；沒過的 13 項都等成片出來才能跑。
