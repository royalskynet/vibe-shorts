#!/usr/bin/env bash
# WO-20 驗收：第一集 WO-19 稿建片（主 session 寫，Devin 不改）
set -u
R=/Users/51mini/dev/vibe-shorts-pipeline; F=$R/films/wv-primer-1; N=$F/narration.md
cd "$R" || exit 2
fail=0; chk(){ echo "FAIL $1"; fail=1; }
bash /tmp/wv-accept-19.sh > /tmp/wv20-a19.log 2>&1 || { cat /tmp/wv20-a19.log; chk "稿子不過 ACCEPT-19"; }
P=$(python3 -c "import sys;from pathlib import Path;sys.path.insert(0,'scripts');import precheck;print(precheck.audit_problems(Path('films/wv-primer-1')))")
[ "$P" = "[]" ] || chk "audit_problems: ${P}"
FULL=$(shasum -a 256 "$N" | cut -d' ' -f1)
AS=$(sed -n 's/^narration_sha: *//p' "$F/audit/approved.md" 2>/dev/null | head -1)
case "$FULL" in "${AS:-NONE}"*) ;; *) chk "approved.md 戳記 ${AS:-無} 不是現在的稿 ${FULL:0:8}";; esac
grep -q "WO-20" "$F/audit/approved.md" || chk "approved.md 不是 WO-20 核准"
V=$F/wv-primer-1.mp4
[ -s "$V" ] || chk "沒有成片"
if [ -s "$V" ]; then
  [ "$V" -nt "$N" ] || chk "成片比稿子舊，沒重建"
  WH=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "$V" | head -1 | sed 's/x$//')
  [ "$WH" = "1920x1080" ] || chk "解析度 ${WH}"
  ffprobe -v error -select_streams a:0 -show_entries stream=codec_type -of csv=p=0 "$V" | grep -q audio || chk "沒有音軌"
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
  S=$(python3 /tmp/wv-shots.py "$V" 5)
  set -- $S; echo "INFO 時長 ${D}s 鏡頭 $1 個 最長同畫面 $2s（從第 $3s）"
  [ "$1" -ge 30 ] || chk "鏡頭只有 $1 個，要 ≥ 30"
  [ "$2" -le 15 ] || chk "最長同畫面 $2s > 15s"
  python3 -c "import sys; sys.exit(0 if 240<=float('$D')<=400 else 1)" || chk "時長 $D 不在 4–6.5 分鐘"
  cmp -s "$V" "$F/dist/wv-primer-1-shorts.mp4" || chk "dist 檔不是最新成片"
  [ "$F/qa/sheet.jpg" -nt "$V" ] || chk "qa/sheet.jpg 沒重產"
fi
grep -q -- '--size 1080x1920' "$F/build.sh" && chk "build.sh 還有直式尺寸"
[ -s "$F/meta/title-shorts.txt" ] || chk "缺標題"
[ -e "$F/meta/published.json" ] && grep -q youtube "$F/meta/published.json" && chk "published.json 有 youtube（不該公開）"
grep -q '一顆砲彈' "$F/index.html" && chk "index.html 還有舊段名「一顆砲彈」"
[ $fail -eq 0 ] && echo "ACCEPT-20 OK"
exit $fail
