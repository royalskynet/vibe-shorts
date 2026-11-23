## 任務

拆單豁免：旁白改字、humanize 的 sha 戳記、claims、說明欄與事實檔的口徑註記互相綁定，分開派會讓 sha 與內容對不上。

工作目錄：`REPO_ROOT`。反方稽核發現 52% 只涵蓋 App Store 與 Google Play 的估算（官方另有網路商店），稿子要補口徑；另有一句超過 35 字。只做下面的取代，其他句子一字不動。不改 `index.html`／`mix.py`／`build.sh`，不 render，不 git commit，不跑 `approve.py`／`voice.py`／`restamp.sh`。

### 1. `films/pikmin-bloom/narration.md`（整句取代，照字面）
- 「你課的每一筆錢，都算進這款遊戲的收入裡。」→「而且這款遊戲有一大塊收入，來自台灣玩家。」
- 「Pikmin Bloom 的活動公告」開頭不存在時，第 1 句「遊戲公司寫公告的時候，會怎麼叫台灣？」→「Pikmin Bloom 的活動公告，會怎麼稱呼台灣？」
- 「可是同一場活動，兩種語言寫出兩個樣子。」→「可是同一場活動，繁中跟簡中寫出了兩個樣子。」
- 「只是繁中寫「全台的全家便利商店門市」，簡中寫「日本和中國台灣地區」。」→「只是活動公告上，繁中寫「全台的全家便利商店門市」，簡中寫「日本和中國台灣地區」。」
- 「二〇二六年上半年，台灣玩家花了約一千八百五十萬美元。」→「二〇二六年上半年，兩大手機商店裡，台灣玩家花了約一千八百五十萬美元。」
- 「全球約三千五百七十萬美元，占了約百分之五十二。」→「全球約三千五百七十萬美元，台灣占了約百分之五十二。」
- 「所以全球每兩塊裡，有一塊多是台灣玩家出的。」→「所以在這兩個商店，每兩塊就有一塊多來自台灣玩家。」
- 「這些數字是 PocketGamer.biz 引用 AppMagic 的估算。」→「這些是 AppMagic 對 App Store 和 Google Play 的估算。」
- 「截至二〇二六年十一月十二日晚間，報導稱官方沒公開說明，為什麼不同語言叫法不同。」→「截至二〇二六年十一月十二日晚間，報導稱官方沒有公開說明原因。」
- 整行刪除「可是官方改了寫法，卻沒說為什麼。」（與前句重複）。
「落點」段只剩「多關心這件跟生活有關的公共事，一起讓台灣更好。」一行，標題保留。

### 2. 重寫戳記與對照檔
- `audit/humanize.md`：首行 `narration_sha: <narration.md 最終內容 sha256>`（`shasum -a 256 films/pikmin-bloom/narration.md | cut -d' ' -f1`），下面列上面十條「原句 → 新句」（刪除那條寫「→ （刪除）」）。
- `audit/claims.md`：同步改句子與對應欄位；新增一行註明「52% 僅 App Store 與 Google Play 的估算，不含官方網路商店」，來源 F4。
- 刪除 `audit/devils-advocate.md`、`audit/coldread-script.md`、`audit/verdicts.md` 若存在（舊 sha 的稽核檔，主 session 稍後重跑）。

### 3. 事實檔與說明欄口徑
- `SOURCES.md` F4 一項與 `meta/facts.md` 的 `TW_REVENUE_H1_2026_USD`、`GLOBAL_REVENUE_H1_2026_USD`、`TW_SHARE_H1_2026` 三列，在來源／值的欄位後加註「（僅 App Store 與 Google Play 的估算，不含官方網路商店）」。
- `meta/caption-shorts.txt`、`caption-reels.txt`、`caption-threads.txt`：凡含「所以全球每兩塊裡，有一塊多是台灣玩家出的」「這些數字是 PocketGamer.biz 引用 AppMagic 的估算」的段落，改成同一意思：「2026 上半年，在 App Store 和 Google Play，台灣玩家花了約 1850 萬美元，全球約 3570 萬美元，台灣占了約 52%。所以在這兩個商店，每兩塊就有一塊多來自台灣玩家。而且這款遊戲沒有正式在中國大陸上架。這些是 AppMagic 對 App Store 和 Google Play 的估算，由 PocketGamer.biz 報導；官方網路商店的收入不在內。」其餘行不動。

## 驗收

```bash
cd REPO_ROOT
f=films/pikmin-bloom/narration.md
grep -q 'Pikmin Bloom 的活動公告，會怎麼稱呼台灣？' "$f"
grep -q '而且這款遊戲有一大塊收入，來自台灣玩家。' "$f"
grep -q '兩大手機商店裡，台灣玩家花了約一千八百五十萬美元' "$f"
grep -q '台灣占了約百分之五十二' "$f"
grep -q '每兩塊就有一塊多來自台灣玩家' "$f"
grep -q '這些是 AppMagic 對 App Store 和 Google Play 的估算' "$f"
grep -q '報導稱官方沒有公開說明原因' "$f"
if grep -qE '每一筆錢|全球每兩塊|可是官方改了寫法|PocketGamer' "$f"; then echo '舊句殘留'; exit 1; fi
if grep -qE '[0-9]' "$f"; then echo '旁白殘留阿拉伯數字'; exit 1; fi
python3 - <<'PY'
import re, sys
nar = open('REPO_ROOT/films/pikmin-bloom/narration.md').read()
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
grep -q 'App Store' films/pikmin-bloom/audit/claims.md
grep -q 'App Store' films/pikmin-bloom/SOURCES.md
grep -q 'App Store' films/pikmin-bloom/meta/facts.md
for c in caption-shorts caption-reels caption-threads; do
  grep -q 'App Store' films/pikmin-bloom/meta/$c.txt
  if grep -qE '全球每兩塊|每一筆錢' films/pikmin-bloom/meta/$c.txt; then echo "舊句殘留 $c"; exit 1; fi
done
```
預期整段 exit 0 並印出 `OK <字數>`；開工前旁白仍是「遊戲公司寫公告的時候」，第一行 grep 就會失敗。

## 不動
`films/pikmin-bloom/index.html`、`mix.py`、`build.sh`、`cast.json`、`TREATMENT.md`、`refs/`、`scripts/`、`tests/`、`PLAN.md`、`films/` 其他資料夾。

## 禁止
1. 不 render、不執行 `build.sh`、不跑 `approve.py`／`voice.py`／`restamp.sh`、不 git commit。
2. 無頭機：禁止回報「請使用者手動貼 token／授權／執行指令」；憑證讀不到＝停手回報阻斷點。
3. 不憑記憶補事實；只做上面列的取代，不改其他句子。
