# Devil's Advocate Evidence Pack

Report: /Users/51mini/dev/vibe-shorts-pipeline/films/nvidia-loop-pause/audit/claims.md
Reviewed: 2026-11-24
Core conclusion as read: 市場的答案很直接：循環的核心資產，是談生意的人。

## 爭點 1
FLAG: inference
TARGET: 市場真正怕的，是這個循環可能不轉了。
ATTACK: inference
OBJECTION: 已開啟的 Reuters 市場報導把行情描述為原已擔憂 AI 投資估值的市場，再受領導危機衝擊；黃仁勳回任能影響整個產業情緒。這支持關鍵人物與情緒效應，卻未把市場反應辨識為特定「循環融資可能停轉」的恐懼。旁白將一種解釋寫成市場真正動機，應限縮為推論。反證沒有否定回任與上漲的關聯，也沒有證明循環融資毫無影響。
EVIDENCE:
- URL: https://ca.marketscreener.com/news/wall-street-soars-on-huang-s-return-to-nvidia-treasury-yields-rise-ce7851dadf8ff627
  DATE: 2026-11-23
  EXCERPT: "Huang's brief absence from the company roiled markets already concerned about the AI investment boom's lofty valuations"
IMPACT: narrow

## 爭點 2
FLAG: extrapolation
TARGET: 這些大生意，是黃仁勳一個一個談出來的。
ATTACK: scope
OBJECTION: 上文列入 AMD 六吉瓦協議，但 AMD 的正式公告將它界定為 AMD 與 OpenAI 的直接合作，並描述兩家公司既有多代產品合作。該來源能確立獨立於輝達的交易雙方，不能確立黃仁勳逐案親談。從輝達自己的 OpenAI 投資案擴及 AMD 等所有大單，超過已展示證據的範圍。這並非證明黃仁勳從未參與；應將親談歸屬限於有直接證據的特定交易。
EVIDENCE:
- URL: https://ir.amd.com/financial-information/sec-filings/content/0001193125-25-230895/d28189dex991.htm
  DATE: 2025-10-06
  EXCERPT: "Under this definitive agreement, OpenAI will work with AMD as a core strategic compute partner"
IMPACT: narrow

## 爭點 3
FLAG: inference
TARGET: 錢繞一圈變成輝達的營收，這叫循環融資。
ATTACK: premise
OBJECTION: 官方當時的措辭是隨部署逐步投資的意向，並非已完成的千億美元資金交付或營收認列證明。這可以支持循環融資的安排或風險分析，不能單憑該公告確立資金已完成一圈、轉成輝達營收。應保留條件與未來式。來源日期是 2025-09-22，也顯示 F1 將公告日期寫成 2025-09-23 不精確；後者可以是報導日期。此反證只限縮公告當時能證明的內容，不宣稱截至 2026-11-24 仍未投資。
EVIDENCE:
- URL: https://blogs.nvidia.com/blog/openai-nvidia/
  DATE: 2025-09-22
  EXCERPT: "NVIDIA also intends to invest up to $100 billion in OpenAI progressively as each gigawatt is deployed."
IMPACT: narrow

## 爭點 4
FLAG: extrapolation
TARGET: 老黃「放假」的十一天，輝達市值蒸發五千七百億美元。
ATTACK: scope
OBJECTION: 報告自己的口徑備註只把 5,730 億美元歸於截至 11-13 的當週，旁白卻擴成 11-12 至 11-23 的完整期間。另有已開啟的 Reuters 專欄記載，回任前一週股價又跌 23%，顯示完整空窗含有後續大幅變動，不能直接沿用前一週損失。應重算明確起訖交易日的市值差；此處不以十月高點累計損失取代十一天空窗損失，也不聲稱已算出正確值。
EVIDENCE:
- URL: https://d2233.cms.socastsrm.com/2026/11/23/trading-day-market-euphoria-as-huang-returns-to-nvidia/
  DATE: 2026-11-23
  EXCERPT: "This astonishing reversal came after a 23% plunge in Nvidia shares last week"
IMPACT: narrow

## 稽核邊界

每個爭點均已搜尋並實際開啟至少一個來源；每個爭點開啟的不同來源不超過三個。摘錄保留原文，均少於 80 字詞。AMD 與 NVIDIA 公告是當事方資料，只用於核對交易主體與公告的限定語，不當作實際履約的獨立證明。Reuters 專欄明列作者觀點，第四項僅援引其行情敘述。

BBC 原連結開啟失敗，未作有效證據；NVIDIA 投資人關係公告頁可開啟但正文未呈現，未引用其正文。未修改報告，未作主 session 的融合裁決。

Engine: codex
