# Devil's Advocate Evidence Pack

Report: REPO_ROOT/films/dune-messiah-trap/audit/claims.md
Reviewed: 2026-11-20
Core conclusion as read: 當我們只按陣營接受答案，就是把判斷力交了出去。

## 爭點 1
FLAG: inference
TARGET: 當我們只按陣營接受答案，就是把判斷力交了出去。
ATTACK: inference
OBJECTION: 現稿把按陣營信任來源直接等同放棄判斷，沒有區分「認為同陣營來源較可靠」與「拒絕任何修正證據」。Lois、Tsakas 與 Riedl 的實驗發現，受試者起初偏信同陣營來源，但取得來源可靠性的外部回饋後會修正信任；偏見可以出自錯誤的先驗可靠性判斷，不能僅憑陣營偏好判定當事人沒有求真動機。這支持窄化推論，不能推翻現稿對「只」按陣營、完全不看證據者的條件式警告。研究測的是美國兩黨支持者在受控任務中的資訊更新，不直接檢驗「善惡二分使人以為勝選解決一切」，也未檢驗自由或生命決定權的移轉。建議把判準落在「即使出現反證，仍只按陣營接受答案」，避免將一般來源信任捷徑一律判成放棄判斷。
EVIDENCE:
- URL: https://cris.maastrichtuniversity.nl/ws/files/284338500/Riedl-2025-Facts-Over-Partisanship-Evidence-Based-Updating.pdf
  DATE: 2025-08-21 線上首刊；典藏封面列正式卷期出版日 2026-01-01
  EXCERPT: "partisans have internal accuracy motives"
IMPACT: narrow

## 爭點 2
FLAG: inference
TARGET: 書裡的保羅，被弗瑞曼人當成救世主，發動了聖戰。
ATTACK: inference
OBJECTION: 「發動了聖戰」容易使觀眾理解成保羅自主發起並掌控整場戰爭。小說另有直接限縮：Scytale 認為聖戰反過來利用保羅；後段敘事也描述保羅被聖戰攫住。前者是角色判斷，不應當成全知定論；後者提供敘事上的佐證。然而同一本書也讓保羅承認自己派遣軍團殺人，因此反證不能支持「保羅無責任」或「沒有參與」。最強成立範圍是控制程度：保留保羅的責任與死傷數字，同時說明聖戰以他之名擴張，且超出他的控制。此處核對的是網路上傳的小說文字，未核對紙本版本及頁碼；不得將上傳者視為出版社。
EVIDENCE:
- URL: https://huggingface.co/Sp24TescSoSAI/guarfeilfSpice/blob/main/Frank%20Herbert%20-%20Dune%20Messiah.txt
  DATE: 未標示（所載作品《Dune Messiah》初版 1969 年；上傳日期未核實）
  EXCERPT: "The Jihad used him."
- URL: https://huggingface.co/Sp24TescSoSAI/guarfeilfSpice/blob/main/Frank%20Herbert%20-%20Dune%20Messiah.txt
  DATE: 未標示
  EXCERPT: "The Jihad had seized him"
- URL: https://huggingface.co/Sp24TescSoSAI/guarfeilfSpice/blob/main/Frank%20Herbert%20-%20Dune%20Messiah.txt
  DATE: 未標示
  EXCERPT: "by sending out his legions."
IMPACT: narrow

## 爭點 3
FLAG: single-source
TARGET: 赫伯特在文章結尾，叫讀者別把他當成領袖。
ATTACK: premise
OBJECTION: NO_EVIDENCE_BACKED_OBJECTION
EVIDENCE:
- URL: https://vasil.ludost.net/dunegenesis.pdf
  DATE: 1980-07（文件標示原刊於 Omni Magazine；此 PDF 重製日期未標示）
  EXCERPT: "Don't look to me as your leader."
IMPACT: retain

本爭點查核說明：已搜尋 Dune Genesis、Herbert、leader 與 1980，並實際開啟報告所列 PDF。末頁先由作者拒絕再提供答案，要求讀者自行尋找解法，接著出現上述句子。上下文支持現稿歸屬；沒有實據可把它改判為保羅的台詞。「結尾」指末段區域，未宣稱它是全文最後一句。

稽核限縮：共選 3 個爭點，按影響力排序。每個爭點均已搜尋並實際開頁；各爭點採用 1 個來源頁，未超過 3 頁上限。兩條異議僅支持窄化，沒有足以反轉整體警語的證據。未修改報告，未把報告內記載的既往裁決當作本輪證據，也未執行主 session 的融合或裁決工作。

Engine: codex
