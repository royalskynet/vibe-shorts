## 任務

工作目錄：`REPO_ROOT`。只寫 `films/pikmin-bloom/` 底下的文字檔，不改 `index.html`／`mix.py`／`build.sh`，不 render，不 git commit，不跑 `approve.py`、`voice.py`。

先讀：`docs/WRITING.md` §7、`docs/寫稿原則.md`、範本 `films/taipei-silence/narration.md`（只學口吻，不抄句子）、`films/pikmin-bloom/meta/facts.md`、`films/pikmin-bloom/SOURCES.md`、`films/pikmin-bloom/TREATMENT.md`。**不要讀 `refs/viral-text/pikmin-seed.md`**。

## 角度（主 session 定，照做）

單人旁白科普，一支只講一個機制：**同一場活動，兩種語言的公告把台灣寫成兩個樣子；台灣又是這款遊戲最大的收入來源；官方改了，但沒說為什麼。** 只擺事實與數字，結論交給觀眾。

只准用 `meta/facts.md` 判「已查證」的事實，且每句事實限定年份或日期：
- 2026-11-10 起，Pikmin Bloom 五週年與全家便利商店聯名活動。繁中公告寫「全台的全家便利商店門市」，簡中公告寫「日本和中國台灣地區」。
- 玩家反應：新聞報導稱玩家揚言刪帳號、退坑、停止消費。
- 官方後續：移除簡體中文選項，原簡中網址改顯示英文並用 Taiwan；截至 2026-11-12 晚間報導稱官方未公開說明為何不同語言稱呼不同。
- 台灣 2026 上半年消費約 1850 萬美元，全球約 3570 萬美元，占約 52%；來源是 PocketGamer.biz 引 AppMagic 估算，旁白要講「估算」。
- 這款遊戲沒有正式在中國大陸上架（報導）。

段落建議 4–5 段：鉤子（觀眾感受 → 一句翻轉 → 知道這件事有什麼用）→ 同活動兩種寫法 → 錢從哪來（52%）→ 官方改了什麼、沒說什麼 → 落點。段名自由。

不准寫：
1. GPS／個資外洩推論、個人經驗（電話推銷之類）、「退坑或繼續玩都對」這類替觀眾表態的句子。
2. 猜官方動機、下「某某是中國的」這類定論、「道歉」「事件」以外的情緒形容詞。
3. 防衛性中立語言：問法不同、不能直接比較、不代表全部、不能說成同一個原因。範圍限定寫進事實本身。
4. 二元對比句：不是X是Y、是X不是Y、並非、與其說…不如說、看似…實則、你以為…其實。直接講 Y。
5. 「應該」「都能」。正片結尾不放提問；問觀眾的話只寫在說明欄。
6. 不用 Niantic、全家、Pikmin 的 logo 或角色名以外的商標描述；人名不出現。

## 要產出的檔案

1. `films/pikmin-bloom/narration.md`：`## 段名` 分段（3–8 段），旁白正文 300–420 字（不含標題與空白），片長約 60–85 秒；每句 ≤35 字，一句講完一個因果，用「而且／可是／所以／只是」接；數字用國字或阿拉伯數字照範本。
2. 寫完照 genie-humanizer 逐句改成台灣口語，寫 `films/pikmin-bloom/audit/humanize.md`：首行 `narration_sha: <narration.md 最終內容的 sha256>`，下面列「原句 → 新句」。sha 用 `shasum -a 256 films/pikmin-bloom/narration.md | cut -d' ' -f1`。改了稿就重算。
3. `films/pikmin-bloom/audit/claims.md`：逐句列旁白每個數字或事實，對應 F 編號。
4. `films/pikmin-bloom/TREATMENT.md`：只重寫「爆款證據：」那一行以外的內容成這支片的企劃（標題、一句話機制、時限、禁止清單，上面「不准寫」六條搬進去）；「爆款證據：」那一行一字不動。
5. 三份說明欄 `meta/caption-reels.txt`、`meta/caption-shorts.txt`、`meta/caption-threads.txt`、`meta/title-shorts.txt`、`meta/tags.txt`：格式照 `films/taipei-silence/meta/` 同名檔；說明欄寫來源（PocketGamer.biz／AppMagic 估算、NOWnews、自由時報）與 AI 揭露行（照範本）；問觀眾的話放說明欄；不複製範本的台北內容。

## 驗收

```bash
cd REPO_ROOT
python3 - <<'PY'
import re, sys, difflib, pathlib
root = pathlib.Path('REPO_ROOT')
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
if not (3 <= secs <= 8): print('段數', secs); sys.exit(1)
for s in sents(nar):
    if len(norm(s)) > 35: print('句超長', s); sys.exit(1)
bad = r'問法不同|不能直接比較|不代表全部|不能說成|並非|與其說|看似|實則|你以為|應該|都能|不是[^。]{0,25}，?是'
m = re.search(bad, nar)
if m: print('禁用語', m.group(0)); sys.exit(1)
for need in ['52', '中國台灣', '全家', '估算']:
    if need not in nar and need.replace('52', '五十二') not in nar:
        print('缺', need); sys.exit(1)
last = re.split(r'^## .*$', nar, flags=re.M)[-1]
if '？' in last or '?' in last: print('落點段有提問'); sys.exit(1)
r = overlap_fail(nar)
if r: print('抄襲 SEED', r); sys.exit(1)
for f in ['caption-reels.txt', 'caption-shorts.txt', 'caption-threads.txt']:
    t = (root / 'films/pikmin-bloom/meta' / f).read_text()
    if 'taipei' in t.lower() or '台北' in t: print('說明欄殘留範本', f); sys.exit(1)
    r = overlap_fail(t)
    if r: print('說明欄抄襲 SEED', f, r); sys.exit(1)
print('OK words', n, 'secs', secs)
PY
sha=$(shasum -a 256 films/pikmin-bloom/narration.md | cut -d' ' -f1)
head -1 films/pikmin-bloom/audit/humanize.md | grep -q "narration_sha: $sha"
grep -q 'F4' films/pikmin-bloom/audit/claims.md
grep -qE '^爆款證據：.*John Cena' films/pikmin-bloom/TREATMENT.md
test -s films/pikmin-bloom/meta/title-shorts.txt
test -s films/pikmin-bloom/meta/tags.txt
```
預期整段 exit 0 並印出 `OK words … secs …`；開工前 `narration.md` 不存在，python 區塊會失敗。

## 不動
`films/pikmin-bloom/index.html`、`mix.py`、`build.sh`、`cast.json`、`meta/facts.md`、`SOURCES.md`、`refs/`、`scripts/`、`tests/`、`PLAN.md`、`films/` 其他資料夾。

## 禁止
1. 不 render、不執行 `build.sh`、不跑 `approve.py`／`voice.py`、不 git commit。
2. 無頭機：禁止回報「請使用者手動貼 token／授權／執行指令」；憑證讀不到＝停手回報阻斷點。
3. 不讀、不複製 `refs/viral-text/pikmin-seed.md` 的任何句子；不憑記憶補事實，稿裡每個數字都要能在 `meta/facts.md` 找到。
