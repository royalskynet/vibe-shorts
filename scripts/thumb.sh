#!/usr/bin/env bash
# 橫式片的 YouTube 縮圖：1280×720。
# 用片子第 0 幀當底——流水線規矩是大標在第 0 幀就完整顯示（docs/WRITING.md §6.3、precheck 會擋），
# 所以縮圖不用另外疊字；本機 ffmpeg 也沒編 drawtext。
# 用法：scripts/thumb.sh films/<片名> [秒（縮圖取哪幀，預設 0；主播滑入的片給 2.2）]
set -euo pipefail
LIB="${LIB:-$HOME/dev/lemo-opuscar}"
DIR="${1:?用法: thumb.sh films/<名稱>}"
[ -f "$DIR/index.html" ] || { echo "找不到 $DIR/index.html" >&2; exit 1; }
mkdir -p "$DIR/dist"

# 片子尺寸：meta/format.json 優先，預設 1920x1080（這支腳本就是給橫式片用的）
W=1920; H=1080
if [ -f "$DIR/meta/format.json" ]; then
  W=$(python3 -c "import json;print(json.load(open('$DIR/meta/format.json'))['w'])")
  H=$(python3 -c "import json;print(json.load(open('$DIR/meta/format.json'))['h'])")
fi
T="${2:-0}"
node "$LIB/core/render/still.mjs" "$DIR" "$T" --size "${W}x${H}" --out "$DIR/dist/thumb-tmp" --prefix ""
ffmpeg -v error -y -i "$DIR/dist/thumb-tmp/t_${T}.jpg" -vf "scale=1280:720" "$DIR/dist/thumb-1280x720.png"
rm -rf "$DIR/dist/thumb-tmp"
echo "$DIR/dist/thumb-1280x720.png"
