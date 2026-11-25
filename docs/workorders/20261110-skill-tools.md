## 任務

工作目錄 /Users/51mini/dev/vibe-shorts-pipeline。先讀計畫 /Users/51mini/dev/vibe-shorts-pipeline/docs/plans/2026-11-10-marketer-pipeline.md 的 A 段，再讀 skills/vibe-shorts/SKILL.md、docs/BROLL.md、scripts/reverse.py 開頭 docstring 與 argparse、scripts/broll.py 的 main()。

### 1. skills/vibe-shorts/SKILL.md 與 docs/BROLL.md
SKILL.md「做一支片」表加兩列，照既有列的三欄格式（步／指令／驗收）：
- 0b 拆對標片：`.venv/bin/python scripts/reverse.py <對標片.mp4> --out <目錄>`，驗收欄寫產出 `reverse.json`、`REVERSE.md`。
- 2c B-roll（畫面缺實景時）：`scripts/broll.py search <關鍵字>` 選素材、`scripts/broll.py fetch <url> --out films/<片名>/broll/<名> --license <授權> --credit <作者> --sources films/<片名>/SOURCES.md`、`index.html` 用 `drawBroll`，細節見 `docs/BROLL.md`；驗收欄寫 `clip.json` 存在且 `SOURCES.md` 有出處行。

指令與參數名照 reverse.py、broll.py 實際的 argparse。docs/BROLL.md 第 2 步補上 `--license <授權> --credit <作者>`。兩檔其他行保持原樣。

writes!: skills/vibe-shorts/SKILL.md docs/BROLL.md

## 驗收

```bash
cd /Users/51mini/dev/vibe-shorts-pipeline
grep -q 'scripts/reverse.py' skills/vibe-shorts/SKILL.md
grep -q 'scripts/broll.py fetch' skills/vibe-shorts/SKILL.md
grep -q 'drawBroll' skills/vibe-shorts/SKILL.md
grep -q -- '--license' docs/BROLL.md
test "$(grep -c '^| ' skills/vibe-shorts/SKILL.md)" -eq 15
```

預期：全部 exit 0；SKILL.md 剛好 15 列（既有 13＋新 2）；BROLL.md 有 --license。

## 禁止

- 禁止改 writes! 以外的檔、禁止改驗收區塊。
- 禁止刪改 SKILL.md 既有列（只新增）。
- 無頭機，禁止回報「請使用者手動執行」，卡住就回報阻斷點。
