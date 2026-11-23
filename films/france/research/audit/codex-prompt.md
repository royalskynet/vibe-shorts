你是獨立事實查核員。對象：REPO_ROOT/films/france/research/REPORT.md（2026 年 10 月法國高中生抗議與 10-17 全國暴亂的懶人包，繁體中文）。

任務：
1. 網址存活：對文末「來源」表 16 個網址逐一實際打開（curl -sIL 或 web search/fetch 皆可）。記錄 HTTP 狀態；403/429 這類反爬不算死鏈，要換方法再開一次確認內容。
2. 逐條核對：正文每一個帶 [N] 的主張，打開對應 N 號來源，確認來源原文支持該主張的主體、數字、日期、限定語。一條都不能跳過，不是抽查。
   - 本機已有部分頁面落檔可先用：REPO_ROOT/films/france/research/pages/*.txt（Jina 抓的正文，含 URL 標頭行）。落檔沒有或不完整的才上網抓。
3. 不要修改 REPORT.md。只產出結果檔。

輸出寫到 REPO_ROOT/films/france/research/audit/codex-verify.md，格式：
- 第一段「網址」表：| # | URL | 狀態 | 備註 |
- 第二段「主張」表：| 段落 | 主張原句（節錄） | [N] | 判定 | 來源原文摘錄（逐字，≤40 字） | 問題 |
  判定只能用：支持／部分支持／不支持／來源打不開
- 第三段「需修改清單」：只列判定非「支持」的，寫建議改法。
- 最後一行：SUMMARY total=<主張數> support=<n> partial=<n> fail=<n> unreachable=<n>

規則：摘錄必須是你實際打開的原文逐字片段；查不到就判「來源打不開」或「不支持」，不得憑記憶補。
