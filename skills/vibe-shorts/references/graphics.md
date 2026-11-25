# 產圖：畫面怎麼來的

`index.html`（HTML＋Canvas／WebGL）→ headless Chromium 逐幀 `render(t)` 截 PNG → ffmpeg 合 `out/video.mp4` → 與 `out/mix.wav` 合軌成 `<片名>.mp4`。改畫面就是改 `index.html`。

## 渲染指令（`$LIB`，預設 `~/dev/lemo-opuscar`）

```bash
node $LIB/core/render/events.mjs . --size 1080x1920                       # window.EV → events.json（混音對時）
node $LIB/core/render/video.mjs  . --fps 30 --size 1080x1920 --workers 6  # 逐幀 → out/video.mp4；6 個 worker 各自冷啟動
bash $LIB/core/render/mux.sh out/video.mp4 out/mix.wav <片名>.mp4 30      # 合軌
node $LIB/core/render/readcheck.mjs . --size 1080x1920                    # 字幕閱讀時長（對談片只警告）
```

## index.html 的對外契約

渲染器只認這些全域變數，少一個就渲不出來：

```js
window.DUR    = 43.808;          // 片長（秒），通常讀 TL.dur
window.render = (t) => { ... };  // 畫第 t 秒，直接寫 canvas
window.READY  = true;            // 字型與資源載完才設 true
window.CUES   = [{t0, t1, text}];        // 字幕表，readcheck 用
window.TEXTS  = (t) => [{id, text, x0, y0, x1, y1, screen}];  // 該幀可見文字位置，textless_check 用
window.EV     = [{t, type, len?}];       // 音效事件，events.mjs 匯出
window.SHAKES = [t, ...];                // 可選：鏡頭震動時間點，要對得上 EV
```

## 資料檔

| 檔 | 產生者 | 內容 |
|---|---|---|
| `timeline.js` | `scripts/voice.py` 產生，**不手改** | `window.TL = {dur, lines:[{section,text,t0,t1,who?}]}`，驅動字幕與卡片切點 |
| `events.json` | `events.mjs` 從 `window.EV` 匯出 | `{dur, ev:[{t,type,len?}]}`，給 `mix.py` |
| `pace.json` | 手寫（可選） | `{"gap_line":1.0,"gap_section":1.3,"tempo":1.0}` |

`EV` 的 type 與對應音效見 `audio.md`；新增 type 要同步該片 `mix.py`，否則沒聲音。

## 視覺硬規格

- 畫布 **1080×1920**、**30 fps**。
- 左右各留 **60px**；主內容在 420px 以下（上面是 HUD／進度刻度）；字幕帶 **1860–1920px**（對談型）。
- **卡型片（taipei-silence 系）的字幕帶在 y≈1300–1440**：短線 1308、單行基線 1400、兩行 glyph 頂到 ~1309；來源列 ~1510。卡內插圖畫在 y 500–1290；人物腳底、姓名牌、地面線都要收在 ≤1290，會撞就整幕抬高（設區域 gy = GY − 140）。新增繪圖函式要寫清錨點方向（例：`skyline(x, y)` 的 y 是地面線、樓往上長、底緣錨 1900–1920），寫反方向會整片壓住字幕與來源列；qa 拼圖縮圖看不出壓字，要 `ffmpeg -ss <秒> -i <片>.mp4 -frames:v 1` 抽單幀放大驗。
- 字體：中文 `"PingFang TC"`，數字年份 `Menlo`。大標 190–250px 粗體、字幕 44–60px、HUD 標籤 24–40px。
- **米色底的白卡片要加有色外框**：藏字檢查只算跟底色差很多的像素，米色上的白卡片算不到；範本 `framed(cx, cy, w, h, col)` 畫外框＋卡片（11-11 songshan-airport 14 張卡因此被擋）。封面大標 170px 不加 `bold` 描邊，描邊會糊字。
- **藏字檢查 FAIL（藏字後 <0.03）要加「面積」不是加「細節」**：淡色填充、細線、半透明罩都不算墨；有效補墨是 INK 填色剪影（城市、人物）、粗描邊框（lineWidth 8–10）、牛皮紙色文件、紅叉、深色警示紋。夜景卡用城市剪影鋪底最划算（一次 +0.1）。
- **第 0 幀就是封面縮圖**：大標在 `t=0` 已完整顯示，不靠淡入（`docs/WRITING.md` §6.3）。
- 片尾最後 0.6 秒淡黑。

色票（`BRAND.md` 正本）：

```
#F29172 亮部／標題      #D97757 主色（Clawd）   #BC5C3E 暗部
#252422 描邊            #201F1D 底色            #3A3632 內框
#F6B966 星芒／思考態    #68E399 LED 正常        #FF856D 腮紅   #FF8577 休眠／錯誤
```

## 片型

對談型（現行）：範本 `films/nerf/`，three.js WebGL＋2D 疊層，女主＋Clawd Bot，渲染約 8–10 分鐘。資料卡型 `films/dating-bill/`（Canvas 2D，約 3 分鐘）只因已發布保留。
