# WO wandavision-5：照主 session 裁決改稿，重跑三道稽核

工作目錄：`/Users/51mini/dev/vibe-shorts-pipeline`。片目錄 `films/wandavision-primer/`。只改 `narration.md`、`SOURCES.md`、`audit/` 下的產物。句號＝去掉 `#` 行與空行後的第 N 行（WO-4 冷讀用的編號）。

## 0 清範本殘檔

`audit/verdicts.md`、`audit/approved.md` 是 WO-1 從 taipei-silence 複製來的舊檔，刪掉。

## 1 改稿（逐條照做）

**力量來源（反方爭點 1＋冷讀 118／120／121／199）**：
- 第一部不准出現「混沌魔法」「天生」「緋紅女巫」。第 118 句刪掉。
- 第 120–122 句改成：寶石在實驗台上喚醒了她的力量；她跟心靈寶石之間，從此有了一條看不見的線。
- 第 199 句改成：汪達的力量，是被心靈寶石喚醒的。
- 第二部 `## 雙胞胎與緋紅女巫` 加兩三句揭曉：原來她天生就帶著魔法，小時候就用過；寶石只是把它喚醒、放大；這種魔法叫混沌魔法。

**其餘冷讀硬傷**：
- 第 55 句「沒有人發現」：補上主詞範圍（看上下文，例：地球上，還沒有人知道它在哪）。
- 第 103 句刪掉；第 104 句改成：他們恨的，是飛彈上的那個名字。
- 第 186 句改成：意識，以賈維斯為基礎，長成一個新的意識。
- 第 195 句改成：那把槌子，只有值得的人舉得起來。
- 第 213 句改成：汪達在遠處，感覺到哥哥死了。（《奧創紀元》汪達不在現場）

**第三部（反方爭點 2、3）**：
- 「又過了兩年」改「又過了三年」，對齊阿嘉莎被困三年。後面如果寫比利「記憶回來」，改成他自己查出身分（來源：https://en.wikipedia.org/wiki/Familiar_by_Thy_Side）。
- 「湯米的靈魂，還缺一具身體」改成：湯米已經有了一具新的身體；他人在哪，沒人知道（來源：https://comicbook.com/marvel/news/agatha-all-along-tommy-story-return-billy/）。前後句跟著順，`## 湯米` 段的說法要一致。
- SOURCES.md 補這兩個網址與 WandaVision 第八集「天生魔法、寶石放大」來源 https://en.wikipedia.org/wiki/WandaVision 。

## 2 重跑（順序固定）

1. 口語化：只過新改的句子，重寫 `audit/humanize.md` 戳記。
2. `scripts/devils.sh films/wandavision-primer`（exit 3 就停下回報原文）。
3. `scripts/coldread.sh films/wandavision-primer script`。冷讀若仍「不通過」，把新的 `[硬傷]` 原文貼進回報，**不要再改稿**，裁決由主 session 做。

## 禁區

同前：不改 `scripts/`、`tests/`、`refs/`、其他片目錄；不寫 verdicts.md、approved.md；不 commit、不上傳、不跑 build／voice／approve。

## 驗收

```bash
bash /tmp/wv-accept-5.sh
```
