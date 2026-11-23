# 調研：claude-motion-skill v0.2.0-beta.1 對本流水線的可借用處（2026-10-13）

來源：<https://github.com/Hype-yolo/claude-motion-skill/releases/tag/v0.2.0-beta.1>（prerelease，2026-10-12，MIT；模型與字型各自授權）。
ZIP 經 SHA256SUMS 驗證通過。221 份 md 原樣存在 `refs/claude-motion-v0.2.0-beta.1/`（含 LICENSE）。
X 推文（hypewangyolo/status/2109635454169673765）抓不到：WebFetch 回 402，r.jina.ai 對 x.com 暫時封鎖。本文只依據 release 內容。

## 它是什麼

一套「案例輔助」的程式動畫 skill。47 套源碼案例（43 套 Lemo、4 套 ReelMimic）、5 套可跑的製作系統、14 個場景入口、30 個模型包。
Agent 用 `route.mjs` 依題目找案例，複製源碼後改寫故事，最後用 `render.mjs` 經 Playwright 逐幀匯出 MP4。

跟我們的關係：**我們的 ③ 出片本來就用 lemo-opuscar（`e3cb16f`）**，它是 Lemo 的超集加上一層守衛與方法論。

## 結論：不整包裝，借三樣

整包裝不划算，依據四點：

1. 規格不合。全部案例與引擎以 1280×720／24fps 橫式設計，我們是 1080×1920／30fps 直式。
2. 片型不合。它的理念是「畫面講完就不要字幕」，我們是字卡驅動的知識短片，FACTS 閘門依賴畫面上的數字。
3. `route.mjs` 對我們的題目幾乎無用。實測查「數學史 定理 證明 知識科普 文字排版」，47 案例 0 命中，只回 `swiss` 引擎，且該引擎 `userReview: pending`。
4. 它鎖 Playwright 1.63.0，`npm run setup` 會再裝一份 Chromium。我們踩過 lemo 安裝 Playwright 刪掉別人 Chromium 的坑（fix 10382）。

### 借 1：渲染守衛（證據強，建議做）

lemo 的 `core/render/page.mjs:78-88` 已經會在 `pageerror` 和必要檔案（script／document）404 時中止。（初稿只 grep 了 video.mjs，誤寫成「沒有任何守衛」，已更正。）
lemo 缺的是下面第二、三道。claude-motion 的 `scripts/render.mjs:35-59` 有三道：

- 收集 `pageerror` 與 HTTP ≥400，有就讓匯出失敗。
- 擋外部網路請求。
- **重複尋幀**：先抓 t=0.31×長度，跳到 0.81×長度，再回來抓同一格，兩張 PNG 位元組必須一樣，否則報 `non-deterministic seek`。

第三道對我們特別重要。我們用 `--workers 6` 平行渲染，每個 worker 各自從中段時間開始畫。只要頁面有任何依賴「上一幀」的狀態（累積粒子、未固定種子的亂數），worker 交界就會跳格，而現在沒有任何東西會抓到。

**已做（10-13）**：`scripts/seek_check.mjs` 對準 worker 交界幀，比對冷啟動和接續畫出來的 PNG，並擋外部請求；`build.sh` 渲染前跑，`precheck.py` 第 22 道門讀報告（須比 index.html 新）。自檢 `tests/test_seek_check.py`。

### 借 2：「拿掉字還剩什麼」檢查（證據中等偏弱，建議試）

出處：`SKILL.md`「检查时临时隐藏标题：若标题一去掉就只剩几何示意，继续完善主体绘制」與 `direction.md` §7。
它對應我們的真實弱點：節奏閘門只量亮度變化，字卡彈入也算動態，所以「整支片其實只在換字」也能過。

可機械化的版本：渲染時注入 CSS 把字幕層與大標設成 `visibility:hidden`，抽每張卡的中點幀，量非底色像素比例與邊緣密度，低於門檻就判「這張卡只靠字」。
門檻要先拿 flt-11days 與 8 支參考爆款逆推，跟節奏閘門同樣做法，兩支參考片驗過才採信。

**已做（10-13）**：`scripts/textless_check.mjs` 攔截 fillText 藏字，扣掉每張卡都有的外框後算每張卡自己的畫面佔比；< 0.03 失敗、< 0.05 警告。flt-11days 校準：卡 3（只剩刻度尺）0.016、卡 5（眼睛＋勾選格）0.060。flt-11days 卡 3 已在 `meta/textless-waive.txt` 豁免。自檢 `tests/test_textless_check.py`（兩個變異都抓得到）。

證據偏弱的原因：作者自己寫明這些是「源码分析产生的创作假设，不是已证明的审美定律」，沒有數字評分或盲測。

### 借 3：動作分階段寫進 TREATMENT（零成本，建議直接採用）

`direction.md` §1、§4 的兩條規則可以直接加進寫稿模板：

- 每段寫成可畫的動詞（拉開、接住、壓下、蓋章），不寫「科技發展」這類抽象詞。抽象詞會退化成圖示輪播。
- 一次動作標出準備、加速、接觸、餘振、停留，主體、鏡頭衝擊、音效都引用同一個 t0。

**已做（10-13）**：兩條寫進 `docs/WRITING.md`。第二條我們已經部分做到：`mix.py` 讀 `events.json`，音效落在頁面匯出的事件格上。缺的是鏡頭衝擊與餘振沒有綁同一個 t0。

## 不借的

| 項目 | 不借的原因 |
|---|---|
| `--gpu metal` | 只加速 WebGL。flt-11days 的 index.html 裡 WebGL 出現 0 次，是 2D canvas |
| 47 案例／模型庫 | 橫式敘事動畫，題材與我們不重疊 |
| swiss 引擎（精確貝塞爾、拍點 snap、基線遮罩揭示） | 最接近字卡片型，但作者標示未獲使用者認可、只有 720p。等要換第二種畫風時再評 |
| `ADAPTATION.md` 來源紀錄 | 我們已有 TREATMENT.md 記畫風來源 |

## 對排程的影響

10-13 定案「三平台授權完成前不單獨試個別段落」。借 1 與借 3 不碰出片內容：借 1 是閘門，借 3 是寫稿模板，可以現在做。借 2 原訂等全鏈路，10-13 使用者要求先做好，門檻用 flt-11days 校準。
