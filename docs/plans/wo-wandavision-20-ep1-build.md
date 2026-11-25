# WO wandavision-20：第一集照 WO-19 定稿建片

工作目錄 `/Users/51mini/dev/vibe-shorts-pipeline`，片目錄 `films/wv-primer-1/`。使用者 11-25 已核過 `narration.md` 全文（WO-19 稿），**稿子一字不改**。

## 步驟

1. `scripts/devils.sh` 跑反方稽核；你自己寫 `audit/verdicts.md`（格式照現有檔），劇透或事實錯的爭點判 PRO_WINS 也不改稿，只記錄理由。跑 `.venv/bin/python scripts/approve.py wv-primer-1 "使用者 11-25 核過全文，私人片，WO-20"`。
2. 改 `index.html` 鏡頭配稿：
   - 段名已改（`一顆砲彈`→`史塔克工業`），所有寫死舊段名的地方跟著改。
   - 刪掉的句子（沒爆砲彈、本尊降臨、悲傷是愛等）對應鏡頭移除；新句子（意識結構、鋼鐵裝甲、眼睜睜看著商標、薩諾斯大軍、幻視倒下時薩諾斯催動時間寶石、收尾的小鎮與神秘力量）要有對應鏡頭。
   - 收尾的小鎮畫面：一座從外面看的普通小鎮，被一層發光的霧或光罩籠罩，不畫裡面的人、不畫電視、不畫黑白畫面。
   - 汪達的小人是長髮（確認 WO-17 的長髮有畫出來）。
   - 鏡頭規格：≥30 個、同一畫面最長 ≤15 秒。
3. 照 `build.sh` 建片（配音、渲染）。建置前若有別支片在建置（`pgrep -fl 'build.sh|render'` 有別片目錄），等它結束。ram_guard 中斷就等記憶體回綠再跑。
4. `cp wv-primer-1.mp4 dist/wv-primer-1-shorts.mp4`；重產 `qa/sheet.jpg`、`qa/cards.jpg`。
5. 若 `qa/verify-20.md` 存在且首行 `VERDICT: FAIL`，照它逐條修（稿子問題不改稿，寫進 `qa/verify-20-reply.md` 交主 session），修完刪該檔。

## 禁區

不改 `narration.md`、`scripts/`、`tests/`、`refs/`、其他片目錄、`/tmp/wv-*`；不跑 yt_upload；不 commit。

## 驗收

`bash /tmp/wv-accept-20.sh` 要印 `ACCEPT-20 OK`。
