# WO wandavision-1：建片目錄＋旁白稿改寫（不建置）

工作目錄：`/Users/51mini/dev/vibe-shorts-pipeline`（repo 根）。片名 `wandavision-primer`。

## 背景

20 分鐘長片《沒看過漫威，也看得懂汪達幻視》。原稿 `/Users/51mini/.agent-reach/wv-primer/narration-20min.md`（約 5600 字，`【】` 章節、長段落）。備料 `/Users/51mini/.agent-reach/wv-primer/SOURCE-MATERIAL.md`。這張單只做文字與目錄，**不跑 build.sh、voice.py、approve.py**。

## 步驟

1. `cp -r films/taipei-silence films/wandavision-primer`，刪掉新目錄裡的 `out dist qa audit/*.log *.mp4 narration-v9-draft.md meta/published.json`（存在才刪）。`build.sh` 的 `OUT=` 改成 `wandavision-primer`。`rhythm-profile` 保持一行 `calm`。
2. 改寫原稿成 `films/wandavision-primer/narration.md`：
   - 章節改成 `## 段名`（開場、第一章…第八章、收尾，段名用原稿【】內的文字，可縮短）。不要兩行 `#` 說明。
   - **一行一句**：每行只有一個句末標點（。？！），結尾句末標點後不再接字。每行去標點後 ≤ 35 字。每個逗號短語（以 ，。？！、 切）去標點後 ≤ 18 字。長句拆成多行，不刪內容。
   - 破折號（—、——）與分號（；）**整篇最多 1 個**，其餘改句號拆句或逗號。「不是…而是」對舉整篇最多 1 次。
   - 前 60 字內要有「你」。
   - 人名統一：「旺達」全部改「汪達」（台灣 Disney+ 譯名）。
   - 保留原稿全部情節與語氣，總字數維持 5000 字以上（約 20 分鐘）。
3. 事實修正（照改，原稿有錯）：
   - **心靈寶石從來沒裝在宇宙魔方裡**。宇宙魔方裝的是空間寶石。改成：心靈寶石藏在一根權杖裡；薩諾斯把權杖交給洛基，二〇一二年洛基帶外星軍隊入侵紐約，復仇者聯盟首次組隊打贏；戰後宇宙魔方被索爾帶回阿斯嘉，權杖留在地球，落進藏在神盾局裡的九頭蛇手上。
   - 《迪克·范·戴克秀》是**一九六一到一九六六年**播出的六零年代喜劇，刪掉「五零年代的家庭喜劇」說法。《汪達幻視》第一集的五零年代黑白風格保留。收尾「為什麼是五零年代？因為她選了記憶裡最安全的那一年」改成以「黑白」為主詞（例：為什麼從黑白開始？因為她記憶裡最安全的畫面，就是那台電視上的黑白重播）。
   - 吉米·吳出自《蟻人與黃蜂女》，不是《蟻人》。
   - 奈及利亞（拉哥斯）事件：刪「二十六條人命」這個數字，改成「造成多名平民死亡，包括十一名瓦干達救援人員」。
4. 劇透刪減（這支片給還沒看劇的人，以下是劇中第 5–8 集才揭的底）：
   - 第七章：刪「體內殘留的心靈寶石能量凝聚成形……站起來一個新的幻視」，改成「她身邊，站著幻視」這類不交代來源的說法。
   - 第八章：艾格妮絲只保留「熱心得過頭、出現得太剛好的鄰居，多留意她」，刪掉塞勒姆、黑暗神書、反殺、吸魔力、兔子與兒子整段。莫妮卡刪「身體被改寫出超能力」那句。
   - 收尾的「那個渾身緋紅光芒的女人」保留（伏筆，不說破）。
5. 寫 `films/wandavision-primer/TREATMENT.md`：第一行標題，下面一行以 `爆款證據：` 開頭，內容抄 `refs/VIRAL-LEDGER.md` 第 561–567 行「汪達幻視入坑前需要補的漫威背景」條目中播放數 ≥ 10 萬的 4 筆（平台｜播放數｜標題｜連結）。其餘段落（分鏡表等）先留 `TODO`，不用寫。
6. 寫 `films/wandavision-primer/SOURCES.md`：表格「稿中說法｜來源 URL」，至少涵蓋第 3 步四項修正，各附一個可公開查的網址（Marvel 官方、Disney+、維基百科皆可）。`meta/facts.md` 清成只剩表頭（這支片沒有統計數字）。
7. 刪掉 `meta/caption-*.txt`、`meta/title-shorts.txt` 裡 taipei-silence 的內容（清空即可，之後另寫）。

## 禁區

- 不改 `scripts/`、`tests/`、`films/` 下其他片目錄、`refs/`（只讀）。`scripts/precheck.py`、`scripts/voice.py`、`tests/test_voice.py` 有別人未提交的改動，不碰、不還原。
- 不 commit、不 push、不上傳、不發布、不跑 `approve.py`。

## 驗收

```bash
bash /tmp/wv-accept-1.sh
```

exit 0 才算完成。失敗就照輸出修稿，不改驗收腳本。
