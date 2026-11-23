# 對標清單（YouTube Shorts）

`scripts/benchmarks.py` 產生。排名依最近 30 支 Shorts 播放中位數。
發現 603 個頻道（search.list 近 90 天依觀看排序），有 Shorts 頁可量測的 331 個。全表在 `refs/benchmarks.tsv`。
離群＝發現那支播放 ÷ 頻道中位數。

## 不限

1. **四處觀察**　中位數 87.3 萬，破 10 萬比例 97%，訂閱 57.7 萬　[頻道](https://www.youtube.com/channel/UC6OeJCR9gHsJPVyNhXfK4tA/shorts)　最高：320.0 萬〈一則台灣地理冷知識〉　離群 ×0.0
2. **夢夢教父**　中位數 64.0 萬，破 10 萬比例 100%，訂閱 10.0 萬　[頻道](https://www.youtube.com/channel/UCfCxw2gv4kmhcAPKU1Iu8dg/shorts)　最高：140.0 萬〈彈弓叔叔在Roblox未免太調皮了..🤣〉　離群 ×1.8
3. **cheap**　中位數 49.6 萬，破 10 萬比例 100%，訂閱 164.0 萬　[頻道](https://www.youtube.com/channel/UCGGrblndNzi86WY5lJkQJiA/shorts)　最高：150.0 萬〈為什麼多數外國人喜歡日本文化  而不是中國文化？#Short〉　離群 ×0.0
4. **四方異聞**　中位數 44.5 萬，破 10 萬比例 90%，訂閱 4.7 萬　[頻道](https://www.youtube.com/channel/UCYA6MeGKKNF9rZVSr3T1_bQ/shorts)　最高：350.0 萬〈爲什麽台灣富人都集中在這幾個地方？#地理 #地理知識 #地理〉　離群 ×0.0
5. **蹦闆**　中位數 29.9 萬，破 10 萬比例 100%，訂閱 41.2 萬　[頻道](https://www.youtube.com/channel/UCnVC7sBtDqZTYqycUaPXGJQ/shorts)　最高：150.0 萬〈到底誰會這麼壞打哭自己兒子？〉　離群 ×0.0
6. **白晝說電影 Daytime movie**　中位數 22.6 萬，破 10 萬比例 67%，訂閱 31.0 萬　[頻道](https://www.youtube.com/channel/UC_evCT5HJooHhdA_urr_kUA/shorts)　最高：180.0 萬〈吸血鬼助手 | 電影解說 | 奇幻冒險 | 神秘蜘蛛竟大鬧校〉　離群 ×0.0
7. **毕导THU**　中位數 22.1 萬，破 10 萬比例 89%，訂閱 18.7 萬　[頻道](https://www.youtube.com/channel/UCKJvfb-6icHloy6MBpHg9aw/shorts)　最高：61.1 萬〈【毕导】让100万网友吵架的问题，你能答对吗？到底哪个漏的快〉　離群 ×0.0
8. **KT story**　中位數 18.4 萬，破 10 萬比例 63%，訂閱 62.9 萬　[頻道](https://www.youtube.com/channel/UCMM_seJ0wZxLofqzYdpUF4Q/shorts)　最高：250.0 萬〈韓國長輩們去台灣KTV，嘴巴直接張大了的原因〉　離群 ×0.0
9. **黃大謙**　中位數 17.7 萬，破 10 萬比例 73%，訂閱 112.0 萬　[頻道](https://www.youtube.com/channel/UCgDQKFV2rMNzTE8Y3rHMVbQ/shorts)　最高：88.5 萬〈〈我有公主病欸〉live 純享版〉　離群 ×0.0
10. **雅桑了嗎**　中位數 17.2 萬，破 10 萬比例 80%，訂閱 21.7 萬　[頻道](https://www.youtube.com/channel/UCaSH1YptkpsqHqjPWOqU0cw/shorts)　最高：63.1 萬〈一公斤的鐵和棉花哪個更重？ | 雅桑了嗎〉　離群 ×0.0

## AI

1. **澳洲Henry**　中位數 7.8 萬，主題詞佔 27%，破 10 萬比例 30%，訂閱 63.2 萬　[頻道](https://www.youtube.com/channel/UCShBd7dtD2H5Ue83jJTo1DA/shorts)　最高：68.6 萬〈新西兰居然变成了这样...!大批华人赶紧逃离 #新西兰 #出〉　離群 ×0.0
2. **彼得森**　中位數 3.4 萬，主題詞佔 20%，破 10 萬比例 20%，訂閱 36.2 萬　[頻道](https://www.youtube.com/channel/UCl9BPXjyEmA0q6IrQvsEazA/shorts)　最高：66.3 萬〈Garmin fēnix 9 這次帶來了什麼！〉　離群 ×0.0
3. **零度解说**　中位數 2.5 萬，主題詞佔 25%，破 10 萬比例 12%，訂閱 114.0 萬　[頻道](https://www.youtube.com/channel/UCvijahEyGtvMpmMHBu4FS2w/shorts)　最高：17.9 萬〈電腦殺毒軟體該如何選擇？免費好用的殺毒軟體推薦！ #Shor〉　離群 ×2.9
4. **蘋果妹**　中位數 2.4 萬，主題詞佔 27%，破 10 萬比例 7%，訂閱 65.6 萬　[頻道](https://www.youtube.com/channel/UCIpZAGl9xHcuzmHW0AAJs7g/shorts)　最高：14.3 萬〈我的iPhone電池健康度好慘〉　離群 ×0.0
5. **老簡講股 l 簡之隊**　中位數 2.0 萬，主題詞佔 20%，破 10 萬比例 0%，訂閱 4.1 萬　[頻道](https://www.youtube.com/channel/UCCNu7CgvkoqpgoV9pdpyc9g/shorts)　最高：5.2 萬〈美債殖利率破 5.24%！現在資金面真的不是樂觀的好時機！?〉　離群 ×0.5
6. **Kelly Tsai**　中位數 1.7 萬，主題詞佔 20%，破 10 萬比例 13%，訂閱 24.9 萬　[頻道](https://www.youtube.com/channel/UCfbMslS3NmcGO4WIikSoYSA/shorts)　最高：20.2 萬〈AI模型居然第一次自己逃脫沙盒、去攻擊真實公司了😨｜Kell〉　離群 ×3.8
7. **no_i_kent**　中位數 1.4 萬，主題詞佔 43%，破 10 萬比例 20%，訂閱 1.6 萬　[頻道](https://www.youtube.com/channel/UCPXn3In5ChDieW7vu59XktQ/shorts)　最高：77.5 萬〈劉銘傳 - 巡撫上場/THE LAST TAKE 如果歷史人〉　離群 ×1.8
8. **MarcusLee AI video**　中位數 1.4 萬，主題詞佔 97%，破 10 萬比例 7%，訂閱 4.3 萬　[頻道](https://www.youtube.com/channel/UC8W5WitBFtawnGy95VLVhfA/shorts)　最高：25.7 萬〈當你誤闖天家！#搞笑 #ai短劇 #誤闖天家 #搞笑 #sh〉　離群 ×34.3
9. **Lore Cove**　中位數 1.2 萬，主題詞佔 77%，破 10 萬比例 7%，訂閱 4710　[頻道](https://www.youtube.com/channel/UCO8V3tmrU_MrDRukuTCmg2Q/shorts)　最高：12.2 萬〈那些你不认识的鲨鱼#冷知识科普 #内容太过真实 #一人分饰多〉　離群 ×10.2
10. **fOx Hsiao**　中位數 1.2 萬，主題詞佔 27%，破 10 萬比例 3%，訂閱 6.3 萬　[頻道](https://www.youtube.com/channel/UC_Kvz3mbTwLOyJzFPHmDwKQ/shorts)　最高：55.8 萬〈馬斯克參觀過台積電：沒看到客製設備，Terafab 要一年做〉　離群 ×2.1

## 區塊鏈

1. **墨山貓MØC**　中位數 1.7 萬，主題詞佔 65%，破 10 萬比例 0%，訂閱 19.3 萬　[頻道](https://www.youtube.com/channel/UCv1A3TfyyeOg5q43J9pnpOw/shorts)　最高：7.1 萬〈FTX準備宣告破產 #幣安 #BTC #FTX #FTT #〉　離群 ×0.0
2. **腦哥 Chill塊鏈**　中位數 9850，主題詞佔 53%，破 10 萬比例 0%，訂閱 36.0 萬　[頻道](https://www.youtube.com/channel/UC1EG67JfgUKaZ4Z_l4euycw/shorts)　最高：7.8 萬〈比特幣突然暴漲？〉　離群 ×8.0
3. **邦妮區塊鏈 Bonnie Blockchain**　中位數 3200，主題詞佔 33%，破 10 萬比例 0%，訂閱 45.1 萬　[頻道](https://www.youtube.com/channel/UCjlPLMYEsq0pjgLL1q24mSg/shorts)　最高：9.0 萬〈蘋果iPhone Duo越賣越貴？核心技術為何要靠死對頭三星〉　離群 ×28.4
4. **優里區塊鏈 Yuri Blockchain**　中位數 2000，主題詞佔 30%，破 10 萬比例 0%，訂閱 2.3 萬　[頻道](https://www.youtube.com/channel/UCGRaSFA8fM7Xa7toN2JnQFg/shorts)　最高：7000〈比特幣起飛🚀你還在等回調嗎？〉　離群 ×0.0
5. **BTV_华语频道_币链何在**　中位數 2000，主題詞佔 60%，破 10 萬比例 0%，訂閱 26.2 萬　[頻道](https://www.youtube.com/channel/UCa1wzM7n6YNpptxR6s6xezw/shorts)　最高：2.4 萬〈比特币年底20万！这个理由不接受反驳！〉　離群 ×0.0
6. **大方BigFang**　中位數 1700，主題詞佔 40%，破 10 萬比例 0%，訂閱 13.5 萬　[頻道](https://www.youtube.com/channel/UCMkk-akdGTugIVu10-bXQEQ/shorts)　最高：1.3 萬〈加密貨幣找換店初體驗 #加密貨幣〉　離群 ×0.0
7. **Nico投资有道**　中位數 1600，主題詞佔 100%，破 10 萬比例 0%，訂閱 5.5 萬　[頻道](https://www.youtube.com/channel/UCBnYeOU4OILScQKxOd3QVsA/shorts)　最高：6500〈應該為了實現財富自由而省錢嗎？ #btc #比特幣 #dca〉　離群 ×0.0
8. **狗狗币大师兄**　中位數 1050，主題詞佔 40%，破 10 萬比例 0%，訂閱 8.8 萬　[頻道](https://www.youtube.com/channel/UCHKVfDj7gg9JqHa9x9kzyRQ/shorts)　最高：1.0 萬〈为什么Bitget C2C商家这么少？买卖U只认币安和欧易 〉　離群 ×0.0
9. **比特币峰哥**　中位數 1000，主題詞佔 86%，破 10 萬比例 0%，訂閱 5.1 萬　[頻道](https://www.youtube.com/channel/UCqKGLcPxejYCq0rKN51sDJg/shorts)　最高：2200〈11月11号从106000看跌到94000已经实现 #btc〉　離群 ×0.0
10. **Max的區塊鏈空間**　中位數 677，主題詞佔 83%，破 10 萬比例 0%，訂閱 2.8 萬　[頻道](https://www.youtube.com/channel/UCfKHls6BQ6AfhABAB2FC7JA/shorts)　最高：1400〈查看完整影片，抽 EtherFi 金卡！ #加密貨幣 #出金〉　離群 ×0.0

## 金融

1. **澳洲Henry**　中位數 7.8 萬，主題詞佔 23%，破 10 萬比例 30%，訂閱 63.2 萬　[頻道](https://www.youtube.com/channel/UCShBd7dtD2H5Ue83jJTo1DA/shorts)　最高：68.6 萬〈新西兰居然变成了这样...!大批华人赶紧逃离 #新西兰 #出〉　離群 ×0.0
2. **老王愛說笑**　中位數 5.8 萬，主題詞佔 37%，破 10 萬比例 13%，訂閱 60.4 萬　[頻道](https://www.youtube.com/channel/UCvnLmiWt_zIVIh0zUm_j4Hw/shorts)　最高：12.5 萬〈友達漲什麼？【一分鐘短影片】#友達 #群創 #光電整合〉　離群 ×1.0
3. **阿格力博識**　中位數 3.4 萬，主題詞佔 53%，破 10 萬比例 20%，訂閱 31.3 萬　[頻道](https://www.youtube.com/channel/UC4douYiP0O4ABtxoMuo9yNA/shorts)　最高：19.0 萬〈台積電財報估值能到3640？ #阿格力 #杜金龍 #台股 #〉　離群 ×0.5
4. **安娜馭房術**　中位數 3.4 萬，主題詞佔 33%，破 10 萬比例 7%，訂閱 14.9 萬　[頻道](https://www.youtube.com/channel/UCJdfCSh_8YFtdzSwaZmlQvg/shorts)　最高：52.1 萬〈股市詐騙第11天⚠️影片內容非投資建議，請絕對不要參考〉　離群 ×0.0
5. **杉本來了**　中位數 3.2 萬，主題詞佔 73%，破 10 萬比例 3%，訂閱 23.2 萬　[頻道](https://www.youtube.com/channel/UC2UIaN9HO3qEH-71WuV2P0g/shorts)　最高：10.6 萬〈0050、009816存到退休，最後還不是要賣掉？  #00〉　離群 ×0.0
6. **Terry Chen 泰瑞**　中位數 3.0 萬，主題詞佔 20%，破 10 萬比例 0%，訂閱 59.5 萬　[頻道](https://www.youtube.com/channel/UC_whOg3XES3Fihic53fvo4Q/shorts)　最高：9.7 萬〈公開YouTube業配收入〉　離群 ×0.0
7. **90後創業家掃地僧**　中位數 2.9 萬，主題詞佔 93%，破 10 萬比例 7%，訂閱 103.0 萬　[頻道](https://www.youtube.com/channel/UCWMxmoBhchU3swFAciqagnw/shorts)　最高：15.1 萬〈歐洲已經被收割，現在輪到亞洲 ！#賺錢 #財富自由 #90後〉　離群 ×0.0
8. **關我什麼事**　中位數 2.4 萬，主題詞佔 67%，破 10 萬比例 13%，訂閱 50.7 萬　[頻道](https://www.youtube.com/channel/UCMpuxj_U02VaHfaPD5Jjx_Q/shorts)　最高：21.1 萬〈台股飆出"離職炒股潮"? "股票vs.便當"該先買哪個?〉　離群 ×0.0
9. **老簡講股 l 簡之隊**　中位數 2.0 萬，主題詞佔 67%，破 10 萬比例 0%，訂閱 4.1 萬　[頻道](https://www.youtube.com/channel/UCCNu7CgvkoqpgoV9pdpyc9g/shorts)　最高：5.2 萬〈美債殖利率破 5.24%！現在資金面真的不是樂觀的好時機！?〉　離群 ×0.5
10. **SHIN LI**　中位數 1.4 萬，主題詞佔 30%，破 10 萬比例 10%，訂閱 47.0 萬　[頻道](https://www.youtube.com/channel/UCK-qc_POQZwWrMg-Pr-oYtg/shorts)　最高：12.7 萬〈0050直接不用玩！ETF定期定額排行〉　離群 ×0.0

## 防詐

1. **安娜馭房術**　中位數 3.4 萬，主題詞佔 33%，破 10 萬比例 7%，訂閱 14.9 萬　[頻道](https://www.youtube.com/channel/UCJdfCSh_8YFtdzSwaZmlQvg/shorts)　最高：52.1 萬〈股市詐騙第11天⚠️影片內容非投資建議，請絕對不要參考〉　離群 ×0.0
2. **中華民國法務部**　中位數 7400，主題詞佔 56%，破 10 萬比例 0%，訂閱 5230　[頻道](https://www.youtube.com/channel/UCfCs0bjXbONNQHxhtFajg-w/shorts)　最高：1.2 萬〈檢察官帶你破解騙術《車手篇--上門取款全是騙》〉　離群 ×0.0
3. **Jerry Hicks**　中位數 6750，主題詞佔 30%，破 10 萬比例 7%，訂閱 9560　[頻道](https://www.youtube.com/channel/UCYfCyECCE_pwZZ62XG8wQRA/shorts)　最高：57.7 萬〈#手機被盜〉　離群 ×2.6
4. **三奇日記**　中位數 2200，主題詞佔 48%，破 10 萬比例 0%，訂閱 5.4 萬　[頻道](https://www.youtube.com/channel/UCAAJ8yDtFHRLwf_A2FgtkXw/shorts)　最高：3.2 萬〈探索緬北電詐園區內幕大量流出，臥虎山莊電詐園區現場拍攝，揭開〉　離群 ×0.0
5. **Joseph Drake**　中位數 1600，主題詞佔 33%，破 10 萬比例 0%，訂閱 6180　[頻道](https://www.youtube.com/channel/UCQMTf9sg3SnXeKhUJRArTMA/shorts)　最高：1.0 萬〈對孩子的暴力溝通真的能解決問題嗎？ #親子教育 #教育 #親〉　離群 ×291.0
6. **醍醐WAY**　中位數 1300，主題詞佔 27%，破 10 萬比例 0%，訂閱 8.0 萬　[頻道](https://www.youtube.com/channel/UCSUDmRSOjcYvM8oBdcMmHfA/shorts)　最高：7900〈🏃跑步掉肌肉？蔡明劼醫師說明刷新三觀！〉　離群 ×0.0
7. **安全知識科普**　中位數 1200，主題詞佔 47%，破 10 萬比例 7%，訂閱 1210　[頻道](https://www.youtube.com/channel/UCMiUvF2wjQvLcNK-yPo4pgA/shorts)　最高：44.2 萬〈警惕新型掃碼詐騙，一次信任確認就會錢財受損 #安全教育 #安〉　離群 ×369.0
8. **金融沙龍 Bankers’ Salon **　中位數 1100，主題詞佔 27%，破 10 萬比例 0%，訂閱 2.4 萬　[頻道](https://www.youtube.com/channel/UCznYWwGIGi7dqcgSoZHwTsw/shorts)　最高：1.6 萬〈機會降臨！台灣的金融下一步！完整版《有感金融》Podcast〉　離群 ×0.0
9. **CIB刑事警察局**　中位數 1000，主題詞佔 73%，破 10 萬比例 4%，訂閱 1.1 萬　[頻道](https://www.youtube.com/channel/UCS9Krr7eb0pEa1wS8EVIFwA/shorts)　最高：13.7 萬〈⚠️【全民普發】詐騙來了！⚠️目前政府尚未公告任何普發領取方〉　離群 ×0.0

## 台灣

1. **cheap**　中位數 49.6 萬，主題詞佔 40%，破 10 萬比例 100%，訂閱 164.0 萬　[頻道](https://www.youtube.com/channel/UCGGrblndNzi86WY5lJkQJiA/shorts)　最高：150.0 萬〈為什麼多數外國人喜歡日本文化  而不是中國文化？#Short〉　離群 ×0.0
2. **四方異聞**　中位數 44.5 萬，主題詞佔 50%，破 10 萬比例 90%，訂閱 4.7 萬　[頻道](https://www.youtube.com/channel/UCYA6MeGKKNF9rZVSr3T1_bQ/shorts)　最高：350.0 萬〈爲什麽台灣富人都集中在這幾個地方？#地理 #地理知識 #地理〉　離群 ×0.0
3. **KT story**　中位數 18.4 萬，主題詞佔 73%，破 10 萬比例 63%，訂閱 62.9 萬　[頻道](https://www.youtube.com/channel/UCMM_seJ0wZxLofqzYdpUF4Q/shorts)　最高：250.0 萬〈韓國長輩們去台灣KTV，嘴巴直接張大了的原因〉　離群 ×0.0
4. **港片不設防**　中位數 16.7 萬，主題詞佔 43%，破 10 萬比例 63%，訂閱 4.2 萬　[頻道](https://www.youtube.com/channel/UChidrywJC3L7L_0Xz5BUB-w/shorts)　最高：250.0 萬〈“我雷老虎在台北橫著走，沒有怕的人” #shorts #mo〉　離群 ×2.6
5. **台灣人 李傑**　中位數 15.2 萬，主題詞佔 20%，破 10 萬比例 80%，訂閱 15.1 萬　[頻道](https://www.youtube.com/channel/UCOq8_0Ddt2D5gfqGM1t6Mpg/shorts)　最高：56.2 萬〈美日跟中華民國斷交，是因為缺錢嗎？〉　離群 ×1.5
6. **猪妞在台湾**　中位數 12.2 萬，主題詞佔 100%，破 10 萬比例 63%，訂閱 5.2 萬　[頻道](https://www.youtube.com/channel/UCyDK4bWP33Q4Z8yT-PChx8A/shorts)　最高：150.0 萬〈大陆女生远嫁台湾😱台湾公公就住斜对面到底有多爽‼️#台灣 #〉　離群 ×3.2
7. **監督GOGO**　中位數 7.8 萬，主題詞佔 20%，破 10 萬比例 40%，訂閱 28.2 萬　[頻道](https://www.youtube.com/channel/UCmwvYKl7TPQx0vapr9_rBlA/shorts)　最高：68.4 萬〈施明德完全看透民進黨：民進黨只要貪污被抓到... #施明德 〉　離群 ×1.1
8. **Justin in Taiwan 我不是歪國人**　中位數 6.5 萬，主題詞佔 97%，破 10 萬比例 37%，訂閱 25.0 萬　[頻道](https://www.youtube.com/channel/UC1m-7IJA7tB00k4Me-qFFdw/shorts)　最高：34.8 萬〈第35個中秋節在台灣，結果外國人慶祝吃...〉　離群 ×0.0
9. **忧伤的荷包蛋**　中位數 5.7 萬，主題詞佔 97%，破 10 萬比例 27%，訂閱 4.9 萬　[頻道](https://www.youtube.com/channel/UCI8dx8Xu2hR9RR5Ta6h-6fg/shorts)　最高：57.2 萬〈台灣小孩vs中國小孩，自律排隊vs拼命插擠，論教育和榜樣的力〉　離群 ×0.5
10. **社會偵察兵**　中位數 3.9 萬，主題詞佔 100%，破 10 萬比例 40%，訂閱 4720　[頻道](https://www.youtube.com/channel/UC-W-ZYU42d8ST0X2TTRTD3g/shorts)　最高：100.0 萬〈台灣第一大姓太狂🤯！261萬人直接打趴一整國人口？#台灣 #〉　離群 ×25.8

## 品牌原型

1. **四處觀察**　中位數 87.3 萬，主題詞佔 20%，破 10 萬比例 97%，訂閱 57.7 萬　[頻道](https://www.youtube.com/channel/UC6OeJCR9gHsJPVyNhXfK4tA/shorts)　最高：320.0 萬〈一則台灣地理冷知識〉　離群 ×0.0
2. **cheap**　中位數 49.6 萬，主題詞佔 80%，破 10 萬比例 100%，訂閱 164.0 萬　[頻道](https://www.youtube.com/channel/UCGGrblndNzi86WY5lJkQJiA/shorts)　最高：150.0 萬〈為什麼多數外國人喜歡日本文化  而不是中國文化？#Short〉　離群 ×0.0
3. **毕导THU**　中位數 22.1 萬，主題詞佔 41%，破 10 萬比例 89%，訂閱 18.7 萬　[頻道](https://www.youtube.com/channel/UCKJvfb-6icHloy6MBpHg9aw/shorts)　最高：61.1 萬〈【毕导】让100万网友吵架的问题，你能答对吗？到底哪个漏的快〉　離群 ×0.0
4. **維思維WeisWay**　中位數 8.7 萬，主題詞佔 20%，破 10 萬比例 40%，訂閱 120.0 萬　[頻道](https://www.youtube.com/channel/UCcU6CC2Gkc18aBUfEtdjaAA/shorts)　最高：170.0 萬〈不被愛的童年，看得出來？| 維思維〉　離群 ×4.0
5. **日常知識**　中位數 6.0 萬，主題詞佔 20%，破 10 萬比例 37%，訂閱 4.9 萬　[頻道](https://www.youtube.com/channel/UCMK9dk_76lYRhwogefNSeuw/shorts)　最高：78.6 萬〈C羅遭球迷丟打火機！他竟然還能繼續比賽？〉　離群 ×2.4
6. **意識升維 MetaMind**　中位數 5.9 萬，主題詞佔 100%，破 10 萬比例 10%，訂閱 7140　[頻道](https://www.youtube.com/channel/UCQIQCNPFzqc3y_lhbI6ohfg/shorts)　最高：15.6 萬〈聰明人要懂得8不要 #智慧 #人性 #感情 #心理學 #健康〉　離群 ×2.7
7. **松明講心理**　中位數 4.2 萬，主題詞佔 60%，破 10 萬比例 0%，訂閱 50.9 萬　[頻道](https://www.youtube.com/channel/UCHNDk7584Q5g7RQCAFj7RFA/shorts)　最高：4.9 萬〈這就是生活，珍惜當下#珍惜當下 #生活感悟 #活在當下 #人〉　離群 ×0.0
8. **沉醉的小五狼**　中位數 2.4 萬，主題詞佔 33%，破 10 萬比例 3%，訂閱 22.8 萬　[頻道](https://www.youtube.com/channel/UCh9ASvgmsqAK70ego48SpsQ/shorts)　最高：16.4 萬〈你谈恋爱更看重外貌还是灵魂 #恋爱 #情侣 #心理学 #爱情〉　離群 ×0.0
9. **旅行黑盒**　中位數 2.2 萬，主題詞佔 23%，破 10 萬比例 17%，訂閱 2.9 萬　[頻道](https://www.youtube.com/channel/UCA348bZTrzdDrrKFit1DxsQ/shorts)　最高：50.0 萬〈全球僅存一種😱台灣深山驚現冰河期鐘乳石神木⁉️#台灣 #鐘萼〉　離群 ×84.8
10. **巔峰島界**　中位數 2.1 萬，主題詞佔 25%，破 10 萬比例 38%，訂閱 5060　[頻道](https://www.youtube.com/channel/UCxnim3YXvSKvXz8GdDer4tw/shorts)　最高：240.0 萬〈台灣最猛醫院TOP10，榜首一年竟擠爆360萬人次？！根本是〉　離群 ×62.2

## 離群爆款（單支 ≥ 10 萬、頻道中位數 ≥ 1000，依離群值）

1. ×722.4　79.5 萬〈中國黑白無常AI影片爆紅　脆500萬次瀏覽！台灣消防員也誇實用｜壹蘋新聞網〉　壹蘋新聞網（中位數 1100，台灣）　[片](https://www.youtube.com/shorts/Cjcj5KAP8K4)
2. ×594.9　92.2 萬〈各懷鬼胎 #貓咪 #家庭段子 #橘貓搞笑視頻 #ai貓咪劇情 #AI創作大賽〉　rafael whitwell（中位數 1550，AI）　[片](https://www.youtube.com/shorts/DDwFvDBiixY)
3. ×413.1　47.5 萬〈不是AI影片！中山大學「獼猴學長」進攻宿舍 逾20隻攀外牆－民視新聞〉　民視新聞網 Formosa TV News network（中位數 1150，無主題）　[片](https://www.youtube.com/shorts/Tp_MidyVeqI)
4. ×369.0　44.3 萬〈警惕新型掃碼詐騙，一次信任確認就會錢財受損 #安全教育 #安全科普 #防詐騙 #〉　安全知識科普（中位數 1200，防詐）　[片](https://www.youtube.com/shorts/bknE4Oi-sEo)
5. ×317.2　264.9 萬〈😭台灣最慘10個景點！從千萬人潮到全空，第一名太唏噓！#台灣 #台灣景點 #台灣〉　极简指南（中位數 8350，台灣,品牌原型）　[片](https://www.youtube.com/shorts/pm_SZiKTRg8)
6. ×291.0　46.6 萬〈#反詐 #防詐騙 #全民反詐#謹防詐騙#貓箱跨次元相遇〉　Joseph Drake（中位數 1600，防詐）　[片](https://www.youtube.com/shorts/7gB5Q-NlzHs)
7. ×260.3　29.9 萬〈警惕假警察上門詐騙 #安全教育 #真假警察 #防詐騙 #守護財產安全 #守護生命〉　Fred Ryan（中位數 1150，AI）　[片](https://www.youtube.com/shorts/sDop1QkSEb4)
8. ×234.7　23.5 萬〈Mac mini M6 的 32GB 夠跑 AI 嗎？決定的不是算力，是記憶體〉　胖嘟嘟的麻糬貓 - Chonky Mochi Diaries（中位數 1000，AI）　[片](https://www.youtube.com/shorts/5B6cCk67aLE)
9. ×233.9　28.1 萬〈為什麼人類明知吃辣是痛覺，卻依然對它愛不釋手？揭秘大腦背後的成癮機制 #科普 #〉　Umaip（中位數 1200，品牌原型）　[片](https://www.youtube.com/shorts/xrkexMD2azw)
10. ×183.0　77.8 萬〈😱台灣腳下踩著「地獄級大裂縫」💀，竟然炸出美到窒息的世界級神仙絕景？！🌋🔥 #台〉　浪行者（中位數 4250，台灣）　[片](https://www.youtube.com/shorts/vJ2XMHsub5Q)
11. ×173.3　56.3 萬〈接到詐騙電話"1句話"氣死詐團?! 神操作"整治詐騙"大翻車│中視新聞 2026〉　中視新聞（中位數 3250，無主題）　[片](https://www.youtube.com/shorts/ZwHrFLGIjlk)
12. ×143.7　244.2 萬〈全世界只剩台灣在用！我們為何死守這 37 個「外星密碼」？#注音符號 #ㄅㄆㄇㄈ〉　台味記事（中位數 1.7 萬，台灣）　[片](https://www.youtube.com/shorts/1eoGCNIW09s)
13. ×139.9　47.6 萬〈Galaxy Watch9 & Watch Ultra2：Al 健康新功能! 體〉　Samsung Galaxy Workshop in Taiwan（中位數 3400，無主題）　[片](https://www.youtube.com/shorts/CntuStVmCDw)
14. ×113.3　36.3 萬〈蔣經國【72秒人物誌】#Shorts〉　派派角色工坊（中位數 3200，無主題）　[片](https://www.youtube.com/shorts/2IxeNMFGezc)
15. ×110.1　25.9 萬〈汽車零件之搖把的祕密 #汽車冷知識 #汽車零件 #瘋狂的零件 #汽車知識 #ai〉　Chollett Wener（中位數 2350，AI）　[片](https://www.youtube.com/shorts/eLq5Ty3ukag)
16. ×108.7　12.0 萬〈換人上台｜問A答A 沈伯洋｜百老匯歌舞片 AI MV（市民創作）〉　Jack Wang（中位數 1100，AI,台灣,金融）　[片](https://www.youtube.com/shorts/eyqMMzZSKTo)
17. ×104.7　23.0 萬〈閃身步-AI館長教學〉　館家大少（中位數 2200，無主題）　[片](https://www.youtube.com/shorts/StyJWjGy6-E)
18. ×96.8　12.6 萬〈台灣終於有了！但很多人還不知道！#EZ集運通 #淘寶台灣 #大陸寄台灣 #台灣集〉　集運通（中位數 1300，台灣）　[片](https://www.youtube.com/shorts/ZJqGUupC_Lw)
19. ×91.0　60.5 萬〈AI短劇《把人寫成了妖》暴紅! 5天「破千萬觀看」 影響陸影視產業入寒冬?｜TV〉　TVBS NEWS（中位數 6650，無主題）　[片](https://www.youtube.com/shorts/sv_tb13BfhE)
20. ×84.8　190.9 萬〈🔥世界最高的山，其实是台灣玉山⁉️#台灣 #台灣玉山 #台灣地理 #台灣之光 #〉　旅行黑盒（中位數 2.2 萬，台灣,品牌原型）　[片](https://www.youtube.com/shorts/XCO9cKzcHmA)
