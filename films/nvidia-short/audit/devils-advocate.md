# Devil's Advocate Evidence Pack

Report: /Users/you/dev/vibe-shorts-pipeline/films/nvidia-short/audit/claims.md
Reviewed: 2026-11-13
Core conclusion as read: 核心結論＝旁白稿逐句陳述的事實。

## 爭點 1
FLAG: extrapolation
TARGET: 輝達財報寫，禁令後那一季，特規晶片一片都沒賣給中國客戶。
ATTACK: scope
OBJECTION: 財報的零銷售聲明明確限定 H20、FY2026 第二季及 China-based customers。旁白省略型號與季度日期，若將「特規晶片」讀成所有中國特規產品，便超出原文。應限縮為「截至二〇二五年七月二十七日那一季，H20 沒有銷售給中國境內客戶」。這條聲明也不能證明全年中國運算營收歸零。反證只確立原文範圍，沒有證明該季另有其他特規型號銷往中國。
EVIDENCE:
- URL: https://nvidianews.nvidia.com/_gallery/download_pdf/68af69043d6332f1d02dec91/
  DATE: 2025-08-27（FY2026 第二季財報；季度截至 2025-07-27）
  EXCERPT: "There were no H20 sales to China-based customers in the second quarter."
IMPACT: narrow

## 爭點 2
FLAG: inference
TARGET: 同時東南亞的帳一直衝，他覺得對不上。
ATTACK: comparison
OBJECTION: H20 對中國境內客戶零銷售，與新加坡帳單營收增加，並不構成財報上的直接矛盾。SEC 原文說明地區營收按帳單地址分類，終端客戶與出貨地可能不同；該期開票至新加坡的受管制資料中心運算營收，超過 99% 是美國客戶訂單。旁白下一句已保留後一項公司說法，因此反證只能窄化「對不上」所暗示的證明力，不能推翻 Lamarco 確實提出疑問，也不能排除個別轉運。這組帳單數據本身不足以證成中國終端需求，更不能單獨證成兩成估算。
EVIDENCE:
- URL: https://www.sec.gov/Archives/edgar/data/1045810/000104581025000209/R20.htm
  DATE: 2025-08-27（10-Q；季度截至 2025-07-27）
  EXCERPT: "Revenue by geographic area is based upon the billing location of the customer."
- URL: https://www.sec.gov/Archives/edgar/data/1045810/000104581025000209/R20.htm
  DATE: 2025-08-27（10-Q；季度截至 2025-07-27）
  EXCERPT: "Customers use Singapore to centralize invoicing"
IMPACT: narrow

## 爭點 3
FLAG: self-reported-only
TARGET: 一年後變三十億，翻了快九十倍。
ATTACK: premise
OBJECTION: NO_EVIDENCE_BACKED_OBJECTION
EVIDENCE:
- URL: https://threadreaderapp.com/thread/2054623784452120917.html
  DATE: 頁面標示 May 13，未顯示年份（搜尋索引標為 2026-05；不據此獨立確定年份）
  EXCERPT: "from $33M at year-end 2023 to $3.0B at year-end 2024"
IMPACT: retain

## 搜尋與限縮紀錄

- 爭點 1 搜尋 NVIDIA second quarter fiscal 2026 H20 no sales China 99% Singapore US customers，實際開啟原始財報 PDF。原文足以限縮用語，未找到足以反向證明該季其他中國特規晶片銷售的實據。
- 爭點 2 另搜尋 Nvidia Singapore billing location revenue not China 99 percent 2025，實際開啟 SEC 的 Segment Information 頁。該頁是公司申報，不是獨立查驗晶片最終用途的結果。
- 爭點 3 搜尋 Megaspeed assets 33 million 3 billion 2024 Culper Nvidia，開啟 Culper 原始 PDF 時遭 403，未引用其搜尋摘要。其後實際開啟 Culper 貼文的 Thread Reader 轉載。數字符合目標句；30 億除以 3,300 萬約為 90.91 倍。沒有取得公司登記原件，也未找到與數字相反的實據。轉載仍屬 Culper 自述，不能充當獨立佐證；來源層級限制本身不等於數字錯誤。
- 另實際開啟報告所列 CBS 頁作背景核對，未用它建立反證。各爭點實開來源均未超過三個；搜尋結果摘要未當作實開證據。

Engine: codex
