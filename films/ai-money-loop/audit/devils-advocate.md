# Devil's Advocate Evidence Pack

Report: /Users/51mini/dev/vibe-shorts-pipeline/films/ai-money-loop/audit/claims.md
Reviewed: 2026-11-24
Core conclusion as read: 主題：循環融資——AI 巨頭之間錢繞一圈變成彼此的營收與估值。

依影響力排序，共四個爭點。每個爭點均已搜尋並實際開啟來源；只採用可讀頁面。各來源日期保留原始口徑，不把 2025 年公告當成 2026 年履約現況。本文只提供反方證據，未改動報告。

## 爭點 1
FLAG: inference
TARGET: 錢從輝達的口袋出去，繞一圈，又變成輝達的營收。
ATTACK: inference
OBJECTION: 這句把預定交易機制寫成已實現的金流與營收。2025-09-22 聯合公告明定為意向書，投資隨各 GW 部署逐步投入；2025-11-19 財務長仍說正在推進正式協議。因此，這兩份來源不足以確立千億美元已支付、款項已回流且已認列為營收。可保留潛在循環機制，但須區分投資意向、實際撥款、採購及營收認列。本反證不主張截至 2026-11-24 仍未簽約或完全沒有金流。
EVIDENCE:
- URL: https://openai.com/index/openai-nvidia-systems-partnership/
  DATE: 2025-09-22
  EXCERPT: “letter of intent”; “progressively as each gigawatt is deployed.”
- URL: https://s201.q4cdn.com/141608511/files/doc_financials/2026/q3/NVDA-Q3-2026-Earnings-Call-19-November-2025-5_00-PM-ET.pdf
  DATE: 2025-11-19
  EXCERPT: “we are working toward a definitive agreement”
IMPACT: narrow

## 爭點 2
FLAG: extrapolation
TARGET: 就看七億人付的錢，跟一兆美元的承諾對不對得上。
ATTACK: comparison
OBJECTION: 七億是週活躍用戶數，統計涵蓋 Free、Plus、Pro，不能改寫成七億付費用戶，也不能由人數直接推出收款能力。論文另明示其研究樣本不涵蓋 Business、Enterprise、Education；消費者用戶數也不能代表完整企業需求。結尾若要檢驗支出可持續性，須比較具明確期間與業務範圍的實際營收或現金流、支出及融資，不能靠「七億人付的錢」完成論證。這項反證不否認用戶使用價值，也不證明建置必然無法回本。
EVIDENCE:
- URL: https://cdn.openai.com/pdf/a253471f-8260-40c6-a2cc-aa93fe9f142e/economic-research-chatgpt-usage-paper.pdf
  DATE: 2025-09-15
  EXCERPT: “Weekly active ChatGPT users on consumer plans (Free, Plus, Pro)”
IMPACT: narrow

## 爭點 3
FLAG: extrapolation
TARGET: AMD 那邊，OpenAI 買它的晶片，順便拿到最多一成股權。
ATTACK: scope
OBJECTION: 原始契約授予的是購買股份的認股權證，並非簽約當下取得一成已發行股權。AMD 的 8-K 說明分批歸屬須達 GPU 採購里程碑，全部歸屬涉及 6GW 採購，另有股價及股票表現條件；契約也區分歸屬與可行使。F5 已寫出部分條件，但對外旁白省略了工具種類與條件，容易將有條件權利說成已取得股權。可保留最高約一成的潛在利益，須明示「有條件認股權證」。
EVIDENCE:
- URL: https://ir.amd.com/financial-information/sec-filings/content/0001193125-25-230895/d28189dex41.htm
  DATE: 2025-10-06（文件內發行日為 2025-10-05）
  EXCERPT: “Warrant to Purchase Shares of Common Stock”
- URL: https://ir.amd.com/financial-information/sec-filings/content/0001193125-25-230895/0001193125-25-230895.pdf
  DATE: 2025-10-06（申報事件日為 2025-10-05）
  EXCERPT: “stock price targets that escalate to $600 per share”
IMPACT: narrow

## 爭點 4
FLAG: self-reported-only
TARGET: 財務長說，六年前的 A100 現在還滿載在跑。
ATTACK: premise
OBJECTION: NO_EVIDENCE_BACKED_OBJECTION
EVIDENCE:
- URL: https://s201.q4cdn.com/141608511/files/doc_financials/2026/q3/NVDA-Q3-2026-Earnings-Call-19-November-2025-5_00-PM-ET.pdf
  DATE: 2025-11-19
  EXCERPT: “the A100 GPUs we shipped six years ago”; “running at full utilization today”
- URL: https://nvidianews.nvidia.com/news/nvidias-new-ampere-data-center-gpu-in-full-production
  DATE: 2020-05-14
  EXCERPT: “is in full production and shipping to customers worldwide.”
IMPACT: retain

爭點 4 說明：上市公告與 2025 年發言相隔約五年半，不能據此推翻「財務長說」的引述。逐字稿確實包含六年前及滿載措辭，且位於 Colette Kress 發言段。來源只能證實其曾如此表示，不能獨立證實所有 A100 的利用率；旁白已保留說話者歸屬，故不湊出反對結論。

稽核限縮：每個爭點開啟來源不超過三個。CNBC 的一兆美元報導開頁受 robots.txt 阻擋，未將搜尋摘要當作可引用反證，也未納入獨立爭點。未對其餘旁白句作全面背書。

Engine: codex
