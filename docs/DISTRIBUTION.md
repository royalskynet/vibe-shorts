# 分發與經營（2026-10-20）

依據：三支公開片 120h 播放 codex 871／dating-bill 185／scam-map 143，dating-bill 109h→122h 只多 2 次（沒進推薦流）。
借鏡 Kin 48 天萬粉復盤（https://x.com/kingao476942/status/2112198262661017812 ，作者自報數字未查證）：
733 則／48 天，爆款來自 AI 熱點當天出片、系列化、引用轉發加增量、大帳號留言區回覆、自轉舊爆文。
輪子卡見 `~/.wheel/registry.tsv` 2026-10-20 四張。

## 1. 一片多形態（零製作增量）

每支片發完，另外出：

| 形態 | 指令 |
|---|---|
| 輪播 | `scripts/carousel.sh films/<片>` → 寫 `meta/caption-carousel.txt` → `meta_publish.py films/<片> --carousel --yes` |
| Threads 文字鉤子 | 寫 `queue/threads/<日期>-<名>.md`（`approved: no`） |
| 自引用（套娃） | 佇列檔加 `quote: <片>/threads`，內文要有新資訊（數據、下一集預告），不重貼原說明 |

發布要人點頭：草稿一律 `approved: no`，使用者說好才改 yes。launchd `com.host.vibe-threads-queue` 每 30 分鐘發到點的。
轉發（repost）不做：官方文件頁 404，查不到端點。

## 2. 回覆他人貼文（手動）

API 拿不到他人貼文 ID（`threads_keyword_search` 未過審，只搜得到自己的貼文）。
做法：session 產回覆草稿清單（目標貼文連結＋一句有增量的回覆），使用者用手機貼。
要全自動得先送 `threads_keyword_search` 審核，這是對外申請，使用者決定。

## 3. 系列化：Claude × 其他 AI

codex 片是三支裡最好的（871，n=3，證據弱）。同一結構換對手出系列：Gemini、Grok、Copilot、Cursor。
每集仍照 CLAUDE.md 對談稿規則：從 `refs/dialogue-corpus/` 找爆款原稿改編，台詞重寫，使用者核稿才建置。
系列名與集數寫進說明欄，第二集起用 `quote:` 引用上一集。

## 節奏目標

每週：1 支片＋1 組輪播＋每天 1 則 Threads 文字貼。熱點出現時插隊。
