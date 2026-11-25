# Devil's Advocate Evidence Pack

Report: /Users/51mini/dev/vibe-shorts-pipeline/films/scam-map/audit/claims.md
Reviewed: 2026-10-14
Core conclusion as read: 核心結論＝旁白稿逐句陳述的事實。

## 爭點 1
FLAG: extrapolation
TARGET: 全台灣最常被詐騙的城市，你猜是哪裡？
ATTACK: scope
OBJECTION: 報告的排名是電信網路類詐騙受理件數除以戶籍人口，不能直接擴張成所有詐騙、所有被害人的城市排名。報告引用的彙整頁明確限定縣市資料只涵蓋電信網路類；官方則稱指標為「詐欺犯罪受理件數」。即使新竹市的計算排名正確，鉤子仍須限定為該類別每人口受理件數最高。此反證窄化排名的意義，沒有推翻新竹市在既定指標下第一。
EVIDENCE:
- URL: https://fromnineon.com/data/taiwan-fraud-statistics/
  DATE: 2026-10-08
  EXCERPT: 縣市資料只涵蓋電信網路類詐騙。
- URL: https://www.npa.gov.tw/ch/app/data/view?id=2206&module=wg054&serno=7218ce42-167b-489b-817b-71fcce2af534
  DATE: 2025-05-01（更新日期）
  EXCERPT: 113年9月至12月「165打詐儀錶板」詐欺犯罪受理件數
IMPACT: narrow

## 爭點 2
FLAG: extrapolation
TARGET: 去年警方的反詐騙平台，全台受理十五萬六千件。平均每一百四十九個人，就有一件。
ATTACK: scope
OBJECTION: 156,411 是同一平台的電信網路類小計，並非平台全年全部受理數。報告的補充口徑承認全類別 176,242 件，卻以「平台受理」作為旁白限定；這個限定仍包含其他類別，沒有解決分母範圍問題。已開啟的彙整頁同時列出兩個數字及類別，因此反方不是拿別套刑案統計硬比。應把旁白限定為電信網路類；149 人一件也只能跟隨這個限定，不能當平台全部案件的率。
EVIDENCE:
- URL: https://fromnineon.com/data/taiwan-fraud-statistics/
  DATE: 2026-10-08
  EXCERPT: 2025 年全年 165 受理詐騙案件 176,242 件
- URL: https://fromnineon.com/data/taiwan-fraud-statistics/
  DATE: 2026-10-08
  EXCERPT: 電信網路詐騙整體  | 156,411  | 48.2  | 97,856  | 39.9
IMPACT: narrow

## 爭點 3
FLAG: single-source
TARGET: 大家最怕假投資，它騙走了一半的錢。
ATTACK: comparison
OBJECTION: NO_EVIDENCE_BACKED_OBJECTION
EVIDENCE:
- URL: https://fromnineon.com/data/taiwan-fraud-statistics/
  DATE: 2026-10-08
  EXCERPT: 投資詐騙：月排行中「假投資詐騙」加「假交友(投資詐財)詐騙」。
- URL: https://fromnineon.com/data/taiwan-fraud-statistics/
  DATE: 2026-10-08
  EXCERPT: 2025 年投資詐騙占電信網路詐騙件數 25.1%，財損卻占 70.9%。
IMPACT: retain

## 查核限制與停損

- 各爭點均完成搜尋與實際開頁。爭點 1 搜尋縣市受理與被害人口徑；爭點 2 搜尋 2025 年 165 全年受理 176,242；爭點 3 搜尋 2025 年投資詐騙財損占比與 70.9%。每個爭點使用的不同來源頁均未超過三頁。
- 爭點 3 的 70.9% 包含假交友投資詐財，與報告單獨的「假投資詐騙」不是同一分類，不能用來推翻 51%。沒有找到同年、同分類、同分母的直接反證，故保留並明記 NO_EVIDENCE_BACKED_OBJECTION；財損資料也不能回答「大家最怕」的心理排序。
- 韭點開始為第三方彙整，數值及介面口徑是其自述；本包不將其升格為官方原始數據核驗。官方儀錶板首頁實際開啟回傳 Internal Error，未作證據引用。爭點 1、2 支持限縮措辭，不足以重算或推翻報告的縣市排名。
- 僅使用指定報告、協定與此次網搜開啟內容；未讀取報告提到的 data/ 檔案，未修改報告，未進行裁決或第二輪辯論。

Engine: codex
