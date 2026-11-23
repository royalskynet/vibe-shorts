#!/usr/bin/env bash
# launchd 入口：autoloop.sh night｜publish。零 token，模型呼叫只在 autoloop.py 叫 claude headless 那一步。
set -uo pipefail
# launchd 預設 PATH 沒有 ~/.local/bin（claude、hpush）與 /opt/homebrew/bin（ffmpeg、node）
PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
export PATH
# 從 Claude session 手動跑時 CLAUDE_* 會漏進 headless claude（fixindex 10029）
unset CLAUDE_CODE_SUBPROCESS_ENV_SCRUB CLAUDECODE CLAUDE_CODE_ENTRYPOINT CLAUDE_CONFIG_DIR
cd "$(dirname "$0")/.."
# 無人值守全走 DeepSeek flash（od），不花 Claude／Codex；外部已設的值優先
OD=opencode-go/deepseek-v4.1-flash
export AUTOLOOP_CLAUDE="${AUTOLOOP_CLAUDE:-$PWD/scripts/oc_headless.sh}" OC_MODEL="${OC_MODEL:-$OD}"
export BAKEOFF_WRITERS="${BAKEOFF_WRITERS:-deepseek}" BAKEOFF_JUDGES="${BAKEOFF_JUDGES:-deepseek}"
export COLDREAD_ENGINES="${COLDREAD_ENGINES:-opencode}" COLDREAD_OPENCODE_MODEL="${COLDREAD_OPENCODE_MODEL:-$OD}"
export DA_ENGINES="${DA_ENGINES:-opencode}" DA_OPENCODE_MODEL="${DA_OPENCODE_MODEL:-$OD}"
exec /usr/bin/python3 -I scripts/autoloop.py "$@"
