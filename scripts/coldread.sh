#!/usr/bin/env bash
# 冷讀審核（使用者 2026-11-05 定，借 Eian「Claude+Codex」流程第一點）：另開一個不知道意圖的模型，只給成品，
# 先寫「我看懂的故事」再挑錯。devils.sh 查事實、review_log 是主 session 自評，兩者都會被已知意圖帶偏。
# 用法：scripts/coldread.sh films/<片> script|film
#   script：只吃 narration.md → audit/coldread-script.md（首行 narration_sha:）
#   film  ：只吃 qa/sheet.jpg、qa/cards.jpg＋逐句字幕 → qa/coldread-film.md（首行 video_sha:）
# 不給 TREATMENT.md、SOURCES.md、verdicts、review_log、對話紀錄。
# 引擎順序 COLDREAD_ENGINES（預設 "codex opencode"，使用者 11-05：Codex 到期前優先用，之後走 deep 同一條 OpenCode Go）；
#   失敗（未登入、額度用完、到期）自動換下一個，寫法照 research 的 devils_advocate.sh。COLDREAD_OPENCODE_MODEL 可覆寫。
# exit 2＝參數或缺素材、exit 3＝所有引擎都不可用，印一行原因，不靜默成功。
set -euo pipefail
IMGS=()
[ $# -eq 2 ] || { sed -n 2,9p "$0"; exit 2; }
FILM="$(cd "$1" && pwd)"
MODE="$2"
NAME="$(basename "$FILM")"
DIR="$(cd "$(dirname "$0")" && pwd)"
OC_MODEL="${COLDREAD_OPENCODE_MODEL:-opencode-go/deepseek-v4.1-flash}"

PROMPT="$(cat "$DIR/coldread/$MODE.txt" 2>/dev/null)" || { echo "沒有 scripts/coldread/$MODE.txt" >&2; exit 2; }

if [ "$MODE" = script ]; then
  [ -f "$FILM/narration.md" ] || { echo "缺 $FILM/narration.md" >&2; exit 2; }
  OUT="$FILM/audit/coldread-script.md"
  SHA="$(shasum -a 256 "$FILM/narration.md" | cut -d' ' -f1)"
  INPUT="# 旁白稿

$(cat "$FILM/narration.md")"
elif [ "$MODE" = film ]; then
  for f in "$FILM/qa/sheet.jpg" "$FILM/qa/cards.jpg"; do
    [ -s "$f" ] || { echo "缺 ${f#$FILM/}：先跑 scripts/qa_sheet.sh films/$NAME" >&2; exit 2; }
  done
  MASTER="$FILM/$NAME.mp4"
  [ -f "$MASTER" ] || { echo "缺 $MASTER" >&2; exit 2; }
  # 字幕＝畫面上真的會出現的字（narration.md 去標題），不用 Whisper 轉寫：Whisper 把「百分之九十七」聽成「90% 70%」會造成假硬傷
  SUB="$(grep -v '^#' "$FILM/narration.md" | grep -v '^[[:space:]]*$')"
  OUT="$FILM/qa/coldread-film.md"
  SHA="$(shasum -a 256 "$MASTER" | cut -d' ' -f1)"
  INPUT="# 字幕（逐句，一行一句）

$SUB"
  IMGS=("$FILM/qa/sheet.jpg" "$FILM/qa/cards.jpg")
else
  echo "模式只有 script 或 film：$MODE" >&2; exit 2
fi

mkdir -p "$(dirname "$OUT")"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
printf '%s\n\n%s\n' "$PROMPT" "$INPUT" > "$TMP/prompt.txt"
# prompt 走參數不走 stdin：stdin 沒關，codex exec 會卡在 "Reading additional input from stdin..."
# 直到逾時（devils.sh 的坑），所以只重導 < /dev/null。
# -o 只取最後一則訊息，前面的思考過程不進產物。
run_engine() {
  local eng="$1" a=()
  case "$eng" in
    codex)
      command -v codex >/dev/null 2>&1 || { echo "PATH 找不到 codex"; return 1; }
      for f in ${IMGS[@]+"${IMGS[@]}"}; do a+=(-i "$f"); done
      codex exec --skip-git-repo-check -s read-only ${a[@]+"${a[@]}"} -o "$TMP/last.md" "$(cat "$TMP/prompt.txt")" </dev/null >"$TMP/log.txt" 2>&1 ;;
    opencode)
      command -v opencode >/dev/null 2>&1 || { echo "PATH 找不到 opencode"; return 1; }
      for f in ${IMGS[@]+"${IMGS[@]}"}; do a+=(-f "$f"); done
      # opencode run 把整段回覆印到 stdout；-f 是陣列旗標，prompt 前加 -- 免得被吃進去
      opencode run -m "$OC_MODEL" ${a[@]+"${a[@]}"} -- "$(cat "$TMP/prompt.txt")" </dev/null >"$TMP/last.md" 2>"$TMP/log.txt" ;;
    *) echo "未知引擎 $eng"; return 1 ;;
  esac || { grep -vi 'token\|key' "$TMP/log.txt" | tail -1; return 1; }
  grep -q '^VERDICT: ' "$TMP/last.md" 2>/dev/null || { echo "回覆沒有 VERDICT 行"; return 1; }
}
ENGINE=""; WHY=""
for eng in ${COLDREAD_ENGINES:-codex opencode}; do
  rm -f "$TMP/last.md"
  if r="$(run_engine "$eng")"; then ENGINE="$eng"; [ "$eng" = opencode ] && ENGINE="opencode/$OC_MODEL"; break; fi
  WHY="${WHY} ${eng}：${r}；"
done
[ -n "$ENGINE" ] || { echo "冷讀引擎都不可用：${WHY}" >&2; exit 3; }
{ echo "$([ "$MODE" = script ] && echo narration_sha || echo video_sha): $SHA"; echo "engine: $ENGINE"; echo; cat "$TMP/last.md"; } > "$OUT"
echo "$OUT"
grep -E '^- \[|^VERDICT: ' "$OUT" || true
