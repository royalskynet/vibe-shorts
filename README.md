# vibe-shorts-pipeline

營銷號（Threads `@paradoxbar.tw`）的知識短片流水線：對標爆款 → 拆解 → 寫稿 → 配音 → 程式渲染 → 閘門 → 三平台匯出 → 發布 → 回饋。私有 repo，放設計、決議、腳本與每支片的原始碼，不放成片檔（見 `.gitignore`）。

2026-10-11 開立。目前進度與下一步只寫在 [PLAN.md](PLAN.md)，這裡不重抄。

## 選題原則

爆款第一：題目從已證實的爆款題型挑，每個決定附爆款證據（平台、播放數、連結）。找爆款用 skill `viral-scout`（[skills/viral-scout/SKILL.md](skills/viral-scout/SKILL.md)），證據帳在 [refs/VIRAL-LEDGER.md](refs/VIRAL-LEDGER.md)。

## 索引

| 位置 | 內容 |
|---|---|
| [PLAN.md](PLAN.md) | 九段流程、各段工具與狀態、下一步（進度正本） |
| [DECISIONS.md](DECISIONS.md) | 決議與裁決：平台、題型、輪子採用與淘汰理由 |
| [BRAND.md](BRAND.md) | 品牌定位 |
| [VOICE.md](VOICE.md) | 配音：候選實測、定案、復現指令；範本音檔在 `assets/voice/` |
| [docs/](docs/) | 寫稿規則 `WRITING.md`、發布設定 `PUBLISH-SETUP.md`、合規、交接文件 |
| [refs/](refs/) | 對標 `BENCHMARKS.md`、拆解 `BREAKDOWN.md`、爆款證據帳、各參考片的鏡頭表與逐字稿 |
| [films/](films/) | 每支片一個資料夾：`TREATMENT.md`、`narration.md`、`build.sh`、畫面原始碼、`SOURCES.md` |
| [scripts/](scripts/) | 對標、拆解、配音、閘門、匯出；發布在 `scripts/publish/` |
| [tests/](tests/) | 每支腳本的最小自檢，不連網 |
| `launchd/`、`ops/` | 背景排程：每日趨勢掃描、平台權杖續期 |
| [skills/](skills/) | 本專案的 Claude skill（symlink 到 `~/.claude/skills/`） |

## 做一支片

```bash
# 1. 選題：先跑 viral-scout 找爆款證據，寫進 refs/VIRAL-LEDGER.md
# 2. 建片資料夾（照 films/scam-map/ 的結構），寫 TREATMENT.md 與 narration.md
films/<名稱>/build.sh                         # 旁白、混音、渲染，產出 films/<名稱>/<名稱>.mp4
scripts/qa_sheet.sh films/<名稱>              # 拼圖＋切點，看完寫 qa/review_log.md（docs/WRITING.md §6）
python3 scripts/precheck.py films/<名稱>      # 發布前閘門，全過才能發
scripts/deliver.sh films/<名稱>/<名稱>.mp4    # 三平台交付檔＋清元資料 → films/<名稱>/dist/
# 3. 發布：scripts/publish/（yt_upload.py、meta_publish.py），每次對外發布要人點頭
```

## 自檢

```bash
for t in tests/test_*.py; do python3 "$t" || echo "FAIL $t"; done
```
