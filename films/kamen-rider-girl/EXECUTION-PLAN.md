# 執行計畫 —《邪神給的腰帶》

目標：做一支可發布的網漫型短片，8–10 分鐘為長線目標，PoC 先做單集。

現況（2026-10-18 核實）：
- `TREATMENT.md` 已落檔，`viral_problems()` 回 `[]`（門檻 10 萬，實際 62.3 萬）→ 爆款閘門**已過**
- `~/dev/lemo-opuscar/styles/kamen-girl/demo/index.html` 已建，但引用的 `main.js` **不存在** → 渲染必失敗
- 本機 lemo 依賴齊備：`.venv` 有 numpy/scipy/soundfile/pillow，`chromium-1228` 已裝
- 現有 9 段流水線可重用：`voice.py`、`mix.py`、`precheck.py`、`deliver.sh`

---

## 步驟 0：補 `main.js`，產出角色 model sheet（**當前卡點**）

**做什麼**：寫 `styles/kamen-girl/demo/main.js`，依 `cel-anime-80s/STYLE.md` §2 規格畫林昭的 model sheet——turnaround（正／3-4／側／背）、3–4 表情、2–3 關鍵 pose、palette 色票。

**驗收指令**：
```bash
LIB=~/dev/lemo-opuscar
cd $LIB && node core/render/still.mjs styles/kamen-girl/demo 0 --out /tmp/msheet
python3 core/render/sheet.py /tmp/msheet/sheet.jpg /tmp/msheet/*.jpg --cols 4
```
**停止條件**：`/tmp/msheet/` 產出 ≥8 張 jpg，`sheet.jpg` 可開啟且角色無破圖。

**風險**：這是全案最大不確定點。`_template` 沒有 `index.html` 範本，`brick-toy` 是 3D three.js 路線；本片是 2D canvas 路線，需參考 `pictogram-motion` 或 `midcentury-toon` 的 2D 寫法。

---

## 步驟 1：定「不公規模數字」的量法（設計缺口）

**做什麼**：TREATMENT 已寫「腰帶顯示的不是能量條，是不公的規模」，但**未定怎麼量**。不定清楚會導致每話口徑不一。需產出一個可重複計算的規則（例：受影響人數 × 持續時間 × 權力落差），寫進 TREATMENT。

**驗收**：規則能對第一話的具體情境算出一個數字，且口徑可套用到後續話數。

**為何排在這**：它是每話都要用的核心機制，比寫劇本更前置。

---

## 步驟 2：寫第一話 `narration.md`

**做什麼**：依 TREATMENT 骨架寫完整旁白稿。

**驗收**：
```bash
python3 scripts/precheck.py films/kamen-rider-girl
```
需過「旁白稿結構」門與「爆款證據」門。

**注意**：`precheck.py` 的 29 道門目前是**單支短片版**（時長、節奏基準、字幕格）。8–10 分鐘會撞時長與節奏門，需先確認哪些門不適用，或走 `shot_grid_exempt` 類豁免機制。

---

## 步驟 3：建 `build.sh` 與畫面

**做什麼**：照 `films/scam-map/` 結構建 `build.sh`、`timeline.js`、各卡畫面。

**驗收**：`films/kamen-rider-girl/build.sh` 產出 mp4。

**注意**：`CLAUDE.md` 明定「建置不併發」——`films/*/build.sh` 一次只跑一支。

---

## 步驟 4：配音與混音

**做什麼**：用 `voice.py` 配 Qwen3-TTS（`VOICE.md` 定案的模板 D），接進 `mix.py`。

**現況**：PLAN.md 記載「試產跑通；接進 mix.py **待做**」——這是**既有未完成項**，不是本片新增。

**驗收**：`verify_tts.py` 通過；Whisper 核稿無吃字。

---

## 步驟 5：閘門與交付

```bash
scripts/qa_sheet.sh films/kamen-rider-girl
python3 scripts/precheck.py films/kamen-rider-girl
scripts/deliver.sh films/kamen-rider-girl/kamen-rider-girl.mp4
```
**注意**：`deliver.sh` 需先跑 `video-scrub` 清 metadata（PLAN.md 記載「成片還帶著編碼器簽名」為既有缺口）。

---

## 步驟 6：發布

**需使用者點頭**（`CLAUDE.md`：對外發布不可收回）。

---

## 已作廢／不採用

- **mediago-drama**：107M、2026-07-30 最後 commit；`docs/model-platform-plan.md` 顯示是模型聚合器，會把零成本鏈路換成計費鏈路。**不裝**
- **ArcReel / Toonflow**：借鏡其角色資產庫概念即可，不裝（本機 AI 影片模型已因角色一致性不可控被淘汰，見 wheel 卡 2026-10-14）
- **本機 AI 影片生成（LTX-Video 等）**：角色的程式繪製一致性是數學保證，生成模型是機率性

---

## 未解風險

1. **步驟 0 是全案瓶頸**：`main.js` 從未寫過，2D 角色 rig 能否達到 cel-anime 規格（杏仁眼、angel ring 高光、硬邊陰影）未經驗證
2. **8–10 分鐘 vs precheck**：29 道門為短片設計，長片時長與節奏門可能全部誤判
3. **150 話連載無狀態管理**：現有 pipeline 是「一題一支」，無跨集延續機制
4. **「不公規模數字」未定**：核心視覺機制無量法
