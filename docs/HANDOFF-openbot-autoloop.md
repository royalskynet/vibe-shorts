> **過時註記（2026-11-15）**：OpenBot 已移除。本文與其他文件裡的 `~/OpenBot/...` 路徑、Emperor／Marketer／Scribe 流程皆已過時。核准檔現在放 `state/approved/`，通知走 `scripts/notify_send.py`（hermes send）。

# HANDOFF：OpenBot 選題 → 凌晨生片 → YT 私人 → 使用者說「發」→ 三平台（10-29 草擬）

輪子：設定（串既有零件，不新造）。新 session 接手先讀本檔＋`~/.claude/projects/-Users-HOST/memory/state/openbot-team.md` 最後 6 行。

**使用者 10-29 定：流程從簡，凡要決定的點（選哪題、稿行不行、發不發）都由 Emperor 在 OpenBot 直接問使用者，回答才往下走。** 不另設核准檔格式之外的機制；下面各步照這條收斂。

## 已上線（10-29 DB 核對）
1. 週一 10:00 Marketer routine「每週選題」→ `~/OpenBot/Shared/marketer-topics-<日期>/proposal.md`＋tasks.csv NO_REVIEW（10-29 00:04 測試 OK，5 處引用全命中熱度檔）。
2. 每晚 22:00 Emperor「晚間交辦」→ NO_REVIEW 派 Inspector 驗→改帳（10-29 22:00 首次實跑，看 `ledger/review-2026-10-29.md`）。
3. 每早 08:30 Emperor「待核准清單」→ 手機遠端給使用者。

## 要接的（使用者 10-29：4/5/6 都做過、憑證現成，生片要凌晨給模型寫程式碼產出）
4. **核准落檔**：使用者在 OpenBot 回 Emperor「做題 N」→ Emperor 寫 `~/OpenBot/Shared/approved/<日期>-<slug>.md`（題目＋proposal 路徑）。只有 Emperor 寫，格式固定，給下一步機械讀。
5. **凌晨生片（模型寫程式碼）**：零 token watcher（launchd，非輪詢 LLM）看到 approved/ 有新檔 → 排夜間批次（`/nightnav` `arm --at 02:00`，使用者 10-xx 定 nightnav 不問時間）由 Claude headless 照 vibe-shorts skill 跑：改編稿（docs/WRITING.md）→ index.html／動畫（`clawd-bot-shot.mjs poseAt`）→ build／deliver → precheck 全過。模型與額度沿用 vibe-shorts 既有做法，先查 PLAN.md／DECISIONS.md 裡實際用的生片路徑再定，別憑本檔猜。
6. **YT 私人審片**：`yt_upload` 私人上傳（記憶 feedback_vibe_shorts_review_via_yt_private）→ 連結寫進 approved 檔並推給 Emperor，08:30 待核准清單帶出。
7. **使用者說「發」**才跑三平台發布（既有 meta_publish／YT 公開）；對外發布＝不可逆，留人工一鍵，不做全自動。

**專案規則衝突（CLAUDE.md）**：「改編稿要使用者核過才建置」。所以第 5 步拆兩晚：第一晚只寫改編稿＋TREATMENT（含「爆款證據：」行）→ 08:30 清單給使用者核稿 → 核過那晚才 build／deliver／YT 私人。要合併成一次核准得先問使用者改規則，不能自行跳過。另守「建置不併發」：凌晨批次一次只建一支。

## 驗收（接完要跑）
- 手動放一個 approved 檔 → 凌晨批次產出成片＋precheck 全 PASS＋YT 私人連結存在（`yt_upload` 回 videoId）。
- 08:30 清單出現該連結（看 Emperor 該次 routine 回覆）。

## 未知（接手先查）
- vibe-shorts 生片實際走哪個模型／session（Claude 主 session、Mythos、或 dcq）——本檔未查證。
- Emperor 寫 approved 檔要不要另給它一個 skill（emperor-dispatch 裡加一段即可）。

## 10-29 01:50 已接（4／5／6／7）
- 狀態機 `scripts/autoloop.py`（零 token；status 由程式依檔案＋precheck 判定，不信模型自述）；測試 `tests/test_autoloop.py`（變異兩處驗過會 fail）。
- launchd：`com.user.vibe-autoloop` 每天 02:00 `night`（建 1 支 script_ok＋寫最多 2 份 approved／script_revise 稿）；`com.user.vibe-autopublish` WatchPaths approved/，只吃 `publish_ok`。plist 在 `launchd/`。
- 偏離本檔：不用 nightnav（它綁 dcq goal state.json）；02:00 launchd 直接掃 approved/，零件更少。
- 生片模型＝Claude headless（Opus 5.5，訂閱 OAuth），`--setting-sources project,local`：user 層的 SUBPROCESS_ENV_SCRUB 會把 -p 權限打回 default（fixindex 10029），user hook 也會在無人時要求改派。skill 由 prompt 指 `~/.claude/skills/vibe-shorts/SKILL.md` 讀。
- 核稿拆兩晚照專案規則：approved→（夜）script_ready→使用者「稿過」→script_ok→（夜）built＋YT 私人→使用者「發」→publish_ok→即時發三平台→published。
- Emperor：emperor-dispatch 手冊加「營銷號核准」段（備份 `.bak-20261029-autoloop`）；08:30「待核准清單」instruction 已換（DB 核對 active=1）。
- 實測：手放 `approved/2026-10-29-gamble-odds.md`（題 3）。**下一步**：10-29 早上看 `scripts/autoloop.sh status` 是否 script_ready、`logs/autoloop.log`；08:30 Emperor 清單是否列「稿待核」。使用者稿過後隔晚驗 built＋yt_private。
- 10-29 01:56 使用者定：核准截止 21:00（台灣）。autoloop 依 approved 檔 mtime，晚於最近一個 21:00 的排隔晚（`cutoff()`，測試含變異）；「發」不受限。Emperor 手冊加這條。發布確認＝08:30 清單裡問，不另加 hpush 閘。
- 選題改爆款第一、題材不限（直銷、政治、幣圈皆可）：Marketer「每週選題」instruction 已換（經 Emperor 代改，Marketer 沒開 Local scripts；DB 核對）。
- **10-31 使用者定：營銷號提醒改由 Marketer 發**（取代上面 08:30 Emperor 清單的營銷號段）。`ops/fleet/vibe_remind.py`（live 副本在 `~/OpenBot/Shared/fleet/`，零 LLM）每天 08:35 跑 `autoloop.py digest`，只有卡在使用者手上的步驟才經 `fleet/notify.py` 貼進 Marketer 對話串；只剩「進行中」或空就不發。launchd `launchd/com.user.fleet-vibe-remind.plist`。使用者在 Marketer 回「稿過／稿改／發／做題」，Marketer 照人設「營銷號核准」段改 approved 檔；Emperor 08:30 只列 ledger 事項。Operator 不進這條流程（使用者 10-31 撤回）：發布走主 session／既有 API 腳本，刪 IG 貼文與登入牆後爆款數字用 wa-chrome。
