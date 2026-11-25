## 任務

拆單豁免：旁白改字、humanize 的 sha 戳記、claims 與說明欄互相綁定，分開派會讓 sha 與內容對不上。

工作目錄：`/Users/51mini/dev/vibe-shorts-pipeline`。第三輪稽核指出：52% 只限 2026 上半年（另一篇報導稱五年累計台灣占比 18%），鉤子要帶期間；「收入」與「消費」口徑混用，全文統一成來源（PocketGamer.biz）用的「消費估算」。只做下面的取代與一次搬移，其他句子一字不動。不改 `index.html`／`mix.py`／`build.sh`，不 render，不 git commit，不跑 `approve.py`／`voice.py`／`restamp.sh`。

### 1. `films/pikmin-bloom/narration.md`（照字面）
- 「而且這款遊戲約有一半的商店消費，來自台灣玩家。」→「而且二〇二六年上半年，這款遊戲約一半的消費估算，來自台灣。」
- 「二〇二六年上半年，這款遊戲在兩大手機商店，台灣收入估算約一千八百五十萬美元。」→「二〇二六年上半年，這款遊戲在兩大手機商店，台灣消費估算約一千八百五十萬美元。」
- 「所以在這兩個商店，每兩塊就有一塊多來自台灣玩家。」→「所以在這個估算裡，每兩塊就有一塊多來自台灣。」
- 搬移：「這些是 AppMagic 對 App Store 和 Google Play 的估算。」整行從「錢從哪來」段最後一行，移到該段第 1 行（「二〇二六年上半年，這款遊戲在兩大手機商店…」）的正下方。該段最終順序：①二〇二六年上半年…消費估算約一千八百五十萬美元 ②這些是 AppMagic… ③全球約三千五百七十萬美元，台灣占了約百分之五十二 ④所以在這個估算裡… ⑤而且這款遊戲沒有正式在中國大陸上架。

### 2. 重寫戳記與對照檔
- `audit/humanize.md`：首行 `narration_sha: <narration.md 最終內容 sha256>`（`shasum -a 256 films/pikmin-bloom/narration.md | cut -d' ' -f1`），下面列三條取代與一次搬移「原句 → 新句」。
- `audit/claims.md`：同步改句子；「收入」一律改成「消費估算」，並註明「口徑以 PocketGamer.biz 的 spending 為準；AppMagic 方法說明為商店內購收入（排除平台費用、含稅）；另一篇 2026-11-03 報導稱過去一年台灣淨收入 1370 萬美元、五年累計台灣占比 18%，期間與口徑不同，本片只用 2026 上半年這組」。
- 刪除 `audit/devils-advocate.md`、`audit/coldread-script.md`、`audit/verdicts.md`（舊 sha 的稽核檔，主 session 稍後重跑）。

### 3. 說明欄（`meta/caption-shorts.txt`、`caption-reels.txt`、`caption-threads.txt`）
- 「台灣收入估算約 1850 萬美元」→「台灣消費估算約 1850 萬美元」
- 「所以在這兩個商店，每兩塊就有一塊多來自台灣玩家」→「所以在這個估算裡，每兩塊就有一塊多來自台灣」
- 「官方網路商店的收入不在內」若出現，保留。
三份裡沒有出現的句子就跳過，其餘行不動。

## 驗收

```bash
cd /Users/51mini/dev/vibe-shorts-pipeline
f=films/pikmin-bloom/narration.md
grep -q '而且二〇二六年上半年，這款遊戲約一半的消費估算，來自台灣。' "$f"
grep -q '台灣消費估算約一千八百五十萬美元' "$f"
grep -q '所以在這個估算裡，每兩塊就有一塊多來自台灣。' "$f"
if grep -qE '收入|商店消費|台灣玩家' "$f"; then echo '舊口徑殘留'; exit 1; fi
if grep -qE '[0-9]' "$f"; then echo '旁白殘留阿拉伯數字'; exit 1; fi
python3 - <<'PY'
import re, sys
nar = open('/Users/51mini/dev/vibe-shorts-pipeline/films/pikmin-bloom/narration.md').read()
body = re.sub(r'^#+.*$', '', nar, flags=re.M)
norm = lambda s: re.sub(r'[\s，、：；「」『』（）,.!?？！。]', '', s)
lines = [l for l in nar.split('\n')]
i = next(k for k, l in enumerate(lines) if l.startswith('## 錢從哪來'))
sec = []
for l in lines[i + 1:]:
    if l.startswith('## '): break
    if l.strip(): sec.append(l)
keys = ['台灣消費估算約一千八百五十萬美元', '這些是 AppMagic', '台灣占了約百分之五十二', '所以在這個估算裡', '沒有正式在中國大陸上架']
for k, l in zip(keys, sec):
    if k not in l: print('段內順序錯', k, '↔', l); sys.exit(1)
if len(sec) != 5: print('錢從哪來段不是 5 行', len(sec)); sys.exit(1)
ss = [s for s in re.split(r'[。？！\n]', body) if len(norm(s)) >= 1]
long_ = [s for s in ss if len(norm(s)) > 35]
if long_: print('句超長', long_); sys.exit(1)
n = len(re.sub(r'\s', '', body))
if not (300 <= n <= 420): print('字數', n); sys.exit(1)
if len(re.findall(r'^## ', nar, flags=re.M)) != 5: print('段數不是 5'); sys.exit(1)
if len(re.findall(r'而且|可是|所以|只是', nar)) < 3: print('連接詞不足'); sys.exit(1)
print('OK', n)
PY
sha=$(shasum -a 256 "$f" | cut -d' ' -f1)
head -1 films/pikmin-bloom/audit/humanize.md | grep -q "narration_sha: $sha"
if [ -e films/pikmin-bloom/audit/verdicts.md ]; then exit 1; fi
if [ -e films/pikmin-bloom/audit/devils-advocate.md ]; then exit 1; fi
if [ -e films/pikmin-bloom/audit/coldread-script.md ]; then exit 1; fi
grep -q '消費估算' films/pikmin-bloom/audit/claims.md
for c in caption-shorts caption-reels caption-threads; do
  if grep -qE '台灣收入估算|每兩塊就有一塊多來自台灣玩家' films/pikmin-bloom/meta/$c.txt; then echo "舊句殘留 $c"; exit 1; fi
done
```
預期整段 exit 0 並印出 `OK <字數>`；開工前旁白仍含「商店消費」，第一行 grep 就會失敗。

## 不動
`films/pikmin-bloom/index.html`、`mix.py`、`build.sh`、`cast.json`、`TREATMENT.md`、`SOURCES.md`、`meta/facts.md`、`refs/`、`scripts/`、`tests/`、`PLAN.md`、`films/` 其他資料夾。

## 禁止
1. 不 render、不執行 `build.sh`、不跑 `approve.py`／`voice.py`／`restamp.sh`、不 git commit。
2. 無頭機：禁止回報「請使用者手動貼 token／授權／執行指令」；憑證讀不到＝停手回報阻斷點。
3. 不憑記憶補事實；只做上面列的取代與搬移，不改其他句子。
