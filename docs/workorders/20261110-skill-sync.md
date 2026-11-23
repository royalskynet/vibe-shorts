## 任務

工作目錄 REPO_ROOT。背景見計畫 REPO_ROOT/docs/plans/2026-11-10-marketer-pipeline.md 的 B 段。

### 1. 新增 scripts/skill_sync.sh
bash，`set -euo pipefail`。用法：`scripts/skill_sync.sh --root <OpenBot 根> [--dry] --agent <目錄名> [--agent <目錄名>…]`。
- 對 skills/vibe-shorts 與 skills/viral-scout，用 `rsync -a --delete` 複製到 `<root>/Shared/skills/<名>/`、每個 `<root>/Agents/<目錄名>/.claude/skills/<名>/`、`<root>/Agents/<目錄名>/.agents/skills/<名>/`。
- 來源目錄用 `$(cd "$(dirname "$0")/.." && pwd)` 推算。
- 先檢查全部 `<root>/Agents/<目錄名>` 都存在，任一缺就印 stderr、exit 2，一個檔都不寫。
- `--dry` 只印每個 rsync 的來源→目的地，exit 0。
- 缺 `--root` 或沒有 `--agent`：印用法、exit 2。

writes!: scripts/skill_sync.sh

## 驗收

```bash
cd REPO_ROOT
T=$(mktemp -d); mkdir -p "$T/Agents/a1"
bash scripts/skill_sync.sh --root "$T" --agent a1
diff -r skills/vibe-shorts "$T/Shared/skills/vibe-shorts"
diff -r skills/viral-scout "$T/Agents/a1/.claude/skills/viral-scout"
diff -r skills/vibe-shorts "$T/Agents/a1/.agents/skills/vibe-shorts"
echo stale > "$T/Agents/a1/.claude/skills/vibe-shorts/OLD.md"; bash scripts/skill_sync.sh --root "$T" --agent a1; test ! -e "$T/Agents/a1/.claude/skills/vibe-shorts/OLD.md"
T2=$(mktemp -d); mkdir -p "$T2/Agents/a1"; rc=0; bash scripts/skill_sync.sh --root "$T2" --agent a1 --agent nope >/dev/null 2>&1 || rc=$?; test "$rc" -eq 2; test ! -e "$T2/Shared"
T3=$(mktemp -d); mkdir -p "$T3/Agents/a1"; bash scripts/skill_sync.sh --root "$T3" --dry --agent a1 >/dev/null; test ! -e "$T3/Shared"
rc=0; bash scripts/skill_sync.sh --agent a1 >/dev/null 2>&1 || rc=$?; test "$rc" -eq 2
```

預期：全部 exit 0；複製三處、刪舊檔、缺目錄 exit 2 且不寫、--dry 不寫、缺參數 exit 2。

## 禁止

- 禁止改 writes! 以外的檔、禁止改驗收區塊。
- 禁止寫 ~/OpenBot 底下任何檔，測試只用 mktemp 目錄。
- 禁止 pip／npm 安裝；無頭機，禁止回報「請使用者手動執行」，卡住就回報阻斷點。
