# WO wandavision-4：口語化 → 反方稽核 → 稿冷讀

工作目錄：`/Users/51mini/dev/vibe-shorts-pipeline`。片目錄 `films/wandavision-primer/`。前置：WO-3 已完成（21 段、三部、8739 字）。

順序固定，因為後兩步的戳記綁 narration.md 的 sha，口語化改完稿才能跑。

## 1 口語化（humanize）

- 讀 `docs/WRITING.md` §7 第 10 條與 `films/taipei-silence/audit/humanize.md`（範例格式）。
- 逐句把 `narration.md` 改成台灣口語：念得出口、主動語態、一句一個動作。不刪情節、不改段名、不改事實、不新增劇透。
- 寫 `audit/humanize.md`：首行 `narration_sha: <改完後 narration.md 的 sha256>`（`shasum -a 256`），下面列改了哪些句（原句 → 新句）。
- 改完仍要過 `bash /tmp/wv-accept-1b.sh && bash /tmp/wv-accept-3.sh`（行長、標點、劇透界線、各部字數）。

## 2 反方稽核

- `scripts/devils.sh films/wandavision-primer`，要 exit 0，產出 `audit/devils-advocate.md`。
- exit 3（引擎都不可用）就停下，把錯誤原文寫進回報，不要自己造證據包。
- **不要寫 `audit/verdicts.md`**，裁決由主 session 做。

## 3 稿冷讀

- `scripts/coldread.sh films/wandavision-primer script`，產出 `audit/coldread-script.md`。
- 如果 VERDICT 是「不通過」，把 `[硬傷]` 條目原文貼進回報，**不要自己改稿**（改稿會讓第 2 步的戳記失效）。

## 禁區

不改 `scripts/`、`tests/`、`refs/`、其他片目錄；不寫 verdicts.md、approved.md；不 commit、不上傳、不跑 build／voice／approve。

## 驗收

```bash
bash /tmp/wv-accept-4.sh
```
