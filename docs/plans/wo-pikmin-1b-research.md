## 任務

工作目錄：`REPO_ROOT`。只做查證與爆款帳，不寫旁白稿、不改 `index.html`、不 render、不 git commit。`films/pikmin-bloom/` 已存在。

背景：手遊 Pikmin Bloom（皮克敏）官方公告把台灣寫成「中國台灣」，台灣玩家出現退坑、停止課金聲浪。這是 2026 年 11 月的即時新聞，你的記憶不可靠，所有事實必須從網路讀到，讀不到寫「未查證」。不要讀或引用 `refs/viral-text/pikmin-seed.md`。

網路讀取一律用這兩條指令（TinyFish 優先，擋了自動往上一階）：
```bash
python3 ~/dev/ladder-search/scripts/ladder.py search "<查詢>"
python3 ~/dev/ladder-search/scripts/ladder.py read <url>
```

### A. 事實查證
五項各查一遍，把「讀到的原文段落」存成 `films/pikmin-bloom/refs/evidence/F<n>.txt`（每檔先寫一行 `URL: <網址>`，再貼讀到的相關原文，至少 200 字，不可自己改寫）：
- F1 官方公告出現「中國台灣」：哪則公告、哪個語言、哪天、哪個平台。
- F2 公告修改：改成什麼、哪天、官方是否已發正式說明（以查證當日為準）。
- F3 玩家反應：刪帳號、退坑、停止課金，只引新聞報導，不引網友留言。
- F4 「台灣玩家 2026 上半年消費約占全球 52%」：找統計平台（Sensor Tower、AppMagic 等）原始頁或報導引用處。
- F5 Pikmin Bloom 在中國大陸是否開放營運。
接著寫 `films/pikmin-bloom/SOURCES.md`（整份改寫，照 `films/taipei-silence/SOURCES.md` 格式）與 `films/pikmin-bloom/meta/facts.md`（欄位 FACTS key｜值｜來源，照範本）。每項寫：事實一句話、數字、來源 URL、來源發布日、查證日 2026-11-19、判定（已查證／僅單一二手來源／未查證）。判「未查證」的項目不放進 `meta/facts.md` 的表。

### B. 爆款證據
先讀 `skills/viral-scout/SKILL.md` 第 1 節與 `refs/VIRAL-LEDGER.md`。用已驗證的指令查：
`yt-dlp --flat-playlist -J "ytsearch40:<q>"`，篩 `duration ≤ 180` 且 `view_count ≥ 100000`。關鍵字：皮克敏 中國台灣、Pikmin Bloom 台灣 退坑、Pikmin Bloom Taiwan China、手遊 把台灣寫成中國 道歉、遊戲公司 中國台灣 玩家 抵制。
把結果 append 到 `refs/VIRAL-LEDGER.md` 末尾（既有內容不改），新段標題 `## 皮克敏「中國台灣」公告風波（2026-11-19 查）`，格式照該檔其他段，末行「判定：」。同題（皮克敏或同事件）與同大題（品牌／遊戲把台灣寫成中國引發抵制）分開列並標明。
`films/pikmin-bloom/TREATMENT.md` 只換「爆款證據：」那一行：有同題 ≥10 萬就寫最多 3 筆（連結＋播放數）；同題 0 筆就寫「同題 0 筆 ≥10 萬（查法：…）」，**不准拿同大題的片湊數放進這行**，同大題只留在帳本。`TREATMENT.md` 其他內容不動。

## 驗收

```bash
cd REPO_ROOT
for n in 1 2 3 4 5; do
  f=films/pikmin-bloom/refs/evidence/F$n.txt
  test -s "$f"
  head -1 "$f" | grep -q '^URL: https\?://'
  test "$(wc -m < "$f")" -ge 200
done
grep -lE '皮克敏|Pikmin' films/pikmin-bloom/refs/evidence/F1.txt films/pikmin-bloom/refs/evidence/F2.txt >/dev/null
grep -q 'F4' films/pikmin-bloom/SOURCES.md
grep -qE '已查證|僅單一二手來源|未查證' films/pikmin-bloom/SOURCES.md
grep -q '皮克敏「中國台灣」公告風波' refs/VIRAL-LEDGER.md
grep -E '^爆款證據：' films/pikmin-bloom/TREATMENT.md | grep -qE 'youtu|同題 0 筆'
if grep -E '^爆款證據：' films/pikmin-bloom/TREATMENT.md | grep -q 'VRUoW4sGWD0'; then exit 1; fi
if grep -rq 'taipei-silence' films/pikmin-bloom/SOURCES.md films/pikmin-bloom/meta/facts.md; then exit 1; fi
```
預期整段 exit 0；開工前 `refs/evidence/` 不存在，第一個 `test -s` 就會失敗。

## 不動
`films/` 其他資料夾、`films/pikmin-bloom/` 的 `index.html`／`mix.py`／`build.sh`／`narration*`、`scripts/`、`tests/`、`PLAN.md`；`refs/VIRAL-LEDGER.md` 只在末尾 append。

## 禁止
1. 不 render、不執行 `build.sh`、不 git commit。
2. 無頭機：禁止回報「請使用者手動貼 token／授權／執行指令」；憑證讀不到＝停手回報阻斷點與需要的 key 名。
3. 查不到寫「未查證」，不准憑記憶補數字或網址；證據檔內容必須是讀到的原文。
