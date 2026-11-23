# 決議與裁決

共同前提：免費優先，不訂閱、不綁信用卡；能用現成輪子就不自造。

## 1. 起號平台：IG Reels 主場 ＋ Threads 起號引擎，X 不當起點

信心高。

- **X 不做起點**：變現門檻是三道一起——先自己付 X Premium 訂閱、500 粉、近 3 個月 500 萬曝光，而且只有 Premium 帳號的互動算錢，非 Premium 的互動進分析但幾乎不計分。先付錢才能被付錢。
- **IG 當內容主場**：Reels 吃掉演算法權重，靜態貼文自然觸及明顯下滑。變現門檻高（500 粉可收禮物、1 萬粉才有訂閱與直播徽章，Bonus 改邀請制），但不用先付錢。
- **Threads 當冷啟動引擎**：台灣人口占全球不到 0.5%，貢獻超過 22% 的 Threads 流量，全球第一，月活約 350 萬；台灣發文量年增 1294%、留言年增 1933%。Threads 自己變現弱，但是目前華語圈最便宜的冷啟動流量，拿來發雜談、把人導去 IG。
- **YouTube Shorts 當第二落點**：台灣看直式短影音的平台占比是 YouTube Shorts 60%、FB 44%、IG 只有 30%。同一支 MP4 丟三個地方零成本，不要只押 IG。

來源：[X 變現規則](https://kompozy.io/creator-growth/x-creator-monetization-2026)、[X 分潤標準](https://www.auditsocials.com/blog/x-creator-monetization-standards-2026)、[IG 變現](https://kompozy.io/creator-growth/instagram-monetization-2026)、[台灣社群數據報告](https://iseeu.tw/taiwan-social-media-report/)、[Threads 台灣指南](https://www.posify.me/tw/blogs/post/threads-taiwan-guide-2026)

## 2. 題型：Vibe 知識短片，格式已收斂

這波 2026-10 還在高點，抖音在推 #Vibe知識大賞。型態固定得很死：

- 無口播、雙語字幕、合成 BGM（我們刻意偏離「無口播」：2026-10-13 起配旁白，見 VOICE.md）
- 1920×1080 30fps、2:00–2:45
- 純程式碼畫面

吃得開的題材：數學悖論、機率反直覺、冷門定理、哲學概念、歷史考古（有人用三星堆），**收尾一律落到人生道理**。幾十萬讚不少見，單條成本有人報到 1 元人民幣以下。

Tom CC 四條經驗裡最可操作的是第三條：**結尾拋一個人人有自己答案的問題**。他那條拿到 397 則留言，另兩條只有 8 和 11。

## 3. 輪子裁決

### 採用

| 輪子 | 授權／狀態 | 用在哪 |
|---|---|---|
| reelbench-skills（video-shots／video-sync／video-scrub） | Apache-2.0，★196 | ②④⑤⑥ |
| lemo-opuscar | — | ③ 渲染，44 種畫風 |
| ffmpeg-skill | — | ⑤ 三平台匯出 |
| Remotion | ★63k，自訂授權（NOASSERTION） | 備用渲染骨架 |
| Manim | MIT，★41k | 走數理題時加 |
| opencc `s2twp` | — | 簡轉繁入庫（引 10-03 舊卡） |
| mlx-audio ＋ Qwen3-TTS | MIT／Apache-2.0 | ⑧ 配音，見 VOICE.md |

警示：

- **Remotion 是自訂授權**，個人與 3 人以下公司免費商用（目前合規），4 人以上要付費。
- `xiazhuo123456789/vibe-knowledge-video`（★2）**只讀規範不安裝**：它的風格規範逆向自 8 條抖音爆款原片、1091 幀逐秒分析，比文字描述精確得多，但是這幾天才開的、沒有社群驗證。GitHub 上同類 skill 共三個，star 2–5，一律只讀不裝。

### 不做

| 候選 | 理由 |
|---|---|
| **higgsfield** | $15／$34／$84 一個月；而且無旁白知識短片沒有人臉要生成，虛擬 influencer 是空需求 |
| **AI Influencer（擬真虛擬人）** | 格式用不到；要月費；Meta 與 YouTube 自 2024 起要求標示擬真 AI 人物，冷啟動信任度打折；雜談號的辨識度本來就靠本人的品味與觀點 |
| Postiz（排程） | AGPL，且起號期手發三平台花不到五分鐘 |
| trends API | Google 到 2026 都沒有官方 Trends API，市面全是第三方爬公開介面、免費額度 20 次／天；本機 `agent-reach` 與 `/research` 已能做，零成本 |
| video-shotcraft ★11k | 主力是產品宣傳片（網頁截圖＋2.5D 運鏡），跟知識短片重疊少；157 張鏡頭卡可當動效參考 |
| claude-seo ★18k | 給網站做 SEO，沒有網站 |
| Google Drive「AI 編導＋診斷系統」 | 來源不明、內容看不到，是賣課的引流包 |
| 0xcodila「接海外單」 | 實際抓下來的開頭是「公司付 ~$500 買 15 秒影片」；底下回覆是一串小帳號喊 booked／brilliant，像互讚群，可信度低 |
| Podcast 工具 8 款 | 沒做 Podcast，而且全是付費 SaaS |

### 保留的例外

想要一個固定的「臉」來撐雜談，就做**插畫風吉祥物**（lemo 的 `cel-anime-80s`、`rubber-hose` 畫風）。不擬真就不用標 AI，沒有恐怖谷問題，成本是零。

要生成實拍感畫面，Kling 有免費額度可以先試，不訂閱。

## 4. 輪子卡（已登記 `~/.wheel/registry.tsv`）

```
輪子：設定｜採用｜不做　IG Reels 主場＋Threads 起號（X 變現要先付費且只算 Premium 互動）
深度：Standard　降級：無
候選：opencc s2twp（引 10-03 舊卡）｜remotion ★63145 push=10-11 自訂授權個人免費
　　｜manim MIT ★41412｜借鏡 xiazhuo123456789/vibe-knowledge-video ★2（逆向 8 條爆款）
淘汰：higgsfield $15-84/mo 且無旁白片不需虛擬人臉｜postiz AGPL 起號期不需排程｜trends API 本機 agent-reach 已可做
官方：https://www.remotion.dev/docs/pricing
社群共識：台灣貢獻 22% Threads 全球流量、月活 350 萬，為華語圈最低成本冷啟動
警示：Remotion NOASSERTION 自訂授權（團隊超 3 人要付費）；三個 vibe skill 皆無社群驗證，只讀不裝
```

```
輪子：採用 Blaizzy/mlx-audio + Qwen3-TTS（M4 原生、Apache-2.0、實測可跑）
深度：Standard　降級：無
候選：mlx-audio ★8k MIT 10-09 活躍｜Qwen3-TTS ★13.7k Apache｜BreezyVoice ★351 Apache 台灣口音（備選）
淘汰：fish-speech/IndexTTS 研究或自訂授權｜ChatTTS AGPL｜Kokoro 中文弱
官方：https://github.com/Blaizzy/mlx-audio
社群共識：GPT-SoVITS／CosyVoice 為中文開源 TTS 兩大主流
警示：VoiceDesign 每次音色不同，需配聲音複製鎖定
```

## 5. 相關入庫紀錄

- Tom CC 起號提示詞全文（繁體校正版）：`royalskynet/research-reports` commit `a339bcd`，檔名 `REPORT-2026-10-09-Vibe知識短片-Opus5.5-起號提示詞全文.md`
- Hindsight doc_id `tom-cc-opus-5-5-vibe-2026-10-11`（繁中版，內文開頭聲明取代同日的簡體版）
- 簡體原件留在 `~/reports/20261011-X-tom_cc_9986-2108512799517450287.md` 不動
- opencc 的五處誤轉已人工校正：局部最優解（×5）、後台／平台、克制、發布（×2）
- 待收：`~/reports/20261006-X-eval-driven-development.md` 還沒進 research-reports

## 2026-10-11 之後的新片政策

**三平台高播放優先於單一平台。** 之前排的 IG 主場／Threads 起號／Shorts 第二落點不再是取捨順序，三邊都要能跑出數字。

**沒有直式參照就自己造。** 之前因為費馬這題在 YouTube 上找不到高播放的直式短片，就退回去抓橫屏爆款當基準。以後不退：同題沒有直式，就把橫屏爆款的敘事結構拆出來，自己重排成直式分鏡，直式版本由我們定義。

**敘事位置改成旁觀者摘要。** 不用第一人稱講述、不扮演當事人。片子的位置是「一個在旁邊看完整件事的人，把它濃縮給你」。好處是同一套結構能套到任何題目，而且不需要為了代入感編造細節。

以上三條只對新片生效，已經做完的 `local-optimum` 和 `flt-11days` 不重做。

## 預覽畫面要帶文字（使用者 2026-10-20 定）

三平台預覽都拿第 0 幀：Threads API 沒有封面參數，IG 不傳 cover_url 也用第 0 幀。france 第 0 幀大標還在逐字滑出，預覽只剩一張空地圖。

**做法：第一卡大標在第 0 幀就完整顯示**（第一卡不做滑入動畫），一個做法三平台通吃，不另做封面圖。`precheck.py`「封面有字」門用 tesseract 驗：字高 ≥ 畫面 4% 的中文字／數字至少 2 個。只對新片生效；已發的 france、codex、scam-map 不重發。

## IG 自動同步 Threads：沒有這條路（2026-10-11 查證）

問題：發 IG Reels 以後能不能自動同步到 Threads，省掉一組授權。

**答案是不能，證據明確。** 官方 Threads 文件只有反方向：建立 Threads 貼文時帶 `crossreshare_to_ig=true`，會把那篇轉成 IG **限時動態**。限時動態 24 小時消失，不是 Reels，對播放量沒用。IG → Threads 這個方向，Graph API 沒有端點。Meta 2024 測過在 Threads 編輯框手動挑 IG 貼文，當時 Reels 還不支援；2026 沒有任何確認的自動設定，連帶音樂的 Reels 都分享不了。

第三方排程器（OneUp、Buffer）做得到，是因為它們自己打 Threads 發布端點，不是用什麼原生功能。我們也是自己打，所以沒有省到。

結論：Threads 留在授權清單裡，兩組 Meta 憑證都要。`tokens.py` 本來就兩邊都做了，不用改程式。

順便查到兩件事，都改了 `docs/PUBLISH-SETUP.md`：

- **App Review 不需要**，但原因不是我原本寫的「停在開發模式」。Meta 的 Standard Access 就是給只有自己人用的應用程式，免審核免企業驗證。關鍵動作是把自己加成 Tester 再去網頁接受邀請。這解掉 Jev 標 0.78 的那條假設。
- **Threads 應用程式會發兩組編號和密鑰**，要用 Threads 那一組。拿錯會在授權失敗。

### 輪子卡

```
輪子：設定 無（IG→Threads 原生自動同步不存在，官方只有 Threads→IG 限時動態）
深度：Standard　降級：無
候選：Threads API crossreshare_to_ig（方向相反，只進限時動態） ｜ 淘汰：OneUp/Buffer：付費訂閱，且實作方式跟我們一樣是自己打端點
官方：https://developers.facebook.com/documentation/threads/create-posts/share-to-ig-stories
社群共識：2024 的手動挑選測試沒有變成自動功能，vendor 文件說可用性看帳號 https://techcrunch.com/2024/10/09/meta-is-testing-a-feature-to-let-you-post-instagram-reels-directly-on-threads
警示：Meta 發片一定要公開網址（官方原話會去下載媒體），無法繞過
```

## 四個流水線洞：工具都在機器上，裁決沿用舊卡

10-11 的工具盤點說有四個洞，這次查了一輪，結論是**不用重新裁決**。10-11 的輪子卡還沒過期（`review_by` 2026-11-10），裡面 `agent-reach`、`video-shots`、`video-scrub`、`ffmpeg-skill` 全都已經標採用或設定。

本機檢查：四個全部裝在 `~/.claude/skills/`。我上一輪說 `ffmpeg-skill` 找不到是錯的，那條指令的第二個 glob 沒中，zsh 整條中止，我把中止當成不存在。

所以洞不是「缺工具」，是**我沒照卡用**。沿用舊卡，不開新卡。

一個查證到的限制成立：這台的 ffmpeg 沒有 `ass`／`subtitles`／`drawtext` 濾鏡（實測 0 個）。要燒字幕得另裝 ffmpeg-full。我們的字幕畫在 canvas 裡，不走 ffmpeg，所以不影響。

Reddit 429 那個洞的修法改了。原本想改走 `agent-reach`，但那會吃 token，跟趨勢掃描「零 token」的設計衝突。改成在腳本裡加退避重試，判斷力需要的那一步（找同題爆款）才交給 `agent-reach`。

## 公開發布的揭露與浮水印（2026-10-11）

全文在 `docs/COMPLIANCE.md`，檢查在 `scripts/precheck.py`。決議與理由：

**YouTube 的 AI 揭露那題答「否」。** 規則只管寫實內容，定義是「觀眾容易誤認為真實的人、地點、場景或事件」，豁免清單明確包含動畫、明顯不寫實的內容、特效。我們的片是 canvas 畫的網點和排版，沒有一格會被誤認成實拍。旁白也不在範圍內：YouTube 自己的例子寫「複製自己的聲音做旁白」不需揭露、「複製別人的聲音」才要，我們的音色是 VoiceDesign 生成的，沒有對應任何真人。揭露不影響營利，所以這不是「怕降流量才不勾」，是這題的正確答案就是否。

**Meta 的說明文字要寫一句。** Meta 2024 的基準線寫「寫實影片**或聽起來像真的音訊**，經數位創造或改造」。我們畫面不寫實，但旁白確實是聽起來像真人的合成語音，這一條可能落在範圍內，而且我沒找到 Meta 把動畫豁免寫進去。成本是一行字，就寫。

IG 2026-08-31 那個「AI-generated profile」標籤不適用，它針對帳號裡出現 AI 生成的**人物**，我們片裡沒有人物。

**不燒浮水印。** 被平台壓低觸及的是**別的平台的**浮水印，不是重複發布本身；多個來源一致說去掉浮水印懲罰就消失。我們自己渲染母帶，天生沒有任何平台 logo。自己的帳號名燒在角落是品牌選擇，我沒找到任何證據顯示能提升觸及，所以不做。

真正會吃掉觸及的三件，兩件我們天生避開：

- 說明文字每個平台要不一樣（多來源說複製貼上同一段會壓低互動）。要做，已寫三份。
- 不要用平台內建曲庫的音樂，那種授權不能跨平台。我們配樂是 `mix.py` 生成的，天生避開。
- 錯開 30 到 90 分鐘發。只有單一來源，證據弱，照做沒成本但不要當成有根據的規則。

**公開網址用隨機 token，不用片名。** Meta 發片時會自己來下載影片，mp4 必須先在公開網址上。用片名當路徑別人猜得到，也能順著猜其他片。每次發布產一個 `secrets.token_hex(16)`，只開那一支，發完就關。Funnel 開著那段時間對整個網際網路可見，不只 Meta。

## 不做：用 CUA 或瀏覽器代理代勞平台授權（2026-10-11）

建應用程式只有網頁沒有 API（Meta 文件全是儀表板流程；Google 的 `gcloud iam oauth-clients create` 鎖在 Workforce Identity 和 IAP，而 IAP 的 OAuth API 已標記淘汰）。所以機器代勞就得登入真帳號，而 Google 2020 的開發者政策明文禁止「自動化按鍵或點擊的腳本，特別是用來自動登入的」。代價是 YouTube 頻道帳號被標記或鎖住，收不回來。

省下的只有一次性十五分鐘，之後權杖自己續。不划算。

候選本身都健康，出局不是品質問題：browser-use ★117632 MIT、playwright-mcp ★38019 Apache-2.0、trycua/cua ★29358 MIT，全部活躍。哪天要上沒有 API 的平台（小紅書、抖音），這張卡要重開。

## 瓶頸在量與分發，不在工藝（2026-10-20）

三支公開片 120h 播放 871／185／143，dating-bill 109h→122h 只多 2 次，沒進推薦流。再加閘門換不到播放。
改投分發：一片多形態、Threads 文字貼排程、熱點快線、系列化。規則與指令 `docs/DISTRIBUTION.md`。
輪子裁決：文字貼／自引用／排程擴充既有膠水（ThreadsPipe-py、pythreads 月下載數百，不採用）；
他人貼文回覆 API 做不到（keyword_search 未過審）改手動；翻譯搬運片不做。

## 政治熱點做中立公民教育，不排除（2026-10-20）

使用者定：政治熱點照收進選題，但片子改做無關立場的政治參與或理論科普，例如「民主不是對抗，是分權與監督」。
不評人物、不選邊；熱點只當鉤子，內容講制度與機制。綜藝剪輯（康熙來了等）仍不收。
cabinet `collectors/mkt_trends.py` 的竄升榜候選命中政治詞會標「政治題→做中立公民教育」。

## 單人旁白預設男聲：m3（2026-10-20）

使用者審法國片後說「這個男聲音很棒，留著」。單人旁白片（專題報導懶人包）預設用 `assets/voice/m3-24k.wav`（聲音描述 `assets/voice/m3-design.txt`、範本台詞 `assets/voice/m-script.txt`），`pace.json` 設 `tempo: 1.2`、`gap_line: 0.4`、`gap_section: 0.8`。設定方式照 `films/france/cast.json` 的 `host.ref`。

使用者要的是沉穩專業、有磁性、語速明快的台灣男記者，不捲舌，不要死氣沉沉。m2 範本語速對了但不夠磁性，女聲 D 和 Clawd 音色在嚴肅新聞題太輕快。對談片的女主＋Clawd 不受這條影響。畫面主播仍用 Clawd。

## 新片改回單人旁白科普（2026-10-29）

使用者看完 gamble-odds 對談稿說「不要用這種對話方式，根本都沒有邏輯，參考之前科普片與爆款，尤其參考 @boundless__explorer 跟之前悖論小酒館」。新片預設改為 m3 單人旁白、一支一個機制，寫法 `docs/WRITING.md` §7；對談格式（§5）只在使用者點名時用。選題仍以爆款為準，題材不限（10-29 使用者定：直銷、政治、幣圈都可，科普角度）。

## 範本換成 taipei-silence：插畫風、只封面有大標（2026-11-04）

使用者問「為何參考帳號的畫風比較精緻」。比對無邊探索 DetyMeyh7-q 與 taipei-silence 拼圖：對方人物有四肢與姿勢、道具有細節與陰影、內頁只有系列標＋畫面＋一行字幕；我們是圓頭方身體、平面幾何、每卡疊大標。做了插畫庫 `assets/illust/`（Humaaans／Open Peeps 皆 CC0 但風格不符，自造），taipei-silence 改用它並拿掉內頁大標，precheck「內頁大標」門擋 ≥72px。使用者核准新片範本從 elected-dictator 改成 taipei-silence；pace.json 同步成 tempo 1.15／0.45／0.8。

## 寫稿擂台＋查證與評審外移（2026-11-06）

使用者退 dunning-kruger（「稿子太無聊，後面沒有爆點」），要「看誰比較會寫」。寫稿規則加 `docs/WRITING.md` §8 爆點結構（借 Melvynx/video-agent-skills，MIT），`scripts/bakeoff.py` 讓 Opus／Fable／Codex／DeepSeek 拿同一份 FACTS.md 寫稿，兩兩換位盲評（MT-Bench 做法）。兩題實測：hsr-umbrella Fable 勝、mrt-escalator Opus 勝（使用者選 Opus 版建片）；評審都偏自己的稿。
使用者再定「省 Claude token」：評審預設改 codex＋deepseek；事實查證改派o，`scripts/facts.py task <slug> "<題目>"` 產工單、`facts.py check` 當驗收。check 要求每個數字寫口徑，起因是 mrt-escalator 把「一座梯一週五個早上尖峰合計」寫成「尖峰一小時」，建片時才被反方稽核抓到。寫手保留 Opus／Fable，建片仍是 Opus。

## 2026-11-10 寫稿原則改成量無邊探索的形狀，刪掉固定四段模版

使用者：「這個寫稿原則不行，砍了吧」「刪掉現有的旁白稿結構檢查，重新改成從 boundless 學習旁白稿、影片節奏」。

- `precheck.py` 的「旁白稿結構」門：刪掉必備段名與順序、轉折首句連詞、鉤子 25 字上限、「你」密度 0.4。留下的只有對標帳號 11 支實測成立的：段數 ≥3、開場 60 字內有「你」或問句、一行 ≤35 字且一個句末標點、逗號短語 ≤18 字、最後一段不總結、正片無提問段、對舉與破折號各 ≤1。
- `docs/寫稿原則.md` 整份重寫成「量到什麼就寫什麼」，樣本仍是 11-03 的 11 支 reel；`docs/WRITING.md` §3、§7 第 9 條同步。
- WRITING §8 爆點結構改為選配，不再由閘門驗。
- 未抓到 11-03 之後的新片：這台沒有瀏覽器，IG 需登入；新樣本要等下一次有機器可抓時再補。
