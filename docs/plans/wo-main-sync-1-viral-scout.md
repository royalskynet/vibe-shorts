# WO-main-sync-1：把 viral-scout 改動與 precheck 修正送上私有 repo 的 main，並同步備份

工作目錄（唯一允許修改的地方）：/Users/51mini/dev/vs-main-wt
（這是私有 repo ~/dev/vibe-shorts-pipeline 的獨立 worktree，已在 main，HEAD=3334171）
來源分支：marketer/boundless-story-gate（別的 session 正在動，禁止碰）

## 做什麼（依序）
1. 在 /Users/51mini/dev/vs-main-wt：`git cherry-pick 78cd14d b1b7d9f`。衝突就停下回報，不硬解。
2. 取 precheck 修正：`git checkout marketer/boundless-story-gate -- scripts/precheck.py`，commit 為「precheck：開場問號改在原文找＋封面字 0.25 倍縮圖再試（取自 a464391，只取 precheck.py）」。
3. 跑測試，基線 FAIL 清單在 /tmp/wo-main-sync/baseline-fail.txt（3 筆：test_illust.mjs、test_seek_check.py、test_textless_check.py）。逐一跑 tests/test_*.py（python3）與 tests/test_*.mjs（node），FAIL 清單必須是基線的子集；多出任何 FAIL 就停下回報，不修。
4. 同步備份：`sh /Users/51mini/dev/ether-projects/bin/subtree-sync vibe-shorts-pipeline /Users/51mini/dev/vibe-shorts-pipeline <worktree 的 HEAD 短 sha>`。
   注意：subtree-sync 拉的是 main；worktree 的 commit 已在 main 上就會被拉到。
5. 預覽：`/Users/51mini/dev/ether-projects/bin/publish-sync --dry-run vibe-shorts`（只准這一種寫法），輸出貼進報告。
6. 完工回報寫到 /tmp/wo-main-sync/report.md：每步 rc、新 commit sha、測試 FAIL 清單、dry-run 輸出。

## 禁止
- 不在 /Users/51mini/dev/vibe-shorts-pipeline 工作目錄做 checkout／stash／reset／merge／build。
- 不把 marketer/boundless-story-gate 合進 main；不搬 1228375、4426112、a464391 其餘檔（voice.py 等）。
- publish-sync 不可去掉 --dry-run、不可省專案名、不設 PUBLISH_SYNC_OVERWRITE。
- 不 push 任何 repo。不碰 ~/.claude、憑證。
- 不移除 worktree（主 session 驗收後自己移）。

## 驗收（主 session 親跑）
bash /tmp/wo-main-sync/accept.sh
