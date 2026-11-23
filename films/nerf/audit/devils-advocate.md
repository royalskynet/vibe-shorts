# Devil's Advocate Evidence Pack

Report: REPO_ROOT/films/nerf/audit/claims.md
Reviewed: 2026-10-18
Core conclusion as read: 核心結論＝旁白稿逐句陳述的事實。

## 爭點 1
FLAG: no-source
TARGET: |-
  Claude，你是不是被降智了？
  沒有。
ATTACK: scope
OBJECTION: 若「降智」指使用者實際收到的回答品質下降，無條件回答「沒有」與官方已確認的事故不符。Anthropic 明確記錄 2025 年 8 月至 9 月初，三項基礎設施錯誤間歇性降低 Claude 回答品質。若「降智」專指刻意削弱模型，本來源沒有證明刻意降級，且官方明確否認因需求、時段或伺服器負載降低品質。因此反證要求區分實際品質退化與刻意削弱，不能把兩者一起否認。事故已有修復，不能據此宣稱目前仍持續退化；稿件也未提供情境日期或模型版本。
EVIDENCE:
- URL: https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues
  DATE: 2025-09-17
  EXCERPT: "Between August and early September, three infrastructure bugs intermittently degraded Claude's response quality."
IMPACT: narrow

## 爭點 2
FLAG: inference
TARGET: 因為妳只打了「修一下」。
ATTACK: inference
OBJECTION: 稿件把按鈕跑版直接歸因於短提示，卻沒有提供原始對話、程式碼差異或重現比較。官方事故紀錄提供另一項有實據的品質退化機制：2026 年 4 月 16 日加入的縮短輸出系統提示，與其他提示變更共同傷害程式碼品質，並於 4 月 20 日撤回。同篇也記錄預設推理強度調低及思考歷史被錯誤清除。這足以削弱「表現變差就是使用者少寫字」的單一歸因；不能證明稿件中的按鈕事故由這些變更造成，也不能把 Claude Code 的事故外推至所有 Claude 介面。該次實際故障原因仍無直接證據。
EVIDENCE:
- URL: https://www.anthropic.com/engineering/april-23-postmortem
  DATE: 2026-04-23
  EXCERPT: "In combination with other prompt changes, it hurt coding quality and was reverted on April 20."
IMPACT: narrow

## 查核範圍紀錄

- 爭點 1 搜尋：`site.anthropic.com engineering postmortem three recent issues degraded Claude September 2025`。實際開啟上述 2025 年官方事故頁，核對事故期間、影響與修復限制。
- 爭點 2 搜尋：`site.anthropic.com engineering Claude Code quality effort prompt system April 2026`。實際開啟上述 2026 年官方事故頁，核對推理設定、快取錯誤與系統提示變更。
- 每個爭點引用 1 個已實際開啟來源，未超過每爭點 3 個來源上限。只保留 2 個有實據爭點；搜尋結果摘要未作為證據。
- 本證據包不裁定未提供的個別對話或 Threads 貼文真偽；不將找不到原始資料視為已證偽。不修改報告。

Engine: codex
