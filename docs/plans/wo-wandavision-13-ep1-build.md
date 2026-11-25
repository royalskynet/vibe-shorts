# WO wandavision-13：第一集建片＋私人上傳 YouTube

工作目錄 `/Users/51mini/dev/vibe-shorts-pipeline`，片目錄 `films/wv-primer-1/`。前置：主 session 已寫 `audit/verdicts.md` 與 `audit/approved.md`（沒有 approved.md 就停下回報，不要自己跑 approve.py）。

## 1 建置

- 開始前 `pgrep -fl 'build.sh'`：有其他片在建就等它跑完（建置不併發）。
- `cd films/wv-primer-1 && bash build.sh > qa/build.log 2>&1`。`out/voice` 有配音快取，沒改的句子會重用。
- 16:9 版面沿用；先 `scripts/qa_sheet.sh films/wv-primer-1` 出 `qa/sheet.jpg` 自己看，有字被裁或破版就修 `index.html` 再建。
- 節奏閘（rhythm）若因片型不過：記錄原文到回報，不要改閘門，影片檔有產出就繼續。其他失敗修片目錄內的檔；修不了停下回報原文。

## 2 私人上傳

- `mkdir -p dist && cp wv-primer-1.mp4 dist/wv-primer-1-shorts.mp4`（上傳腳本吃這個檔名；不跑 deliver.sh）。
- `python3 scripts/publish/yt_upload.py films/wv-primer-1`（**不加 `--public`**），整行輸出寫進 `qa/yt-private.txt`。
- 權限模式擋下上傳就停下回報，由主 session 上傳。

## 禁區

不改 `scripts/`、`tests/`、`refs/`、`narration.md`、`audit/`、其他片目錄、`/tmp/wv-accept-*.sh`；不加 `--public`；不 commit；不跑 approve.py。

## 驗收

```bash
bash /tmp/wv-accept-13.sh
```
