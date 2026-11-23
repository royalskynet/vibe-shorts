# B-roll 素材接入＋清重複元件（2026-11-10，L2）

## 為什麼

使用者 11-10 定：主體不換（lemo-opuscar 渲染＋voice.py 配音＋precheck 閘門），只接 MoneyPrinterTurbo（MPT）的素材搜尋，並清掉自家重複元件。
輪子：借鏡 MPT `app/services/material.py`（MIT）的直式篩選＋最短秒數；不搬它的 moviepy 渲染（wheel 卡 2026-11-10，`~/.wheel/registry.tsv`）。
MPT 預設的 Pexels／Pixabay 要 API key；Wikimedia Commons API 免金鑰，11-10 實測搜 taipei 回 8 支影片，含直式 782×1090、授權有 CC BY 3.0／4.0 與 CC BY-SA。

## 根治

### A. `scripts/broll.py`（派o，工單 20261110-broll-py）

- `search <關鍵字> [--limit N] [--min-sec 3] [--json]`
  - 預設只搜 Commons：`commons.wikimedia.org/w/api.php`，`generator=search&gsrsearch=filetype:video <q>&gsrnamespace=6&prop=imageinfo&iiprop=url|size|mime|extmetadata&iiextmetadatafilter=LicenseShortName|Artist`，User-Agent `vibe-shorts-broll/0.1 (royalskynet)`。
  - 環境變數 `PEXELS_API_KEY` 有值才加搜 Pexels；`--pexels` 明指卻沒 key → exit 2 並印 key 名。不讀憑證檔。
  - 授權白名單 `license_ok(name)`：CC0、Public domain、CC BY x.x 收；SA、NC、ND 擋（SA 會讓整支片被迫同授權）。
  - 排序 `rank(items, min_sec)`：濾掉短於 min_sec，直式（h>w）優先，其次長寬比接近 9:16。
  - 輸出欄位：source、url、page、width、height、duration、license、artist。
- `fetch <網址或本機檔> --out <目錄> [--start 0] [--secs 4] [--fps 30] [--license L] [--credit C] [--sources SOURCES.md]`
  - ffmpeg 一次完成：scale 裁滿 1080×1920（cover）→ `<out>/%04d.jpg`。
  - 寫 `<out>/clip.json`：`{count,fps,w,h,src,license,credit}`。
  - 給 `--sources` 就 append 一行出處（CC BY 必須署名）。
- 為什麼抽成圖片序列：lemo 渲染是逐幀 seek 再截圖（`core/render/video.mjs:56` `window.render(t)`），沒有 `<video>` 支援；圖片序列逐幀確定。

### B. 引擎圖層 `assets/broll/broll.mjs`（派o，工單 20261110-broll-layer）

- 純函式 `frameIndex(t, clip)`：`clip={dir,start,fps,count}`；t 在 [start, start+count/fps) 回 `floor((t-start)*fps)`，否則 -1。
- 純函式 `coverRect(iw, ih, W, H)`：等比放大裁滿，回 `{x,y,w,h}`。
- `framePath(clip, i)`：對齊 ffmpeg `%04d` 從 1 起算。
- `async drawBroll(ctx, clip, t, {W,H,load})`：-1 不畫；load 預設用 `Image` 載入並快取最近 8 張。片子的 `render(t)` 改 async（`page.evaluate` 會等 Promise）。
- 安裝照 `illust_install.sh` 慣例複製進片目錄（serve 掛載根是片目錄，取不到外面檔案）；用法寫 `docs/BROLL.md`。

### C. 清重複元件（主 session 已做）

- 刪 `scripts/tts.sh`：已被 `voice.py` 取代（逐句念＋Whisper 核稿）；唯一引用 `VOICE.md:69` 改指 voice.py。全庫 grep 零殘留。
- 保留且理由：`verify_tts.py` 是 voice.py／voice_design.py／precheck.py 共用庫；`trend_scan.py` 是 PLAN.md:22 備用且 daily-trends.sh 在跑；`ref_analyze.py`（qa_sheet）與 `shots.sh`（成片鏡頭表）用途不同；每片的 mix.py／engine.js 副本保舊片可重建。
- `.gitignore` 加 `films/*/broll/`（素材是別人的內容，不進版控）。

## 預防加固

- `tests/test_broll.py`：license_ok 紅樣本（CC BY-SA 4.0、CC BY-NC 擋）＋rank 排序＋短片過濾，邏輯改錯會 fail。
- `tests/test_broll.mjs`：frameIndex 邊界、coverRect 算式、drawBroll 在 -1 不呼叫 drawImage。
- ponytail：不做自動選片與片內自動插入；之後要升級就讓 TREATMENT.md 的鏡頭表帶關鍵字，由 broll.py 批次 search→fetch。

## 工單

- `docs/workorders/20261110-broll-py.md`
- `docs/workorders/20261110-broll-layer.md`
