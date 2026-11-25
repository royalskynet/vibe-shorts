# WO wandavision-20v：第一集建片的獨立驗收（只看不改）

工作目錄 `/Users/51mini/dev/vibe-shorts-pipeline`，片目錄 `films/wv-primer-1/`。另一個執行人照 `docs/plans/wo-wandavision-20-ep1-build.md` 建好片。稿子使用者已核過，不審稿意，只審片。

## 要查

1. 跑 `bash /tmp/wv-accept-20.sh`，貼原始輸出。
2. `narration.md` 與使用者核過版一致（approved.md 的 sha 對得上，驗收腳本已查）。
3. 看 `qa/sheet.jpg`、`qa/cards.jpg`（必要時 `qa/cards-*.jpg`）：
   - 每張畫面對得上那句在講什麼。
   - 沒畫出《汪達幻視》劇裡的東西：黑白電視、情境喜劇畫面、小鎮裡的人、紅色光罩裡的人物、雙胞胎嬰兒。
   - 汪達的小人是長髮。
   - 段名字卡是「史塔克工業」，沒有「一顆砲彈」。
   - 沒有字壓字、出框、空白畫面。
4. 抽 `out/voice/lines.json` 與稿子比：每一句都有配音，沒有舊稿的句子。

## 產出

只寫 `films/wv-primer-1/qa/verify-20.md`：第一行只能是 `VERDICT: PASS` 或 `VERDICT: FAIL`；任一項不過就 FAIL，逐條列位置、問題、怎麼改。

## 禁區

除了 `qa/verify-20.md` 不改任何檔；不跑 build、voice、approve、yt_upload；不 commit。
