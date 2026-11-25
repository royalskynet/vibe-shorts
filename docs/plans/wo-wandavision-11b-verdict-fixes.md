# WO wandavision-11b：落地反方兩爭點

工作目錄 `/Users/51mini/dev/vibe-shorts-pipeline`，只改 `films/wandavision-primer/` 的 `narration.md`、`pace.json`、`SOURCES.md`、`audit/` 產物。

1. 相戀段：把「後來英雄內鬨，汪達成了通緝犯。」挪到「這兩年，兩人只能偷偷相見。」之前（內戰在先，兩年偷偷相見在後；來源 https://d23.com/wanda-maximoff-and-visions-mcu-origins-explained/ ，補進 SOURCES.md）。
2. 湯米是先出生的（《汪達幻視》第三集）。全稿不准出現「弟弟」：「弟弟叫湯米」改「雙胞胎兄弟叫湯米」；「比利在找的那個弟弟」改「比利在找的雙胞胎兄弟」。來源 https://stanforddaily.com/2021/02/02/WONDERING-ABOUT-WANDAVISION-SEASON-1-EPISODE-1-2-AND-3-RECAP/ 補進 SOURCES.md。
3. 行號若變動，`pace.json` 的 `pause_after` 鍵重新對準兩句劇透提醒句（值 5.5）。
4. 只過新改句子重寫 `audit/humanize.md` 戳記；重跑 `scripts/devils.sh films/wandavision-primer`。新爭點只回報，不再改稿。

禁區：不改 scripts/ tests/ refs/ index.html build.sh；不寫 verdicts.md、approved.md；不 commit、不上傳、不跑 build／voice／approve。

驗收：`bash /tmp/wv-accept-11b.sh` exit 0。
