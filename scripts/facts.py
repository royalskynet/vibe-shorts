#!/usr/bin/env python3
"""事實表（FACTS.md）外移查證（使用者 2026-11-06：查證不花 Claude token，改派o）。

用法：
  scripts/facts.py task <slug> "<題目>" ["<額外要查的點>"]   # 產 dcq 工單 → 印路徑；接著 dcq plan／dcq add
  scripts/facts.py check films/<slug>                         # 機械驗收 FACTS.md，工單的驗收區塊就是這行

check 判的事（fail 印哪條）：五個段都在；「已查證」至少 MIN_FACTS 條；每條四欄（｜分隔）且有 URL；
數字欄有阿拉伯數字的，同一條要寫「口徑：」（期間／單位／母數）。
口徑門的由來：mrt-escalator 把倫敦試驗「一座梯一週五個早上尖峰合計」寫成「尖峰一小時」，建片才被反方稽核抓到。
"""
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECTIONS = ["## 題目", "## 已查證事實", "## 反直覺候選", "## 參考爆款", "## 未查證"]
MIN_FACTS = 8

TASK = """# 工單：查證「{topic}」事實表（films/{slug}）

給 60–90 秒繁中知識短片用。只產一個事實表，寫手之後只能用表裡「已查證」的內容寫稿，所以數字錯一個，整支片就錯。`REPO_ROOT/films/{slug}/FACTS.md` 已存在且 `python3 scripts/facts.py check films/{slug}` 會過，就什麼都不用做（冪等）。

### 查法
- 搜尋 `python3 ~/dev/ladder-search/scripts/ladder.py search "<關鍵字>"`、讀頁 `… ladder.py read <url>`；YouTube 播放數 `yt-dlp --flat-playlist -J "ytsearch25:<關鍵字>"`，只寫實抓原值。
- 一手來源優先（官方新聞稿、法規、論文、主管機關），附日期。二手文章只能當線索，數字要回一手原文核對；對不上以原文為準，並在該條寫明。
- 每個數字寫清楚口徑：期間（一小時／一天／一週合計）、單位、母數、在哪裡量的。原文沒寫就標「口徑：原文未寫」。
- 特別找反直覺、能當片子後段爆點的事實（真正理由跟一般人猜的不一樣、驚人數字、規定其實沒有、別國怎麼做）。
- 同題爆款：YouTube／Shorts 搜 3–5 組中英文關鍵字，列播放數最高的 3–5 支。
{extra}
### 寫到 `films/{slug}/FACTS.md`，格式固定
```
## 題目
## 已查證事實
1. 事實一句｜數字（口徑：…）｜來源 URL（日期）｜「原文關鍵句」
## 反直覺候選
- 可當爆點的點｜依據第幾條
## 參考爆款
- 平台｜N 播放｜作者「標題」（秒數）｜URL
## 未查證／查不到
```
另把參考爆款 append 到 `refs/VIRAL-LEDGER.md` 檔尾：`## {today} {topic}（{slug}）`，每支一行 `- 平台｜N播放｜作者「標題」（秒數）｜URL`，再一行 `查法：…`、一行 `判定：…`。

## 驗收

```bash
cd REPO_ROOT
python3 scripts/facts.py check films/{slug}
grep -qF '（{slug}）' refs/VIRAL-LEDGER.md
```

預期：facts.py 印 `OK FACTS`、exit 0；VIRAL-LEDGER 有本題段落。

## 禁止

- 不准用訓練印象補數字；查不到就寫進「未查證／查不到」。
- 只寫 `films/{slug}/FACTS.md` 與 `refs/VIRAL-LEDGER.md` 檔尾，不改其他檔、不 commit、不 push。
- 不改 `scripts/facts.py`（驗收器）；失敗照原樣回報原始錯誤文字，不得宣告成功。
"""


def problems(text):
    """回傳 FACTS.md 的問題清單；空＝過。"""
    out = [f"缺段「{s}」" for s in SECTIONS if s not in text]
    if out:
        return out
    body = text.split("## 已查證事實", 1)[1].split("\n## ", 1)[0]
    facts = [l.strip() for l in body.splitlines() if re.match(r"\s*\d+[.、]", l)]
    if len(facts) < MIN_FACTS:
        out.append(f"已查證只有 {len(facts)} 條，至少 {MIN_FACTS}")
    for f in facts:
        n = f.split(".", 1)[0].split("、", 1)[0].strip()
        cols = f.split("｜")
        if len(cols) < 4:
            out.append(f"第 {n} 條不到四欄（事實｜數字｜來源｜原文）")
            continue
        if not re.search(r"https?://", f):
            out.append(f"第 {n} 條沒有來源 URL")
        if re.search(r"\d", cols[1]) and "口徑" not in f:
            out.append(f"第 {n} 條有數字沒寫口徑（期間／單位／母數）")
    return out


def main(argv):
    if len(argv) >= 4 and argv[1] == "task":
        slug, topic = argv[2], argv[3]
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,40}", slug):
            print(f"slug 只能小寫英數與 -：{slug}", file=sys.stderr)
            return 2
        extra = f"- 這題額外要查：{argv[4]}\n" if len(argv) > 4 else ""
        today = date.today().isoformat()
        p = ROOT / "docs/workorders" / f"{today.replace('-', '')}-facts-{slug}.md"
        p.write_text(TASK.format(slug=slug, topic=topic, extra=extra, today=today), encoding="utf-8")
        print(p)
        return 0
    if len(argv) == 3 and argv[1] == "check":
        f = Path(argv[2]) / "FACTS.md"
        if not f.is_file():
            print(f"FAIL 找不到 {f}")
            return 1
        bad = problems(f.read_text(encoding="utf-8"))
        print("\n".join(f"FAIL {b}" for b in bad) if bad else "OK FACTS")
        return 1 if bad else 0
    print(__doc__.split("\n\n")[1], file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
