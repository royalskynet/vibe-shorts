#!/bin/bash
# 對成片拉片，產出鏡頭表與運動曲線。
#
# 用法：scripts/shots.sh films/flt-11days
#
# seed 把 shots.json 印到 stdout，沒有 -o 參數。
# 2026-10-12 我寫了 -o <目錄>，它被默默忽略，結果檔案一直是舊的，
# 發布前閘門擋下來才發現。--track 另存運動曲線，validate 的 motion 門要它。
set -euo pipefail

TOOL="$HOME/dev/reelbench-skills/skills/video-shots/scripts/video-shots.mjs"
FILM="${1:?用法: shots.sh <片子目錄>}"
NAME="$(basename "$FILM")"
SRC="$FILM/$NAME.mp4"
OUT="$FILM/shots"

[ -f "$SRC" ] || { echo "找不到成片 $SRC" >&2; exit 1; }
if lsof -t -- "$SRC" >/dev/null 2>&1; then
  echo "還有行程開著 ${SRC}，等建置結束再來。" >&2
  exit 1
fi

mkdir -p "$OUT"
node "$TOOL" seed "$SRC" --track "$OUT/track.json" > "$OUT/shots.json"
node "$TOOL" render "$OUT/shots.json" --md --track "$OUT/track.json" > "$OUT/shots.md"
echo "寫好 $OUT/shots.json　$OUT/track.json　$OUT/shots.md"
