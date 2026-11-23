## 任務

拆單豁免：接續 wo-pikmin-3b-visuals.md 的未完部分，驗收沿用同一段。

工作目錄：`/Users/you/dev/vibe-shorts-pipeline`。`films/pikmin-bloom/index.html`、`meta/facts.md`、`TREATMENT.md` 標題／時限／禁止清單已改完，只剩 `TREATMENT.md` 的 `## 分鏡` 表格還是舊的 7 列。

只做一件事：讀 `docs/plans/wo-pikmin-3b-visuals.md` 的「卡」表（15 列）與「### 3」第 5 點，把 `films/pikmin-bloom/TREATMENT.md` 的分鏡表換成 15 列（表頭不變、衝擊事件全填 `—`、動作欄不得含抽象詞、內容欄填 `narration.md` 對應句逐字、來源欄照第 5 點）。段名：鉤子＝1–3、兩種寫法＝4–5、錢從哪來＝6–10、官方改了什麼＝11–13、落點＝14–15。其他檔與其他段一字不動。

## 驗收

```bash
set -e
cd /Users/you/dev/vibe-shorts-pipeline
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
sys.path.insert(0, '/Users/you/dev/vibe-shorts-pipeline/scripts')
import precheck as p
t = open('/Users/you/dev/vibe-shorts-pipeline/films/pikmin-bloom/TREATMENT.md', encoding='utf-8').read()
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
h = open('/Users/you/dev/vibe-shorts-pipeline/films/pikmin-bloom/index.html', encoding='utf-8').read()
m = re.search(r'[<]script type="module">(.*?)[<]/script>', h, re.S)
if not m: print('找不到 module script'); sys.exit(1)
open('/tmp/wo3b-check.mjs', 'w', encoding='utf-8').write(m.group(1))
r = subprocess.run(['node', '--check', '/tmp/wo3b-check.mjs'], capture_output=True, text=True)
if r.returncode: print(r.stderr); sys.exit(1)
# 每張卡的 hl 詞要在對應旁白句裡
nar = open('/Users/you/dev/vibe-shorts-pipeline/films/pikmin-bloom/narration.md', encoding='utf-8').read()
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
f = '/Users/you/dev/vibe-shorts-pipeline/films/pikmin-bloom/'
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

預期整段 exit 0 並印 `ALL_OK`；現況分鏡只有 7 列，會失敗。

## 禁止
不 render、不跑 `build.sh`／`voice.py`／`approve.py`／`restamp.sh`、不 git commit；無頭機，禁止要使用者手動執行。
