# 進度 —《邪神給的腰帶》

> 接手者先讀這份，再看 `TREATMENT.md`（內容）與 `EXECUTION-PLAN.md`（步驟）。
> 最後更新：2026-10-18

## 一句話現況

**卡在步驟 0（角色 model sheet），已連敗 4 版。** TREATMENT 已定稿、爆款閘門已過；`main.js` 可跑可出圖，但**臉被前髮蓋住**（15 格全是髮型剪影），未通過停止條件。**2026-10-18 使用者指示「存目前進度先這樣」，停在這裡待裁決。**

## 待裁決（接手者先看這個）

核心繪圖路線已連敗 4 次，依 `CLAUDE.md`「同解法連敗 2 次」規定應換路，不應再盲試第 5 版。三條候選：

1. **續修 2D rig**——最後一輪已定位到確切病灶（見下），修好機會不小，但已 4 敗
2. **降級目標**——不再求完整 model sheet，只當 style frame 驗證色指定（一張正面半身），推進步驟 1–3
3. **換引擎**——改用其他既有 style 的 2D 實作（`_template` 無 `index.html` 範本，`pictogram-motion` 是唯一可跑的 2D 參考）

## 步驟 0 最後一輪的確切病灶

用 `NOBACK=1`（停畫後髮）隔離測試證明：**皮膚有被畫出來，臉就在那裡，但被前髮的 `ctx.fill('evenodd')` 反相填成髮色**——`hairOutline`（外圈）與 `faceHole`（內圈）的 even-odd 結果與預期相反，本該挖成臉的位置被填成頭髮。

病灶檔案與行號（`films/kamen-rider-girl/wip/main.js`，即 lemo 的 `styles/kamen-girl/demo/main.js` 副本）：
- 前髮 even-odd 填色：約第 348 行（`if (!window.NOFRINGE) { … ctx.fill('evenodd') }`）
- 外圈：`hairOutline()`；內圈（挖臉）：`faceHole()`
- 偵錯開關 `window.NOFRINGE`／`window.NOBACK` 仍在檔案內，**修好後要清掉**

本輪已修並經目視確認的：背面露臉、nonzero 反向洞（瀏海尖刺／側面第二張臉）、星芒鋸齒、`headShape.path()` 缺 `ctx.beginPath()`。

仍未修：臉被前髮蓋住、正面格只出現一隻眼、側面格鼻／嘴位置錯＋耳朵成細「D」、憤怒表情的眉成「v」形尖刺、色票格蓋 EXPR2 格＋標題重影。

## 本片檔案

| 路徑 | 內容 |
|---|---|
| `TREATMENT.md` | 世界觀、三個補強設定、片名、第一話骨架 |
| `EXECUTION-PLAN.md` | 七步執行計畫 |
| `PROGRESS.md` | 本檔 |
| `wip/main.js` | 角色設定集渲染器（**未完成**，含偵錯開關） |
| `wip/index.html` | 對應頁面 |
| `wip/render-20261018.jpg` | 2026-10-18 最後一次渲染（臉被前髮蓋住的狀態） |

渲染指令：
```bash
cp wip/main.js ~/dev/lemo-opuscar/styles/kamen-girl/demo/main.js
cd ~/dev/lemo-opuscar && node core/render/still.mjs styles/kamen-girl/demo 0 --out /tmp/msheet
```


## 步驟狀態

| 步 | 內容 | 狀態 | 證據／卡點 |
|---|---|---|---|
| 0 | 角色 model sheet（`main.js`） | **進行中** | 會出圖但破圖，見下節 |
| 1 | 定「不公規模數字」量法 | 未開始 | TREATMENT 有寫機制、無量法 |
| 2 | 第一話 `narration.md` | 未開始 | — |
| 3 | `build.sh`＋畫面 | 未開始 | — |
| 4 | 配音混音 | 未開始 | `PLAN.md` 既有缺口：`mix.py` 未接 |
| 5 | 閘門／交付 | 未開始 | `video-scrub` 未跑（既有缺口） |
| 6 | 發布 | 未開始 | **需使用者點頭** |

## 步驟 0 的實際卡點（最重要的交接資訊）

渲染指令與停止條件（照 `EXECUTION-PLAN.md`）：

```bash
LIB=~/dev/lemo-opuscar
cd $LIB && node core/render/still.mjs styles/kamen-girl/demo 0 --out /tmp/msheet
python3 core/render/sheet.py /tmp/msheet/sheet.jpg /tmp/msheet/*.jpg --cols 4
```

停止條件：`/tmp/msheet/` ≥8 張 jpg，`sheet.jpg` 可開啟且角色無破圖。**目前不滿足。**

檔案：`~/dev/lemo-opuscar/styles/kamen-girl/demo/main.js`（同目錄 `index.html` 已引用它）。

**上一輪目視（`Read /tmp/msheet/t_0.jpg`，不可只看 exit code）發現的缺陷**：

1. **背面格露出整張光臉**（最嚴重）——`drawHead` 的 `back` 分支只隱藏五官，`hairBack` 沒把反轉的頭皮蓋掉
2. 正面格只出現一隻眼（右眼沒畫出來）
3. 側面格的鼻／嘴位置錯、耳朵變成一個細「D」且位置錯
4. 憤怒表情的眉變成「v」形尖刺（不是眉）
5. 色票格蓋到 `EXPR2` 格子並產生標題重影

**已知根因**（供接手直接下手，不必重查）：

- `drawFringe` 用多段 `moveTo` 子路徑＋nonzero 填充 → 反向繞向被挖成洞，造成「瀏海尖刺」與側面「第二張臉」。正解是把瀏海與鬢髮做成**單一連續子路徑**，或改用 even-odd 並確保全部同向。
- `core/fonts/fonts.css` **只有** ZCOOL KuaiLe（中英）、Fredoka、Lilita One、IM Fell English。Fredoka／Lilita One **不含中文**，中文標籤一律用 `"ZCOOL KuaiLe"`。
- `styles/cel-anime-80s/` **沒有 JS 引擎**（STYLE.md §10 列的 `cel.js`／`head80.js`／`post.js` 都不存在），本片是照 STYLE.md 文字規格自寫 2D canvas。

**清理項**：`main.js` 的 `inkPath()` 裡還留著一段 no-op（`ctx.save(); ctx.beginPath(); f(ctx); ctx.save(); ctx.scale(1,1); ctx.restore(); ctx.restore();`），先刪。

## 已核實的事實（不要重做）

- 爆款閘門：`viral_problems()` 回 `[]`（門檻 10 萬，實際 **62.3 萬**）。影片 ID `mQoNk-JO8kY` 經 `yt-dlp ytsearch` 取得並以 curl 驗證 200（**先前用過的 `5WYU82-91HI` 是錯的 ID，已作廢**）
- 不採用的方案：mediago-drama（模型聚合器，會把零成本鏈路換成計費鏈路）、ArcReel／Toonflow（只借鏡概念）、本機 AI 影片生成（角色一致性不可控，見 wheel 卡 2026-10-14）
- `precheck.py` 的 29 道門是**單支短片版**；8–10 分鐘會撞時長與節奏門

## 版本控制

本 repo（`~/dev/vibe-shorts-pipeline`）以 `git subtree` 併入私有母 repo **`royalskynet/ether-projects`**，子目錄名 `vibe-shorts-pipeline`。

- `.git/hooks/post-commit` 已裝：commit 後背景跑 `~/dev/ether-projects/bin/subtree-sync`
- 失敗會寫 `~/dev/ether-projects/logs/subtree-sync.log` 並發 Telegram，不會擋 commit
- **注意**：母 repo 的 `publish-sync` 白名單（`bin/publish-sync` 的 `PROJECTS` 字典）**未含**本專案，所以目前不會外洩到公開 repo；要公開須先人工加進該字典並過三道掃描
