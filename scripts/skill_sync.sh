#!/usr/bin/env bash
# 把 skills/vibe-shorts、skills/viral-scout 同步到 OpenBot 的 Shared 與各 agent。
# 用法：scripts/skill_sync.sh --root <OpenBot 根> [--dry] --agent <目錄名> [--agent <目錄名>…]
set -euo pipefail

usage() {
  echo "用法：scripts/skill_sync.sh --root <OpenBot 根> [--dry] --agent <目錄名> [--agent <目錄名>…]" >&2
}

src="$(cd "$(dirname "$0")/.." && pwd)"
root=""
dry=0
agents=()

while [ "$#" -gt 0 ]; do
  case "$1" in
    --root)
      [ "$#" -ge 2 ] || { usage; exit 2; }
      root="$2"; shift 2 ;;
    --dry)
      dry=1; shift ;;
    --agent)
      [ "$#" -ge 2 ] || { usage; exit 2; }
      agents+=("$2"); shift 2 ;;
    *)
      usage; exit 2 ;;
  esac
done

if [ -z "$root" ] || [ "${#agents[@]}" -eq 0 ]; then
  usage
  exit 2
fi

for a in "${agents[@]}"; do
  if [ ! -d "$root/Agents/$a" ]; then
    echo "找不到 agent 目錄：$root/Agents/$a" >&2
    exit 2
  fi
done

skills=(vibe-shorts viral-scout)

sync() {
  local from="$1" to="$2"
  if [ "$dry" -eq 1 ]; then
    echo "$from -> $to"
    return 0
  fi
  mkdir -p "$to"
  rsync -a --delete "$from/" "$to/"
}

for name in "${skills[@]}"; do
  from="$src/skills/$name"
  sync "$from" "$root/Shared/skills/$name"
  for a in "${agents[@]}"; do
    sync "$from" "$root/Agents/$a/.claude/skills/$name"
    sync "$from" "$root/Agents/$a/.agents/skills/$name"
  done
done

exit 0
