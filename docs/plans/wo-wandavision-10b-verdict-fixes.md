# WO wandavision-10b：落地 WO-10 證據包兩爭點裁決，重蓋戳記

工作目錄：`/Users/51mini/dev/vibe-shorts-pipeline`。片目錄 `films/wandavision-primer/`。只改 `narration.md`、`audit/humanize.md`、devils 產物。

主 session 裁決（兩點都 CON_WINS）：

1. 吉米·吳不是受控鎮民。刪掉這三句：「在他們之中，有幾張熟面孔。」「吉米·吳，《蟻人與黃蜂女》的 FBI 探員。」「還有一個藏著真面目的鄰居。」保留「艾格妮絲這個鄰居，多留意她。」（accept-1b 要求蟻人那條是舊門檻，已排除。）
2. 兩人沒在愛丁堡同住兩年：
   - 「後來，兩人在愛丁堡住在一起。」→「這兩年，兩人只能偷偷相見。」
   - 「過著最像人的兩年。」→「最後一次約會，在蘇格蘭愛丁堡。」
   - 第三部「他和汪達一起住過的城市。」→「他和汪達最後一次約會的城市。」

其他句子一字不改。刪句後 `pace.json` 的 `pause_after` 鍵要跟著改成兩句劇透提醒的新句號（值仍 5.5）。`SOURCES.md` 若有只為吉米存在的行可刪。

## 重跑

1. 重寫 `audit/humanize.md` 首行戳記（只列改動句）。
2. `scripts/devils.sh films/wandavision-primer`（exit 3 停下回報原文）。新爭點原文貼回報，不要再改稿。

## 禁區

同 WO-10。

## 驗收

```bash
bash /tmp/wv-accept-10b.sh
```
