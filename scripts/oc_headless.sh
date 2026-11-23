#!/usr/bin/env bash
# autoloop 的 claude 引擎換成 DeepSeek flash：prompt 從 stdin 進來、回覆走 stdout。
# opencode run 讀到非 TTY 的 stdin 會卡住（fix 10324），所以 prompt 先落地成檔案，
# 呼叫時 stdin 一律 </dev/null；exit code 原樣回傳給 autoloop。
set -euo pipefail

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT
cat > "$TMP"

if [ ! -s "$TMP" ]; then
  echo "oc_headless: empty prompt" >&2
  exit 2
fi

MODEL="${OC_MODEL:-opencode-go/deepseek-v4.1-flash}"
BIN="${OC_BIN:-opencode}"

# 無人值守沒人能按允許：repo 外的核准檔、~/.claude/skills 會被 v1 的 external_directory 預設 ask 自動拒絕（11-15 建片 rc=0 卻沒讀到核准檔）
export OPENCODE_CONFIG_CONTENT="${OPENCODE_CONFIG_CONTENT:-{\"permission\":{\"external_directory\":\"allow\"}}}"

# 每次執行留一份完整 log（工具呼叫、失敗、權限拒絕、opencode WARN/ERROR），logs/oc/latest.log 指向最新一份給監看用
LOGDIR="${OC_LOGDIR:-$PWD/logs/oc}"
mkdir -p "$LOGDIR"
RUNLOG="$LOGDIR/$(date +%Y%m%d-%H%M%S)-$$.log"
ln -sf "$RUNLOG" "$LOGDIR/latest.log"

PROMPT="$(cat "$TMP")"
set +e
"$BIN" run -m "$MODEL" --dir "$PWD" --print-logs --log-level WARN -- "$PROMPT" </dev/null 2>&1 | tee "$RUNLOG"
rc=${PIPESTATUS[0]}
set -e
echo "oc_headless: exit rc=$rc" >> "$RUNLOG"

# DNS 瞬斷（11-15 getaddrinfo ENOTFOUND）整支失敗要人工重跑：暫時性網路錯誤只重試一次
# 只在 rc≠0 時重試：跑完成功但中途瞬斷過的 log 也含這些字串，整支重跑會白燒一次建片
NET_ERR=""
[ "$rc" -ne 0 ] && { NET_ERR="$(grep -oE 'ENOTFOUND|ECONNRESET|ETIMEDOUT|EAI_AGAIN' "$RUNLOG" | head -1)" || NET_ERR=""; }
if [ -n "$NET_ERR" ]; then
  echo "oc_headless: retry after $NET_ERR" | tee -a "$RUNLOG"
  sleep "${OC_RETRY_SLEEP:-60}"
  "$BIN" run -m "$MODEL" --dir "$PWD" --print-logs --log-level WARN -- "$PROMPT" </dev/null 2>&1 | tee -a "$RUNLOG"
  rc=${PIPESTATUS[0]}
  echo "oc_headless: exit rc=$rc" >> "$RUNLOG"
fi
exit "$rc"
