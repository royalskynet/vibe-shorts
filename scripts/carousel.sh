#!/usr/bin/env bash
# 成片稿轉 IG／Threads 輪播圖（1080x1350 JPG，只出圖不發佈）。
# 用法：scripts/carousel.sh films/<片>
# 讀該片 timeline.js（voice.py 產生），頁規則在 scripts/carousel/pages.js。
# 產物：films/<片>/out/carousel/p_0.00.jpg … p_<N-1>.00.jpg（檔名格式來自 still.mjs --range）。
set -euo pipefail
[ $# -eq 1 ] || { sed -n 2,5p "$0"; exit 2; }
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$1" && pwd)"
LIB="${LIB:-$HOME/dev/lemo-opuscar}"
[ -f "$FILM/timeline.js" ] || { echo "缺 $FILM/timeline.js（先跑 voice.py）" >&2; exit 2; }

SRC="$FILM/out/carousel-src"; OUT="$FILM/out/carousel"
rm -rf "$SRC" "$OUT"; mkdir -p "$SRC" "$OUT"
cp "$HERE/carousel/index.html" "$HERE/carousel/pages.js" "$FILM/timeline.js" "$SRC/"

N=$(node -e '
  global.window = global; require(process.argv[1]);
  const { buildPages } = require(process.argv[2]);
  console.log(buildPages(window.TL).length);' "$SRC/timeline.js" "$SRC/pages.js")
case "$N" in ''|*[!0-9]*|0) echo "頁數不對：$N" >&2; exit 1;; esac

node "$LIB/core/render/still.mjs" "$SRC" --range "0:$((N-1)):1" --size 1080x1350 --prefix p_ --out "$OUT"
echo "輪播 $N 頁 → $OUT"
