# Devil's Advocate Evidence Pack

Report: /Users/51mini/dev/vibe-shorts-pipeline/films/nvidia-trump-call/audit/claims.md
Reviewed: 2026-11-25
Core conclusion as read: 因為要是真讓他飛走，飛走的是美國手上最厚的一張牌。

## 爭點 1
FLAG: inference
TARGET: 照他的推演，美國守了好幾年的領先，一夜之間就沒了。
ATTACK: inference
OBJECTION: 「一夜之間」將川普對人才流失的憂慮加強為具體的技術轉移速度。CNBC 原文有赴中任職的假設，卻也記載他承認未收到任何實際暗示；因此不能把假設當成已知招聘動向。另一份黃仁勳本人訪談把輝達最重要的優勢歸於 CUDA 安裝基礎與開發者生態，削弱「一個人移動即可立即移轉全部領先」的推論。這些證據支持限縮時間與因果措辭，未證明人才流失沒有風險，也未推翻川普確曾提出這項假設。
EVIDENCE:
- URL: https://pressroom.versantmedia.com/cnbc/press-releases/cnbc-transcript-president-donald-trump-speaks-cnbcs-eamon-javers-and-squawk
  DATE: 2026-11-23
  EXCERPT: "Never even a suggestion."
- URL: https://lexfridman.com/jensen-huang-transcript
  DATE: 未標示
  EXCERPT: "Our single most important thing today is the install base of CUDA."
IMPACT: narrow

## 爭點 2
FLAG: single-source
TARGET: 頂級晶片完全不吃這套，它複雜到對手光要仿製，就得花好幾年。
ATTACK: scope
OBJECTION: 原始專訪支持「川普如此形容」，沒有確立旁白語氣中的技術事實。川普在估算 Blackwell 的領先年數時明言自己不知道，並列出多個猜測數字；領先幾年也不能直接換算成對手仿製所需年數。旁白應保留說話者與估算的不確定性，不能將這段談話擴為所有頂級晶片的已驗證仿製門檻。本次未找到直接證明 Blackwell 已被成功仿製的證據；反證只足以限縮確定程度與適用範圍。
EVIDENCE:
- URL: https://pressroom.versantmedia.com/cnbc/press-releases/cnbc-transcript-president-donald-trump-speaks-cnbcs-eamon-javers-and-squawk
  DATE: 2026-11-23
  EXCERPT: "I don't know what it is. Maybe 2, 3, 4 years"
IMPACT: narrow

<!-- 稽核範圍與來源紀錄
爭點 1 搜尋：Trump Huang CNBC "overnight" "lead" November 23 2026；Nvidia Blackwell engineers team design Jensen Huang chip complexity。
爭點 2 搜尋：Trump CNBC Huang "Beijing" "mats" November 23 2026；Trump Jensen "three chips" "brain" CNBC November 23 2026。
兩項爭點皆實際開啟 CNBC 原始逐字稿；爭點 1 另實際開啟 Lex Fridman 訪談逐字稿，核對 01:15:20 的黃仁勳發言。
每項爭點使用的不同來源頁均未超過 3 頁。Lex 訪談頁面未標示發布日期，不據搜尋摘要填入日期；僅作企業優勢結構的補充，未當作 2026-11-25 的最新狀態證明。
未對報告作裁決或修改；本證據包的 IMPACT 是反方主張的影響範圍。
-->

Engine: codex
