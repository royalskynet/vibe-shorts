# 採用 xilo-opus-video 做法（2026-10-18 定，L2）

來源：xilo〈零基础入门Opus5.5做视频〉https://x.com/xilo2991/status/2104912748794589515 （76.8 萬瀏覽、3011 讚）；
skill 原碼 https://github.com/Kianzzz/xilo-opus-video （MIT），本機副本 /tmp/wheel-xilo/repo（只讀）。

## 根治（三項）

1. `scripts/ref_analyze.py <影片> --out <前綴>`：時長、切點（64x36 灰階相鄰幀差 >12 且 >3 倍鄰幀；ffmpeg scene 在對談片抓 0 刀，不用）、
   每鏡停留秒數與中位數、抽幀拼圖（全尺寸＋手機 360px）。拼圖部分照抄 analyze_video.py（MIT，檔頭註明出處）。
   實測基準：agentmorphy Dd7fGY6gLbH 14 刀／中位 3.2s；DeEYUXSAtIB 18 刀／中位 2.4s。寫進 skills/viral-scout 第 1 節。
2. 目視自評：`scripts/qa_sheet.sh films/<片>` 出 `qa/sheet.jpg`、`qa/sheet-360.jpg`；
   agent 按 7 項（開場／手機可讀／動作／變化／構圖／貼合原稿／聲畫同步）打 1–10 分，寫 `qa/review_log.md`（首行 `video_sha: <成片 sha256>`）。
   precheck 新門「目視自評」：檔在、sha 對上成片、7 項都 ≥8。
3. TREATMENT「禁止清單：」節，precheck 檢查存在且非空；docs/WRITING.md 加說明。對談片預設清單：每句硬切、近景背景看不到窗、居中大字淡入淡出。

## 預防加固

- tests/test_ref_analyze.py：合成 3 段純色影片 → 必須抓到 2 刀（切點邏輯改錯會 fail）。
- tests/test_precheck_review.py：review_log 缺項、sha 不符、某項 7 分 → 門要 FAIL。

## 不採用

運動模糊（渲染 ×4、對談片動作慢）、spring（clawd-bot-shot 已管）、整段合成配音（兩音色逐句）、綠幕真人（要付費模型）。

## 驗收

`for t in tests/test_*.py; do python3 "$t" || echo FAIL $t; done` 全過；`scripts/ref_analyze.py refs/ig-Dd7fGY6gLbH/src.mp4` 印出 14 刀；
sixty-one 跑 qa_sheet＋review_log 後 precheck「目視自評」OK。
