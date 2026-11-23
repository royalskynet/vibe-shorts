# 全鏈路草圖：一片三管道

一支片做一次，匯出成三個平台的版本（IG Reels／YouTube Shorts／Threads 導流）。

## 流程（2026-10-14 改版：對標驅動）

舊流程從 HN 科技新聞選題，費馬片因此離開品牌方向，而且片內沒有鉤子、落點、提問和旁白。新流程先看「什麼已經紅過」，再照它的格式做。依據：龍井 Codex 視頻號復盤（對標帳號→素材庫→文案範例＋題材→程式剪輯）與 10-14 輪子卡（`~/.wheel/registry.tsv`）。

| 段 | 做什麼 | 工具 | 狀態 |
|---|---|---|---|
| ① 對標 | 找流量第一的中文 Shorts 頻道與單支爆款；主題偏好 AI→區塊鏈→金融／防詐／台灣，流量優先 | `scripts/benchmarks.py`（頻道最近 30 支中位數、主題詞比例、中文比例），結果 `refs/BENCHMARKS.md` | ✅ 發現走 YouTube Data API `search.list`（觀看排序、短片、近 90 天，約 3500 配額單位／次），加離群值欄與離群爆款榜 |
| ② 拆解 | 對標前三名各 3 支最高播放：鏡頭表＋口播逐字稿＋前 3 秒鉤子句 | `scripts/breakdown.py`（video-shots＋mlx_whisper） | ✅ |
| ③ 寫稿 | 對標逐字稿當範例＋題材資料 → `narration.md`（鉤子→…→轉折→落點→提問） | 寫稿規則 `docs/WRITING.md` §3；precheck「旁白稿結構」門 | ✅ 門已上（`eafd839`） |
| ④ 配音 | 旁白合成，混進成片 | Qwen3-TTS 模板 D（`VOICE.md`）→ `mix.py` | 試產跑通；接進 mix.py 待做 |
| ⑤ 出片 | 程式渲染畫面；可重用元件逐步累積成素材庫 | `lemo-opuscar`；渲染前 `seek_check.mjs` | ✅ |
| ⑥ 閘門 | 工藝＋故事兩層，全過才能發 | `narration_check.py`（Whisper 聽成片）＋`precheck.py`（29 道） | ✅ |
| ⑦ 匯出 | 三平台檔、清元資料 | `scripts/deliver.sh`（ffmpeg-skill＋video-scrub） | ✅ |
| ⑧ 發布 | YT 公開、IG Reels＋Threads | `yt_upload.py`、`meta_publish.py`（funnel TCP 直通） | ✅；每次對外發布要人點頭 |
| ⑧b 分發 | 一片多形態（輪播、Threads 文字貼、自引用）、手動回覆、系列化（HN 發布即時推播 11-06 刪，CHG-20261106-09） | `meta_publish.py --carousel`、`threads_post.py`（佇列）；規則 `docs/DISTRIBUTION.md` | 2026-10-20 上線，佇列 3 則待核 |
| ⑨ 回饋 | 48 小時後抓三平台數據，決定主力平台與下一個對標 | `scripts/publish/stats.py`（一支一行：上架小時、播放、讚、留言、分享） | ✅ 10-17；節奏先 1–2 天一支，不追日更 |

趨勢掃描 `trend_scan.py`（launchd `com.user.vibe-trends`）降為備用題庫，不再當主要選題來源。

②（拆別人的片）的分工是刻意的：切點與秒數由 ffmpeg 量，景別、運鏡這類判斷才交給模型，最後 15 道程式化關卡逐條對帳。

## 實測紀錄（2026-10-11）

三個 reelbench skill 的自我測試全過：

```
video-shots ✅ 449 項斷言全部通過（15 道門每道都有擊穿用例）
video-sync  ✅ 122 項斷言全部通過
video-scrub ✅ 117 項斷言全部通過（12 道門每道都有擊穿用例）
```

整條鏈用一支測試片跑（16:9、12 秒、4 個場景，另外塞一個假的設備 ID）：

```
[seed] 12s / 30fps / 1920x1080 → 偵測 2 個切點，合併後 3 鏡
reels: 1080,1920   shorts: 1080,1920   x: 1280,720
src.mp4          dev=1 x264-SEI=1
out-reels.mp4    dev=1 x264-SEI=1    ← 只匯出的話，設備 ID 還在
clean-reels.mp4  dev=0 x264-SEI=0    ← 跑過 scrub 才清乾淨
```

三個發現：

- **⑥ 不能省。** ffmpeg-skill 匯出時會把來源 metadata 原樣帶過去，要靠 video-scrub 才清得掉。
- **切點少抓一刀。** 4 個場景只切出 3 鏡。測試片是 lavfi 合成畫面，實片不一定會這樣；要修用 `recut --split` 手動補刀。
- **音量偏小。** 測試片 −21.8 LUFS，平台標準是 −14，正式匯出要加 `--normalize`。

## 安裝版本與兩個坑

版本固定在 `~/dev/` 下的 commit：reelbench `0d2743a`、lemo `e3cb16f`、ffmpeg-skill `1f7e7e3`。三個 repo 都先讀過程式碼才裝，install 腳本只做 symlink，沒有對外連網。

- **lemo 的自動更新已拆掉**：原本的 `setup.sh` 每次呼叫都會從上游 `git reset --hard` 拉最新版，等於每次都在跑沒審過的程式碼。改成自己 clone、不設它的自動更新標記，版本鎖住。
- **lemo 安裝 Playwright 時刪掉 chromium 1228**，`solon-protocol/web` 的 e2e 測試要用這一版。已在 solon 那邊重新安裝並登記，兩個版本現在都在。記在 fixindex 10382。
- **燒字幕的限制**：brew 版 ffmpeg 少了 libass／drawtext，ffmpeg-skill 無法把字幕燒進畫面。lemo 的字幕在渲染時就畫進畫面，所以目前不受影響。之後要給素材後製加字幕才需要換 `ffmpeg-full`（多裝 47 個依賴）。

## 下一步（2026-10-14 定案，取代下方 10-13 那段）

1. ~~① 發現階段改走 `search.list`，加離群值欄，補 AI 類大帳號後重排。~~ ✅ 10-14：發現 603／可量 331 頻道；排除日文頻道、上一輪頻道累加、離群榜（中位數 ≥1000）。AI 加 7 組詞仍無中位數 >7.8 萬的中文 AI 頻道，AI 類流量天花板偏低是事實不是漏抓。
2. ~~② 拆四處觀察、四方異聞、cheap 各 3 支最高播放~~ ✅ 10-14：`scripts/breakdown.py`→`refs/BREAKDOWN.md`，判讀 `refs/BREAKDOWN-NOTES.md`。地圖動畫格式證實；流量要素＝台灣錨點＋反直覺問題；9 支都沒有片尾提問。
3. ~~③ 第二支片寫 `narration.md`，過旁白稿結構門~~ ✅ 10-14：選題原則改為流量優先（使用者：「流量 流量 流量」），題目「全台最常被詐騙的城市」＝台灣錨點＋反直覺（新竹市）。稿 `films/scam-map/narration.md` 211 字約 45 秒，結構門過；數字全出自 165 儀錶板＋內政部 API，算法見 `films/scam-map/SOURCES.md`。
4. ~~④ 配音接進 `mix.py`，⑥ 全過才問發布。~~ ✅ 10-14：`scam-map` 三平台公開（YT https://youtube.com/shorts/aMhz3u30QC8 、IG https://www.instagram.com/reel/DecjzbCjWYg/ 、Threads https://www.threads.com/@paradoxbar.tw/post/Decjz1rinAQ ）。新規則：文本定稿前必跑反方稽核（`scripts/devils.sh`＋precheck 反方稽核門，`docs/WRITING.md` §4），本片跑了 4 輪改 3 句；節奏閘門加 `map` 基準（≤62%、≤8 秒，使用者核准）；地圖格式略過鏡頭格線。precheck 30/30。
**選題原則（2026-10-14 使用者定案，取代「爆款格式＋偏好主題」）**：爆款第一。題目從已證實的爆款題型挑（目前是地理冷知識：四處觀察／四方異聞 277–457 萬播放），AI／區塊鏈／防詐等偏好主題不再優先。**10-14 再收緊：題材完全不設限，「爆款就好」**，不限地理或冷知識；唯一條件是有爆款證據、程式畫面做得出來。scam-map 用防詐主題是錯判：防詐頭部中位數 3.4 萬，地理冷知識 87 萬。

**10-15 把「爆款第一」綁成機械門檻**：`scripts/trend_scan.py` 的題型桶加 `viral` 欄（`viral`／`weak`／`unproven`／`failed`，值一律引 `refs/VIRAL-LEDGER.md` 的逐題判定），只有已驗出同題爆款的桶能進主榜，沒驗過的進待驗區，做過被否決的（冷門定理＝費馬片）整條不列。桶清單不複製到這裡，正本在腳本裡，改桶要同時更新 `why` 欄的證據。改這個的原因：舊版只按 log(互動量)×命中桶數排序，所以每天 21 條候選幾乎全部「同題爆款：沒找到」，費馬片就是這樣被選出來的。輪子卡 2026-10-15（不裝 new-term-radar：SEO 導向、主要信號吃付費 key）。
5. ~~⑤ 過場改版~~ ✅ 10-14：拿掉斜色塊轉場／掃描光／流動網格，陸地換 EOX 2016 衛星底圖（CC BY 4.0，`films/scam-map/fetch_basemap.py`，畫面＋說明附出處），每卡不同鏡頭落點遠近交替（爆款拆解：15–19 次 0.3–0.8 秒大幅運鏡佔分數 26–65%）。節奏閘門 map 基準放寬為靜止秒 ≤75%、亮度 ≥0.95（使用者目視核准，數字低於 6 支頭部片，待數據回來再校）。舊片三平台已刪，新版重發：YT https://youtube.com/shorts/HIfv3Q3CI-Y 、IG https://www.instagram.com/reel/DedPjxdgalU/ 、Threads https://www.threads.com/@paradoxbar.tw/post/DedPj7hALRP 。precheck 30/30。
6. ⑥ 下一支片照「爆款第一」選題（候選：從台灣往地心挖、麥卡托投影下的台灣）。海面仍是深色平色，懷疑是亮度差異偏低主因（證據弱），下一支可試亮色衛星海。⑨ 看 scam-map 新版 24–48 小時數據。
7. ⑦ 第三支片 `films/dating-bill`（台灣單身與約會帳單，材料出自 repo taiwan-dating-cost-model）**文本定稿** ✅ 10-14：起承轉合＋鉤子「你覺得台灣人單身，是因為沒錢嗎？」，只並陳 2013 台北市府／2025 與 2024 yes123 三組數據、不替論點背書、結論交給聽眾；女性框架：主詞都是調查本身，不用「期待老公月薪」類數字。反方稽核 6 版多輪，最終 3 爭點全 PRO_WINS；順手修正材料 repo 錯誤付帳比例（d546733，83.3/50.6→81.5/40.3）。新規則：稿子禁止防衛性中立句（CLAUDE.md、WRITING.md §4）。文本閘門 3/3 過，**成片** ✅ 10-14：風格選 pictogram-motion（三風格樣張比較後使用者定），人形改極簡圓頭＋身塊、無背後圓底；為過 vkv 嚴格節奏基準加底色隨拍呼吸、圖案帶連續捲動、人形隨拍輕跳（靜止秒 73.7%→0%、亮度差 1.01→2.44，基準未放寬）；換卡改硬切蓋滿再滑出（切點 0→9）；片尾配樂在提問句後淡出（Whisper 純配樂尾段幻聽「明镜与点点栏目」）。precheck 31/31，三平台交付檔已出，未發布。

## 下一步（2026-10-13 定案，已被 10-14 取代）

**等三平台授權做完，一次跑完整條：① 選題 → ⑧ 配旁白 → ③ 出片 → ④⑤⑥ → ⑦ 發布。** 在那之前不單獨試個別段落。

- 前置：使用者照 `docs/PUBLISH-SETUP.md` 做完電腦前設定，`tokens.py status` 三行都是「已登入」。
- 這次要第一次驗證的：旁白怎麼混進 `mix.py`（前兩支片都沒有旁白）、2 分鐘級配音的長度和吃字（Whisper 核稿）、三平台端點實際發片。
- 配樂升級（ACE-Step 1.5）不在這一輪，見 wheel registry 10-13。

以下是 10-11 的兩條路，保留作紀錄：

1. **寫 ① 追趨勢的膠水**：每天抓一次熱度，列 5 個候選題，附同題爆款連結交給 ② 去拆。照規則要寫成零 token 的腳本跑背景。
2. **直接挑題做第一支片**：把 ②→⑥ 實跑一遍，先看畫風認不認。

④ 的對照腳本（自己的節奏表 vs 爆款節奏表）兩條路都會用到，還沒寫。

## 工具盤點（2026-10-11）

原始七階段指定的工具，實際被流水線呼叫的只有三個。

| 階段 | 原本指定 | 實際跑的 | 差在哪 |
|---|---|---|---|
| ① 追趨勢 | `twitter search`＋`agent-reach` | `scripts/trend_scan.py` 直打 HN／維基／Google Trends | 兩個指定工具都沒用上。Reddit 走裸 JSON 被 429 擋光，`agent-reach` 本來就是為了繞這種節流而存在 |
| ② 拆爆款 | `video-shots` | `video-shots` ✅ | 照用 |
| ③ 出片 | `lemo-opuscar` | `lemo-opuscar` ✅ | 照用 |
| ④ 品質檢查 | `video-shots` 再拆自己的成片，跟爆款鏡頭表對照 | `scripts/rhythm_check.py`（只比相鄰幀亮度差） | 只做了「動不動」一個維度。景別、運鏡、鏡頭長度分布全都沒對照 |
| ⑤ 三平台匯出 | `ffmpeg-skill` 的 reels／shorts／x preset | 只有 `mux.sh` 出一個檔 | 三平台各自的規格沒分開處理 |
| ⑥ 清 metadata | `video-scrub` | 沒跑 | 成片還帶著編碼器簽名 |
| ⑦ 上片 | 三平台官方 API | 沒接 | 見下方授權調查 |

四個階段的指定工具完全沒進流水線。③ 和 ⑧ 是照設計走的，② 只用在參照片上、沒回頭用在自己的成片上。

## 四個洞補完（2026-10-11）

工具四個全都在機器上，裁決沿用 10-11 的輪子卡。洞不是缺工具，是沒照卡用。

### ① 趨勢掃描的 Reddit 429 — 真因是 UA，不是打太密

原本的 UA 是 `Mozilla/5.0 (Macintosh; ...) vibe-shorts/1.0`。Reddit 擋假冒瀏覽器的 UA，一律回 429。改成它 API 規則要求的格式 `macos:vibe-shorts:1.0 (by /u/royalskynet)` 就 200。

**我第一次診斷錯了**，以為是連續打六個沒有間隔，加了退避重試。重試完還是 429，因為擋法跟頻率無關。而且我連跑三輪把 IP 配額打爆，之後連 curl 配好 UA 也 429，自己把量測搞髒。等配額回復後做乾淨對照：同 IP、相隔三秒，好 UA 200、Mozilla UA 429。

退避重試留著，它本身是對的（Reddit 真的會附 Retry-After）。另外把 subreddit 之間的間隔設成 6 秒：未登入配額約每分鐘十次，六個攤成 30 秒留餘裕。1.5 秒實測還是會 429。

### ④ 對自己的片跑 video-shots — 抓到節奏閘門和場景偵測互相打架

費馬那支拉片結果：12 鏡 / 61.53 秒 / 平均 5.13 秒 / 每分鐘 11.7 切。

S05 到 S12 全部 6.13–6.17 秒，卡片格線 6.153 秒，時間軸很準。但開頭被切出 S02 0.63 秒、S03 0.9 秒兩個短鏡頭。量了那段的畫面亮度：187 → 159 → 216 → 178 → 211，不到一秒跳 30 到 57 個亮度單位。

那是我為了過節奏閘門加的八分音符網點呼吸。**兩個工具方向相反**：節奏閘門要大面積亮度變化才給過，場景偵測正是靠亮度變化找切點。所以過了節奏閘門的片，拉片一定會過度切割。

這不是缺陷，畫面沒有硬切。但它改變了檢查方式：不能用「有沒有短鏡頭」當判準，那在我們的片型上一定假失敗。改用**鏡長中位數貼合卡片格線**，中位數不受假切點影響，還抓得到真的時間軸漂移。實測中位數 6.14 對格線 6.15。

`validate` 的 14 道門有 4 道沒過，全是「鏡頭描述還沒填」那類——那支是給人工拉片標註用的，不是自動自檢工具。

### ⑤⑥ 三平台匯出與清元資料 — 串成 scripts/deliver.sh

`ffmpeg-skill` 的 preset：shorts 上限 180 秒、reels 上限 90 秒。Threads 沒有專屬 preset，借用 reels（同樣 9:16，Threads 影片上限 5 分鐘更寬）。匯出完接 `video-scrub run` 清元資料，因為匯出會把編碼器名稱和建檔時間寫進檔案，碼流裡還有 ffprobe 看不到的 SEI 身份串。

三個交付檔各 69 MB。

## 發布前閘門 scripts/precheck.py（21 道，零 token）

規則寫在文件裡的符合率接近零，所以寫成會擋人的腳本。踩到的兩個坑都變成門：

- **成片比頁面新。** 改了 index.html 的一個數字之後，其他每一道門都過，因為它們比的是 index.html 和 facts.md。但 mp4 是改之前渲染的，畫面上還是舊數字。檔案時間是唯一能機械判斷「這支片有沒有包含最新改動」的依據。
- **元資料判準交給 video-scrub 自己的 verify。** 我原本自己掃 `Lavf`、`libx264` 字串，得到假失敗——那是 ffmpeg 重封裝時自己寫的標籤，跟來源身份無關。清元資料的目的是不搬來源的身份字串。

## 修掉一個已經渲染進成片的錯誤數字

第四張卡寫「1995 年 Wiles 補上證明。129 頁」。查證：Wiles 單篇是 **109 頁**（Annals of Mathematics 141, 443–551，含頭尾 109 頁），加上 Taylor–Wiles 的附論文（553–572）才 130 頁。129 兩種算法都對不上。

已改並重新渲染。預防做成一道門：片中每個數字都要在 `meta/facts.md` 有一行附來源，對不上就擋住發布。費馬那支 8 個數字全部對上。

## 事實數字集中到 FACTS（2026-10-12）

109 頁那個修正沒修乾淨，而且閘門沒抓到。

改完重新渲染之後我去抽第四張卡的畫面看，標題和字幕都是 109，但**畫面正中央的大數字還是數到 129**——計數動畫在繪圖函式裡另外寫了一次 `* 129`。同一個事實寫在兩個地方，我只改了看得見的那個。閘門當時掃的是卡片文字，掃不到繪圖函式，所以 20 道全過。

查下去發現不只一處。`1300 萬行` 寫了三次（標題、字幕、動畫的 `* 13000000`），`29500`、`1637`、`2026`、`11 天` 也都是文字和動畫各寫一次。

結構性的修法是把事實集中成一個物件，文字和動畫都引用它：

```js
const FACTS = {
  WILES_PAGES: 109, LEAN_DAYS: 11, LEAN_LINES_WAN: 1300,
  THEOREMS: 29500, YEAR_CONJECTURE: 1637, YEAR_FORMALIZED: 2026,
};
```

閘門跟著改成驗 FACTS，規則分兩種：

- 值同時出現在 FACTS 的，卡片文字必須寫成 `${FACTS.X}`。那代表這個事實既被畫出來也被講出來，兩邊各寫一次就會分岔。
- 不在 FACTS 的（只在散文裡出現一次，像「1995 年 Wiles 補上證明」），有來源就行，不必硬塞進 FACTS。

散落各處的數字沒辦法跟版面座標區分——同一支檔案裡 `1300` 可能是 1300 萬行，也可能是 y 座標 1300，實際上兩個都有。集中起來才驗得動。
- 10-15 dating-bill 三平台公開：YT https://youtube.com/shorts/k1gEFDl7f9I 、IG https://www.instagram.com/reel/Dee53JtgYBr/ 、Threads https://www.threads.com/@paradoxbar.tw/post/Dee53RfAOKD 。v3 資料卡版、card 基準、precheck 31/31。
- 10-17 對談片 #2 codex「我昨天用了 Codex」三平台公開：YT https://youtube.com/shorts/5aXxzejVXAI 、IG https://www.instagram.com/reel/DelQ5DVk_Wf/ 、Threads https://www.threads.com/@paradoxbar.tw/post/DelQ13LgRKj 。閘門新增 dialogue 格式（10 支 IG 對談爆款全過邊界；免鉤子觀眾門、鏡頭格線、無三位數數字免 facts），precheck 31/31。
- 10-17 失敗試作清除（使用者早先已判定失敗、要求刪除）：對談 #1 clawd-notes「AI 每天都忘了你」、#2 not-human「你不是人類」、「AI 說我不是工程師」三支 YT 私人片已刪（Ij0dpeZUSfg、8ocPzC5pd5E、YLOixsLFRn4），`films/clawd-notes`、`films/not-human` 已刪。之後不要再提這三支或拿來發布。數據（10-17）：YT codex 343 播放（未滿 1 天）＞ dating-bill 146 ＞ scam-map 8；IG／Threads insights 403，權杖缺 `instagram_business_manage_insights`／`threads_manage_insights`。
- 10-17 IG／Threads insights 權限補上（scope 加 `instagram_business_manage_insights`、`threads_manage_insights`，後台 use case 原本就含，不用改；重新授權到 2026-12-16）。無頭授權法：`cdp.py goto <授權網址>` → Playwright 點同意 → 從 `127.0.0.1:9333/json/list` 讀 `/oauth?code=` 分頁網址 → stdin 餵 `tokens.py login <p>`，授權碼不印出。數據（10-17）IG views：codex 56／dating-bill 7／scam-map 31；Threads views：26／28／103。
- 10-18 對談片 #3 nerf「Claude 你是不是被降智了」建置完成，precheck 31/31，YT 私人上傳 https://youtube.com/shorts/4pmgVoAbQAM 待審。核稿改 2 句：「這篇一萬人按讚欸」→「這篇有一萬個讚」（Whisper 把欸聽成哎）；「有。」→「對，我變笨了。」（單音節聽成呀；「降智」短句會被聽成同音「降制」，長句才過）。
- 10-18 nerf 原創稿被否決，YT 私人片 4pmgVoAbQAM 已刪。新規則（CLAUDE.md）：對談稿不寫原創，給爆款原稿＋逐句直譯，使用者改稿後才建置。前三名原稿直譯在 `refs/dialogue-corpus/originals-zh.md`（不進版控）。`films/nerf` 留作建置骨架，改稿後換稿重建。
- 10-18 對談骨架改 agentmorphy 式運鏡：三機位 wide／host／clawd 都看得到窗外台北 101（`LANDMARK` 參數），同機位連續句不切。對談 #3 改用原稿 A「61 次」（@canwebuildthis DePGWqgThxq，7.40萬讚，10-18 重抓）→ `films/sixty-one`，precheck 34/34，YT 私人 https://youtube.com/shorts/DbFQxJJFmfw 待審（舊黑封面版 TO9u4t84bZE 待刪）。
- 10-18 封面：Threads API 無封面參數、IG 未傳 cover_url 都用第 0 幀。codex 骨架片頭從黑淡入 → 封面全黑（已公開 codex 的 IG／Threads 中招，API 改不了）。修：拿掉淡入、首句字幕從第 0 幀顯示；precheck 加「封面幀」門（第 0 幀亮度 ≥24）＋ tests/test_precheck_cover.py。
- 10-18 xilo-opus-video 採用（`docs/PLAN-xilo-adopt.md`）完成：`scripts/ref_analyze.py`（agentmorphy Dd7fGY6gLbH 14 刀／中位 3.17s、DeEYUXSAtIB 18 刀／2.4s，對上基準）、`scripts/qa_sheet.sh`、precheck 新門「禁止清單」「目視自評」＋ tests/test_ref_analyze.py、test_precheck_review.py，docs/WRITING.md §6。
- 10-18 sixty-one 目視自評抓到瑕疵：女主近景時字幕正後方有一顆浮空紅色航空燈（第 3、7、23 句，手機看得到）。骨架拿掉三顆浮空紅燈（sixty-one、nerf；codex 已公開不動），重渲，precheck 36/36。新版 YT 私人 https://youtube.com/shorts/NKsHf53swxM 待審；舊版 DbFQxJJFmfw、黑封面版 TO9u4t84bZE 待刪。
- 10-18 使用者裁定：直譯原稿有抄襲問題，sixty-one 直譯版不發（私人片 NKsHf53swxM、DbFQxJJFmfw、TO9u4t84bZE 待刪）。規則改成「借結構、台詞重寫」（CLAUDE.md、WRITING §5）；precheck 加「台詞非照抄」門（比對 originals-zh.md 直譯句，相似度 >0.6 擋，圈內梗白名單）＋ tests/test_precheck_copy.py；舊稿 17 句被擋。改編稿草案 `films/sixty-one/DRAFT-adapt.md`。
- 下一步：使用者自己改稿（10-18 說改完再給）→ 覆蓋 narration.md、改分鏡與片名 → 建置 → 私人上傳審。

## 交接 2026-10-20 法國動亂片 `films/france`（使用者已核內容與聲音、說「通過，都發」）

- 狀態：22 句單人旁白、男聲 m3（DECISIONS「單人旁白預設男聲」）、Clawd 主播、125 秒。Codex 反方稽核已綁現稿。審片私人片在悖論小酒館 https://youtube.com/shorts/DQz4usFRpLQ （Eight (Cai) 頻道舊私人片 OvP_LK8Y9oY 使用者說先不刪）。
- 10-20 收尾已做：index.html 加 FACTS＋meta/facts.md；三平台 caption 重寫（結尾用科特雷問句，不加留言提問）；public-path 已產；刪掉日曆殘留「兩週期中假」後背景重建（log /tmp/fr-b.log，鏈：build→deliver→shots→narration_check→qa_sheet）。
- 下一步：① 確認 /tmp/fr-b.log 結尾 CHAIN_EXIT=0；② 看 qa/sheet.jpg、sheet-360.jpg，照 docs/WRITING.md §6 寫 qa/review_log.md（首行 video_sha＝qa_sheet.sh 印的 sha，7 項 ≥8）；③ `python3 scripts/precheck.py films/france` 要 30/30；④ 全過後問使用者一次再發：YT 公開（yt_upload.py）、IG Reels＋Threads（meta_publish.py）。
- 使用者想要但說「算了」的：五項訴求畫面仍全列（現只列兩項），本片不改。
- 10-20 續：/tmp/fr-b.log 鏈在 deliver reels 段被 SIGTERM，qa/dist 是舊版；重跑 deliver→shots→narration_check→qa_sheet（/tmp/fr-c.log CHAIN_EXIT=0）。發現 reels preset 把 125 秒片裁成 90 秒（砍掉落點＋提問）：deliver.sh 對 reels／threads 加 `--allow-long`、規格檢查上限 300 秒（Meta 官方 Reels 15 分、Threads 5 分），並加「交付檔時長要等於成片」硬擋；三檔現皆 125.05s。qa/review_log.md 已寫（sha 7962174…）。precheck 36/37，只剩「鏡頭格線」：卡長跟著配音走（3.46–8.57s）沒有固定格線、seed 只切出 4 刀；兩個偵測器的 17 個切點全落在句間邊界 ±0.17s 內，時間軸沒漂移。改門（有 timeline.js 時改驗切點貼句界）要使用者核准。
- 10-20 續2：使用者核准改門。precheck 加 `cut_boundary_problems`（有 timeline.js 時每個切點要落在句間空檔 ±0.3s），tests/test_rhythm_profile.py 補 5 條（含句中切點要擋、零切點不能過）。france 37/37（4 刀全在句界）；dating-bill 同規則 7/7 過。剩 ④：問使用者一次再發三平台。
- 10-20 已發三平台：YT https://youtube.com/shorts/RJESs62mAgE（public，新上傳；審片私人片 DQz4usFRpLQ 10-20 已刪）、IG https://www.instagram.com/reel/DeteJD9inJM/、Threads https://www.threads.com/@paradoxbar.tw/post/DeteJxCgSEB（記在 meta/published.json）。法國片收尾完成。

- 2026-11-01 13:15 value-life（盧比奧雅典演講「珍視生命」，14 句單人旁白，82s）：precheck 46/46，私人上傳 https://youtube.com/shorts/49NcDbC3R2I 待使用者審片點頭再發三平台。反方稽核兩爭點都 CON_WINS：法赫米德死法只有伊朗官方傳記→旁白寫「伊朗官方說」；第 12 句改講有來源的號召。坑：Qwen 念「待著」ASR 聽成「呆住」（0.87），改「別動」過；「世越號」→「试月号」純同音不收表。
- 2026-11-01 13:35 value-life v2：收尾照使用者口述改成國軍段（不是所有英雄都披披風／國軍也不是不怕死／身後是台灣家庭、多山的小國／從台澎金馬到東沙和太平島／珍惜生命才選擇守護），稿經使用者審過才建。片尾不放提問：precheck 加單片豁免 meta/no-question.txt（使用者核准，說明欄仍留提問）。precheck 43/43，私人上傳 https://youtube.com/shorts/8RLQEDCXLeA ；舊審片版 49NcDbC3R2I 未刪。
- 2026-11-01 15:47 value-life 三平台已發：YT https://youtube.com/shorts/8RLQEDCXLeA 、IG https://www.instagram.com/reel/DfMOlj-lLJG/ 、Threads https://www.threads.com/@paradoxbar.tw/post/DfMOepIGIwR 。舊審片私人版 49NcDbC3R2I 已刪（使用者 11-01 核准）。48 小時後（11-03 15:47）跑 stats.py。
- 2026-11-05 10:55 democracy-noise（選前看懂台北第二集〈民主國家怎麼總是亂？〉，接 taipei-silence，22 句、84s、m4）：第六版稿使用者核准，precheck 46/47（只剩發布時才產的公開路徑），私人上傳 https://youtube.com/shorts/uosNeYvZXxY；使用者要求上下往中間收、主播放大後重做，新審片版 https://youtube.com/shorts/9dnN8jGhBIU （舊版 uosNeYvZXxY 未刪）。建置踩三坑都修在源頭／量法：① Whisper 把「百分之九十七」寫成 97%，`%` 被當標點刪掉卡 0.82 → verify_tts.norm 與 precheck.asr_norm 先轉「百分之N」；② 計數器每幀換數字被 readcheck 當字幕 → 跑數字時不掛 id；③ 封面 OCR 被下方 40 人方陣打亂 → first_frame_text 加裁上 30% 再認一次取多者（判準不變，taipei-silence 照過）。藏字檢查 6 卡加密後全過。選罷法 53 條：11-18 起不放 2026 民調，本片不引用。
- 2026-11-11 00:50 songshan-airport（選前看懂台北第三集〈松山機場遷不遷，都幾？〉，26 句、92s、calm）：稿使用者核准（結尾問句照使用者原話），核准後依反方稽核改 6 句措辭；precheck 46/47（只剩發布時才產的公開路徑），私人試片 https://youtube.com/shorts/DzkXuX5-iM0 ，等使用者看片。建置踩兩坑修在 index.html：① 白卡疊米底藏字後 14 卡低於 0.03 → 白卡加色框（`framed`）、長條底改深色；② 封面副標 62px 低於 OCR 字高 4% 且粗體「遷」認不出 → 副標放大到 88px。片冷讀在最後一次重建（只改副標字級）後沒重跑，戳記沿用。
- 2026-11-11 01:00 songshan-airport 已發三平台（使用者看試片後說「就可以發」）：YT https://youtube.com/shorts/KSvfoWuwAdw 、IG https://www.instagram.com/reel/DfkY5OmgIQs/ 、Threads https://www.threads.com/@paradoxbar.tw/post/DfkY5m-hua8 。發前再改 4 句（柏林句只講時序、九家醫院加「這一派說」、後送改「提議分段接送」、「主要差在順序」改「一大差別在順序」），封面大標拿掉粗描邊；precheck 47/47。直升機安全性異議（衛福部）記在 SOURCES S13 與 YT／IG 說明欄，沒進旁白、Threads 說明欄沒放。舊私人試片 DzkXuX5-iM0 未刪。
- 2026-11-05 11:33 democracy-noise 三平台已發：YT https://youtube.com/shorts/9dnN8jGhBIU （審片私人版轉公開）、IG https://www.instagram.com/reel/DfWEr1YCWmL/ 、Threads https://www.threads.com/@paradoxbar.tw/post/DfWEsABzLdG （記在 meta/published.json）。第一版審片 uosNeYvZXxY 已刪（使用者 11-05 核准）。48 小時後（11-07 11:33）跑 stats.py。
- 2026-11-05 冷讀審核＋黑白對比上線（借 Eian「Claude+Codex+Seedance」流程第 1、2 點）：`scripts/coldread.sh films/<片> script|film`（codex 第二模型、只餵成品，exit 3＝不可用）、`scripts/gray_contrast.py films/<片>`（只回報對比最低 3 卡）、precheck 加「冷讀（稿）」「冷讀（片）」WARN 不擋；SKILL 加 3b／5b 兩步。對 democracy-noise 實跑：稿冷讀 `VERDICT: 不通過`（硬傷 11 條，多為數字單位與「亂」的範圍）；片冷讀 `VERDICT: 不通過`（硬傷 2 條：卡05 Whisper 把「百分之九十七」聽成「90% 70%」、卡22 尾段旁白缺對應卡可核）、小問題另 9 條；灰階對比最低為卡20／卡22／卡03（rms 0.111–0.112，p5_95 卡22 僅 0.047）。已發片不動，這三份結論留作下一支的寫稿與卡片參考。
- 2026-11-05 冷讀引擎備援（使用者：Codex 到期前盡量用，之後走 deep 那條 OpenCode Go）：`COLDREAD_ENGINES` 預設 `codex opencode`，codex 失敗自動換 `opencode-go/deepseek-v4.1-flash`，產物第二行 `engine:`。film 模式字幕改讀 narration.md（Whisper 轉寫造成卡05 假硬傷，改後消失）。opencode 實跑 democracy-noise 看得到圖，但把卡13「乾脆不講」讀成「吃飽不講」→ 它的畫面文字硬傷要對原始碼核。
- 2026-11-05 卡22 冷讀硬傷＝QA 工具誤報：card_sheet.py 末卡取到 dur，拍到 80.37s 後的片尾系列卡；改成末句 t1＋0.3 前結束（test_card_sheet 加測，舊邏輯 FAIL）。democracy-noise 卡22 實際畫面正確（11/28＋同一個家鄉），已發片無誤。
- 2026-11-06 democracy-noise 成片冷讀用新拼圖重跑（codex）：卡22 硬傷消失；剩 1 硬傷卡10「畫面沒寫 Facebook」，但旁白＋字幕第 12 行已講 Facebook，裁決為小問題（畫面可補平台名）。小問題 9 條留給下一支參考。
- 2026-11-06 dunning-kruger（單人旁白 m3、18 句、84.5s，夜間批次建片）：precheck 47/47、exit 0，dist 三平台＋封面就緒，未上傳未發布。`rhythm-profile` 由舊範本殘留的 card 改 calm（既有基準、數字沒動；card 三項全不過：0.14／100%／85s）。approve 戳記依核准檔 status=script_ok 補寫，非使用者原話。反方兩爭點 SPLIT、稿冷讀第 9 句硬傷（WARN）：鉤子、第 9 句、落點「常常只是」比證據寬，稿已核准未動，待使用者看片時裁決；片冷讀通過。
- 2026-11-13 12:10 nvidia-short（Culper 放空輝達、黃仁勳辭職，20 句單人旁白，78s，系列「新聞背後的帳」第 1 集）：v6 稿核准（結尾「司法部對這些公司的調查也還沒結束」），precheck 47/48（只缺發布前的 public_path），私人上傳 https://youtube.com/shorts/Vn-zyhOBy0M 待使用者審片點頭再發三平台。坑：藏字檢查只算亮度跟中位數差 >40 的像素，米色底上白紙／淺紙色（亮度 >200）整張不算，文件改牛皮紙 #E3BE78。片冷讀每輪都挑新項目、不收斂（WARN），修硬傷到 3 項後停。
- 2026-11-17 12:25 nvidia-founder-return（投資人為何要黃仁勳回來，18 句單人旁白，79s，系列「新聞背後的帳」第 2 集）：v7 稿 11-17 核准，build 通過，precheck 47/48（只缺發布前的 public_path），dist/ 三檔已產，11-17 13:31 已發三平台（YT https://youtube.com/shorts/zBwx41X4MsY、IG https://www.instagram.com/reel/Df1LudhjUeW/、Threads https://www.threads.com/@paradoxbar.tw/post/Df1LuNZhCvD）；發前重查新聞，路透引 3 名知情人士同 ABC（董事會沒在考慮），連署已 >18 萬 200；第 5 卡靶心改立在報導旁。舊私人片 HouZv2KEuoo 仍在（舊靶心版），待使用者決定刪不刪。角度「投資人為何要創辦人回來」同題 Shorts 0 筆 ≥10 萬，TREATMENT 如實標「角度未驗證」，爆款證據只驗到事件本身。事實是 11-17 快照，發布前要重查（董事會回應、連署人數、輝達財報台灣時間 11-18 上午）。坑：新機 playwright-core 要 chromium_headless_shell-1243，用 `node ~/dev/lemo-opuscar/node_modules/playwright-core/cli.js install chromium-headless-shell` 裝（`npx playwright` 抓到別版 1255）；SOURCES.md 改一個字就讓反方稽核的 sources_sha 對不上，補充說明寫進 meta/facts.md；nvidia-short 的 `framed` 不在範本，新片要自己帶。
