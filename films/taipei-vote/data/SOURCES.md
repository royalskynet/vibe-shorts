# township_2024.csv 資料來源（2026-11-08 抓取）

## 票數（ko/lai/hou）
- 中選會選舉資料庫「第16任總統副總統選舉」（2024-01-13）：https://db.cec.gov.tw/ElecTable/Election?type=President
- 實際抓取的 JSON（theme_id 4d83db17c1707e3defae5dc4d4e9c800）：
  - 縣市清單：https://db.cec.gov.tw/static/elections/data/tickets/ELC/P0/00/4d83db17c1707e3defae5dc4d4e9c800/C/00_000_00_000_0000.json
  - 各縣市鄉鎮市區票數：https://db.cec.gov.tw/static/elections/data/tickets/ELC/P0/00/4d83db17c1707e3defae5dc4d4e9c800/D/{prv}_{city}_00_000_0000.json（22 檔）
- cand_no 1＝柯文哲、2＝賴清德、3＝侯友宜。

## indigenous（原住民族地區 55 鄉鎮市區）
- 原住民族委員會「55個原住民族地區簡介」：https://www.cip.gov.tw/zh-tw/village/list.html?cumid=1E4A2846561931B1
- 參考（未用於比對）：行政院核定原住民地區一覽表 https://gazette.nat.gov.tw/EG_FileManager/eguploadpub/eg031071/ch04/type1/gov31/num8/images/Eg01.pdf

## hakka（客家文化重點發展區 70 鄉鎮市區）
- 客家委員會「客家文化重點發展區鄉（鎮、市、區）一覽表」（106-02-24 客會綜字第1060002892號公告，更新 112-01-06）：https://www.hakka.gov.tw/chhakka/app/data/view?id=236&module=law&serno=38317
- 同資料開放版（70 筆，以區碼呈現，僅用於核對筆數）：https://data.gov.tw/dataset/162466 → https://cloud.hakka.gov.tw/Pub/Opendata/DTST20230500026.csv

## 處理
- 名稱中的「台」一律改成「臺」（原民會頁寫「台東縣」「霧台鄉」「台東市」）。
- 原始檔留在 /tmp/tw_map_project/raw/。
