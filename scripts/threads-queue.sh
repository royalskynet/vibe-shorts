#!/usr/bin/env bash
# launchd 每 30 分鐘：發 queue/threads 裡到點且核准的文字貼。零 token。
set -uo pipefail
PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
cd "$(dirname "$0")/.."
LOG="$HOME/.vibe-trends/threads-queue.log"
mkdir -p "$HOME/.vibe-trends"
OUT=$(/usr/bin/python3 -I scripts/publish/threads_post.py run 2>>"$LOG")
rc=$?
[ -n "$OUT" ] && echo "$(date '+%F %T') $OUT" >> "$LOG"
if [ $rc -ne 0 ]; then
  hpush "Threads 佇列發文失敗 rc=${rc}，見 $LOG" >/dev/null 2>&1
elif [ -n "$OUT" ]; then
  hpush "Threads 佇列：$OUT" >/dev/null 2>&1
fi
