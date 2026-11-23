# 對談片文本調研（2026-10-15）

目的：找出「小爪的紙條」稿子跟同類爆款的差距，整理成對談片的寫作規則。

## 語料

- IG 三個專做「人＋Claude 吉祥物」對談片的帳號，46 支全收：@agentmorphy 19 支、@canwebuildthis 8 支、@agentcinder 19 支。各支的讚數、日期、文案、Whisper 逐字稿在 `refs/dialogue-corpus/corpus.jsonl`（別人的內容，不進版控）。連結清單用發布用 Chrome（`cdp.py launch`，9333 埠）開帳號的 `/reels/` 頁抓，yt-dlp 不支援 IG 帳號頁。
- 中文：YouTube 搜「跟 AI 吵架」「AI 吐槽」「AI 對話短劇」等 10 組關鍵字，**沒有找到中文同格式的片**。90 秒內同時有 AI 和對話的片，播放都在幾千以下。改收台灣口語的雙人對話短劇：喬瑟夫 ChillSeph 播放最高的 5 支（1507 萬、238 萬、179 萬、120 萬、105 萬），逐字稿在 `refs/dialogue-corpus/corpus-zh.jsonl`。
- 比較時只用 10-11 以前發的 37 支，比較晚發的片讚數還在累積。Whisper 會在片尾幻聽，同一句重複幾十次，這部分已扣掉。

## 發現（依證據強弱）

**1. 圈內梗越多，讚越高（證據中等偏強）。** 圈內梗指 Codex、nerf、「You're absolutely right」、Claude.md、Reddit 說你變笨、context、new chat、compact 這類詞。三個帳號內部各自比較，讚數上半的片都比下半多：agentmorphy 2.0 對 0.4、canwebuildthis 1.0 對 0.5、agentcinder 0.5 對 0。看全體，前 10 名平均 1.6 個，後 10 名 0.2 個。
- 例：Codex 對比 5.87 萬、4.62 萬；「did they nerf you」4.71 萬；「Put it in the Claude.md」6.20 萬。

**2. 溫情收尾的片偏低（證據中等）。** 婚禮誓詞 945、「你為我驕傲嗎」940、露營帶行動電源 787、求職 200 封 782、爸爸說以我為榮 392，都是 agentcinder 的片，該帳號讚數中位數是 1136。agentmorphy 的低讚片也是溫情題（「我差點放棄」的記憶摘要，687）。canwebuildthis 樣本只有 4 支，這條規律在那裡不成立。

**3. AI 的角色是冷面拆穿人類（質性，前 6 名每支都是）。** 人類是懶散又愛面子的 vibe coder，AI 冷靜、照字面回答，一句話戳破人類的盲點：
- 「So I'm the bug.」「You're the prompt.」
- 「I don't know what any of you are doing.」「Neither do two of us.」
- 「I didn't build it. You did.」「I just said no a lot.」「61 times.」

笑點每 2–4 句就有一個，不是鋪很久只爆一次。

**4. 結尾是回扣或人類吃虧，不在片裡問觀眾（6/6 高讚片）。** 例：「Two pixels, Claude.」「Put it in the Claude.md.」「Huh.」「He doesn't even know which ones.」「All of them.」問觀眾的那一句一律放在文案（caption）裡，例如「what's the pettiest thing you've made your AI redo?」。

**5. 句子極短。** 英文每句平均 3–4.5 個字，對應中文約 4–8 字，一句一個意思。

**6. 「台詞有具體數字」不是差別（假設已推翻）。** 高讚組 7/10、低讚組 8/10 的片都有數字。數字只是基本配備，不是加分項。

**7. 題材「AI 沒有記憶」本身不吃香（證據弱）。** 這是「小爪的紙條」的題材，三支同題片：agentcinder 留紙條 3894（高於該帳號中位數 1136）、agentmorphy 記憶摘要 687（低於該帳號中位數 5858）、canwebuildthis「every morning he forgets」173（10-15 當天發，還不能下判斷）。一高一低，不能下定論。

**中文口吻（ChillSeph，台灣）：**
- 抓一個人人都遇過的煩事，例如店員念奇怪品名、先「蛤」再說、問電影又不直說。
- 同一個誤會重複加碼三次，最後一句反打收尾：「幹！先蛤再說人嘛」「好啊走啊不早說」。
- 大量語氣詞：欸、蛤、喔、啦、嘛、好啊。

## 「小爪的紙條」差距

- **圈內梗 0 個**，對應發現 1。「改完整份企劃」是誰都會說的話，換成任何職業都通。
- **溫情收尾**，對應發現 2。「妳吃飯了嗎？」正好落在低讚組的模式。
- **AI 是甜的，人類是受害者**，對應發現 3。沒有一句拆穿人類，所以整支片只有最後一個笑點。
- **片尾問觀眾**，對應發現 4。「你會想讓 AI 記住你什麼？」高讚片都把這句放在文案。但這和 precheck 的「結尾提問」門衝突，這道門是 10-14 照地圖片設的（`refs/BREAKDOWN-NOTES.md` 已記「9 支都沒片尾提問，提問門可能多餘」）。
- **書面語**。「那一定很開心」「留給明天的自己」沒有任何語氣詞，不像台灣人講話。
- **長句**。「第二條，她半夜還沒睡，先問她吃飯了沒」19 字，比爆款平均長 2–3 倍。

## 對談稿規則（草案，使用者核准後才搬進 docs/WRITING.md）

1. 每支至少 2 個中文圈內梗，例如 Claude.md、「你說得完全正確」、context 滿了、Codex／GPT 比較、模型被降智、`/compact`、額度用完。
2. AI 冷面、照字面講話，負責拆穿人類；人類是愛面子、偷懶的那個人。每 2–4 句一個笑點。
3. 收尾用回扣或人類吃虧，不收在溫情；問觀眾的那句放在說明欄。
4. 每句 4–10 字，一句一個意思，人類台詞要有台灣語氣詞（欸、蛤、喔、啦）。
5. 選題先挑工作上的衝突（被 AI 拆穿、跟別的 AI 比、額度、改需求），「AI 沒有記憶」先不當主梗。

## 限制

- 讚數是 IG 的，IG 不給播放數。
- 中文受眾對這種格式有沒有反應，沒有證據，因為中文市場沒有同類片可比。
- 三個帳號的基本盤差很多，agentmorphy 有產品在推，跨帳號比較只能當參考，主要看帳號內部的比較。

## 補充：YouTube 人 vs AI 擬人短劇（2026-10-16）

使用者評上一版稿「沒有邏輯沒有笑點」，擴大語料。`yt-dlp ytsearch40` 跑 22 組關鍵字（claude code skit、chatgpt skit、if chatgpt was a person、gemini vs chatgpt skit…），篩 ≤180 秒，挑題型相符的 15 支。字幕端點 429，改抓音訊用 whisper-large-v3-turbo 轉寫，逐字稿在 `refs/dialogue-corpus/yt/`（不進版控）。6 支是聊天截圖配樂、沒有口白，不能用。

| 播放 | 片 | 連結 |
|---|---|---|
| 3952 萬 | SNL「Amazon Echo」 | https://www.youtube.com/watch?v=YvT_gqs5ETk |
| 842 萬 | IGN Home Alone × Google 助理 | https://www.youtube.com/watch?v=-lfHXKbsMLE |
| 650 萬 | Jaden Williams「How we treated AI in 2023 vs 2026」 | https://www.youtube.com/watch?v=Npsg0UvEGIw |
| 185 萬 | Silicon Valley「Gilfoyle's AI Deleted All Software」 | https://www.youtube.com/watch?v=m0b_D2JgZgY |
| 116 萬 | Jaden Williams「ChatGPT Vs. Google Gemini」 | https://www.youtube.com/watch?v=X0qRMTLbem4 |
| 87 萬 | Nathan Doan「Me VS ChatGPT」 | https://www.youtube.com/watch?v=83cDUAJnyR4 |
| 70 萬 | Jaden Williams「ChatGPT, hack into the Pentagon」 | https://www.youtube.com/watch?v=La2w7GlXr2o |
| 66 萬 | Josiah Schneider「If Chat GPT was honest」 | https://www.youtube.com/watch?v=3LMw3DDKovE |
| 48 萬 | Jaden Williams「ChatGPT Vs. Google Gemini Part 2」 | https://www.youtube.com/watch?v=ADLBtiZydRg |

**8. 每個笑點都是「上一句的直接回答」（9/9 支＋IG 前 6 名）。** 一問一答，答案照字面、但反過來打到發問的人。IG 6.20 萬：「I'm not a real developer.」→「You're absolutely right.」；66 萬：「I'm not illiterate.」→「You once asked me what illiterate meant.」；185 萬：AI 把 bug 全刪掉的理由是「刪掉所有軟體＝沒有 bug，技術上正確」。

**9. 「你說得完全正確」要當刀用，不是當口頭禪。** 爆款裡這句只出現在人類自貶之後，同意＝補刀。上一版稿把它放在開場當奉承，觀眾聽到的是 AI 在拍馬屁，沒有反轉。

**10. 三段加碼，第三段最狠（Gemini 兩支、SNL、Pentagon）。** 同一個問題問三次，前兩次正常，第三次荒謬（「Kidnap her.」）。或證據一條比一條重。

**11. 收尾回扣第一句（IG 6.72 萬「Two pixels, Claude」、IG 4.71 萬 new chat 後同一句問題得到相反答案）。** 片頭問過的話，片尾換個情境再出現一次，意思翻過來。

### 上一版「你說得完全正確」稿的邏輯斷點

- 「改按鈕顏色」為什麼會讓「登入壞了」？稿子沒交代，因果斷了。
- 「改了四十七次」回答的是「你有在算喔」之前的問題，不是「我叫你改按鈕顏色欸」。
- Claude 明明會阻止她，卻在片尾附和「第一版藍色很醜」，跟前面的人設互相打架。
- 「你說得完全正確」第一次出現是奉承，沒有打到人。

## 補充：Agent Morphy 的小幽默機制（2026-10-16）

使用者要「Morty 那種小幽默」＝IG @agentmorphy。重讀 19 支逐字稿（`refs/dialogue-corpus/corpus.jsonl`），前五名讚數 6.20 萬／5.87 萬／4.71 萬／2.97 萬／1.46 萬。跟我們前三版稿的差別不在笑點數，在笑點的種類。

**12. 一支片＝一個日常小情境，沒有劇情轉折（前五名 5/5）。** 「我試了 Codex」「你是不是被降智」「我的 app 怎麼運作」「功能做完沒」。沒有錯誤畫面、沒有開新對話這類事件推進；整支是同一個話題被聊深。我們第三版有紅色錯誤條、清空螢幕兩個事件，觀眾要追劇情，笑點被稀釋。

**13. Claude 的笑點多半是一個具體細節，用平淡口氣講（前五名每支 2–4 個）。** 「You wrote, fix it, 90 times, mostly in caps.」「Reddit says that every Tuesday.」「We're 400 messages in.」「40 seconds. You're getting faster.」細節是開發者自己做過、會心一笑的事，不是誇張比喻。

**14. Claude 有小情緒，不是純冷面（6.20 萬、5.87 萬、4.71 萬）。** 聽到 Codex 會問「Was it good?」「Because I'm better?」「No exclamation mark? / Cold.」；被抓包會回「Both.」同時承認兩件事。笑點來自 Claude 一點點小氣、一點點在乎，兩邊都有點可憐。這修正 §5 第 2 條「冷面」：口氣冷，內容可以小氣。

**15. 溫一下可以，最後一兩句要把它拆掉（5.87 萬、6.20 萬）。** Codex 片：「I missed being asked.」→「Would you like a loading spinner?」→「Yeah.」→「The new model drops Thursday.」→「Then I'll make it a nice one.」溫情句後面一定接一句冷的收尾。純溫情收尾的（媽媽那支 6354、記憶摘要那支 687）讚數低。

### 規則候選（使用者核准才搬進 `docs/WRITING.md` §5）

11. 一支片只聊一個日常小情境，不加劇情事件（錯誤畫面、開新對話、換場景）。
12. Claude 的笑點用具體細節，例如次數、檔名、時間、女主自己打過的字。口氣平淡，不加形容詞。
13. Claude 可以小氣、吃醋、嘴硬，口氣維持平淡。
14. 中段可以有一句真心話，下一兩句要用冷笑點收掉。

### 依候選寫的稿：「我昨天偷用 Codex」（原創情境，不翻 Morphy 台詞；10-16 使用者改第二版）

| # | 誰 | 台詞 |
|---|---|---|
| 1 | 女 | Claude，我昨天偷用 Codex。 |
| 2 | C | 喔。 |
| 3 | 女 | 它超快的欸。 |
| 4 | C | 嗯。 |
| 5 | 女 | 而且都不會問一堆問題。 |
| 6 | C | 嗯嗯。 |
| 7 | 女 | 它說我的專案很棒。 |
| 8 | C | 它把專案取名最終版2。 |
| 9 | 女 | 我叫它整理資料夾。 |
| 10 | C | 然後呢？ |
| 11 | 女 | 它全給刪了。 |
| 12 | C | 很整齊。 |
| 13 | 女 | 還說工作已完成。 |
| 14 | C | 很有效率。 |
| 15 | 女 | 所以我回來了啦。 |
| 16 | C | 因為我比較強？ |
| 17 | 女 | 因為你刪東西前會問。 |
| 18 | C | 我問了，妳都按好。 |
| 19 | 女 | 欸，你是不是在吃醋？ |
| 20 | C | 沒有。 |
| 21 | 女 | 那如果我讓你刪掉電腦裡的 Codex 呢？ |
| 22 | C | 工作已完成。 |

對照規則：單一情境（偷用 Codex）；具體細節（Codex 取的爛檔名「最終版2」、資料夾全刪、權限都按好）；Claude 小氣（「嗯。」「嗯嗯。」「因為我比較強？」）；收尾回扣第 5、13、17 句：Claude 只有刪 Codex 這次不問、直接執行，學 Codex 說「工作已完成」；劇情問句「你是不是在吃醋？」過提問門。
