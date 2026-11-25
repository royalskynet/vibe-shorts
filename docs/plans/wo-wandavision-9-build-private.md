# WO wandavision-9：16:9 長片＋劇透倒數＋整片建置＋私人上傳 YouTube

工作目錄：`/Users/51mini/dev/vibe-shorts-pipeline`。片目錄 `films/wandavision-primer/`。前置：WO-11 已驗收，主 session 已寫 `audit/verdicts.md` 與 `audit/approved.md`（沒有 approved.md 就停下回報，不要自己跑 approve.py）。

使用者定：16:9、只發 YouTube 長片；先上傳**私人**影片給使用者看。

## 1 改成 16:9（只改片目錄內的檔）

上一輪（11-24 上午被中斷）已改過 index.html／build.sh 的 16:9 與倒數卡，先檢查現況，缺的才補。

- `index.html`、`engine.js`：畫布與 `W`／`H` 改 1920×1080。版面重排成橫式：插畫在中間偏上，字幕在下方 1/4，字級照比例調，不能有字被裁掉或超出畫面。
- `build.sh`：所有 `--size 1080x1920` 改 `--size 1920x1080`；`FPS=30` 改 `FPS=24`（長片省渲染時間）。
- 範本來自直式短片，凡是寫死直式座標的地方都要改；改完用 `scripts/qa_sheet.sh films/wandavision-primer` 出縮圖，自己看 `qa/sheet.jpg`，有破版先修再進整片渲染。

## 2 劇透倒數五秒

- 第二部、第三部開頭的劇透提醒句念完後，畫面上要有 5 秒倒數。
- 停頓用 `pace.json` 的 `pause_after`（`scripts/voice.py` 的 `layout()` 已支援：`{"第幾句（1 起算，去掉 # 行與空行）": 秒數}`），兩處各給 5.5 秒。不改 `scripts/voice.py`。
- `index.html` 在這兩段空檔畫倒數卡：大字「劇透警告」＋ 5、4、3、2、1 數字，下面一行小字「還沒看《汪達幻視》的人，現在可以先關掉」（第三部換成《阿嘉莎》）。只依賴 `t`（不累積狀態、不讀 `Date.now()`）。
- 時間點從 `window.TL` 算（找到那兩句的 `t1`），不要寫死秒數。

## 3 整片建置

- `cd films/wandavision-primer && bash build.sh`。稿約十分鐘；out/voice 有上次中斷留下的配音快取，沒改的句子會重用。渲染可能一兩個小時，用背景跑並把輸出存到 `qa/build.log`。
- 建置不併發：開始前確認沒有其他 `films/*/build.sh` 在跑（`pgrep -fl 'build.sh'`）；有就等它跑完。
- 節奏閘（rhythm）若因長片不過：記錄原文到回報，**不要改閘門**，影片檔有產出就繼續。其他步驟失敗就修片目錄內的檔後重跑；修不了就停下回報原文。

## 4 私人上傳

- `meta/title-shorts.txt`：一行標題，例「汪達幻視三部曲，一支片補完前情｜汪達幻視・阿嘉莎・幻視任務」。
- `meta/caption-shorts.txt`：三五行說明＋章節時間戳（第一部、第二部、第三部的開始時間，從 `timeline.js` 算）＋「資料來源見留言」。
- `mkdir -p dist && cp wandavision-primer.mp4 dist/wandavision-primer-shorts.mp4`（上傳腳本吃這個檔名；不跑 deliver.sh，那是直式三平台匯出）。
- `python3 scripts/publish/yt_upload.py films/wandavision-primer`（**不加 `--public`**）。把它印出的整行輸出寫進 `qa/yt-private.txt`。
- 如果權限模式擋下上傳，停下回報，由主 session 上傳。

## 禁區

不改 `scripts/`、`tests/`、`refs/`、其他片目錄、`/tmp/wv-accept-*.sh`、`narration.md`、`audit/`；不加 `--public`；不 commit；不跑 approve.py。

## 驗收

```bash
bash /tmp/wv-accept-9.sh
```
