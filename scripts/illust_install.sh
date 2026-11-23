#!/usr/bin/env bash
# 把插畫庫裝進一支片：cp 正本 assets/illust/illust.mjs 到 <film>/illust/。
# 為什麼要複製不能引用：core/render/serve.mjs 把片子目錄當掛載根，片子取不到目錄外的檔案（403），跟 mascot_install.sh 同理。
# 正本改了要重跑；tests/test_illust.mjs 會擋副本跟正本不一致。
# 用法：bash scripts/illust_install.sh films/<名稱>
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FILM="${1:?用法: bash scripts/illust_install.sh films/<名稱>}"
[ -d "$FILM" ] || { echo "沒有這個片子目錄：$FILM"; exit 2; }
mkdir -p "$FILM/illust"
cp "$ROOT/assets/illust/illust.mjs" "$FILM/illust/"
echo "裝好：$FILM/illust/illust.mjs；index.html 用 import { person, prop, PALETTE } from './illust/illust.mjs'"
