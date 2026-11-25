# WO wandavision-14：第一集重做（補薩諾斯動機、刪劇透、畫面加多幕）

工作目錄 `/Users/51mini/dev/vibe-shorts-pipeline`，片目錄 `films/wv-primer-1/`。使用者 11-24 看完第一集私人片的回饋：

1. 「薩諾斯因為家鄉人口過多崩潰這個背景要說」
2. 「畫面也太少了，感覺可以很多幕」
3. 「說居民被控制這已經劇透了，不要劇透」

使用者授權：稿子不用再給他核全文，你自己寫 verdicts、自己跑 approve。

## 1 劇透判準

這支片給「還沒看《汪達幻視》」的人看。只准講《汪達幻視》開播前的電影已經演過的事（到《復仇者聯盟：終局之戰》為止）。《汪達幻視》劇裡揭露的任何事都不講，包括暗示和「多留意某某」這種提示。

已裁決要刪：

- `## 西景鎮` 整段。天劍局拆解遺體、幻視買地、魔法吞掉小鎮、接管居民意識、改寫房子、黑白畫面、陪她演戲，都是劇裡第八、九集才揭露的。
- `## 收尾` 的這些句：「為什麼是情境喜劇／童年避風港」「鎮民眼神放空／被控制的真人」「艾格妮絲多留意她」「這個幻視到底是不是真的」「這個答案會把所有東西串起來」「那顆寶石，那根權杖」「緋紅光的女人」。

替換方向：「無限之戰」段結尾「他在彈指之前，就已經死了。」之後，用兩三句收：汪達失去了他，接下來她去了哪裡、做了什麼，就是《汪達幻視》要講的。不加新事實。收尾保留「你已經可以開播《汪達幻視》了。」和預告下一集那句。

## 2 補薩諾斯動機

放在「無限之戰」段「就在這時候，薩諾斯來了。」附近，三到五句。內容依《復仇者聯盟：無限之戰》：薩諾斯的家鄉泰坦星，人口太多、資源耗盡，最後崩潰滅亡。他因此認定，宇宙要活下去，就得抹掉一半的生命。來源網址補進 `SOURCES.md`（例 https://en.wikipedia.org/wiki/Thanos 或 Avengers:_Infinity_War）。

## 3 稿子硬規格

- 只改 `narration.md`（與連動的 `pace.json`、`SOURCES.md`、`cast.json` 的 say）。
- 總字數 1250–1600。每行一句、≤35 字、一行只一個句號。
- 必須出現：泰坦、人口、薩諾斯、幻視、心靈寶石。
- 不准出現：控制、接管、意識、改寫、黑白、笑聲、情境喜劇、避風港、艾格妮絲、眼神、零件、遺體、買下、真的幻視、緋紅、哈克尼斯、緋紅女巫、混沌魔法、白幻視、比利、湯米、黑暗神書、死神、雪帕德。
- 改完照流程：口語化（只過改動句，重寫 `audit/humanize.md` 戳記）→ `scripts/devils.sh films/wv-primer-1` → 你逐爭點寫 `audit/verdicts.md`（格式照現有檔：`engine=`、`narration_sha:`、`sources_sha:`、`stage: script`，每爭點 `## 爭點 N`／`VERDICT: PRO_WINS|CON_WINS`／`REASON:`；CON_WINS 就改稿，改稿後 devils 只再跑一輪，新的窄爭點只記 verdicts 不再改稿）→ `.venv/bin/python scripts/approve.py films/wv-primer-1 "使用者 11-24 授權免核全文，私人片"`。
- `python3 -c "import sys;from pathlib import Path;sys.path.insert(0,'scripts');import precheck;print(precheck.audit_problems(Path('films/wv-primer-1')))"` 要印 `[]`。

## 4 畫面加多幕

現在 `index.html` 一段 `## ` 只有一張畫面（`SCENES` 9 個），一張停 30 秒以上。改成：

- 每段依句子切成多個鏡頭，畫面約每 6–10 秒換一次，任何一個鏡頭不超過 12 秒。全片至少 30 個不同畫面。
- 換鏡頭的時間點取自 `timeline.js` 的句子時間（`TL.lines`），不要寫死秒數。`render(t)` 只依賴 `t`（不累積狀態、不讀 `Date.now()`）。
- 畫面內容要對到那句在講什麼。例：泰坦星人口擠爆→荒廢；六顆寶石逐一亮起；幻視額頭寶石被扯下；化成灰；五年後人回來、幻視不在。用現有米色插畫風與 `assets/illust/`、現有小人畫法，自己畫新構圖。這些是例子，照「對到句意」的原則自己判斷。
- 不要畫任何第 1 節禁講的劇情（黑白電視裡的汪達幻視、被控制的居民等）。
- 驗收怎麼量：`python3 /tmp/wv-shots.py films/wv-primer-1/wv-primer-1.mp4 5` 逐秒比畫面（去掉上下字幕區），跟目前鏡頭起點差超過 5 就算新鏡頭；印「鏡頭數 最長同畫面秒數 起點秒」。舊片是 13 個、最長 48 秒，要做到 ≥30 個、最長 ≤15 秒。字幕換行不算換鏡頭，要畫面本身換。
- 不改 `scripts/`、`tests/`、`engine.js` 以外的共用檔。

## 5 建置

1. 先確認沒有別的建置在跑：`pgrep -fl "build.sh|hyperframes|voice.py"` 有輸出就等到沒有（每 60 秒查一次）。
2. `cd films/wv-primer-1 && bash build.sh`。ram_guard 砍掉 voice.py 時，等記憶體回 GREEN 再重跑，不併發。
3. `scripts/qa_sheet.sh films/wv-primer-1`。
4. `cp films/wv-primer-1/wv-primer-1.mp4 films/wv-primer-1/dist/wv-primer-1-shorts.mp4`。
5. 刪舊的 `films/wv-primer-1/qa/yt-private.txt`。
6. 節奏閘若仍 BAD，只記錄原文，不改閘門基準。

## 禁區

不改 `scripts/`、`tests/`、`refs/`、其他片目錄、`/tmp/wv-*`；不 commit；不上傳（上傳由後續流程做）；不跑 `yt_upload.py`。

## 驗收

```bash
bash /tmp/wv-accept-14.sh
```

跑到 `ACCEPT-14 OK` 才算完成；失敗就照 FAIL 行修到過。回報附：字數、刪了哪些句、新增的薩諾斯句、鏡頭數、節奏閘原文。

## 第二輪（只在 `films/wv-primer-1/qa/verify-14.md` 存在且首行是 `VERDICT: FAIL` 時）

讀那份檔，逐條修完，重跑第 3–5 步與驗收。修完刪掉 `qa/verify-14.md`。
