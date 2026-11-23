## 任務

拆單豁免：旁白改字、humanize 的 sha 戳記、claims 與說明欄互相綁定，分開派會讓 sha 與內容對不上。

工作目錄：`/Users/you/dev/vibe-shorts-pipeline`。第四輪稽核兩個爭點成立：(1) 鉤子漏了「兩大手機商店」範圍（官方網路商店不在估算內）；(2) AppMagic 把這組數字定義為商店內購淨營收估算（排除平台費用、含稅），不是玩家實際花費，「消費估算」要改成「內購營收估算」。只做下面的取代，其他句子一字不動。不改 `index.html`／`mix.py`／`build.sh`，不 render，不 git commit，不跑 `approve.py`／`voice.py`／`restamp.sh`。

### 1. `films/pikmin-bloom/narration.md`（照字面）
- 「而且二〇二六年上半年，這款遊戲約一半的消費估算，來自台灣。」→「而且二〇二六年上半年，這款遊戲在兩大手機商店，約一半的內購營收估算來自台灣。」
- 「二〇二六年上半年，這款遊戲在兩大手機商店，台灣消費估算約一千八百五十萬美元。」→「二〇二六年上半年，這款遊戲在兩大手機商店，台灣內購營收估算約一千八百五十萬美元。」
其他行（含「這些是 AppMagic 對 App Store 和 Google Play 的估算。」「所以在這個估算裡，每兩塊就有一塊多來自台灣。」）不動。

### 2. 重寫戳記與對照檔
- `audit/humanize.md`：首行 `narration_sha: <narration.md 最終內容 sha256>`（`shasum -a 256 films/pikmin-bloom/narration.md | cut -d' ' -f1`），下面列兩條「原句 → 新句」。
- `audit/claims.md`：同步改這兩句；把「消費估算」一律改成「內購營收估算」，口徑註記改為「口徑以 AppMagic 定義為準：商店內購淨營收估算，排除平台費用、含稅，僅 App Store 與 Google Play，不含官方網路商店；PocketGamer.biz 原文以 spending 描述同一組數字；另一篇 2026-11-03 報導稱過去一年台灣淨收入 1370 萬美元、五年累計台灣占比 18%，期間與口徑不同，本片只用 2026 上半年這組」。
- 刪除 `audit/devils-advocate.md`、`audit/coldread-script.md`、`audit/verdicts.md`（舊 sha 的稽核檔，主 session 稍後重跑）。

### 3. 說明欄與事實檔
- `meta/caption-shorts.txt`、`caption-reels.txt`、`caption-threads.txt`：「台灣消費估算約 1850 萬美元」→「台灣內購營收估算約 1850 萬美元」。沒出現就跳過，其餘行不動。
- `meta/facts.md` 三列 `TW_REVENUE_H1_2026_USD`、`GLOBAL_REVENUE_H1_2026_USD`、`TW_SHARE_H1_2026` 的註記欄補上「AppMagic 定義：內購淨營收估算（排除平台費用、含稅）」，已有的「僅 App Store 與 Google Play」註記保留。

## 驗收

```bash
cd /Users/you/dev/vibe-shorts-pipeline
f=films/pikmin-bloom/narration.md
grep -q '而且二〇二六年上半年，這款遊戲在兩大手機商店，約一半的內購營收估算來自台灣。' "$f"
grep -q '台灣內購營收估算約一千八百五十萬美元' "$f"
grep -q '這些是 AppMagic 對 App Store 和 Google Play 的估算。' "$f"
grep -q '所以在這個估算裡，每兩塊就有一塊多來自台灣。' "$f"
if grep -qE '消費估算|收入|台灣玩家' "$f"; then echo '舊口徑殘留'; exit 1; fi
if grep -qE '[0-9]' "$f"; then echo '旁白殘留阿拉伯數字'; exit 1; fi
python3 - <<'PY'
import re, sys
nar = open('/Users/you/dev/vibe-shorts-pipeline/films/pikmin-bloom/narration.md').read()
body = re.sub(r'^#+.*$', '', nar, flags=re.M)
norm = lambda s: re.sub(r'[\s，、：；「」『』（）,.!?？！。]', '', s)
ss = [s for s in re.split(r'[。？！\n]', body) if len(norm(s)) >= 1]
long_ = [s for s in ss if len(norm(s)) > 35]
if long_: print('句超長', long_); sys.exit(1)
n = len(re.sub(r'\s', '', body))
if not (300 <= n <= 430): print('字數', n); sys.exit(1)
if len(re.findall(r'^## ', nar, flags=re.M)) != 5: print('段數不是 5'); sys.exit(1)
print('OK', n)
PY
sha=$(shasum -a 256 "$f" | cut -d' ' -f1)
head -1 films/pikmin-bloom/audit/humanize.md | grep -q "narration_sha: $sha"
for x in verdicts devils-advocate coldread-script; do
  if [ -e films/pikmin-bloom/audit/$x.md ]; then echo "舊檔殘留 $x"; exit 1; fi
done
grep -q '內購營收估算' films/pikmin-bloom/audit/claims.md
if grep -q '消費估算' films/pikmin-bloom/audit/claims.md; then echo 'claims 舊口徑殘留'; exit 1; fi
grep -q '內購淨營收' films/pikmin-bloom/meta/facts.md
for c in caption-shorts caption-reels caption-threads; do
  if grep -q '台灣消費估算' films/pikmin-bloom/meta/$c.txt; then echo "舊句殘留 $c"; exit 1; fi
done
```
預期整段 exit 0 並印出 `OK <字數>`；開工前旁白仍含「消費估算」，第一行 grep 就會失敗。

## 不動
`films/pikmin-bloom/index.html`、`mix.py`、`build.sh`、`cast.json`、`TREATMENT.md`、`SOURCES.md`、`refs/`、`scripts/`、`tests/`、`PLAN.md`、`films/` 其他資料夾。

## 禁止
1. 不 render、不執行 `build.sh`、不跑 `approve.py`／`voice.py`／`restamp.sh`、不 git commit。
2. 無頭機：禁止回報「請使用者手動貼 token／授權／執行指令」；憑證讀不到＝停手回報阻斷點。
3. 不憑記憶補事實；只做上面列的取代，不改其他句子。
