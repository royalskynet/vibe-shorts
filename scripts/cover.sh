#!/bin/bash
# 從成片第 0 幀產 IG 安全封面：films/<名稱>/dist/<名稱>-cover.jpg（1080x1920）。
#
# 用法：scripts/cover.sh films/<名稱>/<名稱>.mp4 [輸出.jpg]
# deliver.sh 結尾會呼叫；也可單獨跑（不碰 dist 裡的 mp4）。
#
# 為什麼：IG 個人檔案網格把 9:16 封面裁成 3:4，1080 寬只留中間 1440 高，上下各 240px 被切。
# 我們的第 0 幀就是封面，系列標籤與大標頂端在上方 240px 內，網格縮圖頂端被截。
# 做法：第 0 幀等比縮到高 1440（寬 810）置中，四周補第 0 幀左上角的底色，
# 3:4 中央裁切剛好看到完整的第 0 幀。meta_publish.py 發 IG 時用 cover_url 帶上這張。
set -euo pipefail

SRC="${1:?用法: cover.sh <成片.mp4> [輸出.jpg]}"
[ -f "$SRC" ] || { echo "找不到 $SRC" >&2; exit 1; }
DIR="$(cd "$(dirname "$SRC")" && pwd)"
NAME="$(basename "$SRC" .mp4)"
OUT="${2:-$DIR/dist/$NAME-cover.jpg}"
mkdir -p "$(dirname "$OUT")"

# 第 0 幀左上角 1 個像素的 RGB → 0xRRGGBB（片子背景是滿版底色，角落就是邊緣色）
RGB="$(ffmpeg -v error -i "$SRC" -frames:v 1 -vf "format=rgb24,crop=1:1:0:0" -f rawvideo - | od -An -tx1 | tr -d ' \n')"
[[ "$RGB" =~ ^[0-9a-f]{6}$ ]] || { echo "取不到第 0 幀底色（得到「${RGB}」）" >&2; exit 1; }

ffmpeg -v error -y -i "$SRC" -frames:v 1 \
  -vf "scale=1080:1440:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=0x$RGB" \
  -q:v 2 "$OUT"
echo "封面 ${OUT}（底色 #${RGB}）"
