## 任務

拆單豁免：index.html 畫面、facts.md 新列、TREATMENT 分鏡共用同一張 15 卡表，分開派會讓三處對不上。

工作目錄：`REPO_ROOT`。片目錄 `films/pikmin-bloom`。旁白 `narration.md` 已核准定稿（sha256 見驗收），共 15 句、5 段；`index.html` 目前還是 taipei-silence 的範本殘件。本單把畫面做出來。三件事：

1. 重寫 `films/pikmin-bloom/index.html`（15 張卡，一句一卡）。
2. 補 `films/pikmin-bloom/meta/facts.md` 的新 FACTS 列。
3. 外科手術式修改 `films/pikmin-bloom/TREATMENT.md`（只改下面列的幾處，其餘逐字不動）。

不動：`narration.md`、`audit/`、`meta/caption-*.txt`、`mix.py`、`build.sh`、`cast.json`、`pace.json`、`SOURCES.md`、`engine.js`、`timeline.js`（範本殘件，`voice.py` 之後才重產，現在整頁載入會因句數對不上而丟錯，這是預期）、`scripts/`、`tests/`、`PLAN.md`、其他片。禁止：render、跑 `build.sh`／`voice.py`／`approve.py`／`restamp.sh`、git commit。無頭機：禁止回報「請使用者手動貼 token／授權／執行指令」。

### 1. index.html

以現有檔為骨架（先整檔讀完）：保留 helpers（`say`、`plain`、`rr`、`man`、`fig`、`crowd`、`bars`、`framed` 用得到的就留，用不到的可刪）、`drawCard`、`caption`、`series()`、片尾系列卡、`render`、與契約匯出（`window.DUR`、`render`、`TEXTS`、`CUES`、`SHAKES`、`EV`、`VOICE`、`READY` 全部保留，邏輯不改）。`render(t)` 只依賴 `t`，不累積狀態、不讀 `Date.now()`、不發請求。小人與道具只用 `./illust/illust.mjs` 的 `person`（姿勢 stand／armsUp／shrug／think，臉 none／smile／worried）與 `prop`（document、phone、card、bulb、flag、house、speech、balance、megaphone、question）。

字串（逐字照用）：
- `<title>`：`Pikmin Bloom 公告怎麼稱呼台灣`
- `SERIES = '皮克敏公告風波'`，`EP = 1`，`HANDLE = '@paradoxbar'` 不變。
- 檔首註解改寫成皮克敏片的說明，禁止清單註解換成本片的（見下方「畫面禁止」）。

頂端 `FACTS`（唯一的數字來源；卡片裡所有阿拉伯數字一律寫 `${FACTS.X}`，不准裸寫）：
```js
const FACTS = {
  Y2026: 2026,
  EVENT_MONTH: 11,
  EVENT_DAY: 10,
  STATUS_DAY: 12,
  TW_REV_WAN: 1850,       // 台灣 2026 上半年內購營收估算，萬美元
  GLOBAL_REV_WAN: 3570,   // 全球同口徑，萬美元
  TW_SHARE: 52,           // 台灣占比 %
};
const QUOTE_ZH_TW = '全台的全家便利商店門市';   // F1 繁中公告用語
const QUOTE_ZH_CN = '日本和中國台灣地區';       // F1 簡中公告用語，維持此字形，不轉簡體
```
（引文兩句放在 FACTS 外，因為 precheck 只掃 FACTS 的數字；字必須與 `meta/facts.md` 的 `ISSUE_TEXT_ZH_CN` 與旁白完全一致。）

`CARDS`：恰好 15 張，順序與旁白行一一對應（下表），每張一行 `{ head: '…', hud: '…', hl: [...], draw: fn }`，`hl` 的每個詞必須是該句旁白的子字串（表中 hl 欄以「、」分隔多個詞，各自是陣列的一個元素）。`if (TL.lines.length !== N) throw …` 的檢查保留（N＝`CARDS.length`）。封面大標只在第 0 卡畫，`head` 取 `稱呼台灣`（4 字，170px 寬約 680px，放得下）；其餘卡的 `head` 只當識別，不畫在畫面上。

| 卡 | 旁白句（摘要） | head | hud（來源列） | hl | 畫面動作（程式畫，具體可看） |
|---|---|---|---|---|---|
| 1 | 公告怎麼稱呼台灣？ | 稱呼台灣 | 示意圖 | 稱呼台灣 | 小人（think）拿手機，上方浮出一張空白公告 document，問號 prop 搖擺 |
| 2 | 繁中跟簡中寫出兩個樣子 | 兩個樣子 | 示意圖 | 兩個樣子 | 畫面一分為二：左 document 標「繁中」，右 document 標「簡中」，右邊與左邊錯開 12px 對比 |
| 3 | 兩大手機商店約一半內購營收估算來自台灣 | 約一半 | PocketGamer.biz | 約一半 | 兩個手機 prop 並排標「App Store」「Google Play」，上方一個圓餅從 0 長到約一半（半圓以陶土紅填），圓餅旁標「估算」 |
| 4 | `${Y2026}` 年 `${EVENT_MONTH}` 月 `${EVENT_DAY}` 日起五週年、全家聯名 | 五週年聯名 | NOWnews | 五週年 | 日曆方塊顯示 `${FACTS.EVENT_MONTH}/${FACTS.EVENT_DAY}`，旁邊 house prop 當便利商店，小人 armsUp |
| 5 | 繁中寫「全台的全家便利商店門市」，簡中寫「日本和中國台灣地區」 | 兩種寫法 | NOWnews、UDN | 繁中、簡中 | 兩張 document 卡並排，卡上分別大字印 `QUOTE_ZH_TW`、`QUOTE_ZH_CN`（可換行，字夠大），簡中卡上「中國」二字用陶土紅標出 |
| 6 | 七月報導，上半年台灣內購營收估算約 1850 萬美元 | 台灣估算 | PocketGamer.biz | 一千八百五十萬美元 | 長條 `bars` 風格：一條台灣長條從 0 長到標籤 `${FACTS.TW_REV_WAN} 萬美元（估算）`，標示 `${FACTS.Y2026} 上半年` |
| 7 | 這是 AppMagic 的估算，只算 App Store 加 Google Play | AppMagic 估算 | AppMagic | AppMagic | 兩個商店圖示 card prop 被框起來，框外打斜線的第三個「官方網路商店」灰掉，字樣「估算，不含官方網路商店」 |
| 8 | 全球約 3570 萬美元，台灣占約百分之五十二 | 占比 | PocketGamer.biz | 百分之五十二 | 全球長條 `${FACTS.GLOBAL_REV_WAN} 萬`，其中台灣段以陶土紅填到 `${FACTS.TW_SHARE}%`，百分比數字大字跳升 |
| 9 | 每兩塊就有一塊多來自台灣 | 每兩塊 | 依 AppMagic 估算 | 一塊多 | 兩枚硬幣一組，連續排三組，每組其中一枚染陶土紅，其餘米色，依序出現 |
| 10 | 這款遊戲沒有正式在中國大陸上架 | 沒有上架 | NOWnews | 沒有正式 | 一個商店貨架（card prop 排成格），其中一格貼上「未上架」灰章，小人 shrug，不畫地圖與國界 |
| 11 | 有玩家揚言刪帳號、退坑、不再消費 | 玩家反應 | NOWnews | 刪帳號、退坑、不再消費 | 三個手機 prop 依序從亮變暗，旁邊 speech prop 冒出，小人 worried |
| 12 | 官方把簡中選項拿掉，原簡中網址改顯示英文，並用 Taiwan | 官方調整 | NOWnews、UDN、自由時報 | 拿掉、Taiwan | 語言選單三列：繁中、簡中（被橫線劃掉、淡出）、English；下方網址列文字由「簡中」換成「English」，出現 `Taiwan` 字樣 |
| 13 | 截至 `${Y2026}` 年 `${EVENT_MONTH}` 月 `${STATUS_DAY}` 日晚間，官方沒有公開說明 | 沒有說明 | NOWnews | 沒有公開說明 | 麥克風 megaphone prop 旁一個空白對話框 speech，框內只有跳動的省略號，右下標 `${FACTS.EVENT_MONTH}/${FACTS.STATUS_DAY} 晚間` |
| 14 | 大家可以用投入時間或金錢與否，來投票 | 用投入投票 | 示意圖 | 投入時間或金錢、投票 | 一個時鐘與一枚硬幣各丟進一個投票箱（balance 或 house prop 皆可），小人 smile |
| 15 | 退坑或繼續玩，都是個人自由 | 個人自由 | 示意圖 | 個人自由 | 兩個小人往兩個方向走開（一個向左、一個向右），都 smile，地面一條線 |

hud（來源列）寫在 `CARDS` 裡就是字串，`drawCard` 畫 `來源｜${cd.hud}`。卡 3／6／8 若 hud 太長，維持上表字串即可；第 14、15 卡 hud 用「示意圖」。

畫面禁止（寫進檔首註解）：
- 不畫地圖、國界、`prop('flag')`、任何國旗；不畫 Pikmin 角色；不畫 Niantic、全家的 logo（用「全家」兩字文字與通用 house prop 即可，不模仿招牌）。
- `ISSUE_TEXT_INAPP`（遊戲內台北活動通知）不上畫面。
- 引文只能用上面兩個常數的字，不得自行翻成簡體或換字。
- 畫面不得出現超出旁白的主張；錢的卡一律帶「估算」字樣；卡 3、7 要有「兩大手機商店／App Store 與 Google Play」。
- 不出現「應該」「都能」。

### 2. meta/facts.md

在現有表格末尾補 7 列，key 名逐字：`Y2026`、`EVENT_MONTH`、`EVENT_DAY`、`STATUS_DAY`、`TW_REV_WAN`、`GLOBAL_REV_WAN`、`TW_SHARE`，值與來源如下（來源欄寫法比照既有列）：
- `Y2026`＝2026：F1／F4，旁白中的年份。
- `EVENT_MONTH`＝11、`EVENT_DAY`＝10：F1，活動自 2026-11-10 展開。
- `STATUS_DAY`＝12：F2，截至 2026-11-12 晚間報導稱官方未公開說明。
- `TW_REV_WAN`＝1850：對應 `TW_REVENUE_H1_2026_USD`＝18500000 換成萬美元，AppMagic 內購淨營收估算，僅 App Store 與 Google Play。
- `GLOBAL_REV_WAN`＝3570：對應 `GLOBAL_REVENUE_H1_2026_USD`＝35700000，同口徑。
- `TW_SHARE`＝52：對應 `TW_SHARE_H1_2026`（52%），同口徑。
另補兩列文字型：`QUOTE_ZH_TW`＝全台的全家便利商店門市（F1 繁中公告用語）、`QUOTE_ZH_CN`＝日本和中國台灣地區（F1 簡中公告用語）。既有列不動。

### 3. TREATMENT.md（外科手術式，只改這五處）

1. 標題（第 1 行）改成：`# Pikmin Bloom：同一場活動，公告怎麼稱呼台灣（單人旁白科普）`
2. 第一段（「格式照 …」那段）把「台灣又是這款遊戲最大的收入來源」換成「台灣占這款遊戲在兩大手機商店內購營收估算的約一半（AppMagic 估算，2026 上半年）」，其餘字不動。
3. `## 時限` 裡「結論收在落點」那一條：把「落點立場是請大家多關心這件跟生活有關的公共事，一起讓台灣更好；」換成「落點照使用者核准定稿：「大家可以用投入時間或金錢與否，來投票。」「退坑或繼續玩，都是個人自由。」；」，條內其餘字不動。
4. `## 禁止清單` 第 1 條：刪掉「，不得說「退坑或繼續玩都對」」這一段，其他字不動。第 2–6 條與其餘時限條目逐字不動。
5. `## 分鏡（草擬）` 的表格換成 15 列，表頭不變（`| 段 | 卡 | 內容（字幕） | 動作（畫面） | 衝擊事件 | 來源 |`），列內容取自上面「卡」表：段名依旁白段（鉤子＝1–3、兩種寫法＝4–5、錢從哪來＝6–10、官方改了什麼＝11–13、落點＝14–15）；「內容（字幕）」填該卡旁白逐字；「動作」取畫面動作欄（不得含：科技、進步、發展、意義、未來、希望、重大、象徵、氛圍、感覺、概念）；「衝擊事件」全填 `—`；「來源」填 F 編號（1–2、4、5 用 F1；6–10 用 F4，其中 10 用 F5；11 用 F3；12 用 F2；13 用 F2；14–15 填 `—`）。最後把該節標題的「（草擬）」去掉。
6. `## 写法决定` 節（簡體字標題與內容）改成繁體：標題 `## 寫法決定`，條目依序為：「只用 `meta/facts.md` 判已查證的事實，每句事實限定年份或日期」「52、中國台灣、全家、估算為本支稿必備數字與地名；金額一律帶「估算」與「兩大手機商店」」「玩家反應、官方調整、營收估算分別對應 F3、F2、F4 的查證來源」「說明欄寫來源（PocketGamer.biz／AppMagic 估算、NOWnews、自由時報）與 AI 揭露行（照範本）；問觀眾的話放說明欄；不複製範本的台北內容」「`TREATMENT.md` 的「爆款證據：」一行一字不動」。（這一節若有其他現存條目，語意保留、字改繁體。）

爆款證據那一行（以「爆款證據：」開頭的整行）逐字不動；`## 時限`、`## 禁止清單` 其餘內容逐字不動。

## 驗收

```bash
set -e
cd REPO_ROOT
F=films/pikmin-bloom
# 不該動的檔
[ "$(shasum -a 256 $F/narration.md | cut -d' ' -f1)" = "06bea4a63db540617277c22004816df1fff802ba839387fbdb9f200863a34cc5" ] || { echo 'narration 被改'; exit 1; }
n=$(find $F/audit $F/meta/caption-shorts.txt $F/meta/caption-reels.txt $F/meta/caption-threads.txt $F/mix.py $F/build.sh $F/cast.json $F/pace.json $F/SOURCES.md $F/timeline.js $F/engine.js $F/narration.md -newer /tmp/wo3b-start | wc -l | tr -d ' ')
[ "$n" = "0" ] || { echo "不該動的檔被動了 $n"; exit 1; }
# 爆款證據行逐字不動
[ "$(grep '^爆款證據：' $F/TREATMENT.md | shasum -a 256 | cut -d' ' -f1)" = "3846cd651667a88789693240f2b03462e4a08dff5d000066ff940c8c30fe58bc" ] || { echo '爆款證據行被改'; exit 1; }
# 禁止清單第 2–6 條逐字不動
[ "$(grep -E '^- [2-6]\. ' $F/TREATMENT.md | shasum -a 256 | cut -d' ' -f1)" = "4bf50eefa631d6e110d60153b03eb3d8e3c249e44410c53577c82736bf7ad93b" ] || { echo '禁止清單 2-6 被改'; exit 1; }
# TREATMENT 舊句清除、新句到位
for bad in '退坑或繼續玩都對' '多關心這件跟生活有關' '最大的收入來源' '消費探究' '写法决定' '草擬'; do
  if grep -q "$bad" $F/TREATMENT.md; then echo "TREATMENT 殘留：$bad"; exit 1; fi
done
grep -q '投入時間或金錢與否' $F/TREATMENT.md || { echo 'TREATMENT 缺落點定稿'; exit 1; }
grep -q '公告怎麼稱呼台灣' $F/TREATMENT.md || { echo 'TREATMENT 標題沒換'; exit 1; }
python3 - <<'PY'
import sys, re
sys.path.insert(0, 'REPO_ROOT/scripts')
import precheck as p
t = open('REPO_ROOT/films/pikmin-bloom/TREATMENT.md', encoding='utf-8').read()
rows = p.storyboard_rows(t)
head = [c.strip() for c in rows[0].strip('|').split('|')]
ai = next(i for i, c in enumerate(head) if c.startswith('動作'))
body = rows[2:]
if len(body) != 15: print('分鏡不是 15 列', len(body)); sys.exit(1)
for ln in body:
    cells = [c.strip() for c in ln.strip('|').split('|')]
    if len(cells) < len(head): print('欄位不足', ln[:30]); sys.exit(1)
    hit = [w for w in p.ABSTRACT if w in cells[ai]]
    if hit or cells[ai] in ('', '—', '-'): print('動作不合格', cells[1], hit); sys.exit(1)
if p.forbid_problems(t) or p.viral_problems(t): print('禁止清單或爆款證據閘門不過'); sys.exit(1)
print('TREATMENT OK')
PY
# index.html
H=$F/index.html
if grep -qE '台北|賴清德|侯友宜|藍綠|民調|選前看懂|LAI_|HOU_|Y2024|Y2018|民進黨|國民黨|沉默螺旋|Griffin' $H; then echo 'index.html 殘留台北範本內容'; grep -nE '台北|賴清德|侯友宜|藍綠|民調|選前看懂|LAI_|HOU_|Y2024|Y2018|民進黨|國民黨|沉默螺旋|Griffin' $H | head; exit 1; fi
c=$(grep -cE '^\s*\{\s*head:' $H); [ "$c" = "15" ] || { echo "CARDS 不是 15 張：$c"; exit 1; }
grep -q 'TL.lines.length !== N' $H || { echo '句數檢查被移除'; exit 1; }
grep -q "SERIES = '皮克敏公告風波'" $H || { echo 'SERIES 不對'; exit 1; }
grep -q 'title>Pikmin Bloom 公告怎麼稱呼台灣' $H || { echo 'title 不對'; exit 1; }
for k in 'window.DUR' 'window.render' 'window.TEXTS' 'window.CUES' 'window.SHAKES' 'window.EV' 'window.VOICE' 'window.READY'; do
  grep -q "$k" $H || { echo "契約匯出缺 $k"; exit 1; }
done
if grep -qE "flag'|prop\('flag" $H; then echo '畫面用了 flag'; exit 1; fi
if grep -qE 'ISSUE_TEXT_INAPP|中國台灣台北' $H; then echo '遊戲內通知文字上畫面'; exit 1; fi
grep -q "QUOTE_ZH_CN = '日本和中國台灣地區'" $H || { echo '簡中引文字形不對'; exit 1; }
grep -q "QUOTE_ZH_TW = '全台的全家便利商店門市'" $H || { echo '繁中引文字形不對'; exit 1; }
# 模組程式語法
python3 - <<'PY'
import re, subprocess, sys
h = open('REPO_ROOT/films/pikmin-bloom/index.html', encoding='utf-8').read()
m = re.search(r'[<]script type="module">(.*?)[<]/script>', h, re.S)
if not m: print('找不到 module script'); sys.exit(1)
open('/tmp/wo3b-check.mjs', 'w', encoding='utf-8').write(m.group(1))
r = subprocess.run(['node', '--check', '/tmp/wo3b-check.mjs'], capture_output=True, text=True)
if r.returncode: print(r.stderr); sys.exit(1)
# 每張卡的 hl 詞要在對應旁白句裡
nar = open('REPO_ROOT/films/pikmin-bloom/narration.md', encoding='utf-8').read()
lines = [l for l in nar.splitlines() if l.strip() and not l.startswith('#')]
cards = re.findall(r"^\s*\{\s*head:.*$", h, re.M)
for i, (c, ln) in enumerate(zip(cards, lines), 1):
    hl = re.search(r"hl:\s*\[(.*?)\]", c)
    for w in re.findall(r"'([^']+)'", hl.group(1) if hl else ''):
        if w not in ln: print(f'卡{i} hl「{w}」不在旁白：{ln}'); sys.exit(1)
print('index.html OK')
PY
# 數字閘門：FACTS 與 facts.md 對得上，卡片裸數字檢查
python3 - <<'PY'
import re, sys
f = 'REPO_ROOT/films/pikmin-bloom/'
h = open(f + 'index.html', encoding='utf-8').read()
src = open(f + 'meta/facts.md', encoding='utf-8').read().replace(',', '')
blk = re.search(r"const FACTS = \{(.*?)\n\};", h, re.S)
if not blk: print('沒有 FACTS'); sys.exit(1)
pairs = re.findall(r"(\w+):\s*(\d+)", blk.group(1))
keys = [k for k, _ in pairs]
for k in keys + ['QUOTE_ZH_TW', 'QUOTE_ZH_CN']:
    if not re.search(r'\b' + k + r'\b', src): print('facts.md 缺 key', k); sys.exit(1)
vals = {v for _, v in pairs}
for k, v in pairs:
    if v not in src: print('facts.md 缺值', k, v); sys.exit(1)
cards = re.findall(r"^\s*\{\s*head:.*$", h, re.M)
bare = {n for line in cards for n in re.findall(r"(?<![\w.$}])\d{3,}", line)}
if bare: print('卡片裸寫數字', bare); sys.exit(1)
if len(keys) < 7: print('FACTS 少於 7 項'); sys.exit(1)
print('FACTS OK', keys)
PY
echo ALL_OK
```
預期整段 exit 0，最後印 `ALL_OK`。開工前 `index.html` 還是台北範本，第一個殘留檢查就會失敗。
