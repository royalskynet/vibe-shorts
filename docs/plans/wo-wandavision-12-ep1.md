# WO wandavision-12：拆成三集，先做第一集（看《汪達幻視》前，約五分鐘）

工作目錄：`/Users/51mini/dev/vibe-shorts-pipeline`。使用者 11-24 定：三部前情改成三支各約五分鐘的片，先做第一支。16:9、只發 YouTube。

## 1 建片目錄

- `cp -r films/wandavision-primer films/wv-primer-1`（帶走已改好的 16:9 `index.html`／`engine.js`／`build.sh` 與 `out/voice` 配音快取，沒改的句子會重用）。
- 刪 `films/wv-primer-1/` 下：`audit/verdicts.md`、`audit/approved.md`、`audit/coldread-script.md`、任何 `*.mp4`、`dist/`、`qa/` 裡的舊 log 與 `yt-private.txt`。
- `build.sh` 的 `OUT=` 改 `wv-primer-1.mp4`。
- `pace.json` 的 `pause_after` 清成 `{}`（第一集沒有劇透倒數）。`index.html` 的倒數卡若依 `pause_after`／特定句號觸發，確認第一集不會畫出來。

## 2 稿子（只改 `films/wv-primer-1/narration.md`）

- 來源：`films/wandavision-primer/narration.md` 的第一部（`## 第一部｜開場` 到第一部 `## 收尾` 為止，1643 字），刪掉第二、三部全部段落。
- 壓到 1350–1600 字（實測語速含停頓約 4.9 字／秒，約五分鐘）。判準：少了這句，觀眾看《汪達幻視》會不會看不懂？不會就刪。只刪、改短，不加新事實。
- 開頭改成系列第一集的說法：例「這是汪達幻視三部曲觀劇前情，三集裡的第一集」，刪掉「這支片分三部，照順序講完」。
- 結尾改成預告下一集，例「下一集，我們接著講看《阿嘉莎》之前要知道的事。」保留「你已經可以開播《汪達幻視》了」。
- 不准出現（驗收會擋）：哈克尼斯、緋紅女巫、混沌魔法、白幻視、比利、湯米、黑暗神書、天生、死神、雪帕德、罐頭、黑寡婦、弟弟、分三部。要保留：心靈寶石、奧創、幻視、皮特羅、薩諾斯、西景鎮、天劍局、內鬨、彈指之前。
- 每行一句、≤35 字、一行只一個句號。
- `SOURCES.md` 刪掉只跟第二、三部有關的列（阿嘉莎、比利、湯米、雪帕德、VisionQuest 宅邸 AI 等），其餘保留。

## 3 meta

- `meta/title-shorts.txt`：一行，例「汪達幻視三部曲前情 1／3｜看《汪達幻視》前要知道的事」。
- `meta/caption-shorts.txt`：三五行說明＋「資料來源見留言」。

## 4 重跑

1. 口語化：只過改動句，重寫 `audit/humanize.md` 戳記（首行 `narration_sha:`）。
2. `scripts/devils.sh films/wv-primer-1`（exit 3 就停下回報原文）。不跑 coldread。

## 禁區

不改 `scripts/`、`tests/`、`refs/`、`films/wandavision-primer/`、其他片目錄、`/tmp/wv-accept-*.sh`；不寫 verdicts.md、approved.md；不 commit、不上傳、不跑 build／voice／approve。

## 驗收

```bash
bash /tmp/wv-accept-12.sh
```

回報附：字數、刪了哪些句（一行一句）、devils 爭點原文。
