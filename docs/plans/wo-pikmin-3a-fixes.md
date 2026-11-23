## 任務

拆單豁免：旁白改字、humanize 的 sha 戳記、說明欄殘留清理互相綁定，分開派會讓 sha 對不上。

工作目錄：`/Users/you/dev/vibe-shorts-pipeline`。使用者已核過 `/tmp/pk-narration-approved.md`（稿子基準），只做下面三項修正，其他句子一字不動。不改 `index.html`／`mix.py`／`build.sh`，不 render，不 git commit，不跑 `approve.py`／`voice.py`。

### 1. 修改 `films/pikmin-bloom/narration.md`
只做這些取代（完全照字面）：
- 「你課的錢，跟這個寫法有關。」→「你課的每一筆錢，都算進這款遊戲的收入裡。」
- 「2026-11-10 起，」→「二〇二六年十一月十日起，」
- 「2026 上半年，」→「二〇二六年上半年，」
- 「約 1850 萬美元」→「約一千八百五十萬美元」
- 「約 3570 萬美元」→「約三千五百七十萬美元」
- 「約 52%」→「約百分之五十二」
- 「2026-11-12 晚間」→「二〇二六年十一月十二日晚間」
英文名稱（Pikmin Bloom、PocketGamer.biz、AppMagic、Taiwan）不動。

### 2. 重寫戳記與對照檔
- 刪除範本殘留的舊戳記：`films/pikmin-bloom/audit/approved.md`、`audit/devils-advocate.md`、`audit/verdicts.md`（它們是 taipei-silence 的內容，不屬於這支片）。
- 重寫 `films/pikmin-bloom/audit/humanize.md`：首行 `narration_sha: <narration.md 最終內容 sha256>`（`shasum -a 256 films/pikmin-bloom/narration.md | cut -d' ' -f1`），下面列上面七條「原句 → 新句」。
- 更新 `films/pikmin-bloom/audit/claims.md`：數字改成國字後，逐句對應 F 編號的欄位同步改。

### 3. 說明欄殘留
- `films/pikmin-bloom/meta/caption-shorts.txt`、`caption-reels.txt`、`caption-threads.txt`：刪掉任何含「第 1 集」「第二集」「😂」的行（範本殘留），其餘不動。三份說明欄裡的數字與日期改成跟旁白一致的寫法不是必要，不要動。
- `meta/title-shorts.txt` 與 `meta/tags.txt` 若不是以換行結尾，補一個換行。

## 驗收

```bash
cd /Users/you/dev/vibe-shorts-pipeline
f=films/pikmin-bloom/narration.md
grep -q '你課的每一筆錢，都算進這款遊戲的收入裡' "$f"
if grep -q '跟這個寫法有關' "$f"; then exit 1; fi
if grep -qE '[0-9]' "$f"; then echo '旁白殘留阿拉伯數字'; exit 1; fi
grep -q '二〇二六年十一月十日起' "$f"
grep -q '一千八百五十萬美元' "$f"
grep -q '三千五百七十萬美元' "$f"
grep -q '百分之五十二' "$f"
grep -q '二〇二六年十一月十二日晚間' "$f"
changed=$(diff /tmp/pk-narration-approved.md "$f" | grep -c '^>')
test "$changed" -ge 5
test "$changed" -le 10
n=$(sed '/^#/d' "$f" | tr -d '[:space:]' | wc -m)
test "$n" -ge 300
test "$n" -le 420
if [ -e films/pikmin-bloom/audit/approved.md ]; then exit 1; fi
if [ -e films/pikmin-bloom/audit/devils-advocate.md ]; then exit 1; fi
if [ -e films/pikmin-bloom/audit/verdicts.md ]; then exit 1; fi
sha=$(shasum -a 256 "$f" | cut -d' ' -f1)
head -1 films/pikmin-bloom/audit/humanize.md | grep -q "narration_sha: $sha"
for c in caption-shorts caption-reels caption-threads; do
  if grep -qE '第 ?1 ?集|第二集|😂' films/pikmin-bloom/meta/$c.txt; then echo "殘留 $c"; exit 1; fi
done
test -n "$(tail -c1 films/pikmin-bloom/meta/title-shorts.txt | tr -d '\n')" && exit 1
true
```
預期整段 exit 0；開工前旁白還有阿拉伯數字與「跟這個寫法有關」，第二、三行就會失敗。

## 不動
`films/pikmin-bloom/index.html`、`mix.py`、`build.sh`、`cast.json`、`meta/facts.md`、`SOURCES.md`、`TREATMENT.md`、`refs/`、`scripts/`、`tests/`、`PLAN.md`、`films/` 其他資料夾。

## 禁止
1. 不 render、不執行 `build.sh`、不跑 `approve.py`／`voice.py`、不 git commit。
2. 無頭機：禁止回報「請使用者手動貼 token／授權／執行指令」；憑證讀不到＝停手回報阻斷點。
3. 不憑記憶補事實；只做上面列的取代，不改其他句子。
