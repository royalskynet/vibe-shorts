# 連中兩期千萬發票（深夜對談 #3）草稿，待使用者核

爆款證據：YouTube｜116萬播放｜Jaden Williams「ChatGPT Vs. Google Gemini」（雙人一問一答題型）｜https://www.youtube.com/watch?v=X0qRMTLbem4；YouTube｜17.4萬播放（48h 內，竄升榜第一）｜萬物研究院「為什麼你從沒見過膽大的老電工?」（「為什麼 X？」反直覺題型，10-20 竄升榜前 30 有 20 支是這型）｜https://www.youtube.com/shorts/0nC5L7Tl49E；PTT｜273推／646回應（10-20 全站熱門第一）｜[爆掛] 澎湖千萬發票破解手法｜https://www.ptt.cc/bbs/Gossiping/M.1792423413.A.28E.html

## 為什麼這樣做

- 選題來源：`scripts/trend_zh.py` 10-20 報告，PTT 全站熱門第一＋第四都是這則新聞。YouTube 同題只有 1 支 10 播放（EZTV），題還沒人做。
- 品牌對位：悖論小酒館＝機率反直覺。一億分之一對一萬分之一，兩個數字差一萬倍。
- 鉤子照三支復盤的共同教訓：前三秒數字結論先出，機構與年份後補（refs/postmortem.md）。
- 結構借 codex 片（Agent Morphy 小幽默）：Claude 口氣平淡、句短；收尾回扣「手」。
- 法律邊界：不點名、不說當事人怎麼中的。案子只講報導寫的事實（連中兩期、財政部認定中）。「掃 QR Code 冒領被判詐欺」是南區國稅局公告的另一案，台詞用「有人」，不連到澎湖案。

## 事實與來源

- 7–8 月期全台 17 張千萬特別獎：財政部賦稅署 115-10-05 新聞稿｜https://www.dot.gov.tw/singlehtml/ch26?cntId=1101748d1b894265b60b0c5e6dcc1e79
- 特別獎：「統一發票八位數號碼與中獎號碼完全相同者，獎金新臺幣一千萬元」，開一組，單張機率一億分之一：統一發票給獎辦法第 7 條附近｜https://law.moj.gov.tw/LawClass/LawAll.aspx?PCode=G0340083
- 隨機碼 4 位數，一萬種組合：PTT 原文所述；官方條碼規格 PDF（https://www.einvoice.nat.gov.tw/static/ptl/ein_upload/attachments/1575448081679_0.pdf）沒讀出文字，建置前要再核。
- 澎湖同一人連中 5–6 月、7–8 月千萬，發票經警方查證非偽造，地檢署行文財政部認定：自由時報 劉禹慶 115-10-19｜https://news.ltn.com.tw/amp/news/society/breakingnews/5611384
- 曬發票要遮 QR Code 與隨機碼；有人掃他人曬圖的 QR Code 用兌獎 APP 冒領，判詐欺取財、返還金額：南區國稅局，鉅亨網轉述｜https://news.cnyes.com/news/id/5606809

## 待核問題

- 第 8 句「兩張都中，是一億乘一億分之一」是指「兩張特定發票都中」，不是「這個人連中的機率」。要不要改口語一點？
- 第 18 句「一萬分之一靠手」會不會讓人以為在說澎湖案？
