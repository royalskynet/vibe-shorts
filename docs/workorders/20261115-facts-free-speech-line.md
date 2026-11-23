# 工單：查證「言論自由的界線：說和做分開管（鉤子：2026-11 羅大佑言論自由爭議）」事實表（films/free-speech-line）

給 60–90 秒繁中知識短片用。只產一個事實表，寫手之後只能用表裡「已查證」的內容寫稿，所以數字錯一個，整支片就錯。`/Users/you/dev/vibe-shorts-pipeline/films/free-speech-line/FACTS.md` 已存在且 `python3 scripts/facts.py check films/free-speech-line` 會過，就什麼都不用做（冪等）。

### 查法
- 搜尋 `python3 /Users/you/dev/ladder-search/scripts/ladder.py search "<關鍵字>"`、讀頁 `… ladder.py read <url>`；YouTube 播放數 `yt-dlp --flat-playlist -J "ytsearch25:<關鍵字>"`，只寫實抓原值。
- 一手來源優先（官方新聞稿、法規、論文、主管機關），附日期。二手文章只能當線索，數字要回一手原文核對；對不上以原文為準，並在該條寫明。
- 每個數字寫清楚口徑：期間（一小時／一天／一週合計）、單位、母數、在哪裡量的。原文沒寫就標「口徑：原文未寫」。
- 特別找反直覺、能當片子後段爆點的事實（真正理由跟一般人猜的不一樣、驚人數字、規定其實沒有、別國怎麼做）。
- 同題爆款：YouTube／Shorts 搜 3–5 組中英文關鍵字，列播放數最高的 3–5 支。
- 這題額外要查：只查這一個機制，不查德國、貝茲梅諾夫、其他國家：
- 羅大佑 2026-11 爭議：他在專訪說了什麼（原話）、行政院與梁文傑等如何回應。線索：https://www.ettoday.net/news/20261112/3270701.htm 、https://news.ltn.com.tw/news/politics/breakingnews/5638189 、https://www.setn.com/news/1937955
- 大法官釋字第 644 號（2008-06-20）：被宣告違憲的人民團體法條文、理由書關於『主張共產主義、分裂國土』屬政治言論、只能管『明顯而立即危險』的原句。來源用憲法法庭／司法院官網。
- 反滲透法（2020-01-15 公布）：第 1 條立法目的、『滲透來源』定義、受指示或資助才構成的要件（第 3–7 條）；至今起訴／判決件數（法務部或司法院統計，查不到就寫未查證）。
- 刑法第 100 條 1992 年修法（刪除『陰謀犯』、言論內亂罪除罪化）的原文與日期。
- 同題爆款：YouTube 搜『言論自由 界線』『羅大佑 言論自由』『釋字644』『反滲透法 是什麼』。
時間有限：每項找到一手來源就寫進 FACTS.md，邊查邊寫，不要全查完才動筆。

### 寫到 `films/free-speech-line/FACTS.md`，格式固定
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
另把參考爆款 append 到 `refs/VIRAL-LEDGER.md` 檔尾：`## 2026-11-15 言論自由的界線：說和做分開管（鉤子：2026-11 羅大佑言論自由爭議）（free-speech-line）`，每支一行 `- 平台｜N播放｜作者「標題」（秒數）｜URL`，再一行 `查法：…`、一行 `判定：…`。

## 驗收

```bash
cd /Users/you/dev/vibe-shorts-pipeline
python3 scripts/facts.py check films/free-speech-line
grep -qF '（free-speech-line）' refs/VIRAL-LEDGER.md
```

預期：facts.py 印 `OK FACTS`、exit 0；VIRAL-LEDGER 有本題段落。

## 禁止

- 不准用訓練印象補數字；查不到就寫進「未查證／查不到」。
- 只寫 `films/free-speech-line/FACTS.md` 與 `refs/VIRAL-LEDGER.md` 檔尾，不改其他檔、不 commit、不 push。
- 不改 `scripts/facts.py`（驗收器）；失敗照原樣回報原始錯誤文字，不得宣告成功。
