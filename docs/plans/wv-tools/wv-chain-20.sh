#!/usr/bin/env bash
# WO-20 串接：做 → 獨立驗收 → 過了私人上傳；最多兩輪
set -u
R=/Users/51mini/dev/vibe-shorts-pipeline; F=$R/films/wv-primer-1
DR=~/.hermes/profiles/coco/skills/autonomous-ai-agents/devin/scripts/devin-run
cd "$R" || exit 2
while kill -0 "$(cat /tmp/wv-chain-16.pid)" 2>/dev/null; do sleep 30; done
for round in 1 2; do
  echo "== round $round 執行 $(date +%H:%M)"
  $DR "$R" "照 docs/plans/wo-wandavision-20-ep1-build.md 做完（若 films/wv-primer-1/qa/verify-20.md 存在，照工單驗收段處理）。已完成的步驟先用驗收腳本與 audit_problems 確認，過了就不重做，從沒完成的步驟接著做；建置前若有別支片在建置，等它結束。驗收指令：bash /tmp/wv-accept-20.sh，要印 ACCEPT-20 OK。" > /tmp/wv20-work-$round.log 2>&1
  echo "== round $round 驗收人 $(date +%H:%M)"
  rm -f "$F/qa/verify-20.md"
  $DR "$R" "照 docs/plans/wo-wandavision-20v-verify.md 做獨立驗收，只寫 films/wv-primer-1/qa/verify-20.md。" > /tmp/wv20-verify-$round.log 2>&1
  bash /tmp/wv-accept-20.sh > /tmp/wv20-accept-$round.log 2>&1; ac=$?
  head -1 "$F/qa/verify-20.md" 2>/dev/null | grep -qx 'VERDICT: PASS'; vp=$?
  echo "accept=$ac verify_pass=$((1-vp))"
  if [ $ac -eq 0 ] && [ $vp -eq 0 ]; then
    python3 scripts/publish/yt_upload.py films/wv-primer-1 > "$F/qa/yt-private.txt" 2>&1
    tail -2 "$F/qa/yt-private.txt"; grep -q '（private）' "$F/qa/yt-private.txt" && echo CHAIN-OK && exit 0
    echo CHAIN-UPLOAD-FAIL; exit 3
  fi
done
echo CHAIN-FAIL; exit 1
