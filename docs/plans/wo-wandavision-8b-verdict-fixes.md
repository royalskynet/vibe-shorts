# WO wandavision-8b：落地反方裁決兩句，重蓋戳記

工作目錄：`/Users/51mini/dev/vibe-shorts-pipeline`。片目錄 `films/wandavision-primer/`。只改 `narration.md`、`audit/humanize.md`、devils 產物。

主 session 對 WO-8 證據包的裁決：

1. 爭點 1 CON_WINS：「指令只有一個，消滅幻視。」→「它奉命去消滅幻視。」（白幻視也攻擊汪達，不寫排他）
2. 爭點 2 CON_WINS：
   - 「那是阿嘉莎幾百年前編的歌。」→「那是阿嘉莎和兒子一起寫的歌。」
   - 「她用這首歌，騙女巫上路。」→「兒子死後，她拿這首歌騙女巫上路。」
3. 爭點 3 PRO_WINS：不動。

其他句子一字不改。

## 重跑

1. 重寫 `audit/humanize.md` 首行戳記（只列這三句）。
2. `scripts/devils.sh films/wandavision-primer`（exit 3 就停下回報原文）。新證據包的爭點原文貼進回報，**不要再改稿**。

## 禁區

同 WO-8。

## 驗收

```bash
bash /tmp/wv-accept-8b.sh
```
