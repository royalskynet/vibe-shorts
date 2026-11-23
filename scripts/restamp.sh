#!/usr/bin/env bash
# 改稿後一次重跑會失效的戳記，不再手動逐個跑（2026-11-11 songshan-airport 改稿重跑 6 輪、漏過一次戳記才加）。
# 用法：scripts/restamp.sh films/<片>
# 順序：片目錄有 gen.py 就先重產文件 → devils.sh 反方稽核 → coldread.sh script 稿冷讀。
# 任何一步失敗就停（set -e），不跳過。戳記只能由這些腳本重跑寫入，不要手改 sha。
# 跑完印出還要人或主 session 做的：verdicts 裁決、使用者核稿（approve.py 要原話）、建置後的片冷讀與 precheck。
set -euo pipefail
[ $# -eq 1 ] || { sed -n 2,6p "$0"; exit 2; }
FILM="$(cd "$1" && pwd)"
NAME="$(basename "$FILM")"
DIR="$(cd "$(dirname "$0")" && pwd)"
[ -f "$FILM/narration.md" ] || { echo "缺 $FILM/narration.md" >&2; exit 2; }

if [ -f "$FILM/gen.py" ]; then
  echo "[1/3] gen.py 重產文件"
  python3 "$FILM/gen.py" "$FILM"
else
  echo "[1/3] 沒有 gen.py，跳過"
fi
echo "[2/3] 反方稽核"
"$DIR/devils.sh" "$FILM"
echo "[3/3] 稿冷讀"
"$DIR/coldread.sh" "$FILM" script

SHA="$(shasum -a 256 "$FILM/narration.md" | cut -d' ' -f1)"
echo "----"
echo "narration_sha: $SHA"
echo "還要做："
echo "  1. 讀 audit/devils-advocate.md，逐爭點重寫 audit/verdicts.md（narration_sha 寫上面這個）"
echo "  2. 稿子貼給使用者，說通過才跑 python3 scripts/approve.py films/$NAME \"<原話>\""
echo "  3. 建置後跑 scripts/coldread.sh films/$NAME film，再跑 python3 scripts/precheck.py films/$NAME"
