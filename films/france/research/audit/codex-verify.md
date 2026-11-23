## 網址

| # | URL | 狀態 | 備註 |
|---|---|---|---|
| 1 | https://en.wikipedia.org/wiki/2026_French_lyc%C3%A9e_protests | HTTP 200 | HEAD 200；讀取pages/wiki.txt，因標記TRUNCATED另以Jina取得完整頁。 |
| 2 | https://www.aljazeera.com/news/2026/9/30/whats-behind-french-student-protests-that-turned-violent | HTTP 200 | HEAD 200；讀取pages/src3.txt中此URL的完整camofox正文。 |
| 3 | https://komonews.com/news/nation-world/gallery/analyst-says-france-unrest-has-shifted-from-schools-to-lawlessness-and-anarchy-arrested-rioters-immigration | HTTP 200 | HEAD 200；原URL為相簿。Jina 200；循Read The Article連結讀取正文（亦Jina 200）。 |
| 4 | https://www.france24.com/en/europe/20261018-live-vance-blames-immigration-for-violence-during-protests-in-france | HTTP 200 | HEAD 200；讀取pages/src4.txt；Jina重抓僅得框架，另直接GET取得完整直播文字。 |
| 5 | https://www.france24.com/en/france/20261001-french-pm-to-present-belt-tightening-2027-budget-including-frozen-wages-and-new-taxes | HTTP 200 | HEAD 200；本機未收錄，Jina 200取得正文。 |
| 6 | https://www.theguardian.com/world/2026/oct/17/protests-france-high-prices-social-security-gilets-jaunes | HTTP 200 | HEAD 200；正文位於pages/batch2.txt。 |
| 7 | https://www.dw.com/en/france-protesters-clash-with-police-in-nationwide-protests-amid-rising-social-polarization/a-79685584 | HTTP 200 | HEAD 200；正文位於pages/batch2.txt。 |
| 8 | https://www.theguardian.com/world/2026/oct/18/french-government-crisis-talks-violent-unrest-policing-macron | HTTP 200 | HEAD 200；正文位於pages/src2.txt。 |
| 9 | https://www.nbcnews.com/world/europe/france-violence-riots-looting-paris-limoges-curfews-macron-protests-rcna604292 | HTTP 200 | HEAD 200；正文位於pages/batch3.txt。 |
| 10 | https://www.afp.com/en/macron-denounces-unbridled-violence-france-hit-new-clashes | HTTP 200 | HEAD 200；pages/batch3.txt雖標TRUNCATED，相關談話段落完整可讀。 |
| 11 | https://www.bbc.com/news/articles/crwyd02yz22vo | HTTP 200 | HEAD 200；正文位於pages/batch3.txt。 |
| 12 | https://efe.com/english/latest-news/2026-10-18/france-protests-2000-arrested-600-police-officers-firefighters-injured/ | HTTP 403 | HEAD 403；換Jina再開，代理HTTP 200但目標403且只有Checking your browser。pages/src2.txt有此確切URL的完整正文，據此核對；目前線上正文受阻，不能判死鏈。 |
| 13 | https://www.theguardian.com/world/2026/oct/10/school-protesters-sevran-paris-suburb-france | HTTP 200 | HEAD 200；本機未收錄，Jina 200取得正文。 |
| 14 | https://www.insee.fr/fr/statistiques/6793282 | HTTP 200 | HEAD 200；正文及統計表位於pages/src4.txt。 |
| 15 | https://www.ouest-france.fr/economie/budget-collectivites-etat/budget-2027-faute-de-compromis-les-deputes-mettent-en-pause-lexamen-du-projet-de-loi-de-finance-4b5a8f6a-cc0f-11f1-b8bc-a46147b584ed | HTTP 403 | HEAD 403；換Jina再開HTTP 200，成功取得同URL正文；反爬，非死鏈。 |
| 16 | https://www.nytimes.com/2026/10/09/world/europe/france-protest-history.html | HTTP 403 | HEAD 403；換Jina再開HTTP 403（AbuseAlleviationError）。pages/batch2.txt保存同URL的camofox頁面，內文及照片說明可讀；線上受阻，非已確認死鏈。 |

查核日期：2026-10-20。HTTP狀態採本次 `curl -sIL` 最終回應。頁面200不等於正文完整；403不判死鏈。來源[3]正文連結為 https://komonews.com/news/nation-world/analyst-says-france-unrest-has-shifted-from-schools-to-lawlessness-and-anarchy-arrested-rioters-immigration 。

## 主張

計數單位為可獨立核對的主張；複合句拆列，同一句重複出現仍逐處核對。並列引註逐一檢查，能共同支持者可判支持，問題欄註明實際支撐來源；「只有」等排他限定另外判定。首段前兩句雖未各自緊接引註，也按鄰近[4]納入，避免漏查。摘錄每列合計不超過40個字元（不含外加引號及來源標籤）；全部取自實際開啟的頁面或使用者允許的本機落檔。支持表示引文能支持正文措辭，不等於對原始消息做獨立採訪驗證。[12]、[16]採本機可讀正文，故不將相關主張判成「來源打不開」。

| 段落 | 主張原句（節錄） | [N] | 判定 | 來源原文摘錄（逐字，≤40 字） | 問題 |
|---|---|---|---|---|---|
| C01 一句話① | 這波動亂起於高中生抗議學校條件 | [4] | 部分支持 | [4]「poor conditions in schools」 | [4]支持教育條件與生活費抗議，未交代起點；前句無獨立引註，按鄰近[4]納入。 |
| C02 一句話② | 10 月中工會、黃背心與反生活費運動併入 | [4] | 部分支持 | [4]「Students, unions, and yellow vest」 | 參與群體有依據；[4]未證實「10月中」的加入時點。 |
| C03 一句話③ | 10-17 全國 55 萬人上街後失控 | [4] | 部分支持 | [4]「an estimated 800,000 people」 | [4]可見主辦方80萬及暴力；未見內政部55萬，且不宜把所有參與者寫成失控。 |
| C04 一句話④ | 當天 2,397 人被捕 | [4] | 支持 | [4]「2,397 arrests were made on Saturday」 | — |
| C05 一句話⑤ | 997 名警察與憲兵受傷 | [4] | 支持 | [4]「997 police officers and gendarmes」 | — |
| C06 一句話⑥ | 主流報導把它定性為「高中生抗議與生活費抗議合流後失控」 | [1][2][4] | 部分支持 | [1]「against the cost of living」 | [1]支持10-17合流；[2]是9-30報導，無法證實10-17結果；引號內中文為綜合轉述，非三篇原文共同定性。 |
| C07 一句話⑦ | 不是移民暴動 | [1][2][4] | 部分支持 | [2]「The protests are over conditions」 | 教育及經濟訴求有支持，但三來源未提供足以排除所有移民因素的調查或共同定性。 |
| C08 時間線9-18 | 巴黎郊區克雷泰伊（Créteil）的高中生開始示威與封校 | [1] | 支持 | [1]「18 September 2026」；[1]「having originated in」 | — |
| C09 時間線9月下旬 | 教育部 9-30 統計全國約 3,700 所高中中約 400 所受影響 | [3] | 不支持 | [3]「over 700 secondary schools」 | 所引相簿及連出的正文均未載400/3,700或9-30教育部統計；[2]9-30報導有該數字，報導日也不必然是統計日。 |
| C10 時間線10-01① | 總理勒克努（Lecornu）提出 2027 預算 | [5] | 支持 | [5]「government presented its 2027 budget」 | — |
| C11 時間線10-01② | 凍結公務員薪資 | [5] | 支持 | [5]「freezing public sector wages」 | — |
| C12 時間線10-01③ | 凍結最低級距以外的退休金 | [5] | 支持 | [5]「all but the lowest ‌pensions」 | — |
| C13 時間線10-01④ | 稅收淨增 180 億歐元 | [5] | 支持 | [5]「increase by €18 billion」 | 核對為國家預算淨稅收較本年增加的提案數字。 |
| C14 時間線10-06① | 教師、家長、工會加入，變成全國性動員 | [1] | 支持 | [1]「On 6 October」；[1]「teachers, parents, and」 | — |
| C15 時間線10-06② | 工會估計 45 萬人參與 | [1] | 支持 | [1]「450,000 people participated nationwide」 | — |
| C16 時間線10-17前① | 一名 15 歲學生被炸斷手 | [6] | 支持 | [6]「after a 15-year-old lost a hand」 | 原文在警用鎮暴武器造成傷害的脈絡敘述；未與10-17另一名17歲傷者混同。 |
| C17 時間線10-17前② | 努涅斯（Nuñez）暫停對學生使用一種震爆彈 | [6] | 支持 | [6]「suspended the use of a type」 | — |
| C18 時間線10-17前③ | 但說 10-17 仍可使用 | [6] | 支持 | [6]「they could be used on Saturday」 | — |
| C19 時間線10-17① | 學生、工會、黃背心合流上街 | [4][7] | 支持 | [4]「Students, unions, and yellow vest」 | [4]列三群體；[7]正文Who took part段也明載。 |
| C20 時間線10-17② | 內政部說 55 萬人 | [4][7] | 支持 | [7]「some 550,000 people」 | 55萬由[7]支持；[4]未見此數字。 |
| C21 時間線10-17③ | 主辦方說 80 萬人 | [4][7] | 支持 | [4]「organisers of French protests」；[4]「800,000」 | 80萬由[4]支持；[7]未見80萬。 |
| C22 時間線10-17④ | 利摩日 19 世紀的市政廳被縱火燒毀 | [8][9] | 支持 | [8]「19th-century town hall was burned down」 | [9]亦敘述19世紀建物及尖塔火中倒塌；「燒毀」按嚴重焚毀解讀。 |
| C23 時間線10-18① | 馬克宏全國談話 | [4][10] | 支持 | [4]「18/10/2026 - 20:29」；[10]「address to the nation」 | [10]刊登時間10-19 01:08，內文Sunday與[4]時間戳支持10-18談話。 |
| C24 時間線10-18② | 稱暴力「毫無理由」 | [4][10] | 支持 | [4]「nothing justifies」 | 意譯可成立；直接措辭在[4]，[10]重點為unbridled violence。 |
| C25 時間線10-18③ | 承諾對警方應對「完全透明」 | [4][10] | 支持 | [10]「full transparency」 | — |
| C26 時間線10-19① | 政府危機會議後要求部分城市實施局部宵禁 | [9] | 支持 | [9]「asked some cities to impose a partial」 | 要求地方當局引入，不代表所有城市已實施。 |
| C27 時間線10-19② | 巴黎不全面宵禁 | [9] | 支持 | [9]「putting all of Paris」 | — |
| C28 時間線10-19③ | 也不宣布緊急狀態 | [9] | 支持 | [9]「stopped short of declaring an emergency」 | — |
| C29 時間線11-05 | 工會與黃背心已宣布下一波大型抗議 | [11] | 支持 | [11]「on 5 November」；[11]「announced huge protests」 | — |
| C30 三股力量1① | 訴求是補足老師、縮小班級、減輕課表、修繕校舍 | [1] | 支持 | [1]「overcrowded classrooms」；[1]「run-down buildings」 | 逐項對照teacher shortages、exhausting timetables等；此句未使用「只有」。 |
| C31 三股力量1② | 一名學生整年沒有國文老師 | [1] | 部分支持 | [1]「seven months without a French teacher」 | 七個月寫成整年；French teacher應譯法文老師，原文還限定是有法文考試的年度。 |
| C32 三股力量1③ | 班級 32 到 36 人 | [1] | 支持 | [1]「classes of 32 to 36 students」 | — |
| C33 三股力量2① | 2027 預算凍薪加稅 | [5] | 支持 | [5]「freezing public sector wages」；[5]「€18 billion」 | — |
| C34 三股力量2② | 社群號召復活 2018 年的黃背心運動 | [6] | 支持 | [6]「calls on social media to revive」；[6]「2018」 | — |
| C35 三股力量3① | 商業團體估計超過 1,500 家店被搶或被砸 | [8][12] | 支持 | [8]「more than 1,500 shops and businesses」 | [8]為超過1,500；[12]為估計1,500，來源精確程度不同。 |
| C36 三股力量3② | 損失數千萬到數億歐元 | [8][12] | 部分支持 | [8]「tens of millions」；[12]「could run into」 | [8]稱數千萬；[12]稱可能達數億。正文把不同估計及未確定的預測合成已知損失範圍。 |
| C37 三股力量3③ | 利摩日市長說…「不是為理念示威的人」 | [8] | 支持 | [8]「not demonstrators that defend causes」 | — |
| C38 三股力量3④ | 「是組織起來作戰的人」 | [8] | 支持 | [8]「people organised for war」 | — |
| C39 數字對照／上街① | 內政部 55 萬 | [4][7] | 支持 | [7]「some 550,000 people」 | 此數字由[7]支持。 |
| C40 數字對照／上街② | 主辦方 80 萬 | [4][7] | 支持 | [4]「an estimated 800,000 people」 | 此數字由[4]支持。 |
| C41 數字對照／預估 | 內政部賽前預估｜最多 15 萬 | [12] | 支持 | [12]「up to 150,000 people would take part」 | 原文為示威前夕的參與預估；「賽前」是用詞不當，宜用「示威前」。 |
| C42 數字對照／被捕① | 2,397 人 | [4][8] | 支持 | [4]「2,397 arrests were made on Saturday」 | 精確數字由[4]支持；[8]僅近2,400。 |
| C43 數字對照／被捕② | 巴黎 855 人，創紀錄 | [4][8] | 支持 | [8]「a record 855 people had been arrested」 | 巴黎精確數字及紀錄由[8]支持。 |
| C44 數字對照／受傷① | 警察與憲兵受傷｜997 人 | [4] | 支持 | [4]「997 police officers and gendarmes」 | — |
| C45 數字對照／受傷② | 7 人重傷 | [4] | 支持 | [4]「Seven of them were badly wounded」 | — |
| C46 數字對照／店家 | 1,500 家以上（商業團體估計） | [8][12] | 支持 | [8]「more than 1,500 shops and businesses」 | — |
| C47 數字對照／死亡① | 南特一名警察在另一場執法中遭車撞死 | [1] | 支持 | [1]「a separate police intervention in Nantes」 | — |
| C48 數字對照／死亡② | 肇事者與抗議無關 | [1] | 不支持 | [1]「the incident that prompted the operation」 | 原文僅說肇事者與觸發該次執法的事件無關，不能擴張為與抗議無關；同來源另列巴黎示威者心肺停止死亡。 |
| C49 數字更新① | 被捕與受傷數字在 48 小時內修正多次 | [6][4] | 支持 | [6]「1,200 people had been arrested」；[4]「2,397」 | [6]依序1,200→1,800被捕，[4]10-18 20:49為2,397；傷者150→997。 |
| C50 數字更新② | 總理 10-17 晚說 1,200 人被捕 | [6] | 支持 | [6]「Late on Saturday」；[6]「1,200 people」 | — |
| C51 數字更新③ | 150 名警察受傷 | [6] | 支持 | [6]「150 police hurt」 | — |
| C52 數字更新④ | 10-18 內政部更新為 2,397 人 | [4] | 支持 | [4]「18/10/2026 - 20:49」；[4]「2,397 arrests」 | — |
| C53 數字更新⑤ | 與 997 人 | [4] | 支持 | [4]「997 police officers and gendarmes」 | — |
| C54 移民說法1① | 美國總統川普 10-18 在 Truth Social 寫「France is burning!」 | [9] | 支持 | [9]「Sunday on Truth Social」；[9]「France is burning!」 | — |
| C55 移民說法1② | 10-19 再要求法國關閉邊境 | [9] | 支持 | [9]「again on Monday」；[9]「CLOSE THE BORDERS, FAST!」 | — |
| C56 移民說法1③ | 副總統范斯在 X 上說這是給美國的警告 | [9] | 支持 | [9]「the protests served as a warning」 | — |
| C57 移民說法2① | KOMO 轉述的分析人士說，事件已從校園轉成「無政府狀態」 | [3] | 支持 | [3]「“lawlessness” and “anarchy,”」 | 循相簿Read The Article打開正文，說話者Niles Gardiner；屬分析人士觀點。 |
| C58 移民說法2② | 同一篇稱抗議起於塞納-聖但尼省（Seine-Saint-Denis） | [3] | 支持 | [3]「peaceful blockades in the low-income」 | 確實出現在同篇照片說明，非分析人士對起點的查證結論。 |
| C59 移民說法2③ | 和維基百科寫的克雷泰伊不同 | [1] | 支持 | [1]「having originated in」；[1]「Créteil」 | 來源記述差異成立，不能由此判定何者是真正最早起點。 |
| C60 移民說法2④ | 衛報 10-10 報導的示威學校位於…塞夫朗（Sevran） | [13] | 支持 | [13]「his high school in Sevran」 | — |
| C61 移民說法2⑤ | 塞納-聖但尼省的塞夫朗 | [13] | 支持 | [13]「départements_, Seine-Saint-Denis」 | — |
| C62 移民說法3① | 塞納-聖但尼省移民占人口 31.6% | [14] | 部分支持 | [14]「Seine-Saint-Denis \| 31,6」 | 數字正確，但為2020–2021人口估計，非2026現況；immigré不等同外國人或移民後代。 |
| C63 移民說法3② | 全法最高 | [14] | 部分支持 | [14]「Champ : France hors Mayotte.」 | 在表列省份確為最高，但官方範圍排除Mayotte；「全法」無範圍限定。 |
| C64 移民說法4① | 主流媒體列出的訴求清單只有教育條件與生活費 | [1] | 部分支持 | [1]「the stress caused by」 | [1]另列Parcoursup申請壓力；若廣義教育條件可涵蓋，仍不足以支持「只有」的完整窮盡說法。 |
| C65 移民說法4② | 主流媒體列出的訴求清單只有教育條件與生活費 | [4] | 部分支持 | [4]「rising living costs and poor conditions」 | [4]支持主要議題，不是聲稱列盡所有訴求。 |
| C66 移民說法4③ | 主流媒體列出的訴求清單只有教育條件與生活費 | [8] | 部分支持 | [8]「more money for public services」 | [8]另有提高公共服務支出訴求；不能用「只有」排除其他訴求。 |
| C67 政治效應1① | 極右派候選人勒龐（Le Pen）譴責暴徒 | [6] | 支持 | [6]「Marine Le Pen condemned “the rioters”」 | — |
| C68 政治效應1② | 指控梅朗雄（Mélenchon）的政黨讓暴力合理化 | [6] | 支持 | [6]「“legitimised the violence”」 | — |
| C69 政治效應1③ | 目前在 2027 年 4 月總統大選民調領先 | [9] | 支持 | [9]「leads the polls ahead of April’s vote」 | 原文10-19報導所述當時民調；未載幅度或特定民調機構。 |
| C70 政治效應2① | 綠黨黨魁要求內政部長下台 | [12] | 支持 | [12]「Tondelier」；[12]「called for Núñez to resign」 | — |
| C71 政治效應2② | 理由是低估規模 | [12] | 支持 | [12]「underestimated the scale of the protests」 | — |
| C72 政治效應3① | 國會 2027 預算審議因無共識暫停 | [15] | 部分支持 | [15]「pour se consacrer à celui de la sécurité」 | 無共識及暫停均成立，但直接程序原因是轉審社會安全預算；標題並不足以將無共識寫成唯一原因。 |
| C73 政治效應3② | 政府目標是 2027 年赤字降到 GDP 的 5% | [15] | 支持 | [15]「déficit public à 5% du PIB en 2027」 | — |
| C74 跟歷史比① | 法國街頭抗議傳統可追溯到 19 世紀 | [16] | 支持 | [16]「street revolts throughout the 19th」 | 原文更上溯1789；正文說可追溯19世紀並無矛盾。 |
| C75 跟歷史比② | 啟發《悲慘世界》的 1832 年起義 | [16] | 支持 | [16]「in 1832 that inspired “Les Misérables”」 | — |
| C76 跟歷史比③ | 1968 年五月學運 | [16] | 支持 | [16]「May 1968 student uprising」 | 此項在同頁照片說明，非主文段落。 |
| C77 跟歷史比④ | 2018 年黃背心 | [16] | 支持 | [16]「Yellow Vest protests that began in 2018」 | — |
| C78 跟歷史比⑤ | 黃背心從 2018 年 11 月持續到 2020 年 6 月 | [7] | 支持 | [7]「from November 2018 to June 2020」 | 原文限定mass weekly protests；宜保留「每週大規模示威」以免讀成整個運動此後終止。 |
| C79 跟歷史比⑥ | 起因是油價上漲 | [7] | 支持 | [7]「initially against rising fuel prices」 | — |
| C80 跟歷史比⑦ | NBC 稱這次是法國「數年來最嚴重的暴力」 | [9] | 支持 | [9]「its worst violence in years」 | — |

## 需修改清單

- C01（一句話①，[4]，部分支持）：在起點句補[1]或[2]。
- C02（一句話②，[4]，部分支持）：改為「10-17 學生、工會與黃背心共同參與生活費抗議」，或另補加入日期來源。
- C03（一句話③，[4]，部分支持）：改「內政部估55萬人參與，部分抗議發生暴力」，補[7]。
- C06（一句話⑥，[1][2][4]，部分支持）：移除引號，改為「學生抗議其後與生活費抗議合流，部分示威出現暴力」，引[1]及[4]。
- C07（一句話⑦，[1][2][4]，部分支持）：改「這些來源主要描述教育與生活費訴求，未將移民列為起因」，避免排他結論；可另引[9]的法國官員說法。
- C09（時間線9月下旬，[3]，不支持）：改引[2]，寫「據9-30報導，教育部表示約3,700所高中中約400所受影響」。
- C31（三股力量1②，[1]，部分支持）：改「一名學生在有法文考試的年度，七個月沒有法文老師」。
- C36（三股力量3②，[8][12]，部分支持）：改「不同商業團體估計損失達數千萬歐元，另警告可能達數億歐元」。
- C48（數字對照／死亡②，[1]，不支持）：改「肇事者與引發該次執法的事件無關」；死亡欄另補巴黎示威者心肺停止死亡及調查中狀態，避免看似完整卻漏列。
- C62（移民說法3①，[14]，部分支持）：改「INSEE 2020–2021年估計，塞納-聖但尼省移民占人口31.6%」，必要時補統計定義。
- C63（移民說法3②，[14]，部分支持）：改「在該表涵蓋的法國各省中最高（不含Mayotte）」。
- C64（移民說法4①，[1]，部分支持）：改「[1]列出的主要訴求包含師資、班級、校舍、課表與Parcoursup申請壓力」。
- C65（移民說法4②，[4]，部分支持）：刪「只有」，改「France24主要描述生活費與學校條件訴求」。
- C66（移民說法4③，[8]，部分支持）：改「衛報列出教育條件、生活費及公共服務支出等訴求」。
- C72（政治效應3①，[15]，部分支持）：改「國民議會10-19晚暫停國家預算審議，轉審社會安全預算；各黨仍無共識」。

SUMMARY total=80 support=65 partial=13 fail=2 unreachable=0
