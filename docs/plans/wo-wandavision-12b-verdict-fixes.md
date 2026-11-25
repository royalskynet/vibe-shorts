# WO wandavision-12b：第一集落地反方兩爭點

工作目錄 `/Users/51mini/dev/vibe-shorts-pipeline`，只改 `films/wv-primer-1/` 的 `narration.md`、`SOURCES.md`、`audit/` 產物。

1. 飛彈（爭點 1）：殺死父母的爆炸和印著史塔克工業的未爆彈是兩顆。改成類似：「一顆飛彈打穿了他們的公寓。父母當場死亡。第二顆飛彈落在兄妹身邊，沒有爆炸。彈頭上印著一行字。史塔克工業。」來源 https://d23.com/wanda-maximoff-and-visions-mcu-origins-explained/ 補進 SOURCES.md。
2. 「唯一」（爭點 2）：「幻視主動提出唯一的解法。」改「幻視主動提出一個解法。」全稿不准有「唯一」。
3. 字數仍要 1350–1600，每行 ≤35 字、一行一個句號。
4. 只過新改句子重寫 `audit/humanize.md` 戳記；重跑 `scripts/devils.sh films/wv-primer-1`。新爭點只回報，不再改稿。

禁區：不改 scripts/ tests/ refs/ index.html build.sh、其他片目錄；不寫 verdicts.md、approved.md；不 commit、不上傳、不跑 build／voice／approve。

驗收：`bash /tmp/wv-accept-12b.sh` exit 0。
