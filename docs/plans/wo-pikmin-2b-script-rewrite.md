## 任務

工作目錄：`/Users/51mini/dev/vibe-shorts-pipeline`。**重寫** `films/pikmin-bloom/narration.md` 與相關文字檔（上一版是事實清單，沒有鉤子、不是口語，還混進查證資料沒有的句子，整份作廢）。不改 `index.html`／`mix.py`／`build.sh`，不 render，不 git commit，不跑 `approve.py`、`voice.py`。

先讀：`docs/WRITING.md` §7 與 §8、`docs/寫稿原則.md`、範本 `films/taipei-silence/narration.md`（學它的口吻與節奏：問句鉤子、生活化比喻、「可是／所以」接句；不抄句子）、`films/pikmin-bloom/meta/facts.md`、`films/pikmin-bloom/SOURCES.md`、`films/pikmin-bloom/refs/evidence/F1.txt` 到 `F5.txt`。**不要讀 `refs/viral-text/pikmin-seed.md`**。

## 這是旁白，不是摘要

單人男聲念給手機觀眾聽，每句 15–35 字，一句講完一個因果。數字要換成聽得懂的比喻或比較（例如把「五成二」說成「每賺兩塊，有一塊多是台灣玩家付的」這類可驗算的講法，算式必須從 facts.md 的數字推得出來）。讀起來像朋友在講一件剛發生的事。

## 角度（主 session 定，照做）

一支只講一個機制：**同一場活動，兩種語言的公告把台灣寫成兩個樣子；台灣是這款遊戲最大的收入來源；官方改了，但沒說為什麼。** 只擺事實與數字，結論交給觀眾。

段落固定 4–5 段，每段 `## 段名`：
1. 鉤子（10 秒內）：以問句開頭，先抓觀眾的感受（例：遊戲公司寫公告的時候，會怎麼稱呼台灣），接一句翻轉（同一場活動，兩種語言寫出兩個樣子），再一句這件事跟你的關係（你課的金，跟這個寫法有關）。**第一句不准以日期或數字開頭。**
2. 兩種寫法：2026-11-10 起 Pikmin Bloom 五週年與全家便利商店聯名；繁中寫「全台的全家便利商店門市」，簡中寫「日本和中國台灣地區」。
3. 錢從哪來：2026 上半年台灣消費約 1850 萬美元，全球約 3570 萬美元，占約 52%，來源 PocketGamer.biz 引 AppMagic **估算**；加一句這款遊戲沒有正式在中國大陸上架（報導）。
4. 官方改了什麼：報導稱玩家揚言刪帳號、退坑、停止消費；官方移除簡中選項，原簡中網址改顯示英文並用 Taiwan；截至 2026-11-12 晚間報導稱官方未公開說明為什麼不同語言稱呼不同。
5. 落點：一句立場，請大家多關心這件跟生活有關的公共事（照 `docs/WRITING.md` §7 第 8 條），不放提問。

## 不准寫（出現就是不合格）

1. 查證資料（`meta/facts.md`、`refs/evidence/`）裡沒有的任何事實。上一版的「僅在台灣地區提供完整服務」「全球營收為全年總計」「玩家請留意」「數字皆為…非官方公告」都是編的，不准再出現。
2. GPS／個資外洩推論、個人經驗、「退坑或繼續玩都對」這類替觀眾表態的句子；猜官方動機；「某某是中國的」這類定論。
3. 防衛性中立語言：問法不同、不能直接比較、不代表全部、不能說成同一個原因。範圍限定寫進事實本身（日期、平台、對象）。
4. 二元對比句：不是X是Y、是X不是Y、並非、與其說…不如說、看似…實則、你以為…其實。直接講 Y。
5. 「應該」「都能」；正片結尾提問；命令觀眾做事（請…）。
6. Niantic、全家、Pikmin 的 logo 描述；人名。

## 要產出的檔案

1. `films/pikmin-bloom/narration.md`：4–5 段，旁白正文 300–420 字（不含標題與空白），約 60–85 秒。
2. 寫完照 genie-humanizer 逐句改成台灣口語，寫 `films/pikmin-bloom/audit/humanize.md`：首行 `narration_sha: <narration.md 最終內容 sha256>`（`shasum -a 256 films/pikmin-bloom/narration.md | cut -d' ' -f1`），下面列「原句 → 新句」。改稿後重算。
3. `films/pikmin-bloom/audit/claims.md`：逐句列旁白每個數字或事實，對應 F 編號與 `refs/evidence/F<n>.txt` 的原文片段。
4. `films/pikmin-bloom/TREATMENT.md`：「爆款證據：」那一行一字不動，其餘改成這支片的企劃（標題、一句話機制、時限、禁止清單）。上一版若已改好且合格可保留。
5. `meta/caption-reels.txt`、`caption-shorts.txt`、`caption-threads.txt`、`title-shorts.txt`、`tags.txt`：格式照 `films/taipei-silence/meta/` 同名檔；寫來源（PocketGamer.biz／AppMagic 估算、NOWnews、自由時報）與 AI 揭露行（照範本）；問觀眾的話放說明欄。上一版若已合格可保留。

## 驗收

```bash
cd /Users/51mini/dev/vibe-shorts-pipeline
python3 - <<'PY'
import re, sys, difflib, pathlib
root = pathlib.Path('/Users/51mini/dev/vibe-shorts-pipeline')
seed = (root / 'refs/viral-text/pikmin-seed.md').read_text()
def norm(s): return re.sub(r'[\s，、：；「」『』（）,.!?？！。]', '', s)
def sents(t):
    t = re.sub(r'^#+.*$', '', t, flags=re.M)
    return [s.strip() for s in re.split(r'[。？！\n]', t) if len(norm(s)) >= 6]
SEED_S = [norm(s) for s in sents(seed)]
SEED_N = norm(seed)
def overlap_fail(text):
    for a in sents(text):
        na = norm(a)
        if any(difflib.SequenceMatcher(None, na, b).ratio() >= 0.5 for b in SEED_S):
            return 'sentence-sim: ' + a
        for i in range(0, max(1, len(na) - 11)):
            if len(na) >= 12 and na[i:i+12] in SEED_N:
                return '12gram: ' + a
    return None
ctrl = '以下是旁白。\n' + '但真正應該出來說明的公司，反而沒有受到同等程度的追問。'
if overlap_fail(ctrl) is None:
    print('負控制未失敗，相似度閘形同虛設'); sys.exit(1)
nar = (root / 'films/pikmin-bloom/narration.md').read_text()
body = re.sub(r'^#+.*$', '', nar, flags=re.M)
n = len(re.sub(r'\s', '', body))
if not (300 <= n <= 420): print('字數', n); sys.exit(1)
secs = len(re.findall(r'^## ', nar, flags=re.M))
if not (4 <= secs <= 5): print('段數', secs); sys.exit(1)
ss = sents(nar)
for s in ss:
    if len(norm(s)) > 35: print('句超長', s); sys.exit(1)
avg = sum(len(norm(s)) for s in ss) / len(ss)
if avg < 14: print('平均句長過短（像清單）', round(avg, 1)); sys.exit(1)
first = re.split(r'^## .*$', nar, flags=re.M)[1].strip()
if '？' not in first and '?' not in first: print('鉤子段沒有問句'); sys.exit(1)
if re.match(r'[0-9０-９]', first): print('第一句以數字開頭'); sys.exit(1)
if len(re.findall(r'而且|可是|所以|只是', nar)) < 3: print('接句連接詞不足'); sys.exit(1)
bad = r'問法不同|不能直接比較|不代表全部|不能說成|並非|與其說|看似|實則|你以為|應該|都能|不是[^。]{0,25}，?是|僅在台灣|全年|請留意|玩家請|文案已調整|非官方公告|請大家'
m = re.search(bad, nar)
if m: print('禁用語', m.group(0)); sys.exit(1)
allowed = {'2026', '11', '10', '12', '1850', '3570', '52', '2', '5'}
for d in re.findall(r'[0-9]+', nar):
    if d not in allowed: print('白名單外數字', d); sys.exit(1)
for need in ['中國台灣', '全家', '估算']:
    if need not in nar: print('缺', need); sys.exit(1)
if not re.search(r'52|五十二|五成二|一半', nar): print('缺占比'); sys.exit(1)
last = re.split(r'^## .*$', nar, flags=re.M)[-1]
if '？' in last or '?' in last: print('落點段有提問'); sys.exit(1)
r = overlap_fail(nar)
if r: print('抄襲 SEED', r); sys.exit(1)
for f in ['caption-reels.txt', 'caption-shorts.txt', 'caption-threads.txt']:
    t = (root / 'films/pikmin-bloom/meta' / f).read_text()
    if 'taipei' in t.lower() or '台北' in t: print('說明欄殘留範本', f); sys.exit(1)
    r = overlap_fail(t)
    if r: print('說明欄抄襲 SEED', f, r); sys.exit(1)
print('OK words', n, 'secs', secs, 'avg', round(avg, 1))
PY
sha=$(shasum -a 256 films/pikmin-bloom/narration.md | cut -d' ' -f1)
head -1 films/pikmin-bloom/audit/humanize.md | grep -q "narration_sha: $sha"
grep -q 'F4' films/pikmin-bloom/audit/claims.md
grep -qE '^爆款證據：.*John Cena' films/pikmin-bloom/TREATMENT.md
test -s films/pikmin-bloom/meta/title-shorts.txt
test -s films/pikmin-bloom/meta/tags.txt
```
預期整段 exit 0 並印出 `OK words … secs … avg …`；上一版稿（7 段、平均句長短、無問句鉤子、含「僅在台灣」）會在段數那一關失敗。

## 不動
`films/pikmin-bloom/index.html`、`mix.py`、`build.sh`、`cast.json`、`meta/facts.md`、`SOURCES.md`、`refs/`、`scripts/`、`tests/`、`PLAN.md`、`films/` 其他資料夾。

## 禁止
1. 不 render、不執行 `build.sh`、不跑 `approve.py`／`voice.py`、不 git commit。
2. 無頭機：禁止回報「請使用者手動貼 token／授權／執行指令」；憑證讀不到＝停手回報阻斷點。
3. 不讀、不複製 `refs/viral-text/pikmin-seed.md` 的任何句子；不憑記憶補事實，稿裡每個數字都要能在 `meta/facts.md` 找到。
