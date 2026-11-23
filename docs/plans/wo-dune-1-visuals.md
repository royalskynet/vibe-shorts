## 任務

工作目錄：`/Users/you/dev/vibe-shorts-pipeline`。片目錄 `films/dune-messiah-trap`。旁白 `narration.md` 已核准定稿（17 句、5 段），`index.html` 目前還是 taipei-silence 範本殘件。本單把畫面做出來，一句一卡共 17 卡，並同步 TREATMENT 分鏡。

只做兩件事：
1. 重寫 `films/dune-messiah-trap/index.html`（17 張卡）。
2. 把 `films/dune-messiah-trap/TREATMENT.md` 的分鏡表換成 17 列（其他段落逐字不動）。

不動：`narration.md`、`audit/`、`meta/`、`SOURCES.md`、`mix.py`、`build.sh`、`cast.json`、`pace.json`、`engine.js`、`timeline.js`（範本殘件，`voice.py` 之後才重產，現在整頁載入會因句數對不上而丟錯，這是預期）、`scripts/`、`tests/`、其他片（尤其 `films/pikmin-bloom`）。禁止：render、跑 `build.sh`／`voice.py`／`approve.py`、git commit。無頭機：禁止回報「請使用者手動執行」。

### index.html

先整檔讀完現有 `films/dune-messiah-trap/index.html`，並讀範本脈絡 `films/pikmin-bloom/index.html`（只讀，同一架構的另一支新片）。保留 helpers、`drawCard`、`caption`、`series()`、片尾系列卡、`render`、與契約匯出（`window.DUR`、`render`、`TEXTS`、`CUES`、`SHAKES`、`EV`、`VOICE`、`READY` 全保留，邏輯不改）。`render(t)` 只依賴 `t`，不累積狀態、不讀 `Date.now()`、不發請求。

小人與道具只用 `./illust/illust.mjs` 的 `person`（姿勢 stand／armsUp／shrug／think，臉 none／smile／worried）與 `prop`（document、phone、card、bulb、flag、house、speech、balance、megaphone、question）。沙漠、沙蟲、王冠、帳單、齒輪腦、投幣機、星球、蜥蜴輪廓用 canvas 基本圖形自己畫（弧線、矩形、圓、多邊形），扁平、米色插畫風，不要擬真。

字串（逐字照用）：
- `<title>`：`沙丘其實在警告你別信救世主`
- `SERIES = '用腦袋看世界'`，`EP = 1`，`HANDLE = '@paradoxbar'`。
- 檔首註解換成本片說明與下方「畫面禁止」。
- 只有第 0 卡有大標，大標文字 `沙丘其實在警告你`，第 0 幀就完整顯示；其餘卡沒有大標。

頂端 `FACTS`（唯一數字來源，卡片裡所有阿拉伯數字一律寫 `${FACTS.X}` 或由 FACTS 運算，不准裸寫）：
```js
const FACTS = { Y_ESSAY: 1980, DEATH_TOLL: 61000000000, PLANETS_STERILIZED: 90, Y_ICKE_BOOK: 1999, Y_POLL: 2013, REPTILIAN_BELIEVER_PCT: 4 };
```
（`DEATH_TOLL` 顯示成「610 億」時用 `FACTS.DEATH_TOLL / 1e8` 運算；`meta/facts.md` 已有這些 key，不用改。）

17 卡（`CARDS` 陣列，每卡一行 `{ head, hud, hl, draw }`；`hl` 每個詞必須逐字出現在該卡旁白句內；`hud` 是來源小標，示意畫面寫「示意圖」）：

1. 你是不是也覺得，《沙丘》是英雄打倒壞人的故事？ — 沙漠地平線，高台上一個小人輪廓被光打亮。hud 示意圖。
2. 一個被放逐的王子，帶著部落推翻帝國，自己當上皇帝。 — 一排小人方陣推倒黑色高塔，王冠落在一個小人頭上。示意圖。
3. 可是作者赫伯特在一九八〇年的文章裡，警告大家別把批判能力交給偉大的領袖。 — 一本書翻開，齒輪形的腦從小人頭上飛進王冠。hud 含 `${FACTS.Y_ESSAY}`（Dune Genesis）。
4. 書裡的保羅，被弗瑞曼人當成救世主，發動了聖戰。 — 眾小人向王冠小人舉手，後方旗幟揮動。示意圖。
5. 續集裡他自己算帳，這場聖戰殺了六百一十億人。 — 長帳單展開，數字 `${FACTS.DEATH_TOLL / 1e8}` 億跳動。hud 小說內統計，非真實數字。
6. 同一筆帳裡，還有九十個星球被毀成了死地。 — 一排星球逐顆變黑，數量 `${FACTS.PLANETS_STERILIZED}`。同上 hud。
7. 現實裡的政治，也常用同一種想法。 — 畫面切成左右兩塊對稱色塊（灰藍／鼠尾草綠），中間一條線。示意圖。
8. 當我們認定自己這邊全是好人，對面全是壞人， — 兩塊色塊各自的小人笑臉，對面小人變成灰色剪影。示意圖。
9. 就容易覺得只要我們這邊贏，問題就全解決了。 — 兩塊色塊裡的小人同時舉拳，中間的線震動。示意圖。
10. 對立的陣營裡，都有人這樣想。 — 鏡頭拉遠，兩塊色塊鏡像對稱。示意圖。
11. 把壞人想得越徹底，連外星人都能被套進去當壞人。 — 地球上空浮現一個抽象的外星輪廓被打上叉。示意圖。
12. 一九九九年，大衛·艾克出書說，蜥蜴人的血統網絡，控制著各國政府。 — 一本書立起，政府大樓上方有線連到鱗片紋理的輪廓。hud 含 `${FACTS.Y_ICKE_BOOK}`（《The Biggest Secret》）。
13. 二〇一三年美國有一份民調，百分之四的受訪登記選民， — 一百個小人方陣，其中 `${FACTS.REPTILIAN_BELIEVER_PCT}` 個亮起芥末黃。hud 含 `${FACTS.Y_POLL}`（Public Policy Polling）。
14. 回答相信變形蜥蜴人在操控社會。 — 亮起的那幾個小人頭上冒出問號，旁邊一個變形輪廓。hud 同上。
15. 赫伯特在文章結尾，叫讀者別把他當成領袖。 — 作者剪影把王冠摘下放在地上。hud 含 `${FACTS.Y_ESSAY}`（Dune Genesis）。
16. 當我們只按陣營接受答案，就是把判斷力交了出去。 — 一條岔路，小人把齒輪腦放進路口的投幣機。示意圖。
17. 自由，甚至生命的決定權，就可能落到不必對你負責的人手裡。 — 投幣機吐出一張票，一隻不帶表情的手把齒輪腦收進口袋，畫面定格。示意圖。

畫面禁止：電影劇照與海報元素、演員擬真畫像、政黨標誌／黨旗／黨徽、候選人姓名與臉、真實人物肖像（艾克、赫伯特只畫剪影）、「我們這邊對面那邊」不得對應任何真實台灣政黨名稱。

### TREATMENT.md

只改 `## 分鏡 v1` 那一節的表格：表頭不變（`| 段 | 卡 | 內容（字幕） | 動作（畫面） | 衝擊事件 | 來源 |`），換成上面 17 卡共 17 列；段名依旁白段（鉤子＝1–2、代價＝3–6、類比＝7–10、延伸＝11–14、落點＝15–17）；「內容（字幕）」填該卡旁白逐字；「動作」取上面畫面描述；「衝擊事件」全填 `—`；「來源」填 F 編號（3、15 用 F1；5、6 用 F2；12–14 用 F3；其餘「示意」）。節標題改 `## 分鏡 v2`。動作欄不得含：科技、進步、發展、意義、未來、希望、重大、象徵、氛圍、感覺、概念。其餘段落逐字不動。

## 驗收

```bash
cd /Users/you/dev/vibe-shorts-pipeline
F=films/dune-messiah-trap
[ "$(shasum -a 256 $F/narration.md | cut -d' ' -f1)" = "706ab410c749e5d0dd91d54b96661df8e11c94540facf21524e8f23dbc577584" ] || { echo 'narration 被改'; exit 1; }
n=$(find $F/audit $F/meta $F/mix.py $F/build.sh $F/cast.json $F/pace.json $F/SOURCES.md $F/timeline.js $F/engine.js $F/narration.md -newer docs/plans/wo-dune-1-visuals.md | wc -l | tr -d ' ')
[ "$n" = "0" ] || { echo "不該動的檔被動了 $n"; exit 1; }
for bad in '台北' '藍大於綠' '沉默螺旋' '選前看懂台北' 'taipei'; do
  if grep -q "$bad" $F/index.html; then echo "index 殘留：$bad"; exit 1; fi
done
grep -q '沙丘其實在警告你別信救世主' $F/index.html || { echo 'title 沒換'; exit 1; }
grep -q "沙丘其實在警告你'" $F/index.html || grep -q '沙丘其實在警告你"' $F/index.html || grep -q '沙丘其實在警告你`' $F/index.html || { echo '封面大標沒放'; exit 1; }
python3 - <<'PY'
import re, sys
f = '/Users/you/dev/vibe-shorts-pipeline/films/dune-messiah-trap/'
h = open(f + 'index.html', encoding='utf-8').read()
lines = [l.strip() for l in open(f + 'narration.md', encoding='utf-8') if l.strip() and not l.startswith('#')]
blk = re.search(r"const CARDS = \[(.*?)\n\];", h, re.S)
if not blk: print('沒有 CARDS'); sys.exit(1)
cards = re.findall(r"^\s*\{\s*head:.*$", blk.group(1), re.M)
if len(cards) != 17 or len(lines) != 17: print('卡數或旁白句數不是 17', len(cards), len(lines)); sys.exit(1)
for i, (c, ln) in enumerate(zip(cards, lines), 1):
    hl = re.search(r"hl:\s*\[(.*?)\]", c)
    for w in re.findall(r"'([^']+)'", hl.group(1) if hl else ''):
        if w not in ln: print(f'卡{i} hl「{w}」不在旁白：{ln}'); sys.exit(1)
b = re.search(r"const FACTS = \{(.*?)\};", h, re.S)
if not b: print('沒有 FACTS'); sys.exit(1)
src = open(f + 'meta/facts.md', encoding='utf-8').read().replace(',', '')
pairs = re.findall(r"(\w+):\s*(\d+)", b.group(1))
if len(pairs) != 6: print('FACTS 不是 6 項', pairs); sys.exit(1)
for k, v in pairs:
    if not re.search(r'\b' + k + r'\b', src) or v not in src: print('facts.md 缺', k, v); sys.exit(1)
bare = {n for line in cards for n in re.findall(r"(?<![\w.$}])\d{3,}", line)}
if bare: print('卡片裸寫數字', bare); sys.exit(1)
t = open(f + 'TREATMENT.md', encoding='utf-8').read()
if '## 分鏡 v2' not in t or '## 分鏡 v1' in t: print('TREATMENT 節標題沒換'); sys.exit(1)
sec = t.split('## 分鏡 v2', 1)[1]
rows = [r for r in sec.splitlines() if r.startswith('|')]
if len(rows) != 19: print('分鏡表列數不是 表頭+分隔+17', len(rows)); sys.exit(1)
for r in rows[2:]:
    for w in ['科技', '進步', '發展', '意義', '未來', '希望', '重大', '象徵', '氛圍', '感覺', '概念']:
        if w in r.split('|')[4]: print('動作含抽象詞', w); sys.exit(1)
print('OK')
PY
echo ALL_OK
```
預期整段 exit 0，最後印 `ALL_OK`。開工前 `index.html` 還是台北範本，第一個殘留檢查就會失敗。
