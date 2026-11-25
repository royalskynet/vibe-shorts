# Devil's Advocate Evidence Pack

Report: /Users/51mini/dev/vibe-shorts-pipeline/films/nvidia-huang-returns/audit/claims.md
Reviewed: 2026-11-24
Core conclusion as read: 一個人值多少錢，市場直接用鈔票回答了。

## 爭點 1
FLAG: extrapolation
TARGET: 光對 OpenAI 的投資承諾，就是一千億美元。
ATTACK: scope
OBJECTION: 報告引用的 2025 年交易公告，實際宣布的是意向書，以及隨每一 gigawatt 部署逐步投資「最高」一千億美元的意向。旁白去掉上限、分期與部署條件，將條件式投資意向寫成確定金額。這削弱以確定大單規模支撐回聘必要性的論證。此反證只界定原始公告的承諾口徑，不證明截至稽核日仍未簽約，也不證明交易已取消。
EVIDENCE:
- URL: https://openai.com/index/openai-nvidia-systems-partnership/
  DATE: 2025-09-22
  EXCERPT: "NVIDIA intends to invest up to $100 billion"；"progressively as each gigawatt is deployed."
IMPACT: narrow

## 爭點 2
FLAG: inference
TARGET: 美國政府高層跟董事會說，他回來不構成國安風險。
ATTACK: inference
OBJECTION: F2 所引公司公告將「無國安風險」明確歸屬於董事會收到政府意見後的信心判斷，沒有披露政府意見原文。Lucian Bebchuk 的同期分析也直接指出這個歸屬差異。不過，實開的 AP 報導另記載川普自稱政府曾向公司保證，因此不能反推「政府未曾保證」或判定旁白實質為假。最強可成立異議只限來源歸屬：若沿用 F2，應寫成董事會判斷；若寫政府保證，應明確歸於川普說法，不能寫成已獨立核實的國安結論。
EVIDENCE:
- URL: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Board-Reinstates-Jensen-Huang-as-President-CEO-and-Board-Director/default.aspx
  DATE: 2026-11-23
  EXCERPT: "based on that input, the Board is confident"
- URL: https://corpgov.law.harvard.edu/2026/11/23/nvidias-u-turn/
  DATE: 2026-11-23
  EXCERPT: "the announcement does not state that the U.S. government concluded"
- URL: https://apnews.com/article/nvidia-jensen-huang-chips-china-ai-fce355eac6dd81677f3005578c5c8ca4
  DATE: 未標示（開頁正文未顯示日期；搜尋索引標示 2026-11-23）
  EXCERPT: "Trump also said his administration assured Nvidia"
IMPACT: narrow

## 爭點 3
FLAG: inference
TARGET: 那十一天，公司交給財務長克雷斯代理。
ATTACK: scope
OBJECTION: 「十一天」可以描述 11 月 12 日辭職公告到 11 月 23 日回任公告的日期差，但不能直接當作實際代理任期。SEC 8-K 明載董事會已於 11 月 22 日恢復黃仁勳職務，即刻生效；11 月 23 日是所附新聞稿日期。公司新聞稿與 AP 的「十一天」敘事支持公告間隔，並未消除申報文件中較早生效日的差別。應區分公告時間與職務生效時間；文件未給具體時刻，本次不推算精確代理時數，也不將美國日期直接換成台灣日期。
EVIDENCE:
- URL: https://www.sec.gov/Archives/edgar/data/1045810/000104581026000090/nvda-20261122.htm
  DATE: 2026-11-23（簽署日；最早事件日 2026-11-22）
  EXCERPT: "On November 22, 2026"；"effective immediately."
- URL: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Board-Reinstates-Jensen-Huang-as-President-CEO-and-Board-Director/default.aspx
  DATE: 2026-11-23
  EXCERPT: "Nov. 23, 2026"；"today announced that effective immediately"
IMPACT: narrow

稽核界線：共選 3 個爭點，依其對核心論證的影響排序。每個爭點均已搜尋並實際開頁；每個爭點最多使用 3 個來源。BBC 原連結開啟失敗，未作證據。本證據包不裁決報告，也未修改報告。

Engine: codex
