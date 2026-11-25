## 任務

拆單豁免：旁白改字、humanize 的 sha 戳記、claims 與說明欄互相綁定，分開派會讓 sha 與內容對不上。

工作目錄：`/Users/51mini/dev/vibe-shorts-pipeline`。第二輪反方稽核與冷讀指出：AppMagic 數字是商店內購收入估算（不是玩家「花了」的毛額）、報導與改動位置沒說清楚。只做下面的取代，其他句子一字不動。不改 `index.html`／`mix.py`／`build.sh`，不 render，不 git commit，不跑 `approve.py`／`voice.py`／`restamp.sh`。

### 1. `films/pikmin-bloom/narration.md`（整句取代，照字面）
- 「而且這款遊戲有一大塊收入，來自台灣玩家。」→「而且這款遊戲約有一半的商店消費，來自台灣玩家。」
- 「二〇二六年上半年，兩大手機商店裡，台灣玩家花了約一千八百五十萬美元。」→「二〇二六年上半年，這款遊戲在兩大手機商店，台灣收入估算約一千八百五十萬美元。」
- 「報導稱有玩家揚言刪帳號、退坑、不再消費。」→「NOWnews 報導，有玩家揚言刪帳號、退坑、不再消費。」
- 「官方把簡體中文選項拿掉，原簡中網址改顯示英文，並用 Taiwan。」→「官方把這則公告的簡體中文選項拿掉，原簡中網址改顯示英文，並用 Taiwan。」
- 「截至二〇二六年十一月十二日晚間，報導稱官方沒有公開說明原因。」→「截至二〇二六年十一月十二日晚間，NOWnews 報導官方沒有公開說明原因。」

### 2. 重寫戳記與對照檔
- `audit/humanize.md`：首行 `narration_sha: <narration.md 最終內容 sha256>`（`shasum -a 256 films/pikmin-bloom/narration.md | cut -d' ' -f1`），下面列上面五條「原句 → 新句」。
- `audit/claims.md`：同步改句子；註明「1850／3570 萬美元為 AppMagic 的商店內購收入估算（排除平台費用、含稅），PocketGamer.biz 稱之為玩家消費」，來源 F4。
- 刪除 `audit/devils-advocate.md`、`audit/coldread-script.md`、`audit/verdicts.md`（舊 sha 的稽核檔，主 session 稍後重跑）。

### 3. 說明欄（`meta/caption-shorts.txt`、`caption-reels.txt`、`caption-threads.txt`）
- 「台灣玩家花了約 1850 萬美元」→「台灣收入估算約 1850 萬美元」
- 「報導稱有玩家揚言」→「NOWnews 報導，有玩家揚言」
- 「官方把簡體中文選項拿掉」→「官方把這則公告的簡體中文選項拿掉」
- 「報導稱官方沒公開說明，為什麼不同語言叫法不同」→「NOWnews 報導官方沒有公開說明原因」
三份裡沒有出現的句子就跳過，其餘行不動。

## 驗收

```bash
cd /Users/51mini/dev/vibe-shorts-pipeline
f=films/pikmin-bloom/narration.md
grep -q '而且這款遊戲約有一半的商店消費，來自台灣玩家。' "$f"
grep -q '這款遊戲在兩大手機商店，台灣收入估算約一千八百五十萬美元' "$f"
grep -q 'NOWnews 報導，有玩家揚言刪帳號、退坑、不再消費。' "$f"
grep -q '官方把這則公告的簡體中文選項拿掉' "$f"
grep -q 'NOWnews 報導官方沒有公開說明原因' "$f"
if grep -qE '台灣玩家花了|有一大塊收入|報導稱' "$f"; then echo '舊句殘留'; exit 1; fi
if grep -qE '[0-9]' "$f"; then echo '旁白殘留阿拉伯數字'; exit 1; fi
python3 - <<'PY'
import re, sys
nar = open('/Users/51mini/dev/vibe-shorts-pipeline/films/pikmin-bloom/narration.md').read()
body = re.sub(r'^#+.*$', '', nar, flags=re.M)
norm = lambda s: re.sub(r'[\s，、：；「」『』（）,.!?？！。]', '', s)
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
grep -q '商店內購收入' films/pikmin-bloom/audit/claims.md
for c in caption-shorts caption-reels caption-threads; do
  if grep -qE '台灣玩家花了' films/pikmin-bloom/meta/$c.txt; then echo "舊句殘留 $c"; exit 1; fi
done
```
預期整段 exit 0 並印出 `OK <字數>`；開工前旁白仍含「有一大塊收入」，第一行 grep 就會失敗。

## 不動
`films/pikmin-bloom/index.html`、`mix.py`、`build.sh`、`cast.json`、`TREATMENT.md`、`SOURCES.md`、`meta/facts.md`、`refs/`、`scripts/`、`tests/`、`PLAN.md`、`films/` 其他資料夾。

## 禁止
1. 不 render、不執行 `build.sh`、不跑 `approve.py`／`voice.py`／`restamp.sh`、不 git commit。
2. 無頭機：禁止回報「請使用者手動貼 token／授權／執行指令」；憑證讀不到＝停手回報阻斷點。
3. 不憑記憶補事實；只做上面列的取代，不改其他句子。
