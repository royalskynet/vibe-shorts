#!/usr/bin/env bash
# 每天一次：抓熱度、列候選題、附同題爆款，然後推一行通知。
# 零 token：全程沒有模型呼叫，由 launchd 在背景跑。
set -uo pipefail
# launchd 預設 PATH 沒有 ~/.local/bin：hpush 找不到 → rc=127（10-16 zombie-audit）；也沒有 /opt/homebrew/bin：ffmpeg 找不到 → viral_text 10 支全敗（10-20）
PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
cd "$(dirname "$0")/.."

REPORT="$HOME/.vibe-trends/$(date +%F).md"
LOG="$HOME/.vibe-trends/run.log"
mkdir -p "$HOME/.vibe-trends"

{
  echo "=== $(date '+%F %T') start"
  /usr/bin/python3 -I scripts/trend_scan.py --refs
  echo "=== rc=$? trend_scan"
  /usr/bin/python3 -I scripts/trend_zh.py
  echo "=== rc=$? trend_zh"
  # 竄升榜前 10 支轉逐字稿累積（mlx_whisper 在 .venv）
  # 走全機重活閘：whisper 峰值約 8GB，不能跟模擬器／TTS／Laya 疊跑；排隊逾時 rc=75＝今天跳過
  heavy --timeout 3600 --max-run 1800 -- .venv/bin/python scripts/viral_text.py
  echo "=== rc=$? viral_text end"
} >> "$LOG" 2>&1

# 熱榜不在這裡推：cabinet MKT 雷達（collectors/mkt_trends.py，07:00）讀中文熱榜前三＋建議＋理由，併進 09:00 晨報（10-20 使用者定，避免重複）。
# 這裡只在中文雷達沒產出時告警。
ZH="$HOME/.vibe-trends/zh-$(date +%F).md"
if [ ! -f "$ZH" ]; then
  hpush "中文熱榜 $(date +%m-%d) 沒產出，MKT 雷達今天沒東西可讀，見 $LOG" >/dev/null 2>&1
fi

# 復盤初記滿 120h 就補數字（refs/postmortem.md 沒有「初記」時腳本直接退出）
UPD=$(/usr/bin/python3 -I scripts/publish/postmortem_refresh.py 2>>"$LOG")
rc=$?
if [ $rc -ne 0 ]; then
  hpush "復盤補數失敗 rc=${rc}，見 $LOG" >/dev/null 2>&1
elif [ -n "$UPD" ]; then
  hpush "復盤補數：$UPD 滿 5 天，數字已更新，教訓要不要改看 refs/postmortem.md" >/dev/null 2>&1
fi
