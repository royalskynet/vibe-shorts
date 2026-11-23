# 片中數字與來源

`index.html` 寫 `FACTS` 時照這張表。算法與原始網址見 `../SOURCES.md`。

| FACTS | 值 | 稿中說法 | 來源 |
|---|---|---|---|
| WHEEL_POCKETS | 37 | 三十七格 | 歐式單零輪盤 0＋1–36（Wikipedia Roulette） |
| RED_POCKETS | 18 | 十八紅，十八黑 | 同上 |
| PAYOUT | 1 | 只賠你一倍 | Roulette §Bet odds table：Red/Black 1 to 1 |
| STAKE | 100 | 每押一百塊 | 舉例金額 |
| EXPECTED_LOSS | 2.7 | 平均少拿兩塊七 | 100 × 1/37 ≈ 2.70（Roulette house edge 2.70%） |
| WIN_1 | 48.6 | 贏的機會將近一半 | 18/37 |
| WIN_100 | 35.5 | 押一百把，還有三成五 | 二項分布 n=100，SOURCES 算法 |
| WIN_1000 | 18.8 | 押一千把，剩不到兩成 | 二項分布 n=1000 |
| WIN_10000_PER_1000 | 3 | 一千個人只剩三個 | 二項分布 n=10000 → 0.333% |
| BANKROLL | 1000 | 帶一千塊 | 舉例金額 |
| TARGET | 2000 | 翻到兩千就走 | 舉例金額 |
| DOUBLE_FAIR | 50 | 沒有那格零，機會是一半 | 公平賭局 i/N |
| DOUBLE_PCT | 36.8 | 只剩三成七 | 賭徒破產公式（Wikipedia Gambler's ruin） |
| RUIN_PCT | 63.2 | 另外六成三輸光 | 1 − 0.368 |
