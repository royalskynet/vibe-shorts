# BLOCKED — mrt-escalator（2026-11-07 夜間批次）

## 卡在哪

`build.sh` 第一步 `voice.py` exit 1：第 16 句核稿過不了（門檻 0.90，最好 0.86），建置在這裡停下，沒有成片，也沒有 `dist/`。

> 改成兩邊都站，載到一萬六千兩百二十人，多了快三成。

- Whisper 聽回：`改成两边兜战再到16220人多了快三成`。共跑 2 輪、6 次：第一輪最好 0.81，第二輪三次都 0.86。
- 差的三個字「都→兜、站→战、載→再」同音，判斷是 Whisper 猜錯字，不是念錯。這是從文字推的，沒有人耳確認。
- `voice.py` 這類失敗的既定修法是改稿（skill `references/audio.md`），但核准檔規定不准再改台詞，任務也規定不放寬閘門，所以停下。

沒做的事：沒改 `lines.json` 的相似度、沒繞過 `voice.py` 手動跑後段、沒改 `SIM_MIN`、`HOMOPHONE`、`norm`。

## 要使用者選一個

1. **（建議）核准第 16 句小改**：例如「改成兩側都站，一週載到一萬六千兩百二十人，多了快三成。」實際念法要再跑核稿確認。
2. **核准閘門修正**：`scripts/verify_tts.py` 的 `norm` 有個 bug，Whisper 吐「16,220」時逗號後才刪，會拆成 16 和 220 分開拼，念對也扣分（第一輪 0.81 就吃到這個）。修它，或把「都／兜、站／战、載／再」收進 `HOMOPHONE`。後者會放過真的念錯，不建議。
3. **人耳聽 `out/voice/16.wav`**，確認念對後裁決放行。

## 解開後怎麼接

```bash
cd films/mrt-escalator && bash build.sh    # 只重念第 16 句，其餘沿用
cd ../.. && scripts/qa_sheet.sh films/mrt-escalator   # 看圖寫 qa/review_log.md
scripts/coldread.sh films/mrt-escalator film
python3 scripts/precheck.py films/mrt-escalator
scripts/deliver.sh films/mrt-escalator/mrt-escalator.mp4
python3 scripts/precheck.py films/mrt-escalator    # 交付檔要在 deliver 後才過
```

改第 16 句的話，要先重跑 `approve.py`、humanize 戳記、`devils.sh` 與裁決。

## 已完成

- 核准與 audit：`audit/approved.md`、`humanize.md` 綁現稿；`devils.sh` 重跑，`verdicts.md` 已裁決。
- 配音：20 句有 19 句過核稿，第 12 句重念到 1.00。
- 文件：TREATMENT、SOURCES、`meta/facts.md`、三份 caption 已同步，`meta/public-path.txt` 已產。
- 畫面：第 12、13、15–17 卡同步新稿；第 13 卡改成 24 公尺＋十個小人（四走六站）。
- 源頭修正：封面留到 2.8 秒、跳數途中不登記 TEXTS（readcheck）；第 8、9、10、12、13、18 卡加牛皮紙塊面（textless）。
- 以現在的 timeline 跑過 readcheck、textless、seek_check，結果見批次回報；第 16 句重念後片長會變，`build.sh` 會重跑這三道。

## 發布前要使用者看的內容風險（台詞已核過，沒動）

- 反方稽核兩個爭點都是 SPLIT：第 17 句把單站單梯的兩週差額說成長梯通則；第 18 句的短梯結論只靠 Canary Wharf 觀察。已在畫面與 SOURCES 標明範圍。
- 稿冷讀 `VERDICT: 不通過`（WARN，不擋），見 `audit/coldread-script.md`。值得看的是：第 13 句說四成願意走、第 14 句卻說走路側空著；第 20 句「不用再怕被瞪」承諾偏強。
