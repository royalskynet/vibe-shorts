# Threads 帳號清理進度（2026-10-13）

- 帳號：@iris96284 → @paradoxbar.tw，名稱「悖論小酒館」、新頭貼、新簡介，已生效。
- 串文：47 篇已刪光（網頁點擊）。
- 回覆：API 刪 96 則（含試刪 1 則）。10-14 翻頁實數：前 11 頁還有 275 則（最舊 2025-08-20），第 12 頁 500，實際更多。每次排程跑完 hpush 白話摘要到 Telegram（plist 需補 PATH 含 ~/.local/bin，否則找不到 hermes）。
  - 每日排程（10-14 起）：`scripts/publish/prune_replies.py`，launchd `com.user.threads-prune-replies` 每天 18:35 跑，log 在 `logs/prune-replies.log`；列表正常且 0 則才自己 bootout，列表 500／刪除失敗不停。舊的 /tmp 迴圈已停。
  - 10-14 01:30 手動 kickstart 一次：被「已超過 Threads API 限速」擋，0 則刪除（前一天剛刪 96 則，配額看起來是滾動 24h）。
  - **10-19 20:57 清完**：18:35 排程刪 15 則後撞 Threads 貼文配額（`error_user_title: 已超過 Threads API 限速`，log 有原始錯誤，不是原因不明）；20:57 手動再跑補刪最後 5 則，`list_mine()` 空、`count_mine()` 回 `(0, True)`。排程仍載入，明天 18:35 跑一次看到 0 則會自己 bootout。
  - 坑：`/me/replies` 帶 `limit=100` 會回 500；翻到後面某頁也會 500。做法是每次只抓第一頁、刪完再抓。
- 轉發：API 看不到 App 內轉發（`/me/threads` 回 0），改用網頁點「轉發→移除」。腳本計數至少 73 次點擊（未逐則核對），之後兩輪逾時被砍、無計數。10-13 收工時剩約 7 顆轉發按鈕（2025-12-29～2026-02-02，含「回覆已無法顯示的貼文」），使用者決定不再處理。
- 權杖：`THREADS_ACCESS_TOKEN` 在 creds，到 2026-12-12；scope 含 threads_basic、content_publish、delete、read_replies。
- Meta 後台（app paradoxbar-threads）：redirect／解除安裝／刪除回呼網址已填，threads_delete、threads_read_replies 已新增，@paradoxbar.tw 為 Threads 測試人員（已接受）。
- 不採用：DeleteThreads（同一條官方 OAuth API、一樣受 100 則/日限制，營運者不明，權杖存對方伺服器）。
