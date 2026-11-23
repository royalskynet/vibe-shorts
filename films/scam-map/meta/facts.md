# 片中數字與來源

算法與 API 細節見 `../SOURCES.md`；`index.html` 載入時會拿 `FACTS` 跟 `map.js`（從原始資料算出）比對，對不上就丟錯。

| FACTS | 值 | 來源 |
|---|---|---|
| YEAR | 2025 | 統計年度 |
| TOTAL_CASES | 156411 | 165 打詐儀錶板 GetMonthlyCityFraudData，2025-01～12 各縣市 Cases 加總 |
| NATIONAL_PER100K | 671 | 156411 ÷ 23299132（內政部戶政司 ODRP014，2025-12）× 100000 |
| NATIONAL_ONE_IN | 149 | 100000 ÷ 671 |
| HSINCHU_PER100K | 881 | 新竹市 4015 件 ÷ 455740 人 × 100000 |
| HSINCHU_ONE_IN | 114 | 455740 ÷ 4015 |
| HSINCHU_ABOVE_PCT | 31 | 881 ÷ 671 − 1 |
| MONTHS_TOTAL | 21 | 2025-01～2026-09 |
| MONTHS_FIRST | 18 | GetMonthlyCityCaseStatistics 的 CasePopulationRatio 第一名＝新竹市的月數 |
| KINMEN_PER100K | 209 | 金門縣 291 件 ÷ 139313 人 × 100000 |
| SHOP_HSINCHU_PCT | 24 | GetMonthlyCityFraudMethodRanking（cityId=14）假網拍 968 ÷ 4015 |
| SHOP_NATIONAL_PCT | 22 | GetMonthlyFraudMethodRanking 假網拍 34947 ÷ 156411 |
| INVEST_LOSS_PCT | 51 | 同上，假投資財損 ÷ 全年財損 |

地圖：taiwan-atlas 2021.9.20（MIT），底層內政部國土測繪中心縣市界。
