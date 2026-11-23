# BLOCKED — taipei-rent 卡在「稿子已核准」（2026-11-02 夜間批次）

## 卡在哪

`build.sh` 第一步 `voice.py` 會被核准門擋（`precheck.approval_problems`，11-01 新增）：`audit/approved.md` 不存在。
我沒有自己跑 `scripts/approve.py`，原因是**現在的 narration.md 不是你 10-30 核過的那一版**：

- 核准檔 `OpenBot/Shared/approved/2026-10-29-taipei-rent.md`（status script_ok，10-30/31）對應的是 commit `0e012b4` 的稿。
- 工作區的 narration.md 在 11-01 18:46 又被改過，沒 commit（`git diff films/taipei-rent/narration.md`）：

```diff
-維也納的做法不一樣。
+但維也納的做法剛好相反。
...
-## 收尾
-住的問題，跟每個人都有關。
-一起多關心，讓台灣更好。
```

看起來是 11-01 加兩道新門（轉折段第一句要有轉折連詞、提問後不能再有段）後，有人把稿改成能過門。taipei-childcare 也有一樣的改法。
舊版過不了新門，新版沒經你審，所以兩版都不能直接建。

另外有一個事實問題：「剛好相反」把反方稽核爭點 2 的裁決改回去了。`audit/verdicts.md` 爭點 2 是 CON_WINS：台北的「三間」是住宅戶數，維也納的「六成」是人口，口徑不同，所以 10-30 才把「正好相反」改成「不一樣」。

## 要你決定（建議第 1 個）

1. **轉折第一句改成「但維也納的做法不一樣。」**，收尾段照現在刪掉。「但」有轉折連詞，可以過新門，也守住爭點 2 的裁決。你說通過後跑：
   `python3 scripts/approve.py films/taipei-rent "<你的原話>"`
2. 照現在的「但維也納的做法剛好相反。」核准。要接受口徑不同的對照（反方稽核要重裁爭點 2）。
3. 你自己改稿。

核准後照這個順序跑，不用重做這輪的檔：
humanize 戳記（`audit/humanize.md` 換現稿 sha）→ `scripts/devils.sh films/taipei-rent` 重裁 → `cd films/taipei-rent && bash build.sh` → `scripts/qa_sheet.sh` ＋ `qa/review_log.md` → `scripts/publish/public_path.py`（precheck「公開路徑是隨機 token」要它）→ precheck → `scripts/deliver.sh`。

## 這輪已完成（照核准檔「建片注意」，不用重做）

- `index.html` 依現稿 27 句全部重做，一句一卡。框架照抄 pedestrian-hell 第三版（6cf2cc3）：換卡原地交叉淡化 0.6 秒、不滑入、不交替底色、沒有章名全屏卡、沒有懶人包卡、沒有換卡音效。兩種主張用同一個標籤樣式，兩張「代價」卡同構圖（錢：硬幣變少；時間：時鐘）。不用政黨色。
- `FACTS` 13 項，`meta/facts.md` 重寫，每項都對到 SOURCES 列號。precheck「數字都有來源」OK。
- `mix.py` 從 pedestrian-hell 第三版複製（F 大調溫和配樂、沒有音效、限幅 1.4 倍）。`cast.json`／`pace.json`／`rhythm-profile`（m4、tempo 1.0、calm）照核准檔沒動。
- `TREATMENT.md` 分鏡表照 27 句重寫，動作欄沒有抽象詞。
- 三份說明文字、`title-shorts.txt`、`tags.txt` 已寫，說明文字相關門全部 OK。不寫人名、黨名、「候選人／選舉／政見／市長」。
- 渲染前的三道檢查用暫存目錄的**假時間軸**（每字 0.22 秒估算）跑過：尋幀一致 OK、字幕閱讀時長全 OK（三張短句卡拿掉副標）、藏字檢查沒有 FAIL（卡 14、23 是 WARN）。真時間軸出來後 build.sh 會再跑一次。
- 拼圖自看過：27 張卡都有出圖，沒有 JS 錯誤；「15.4×」標籤原本被右緣裁到，已修。

precheck 現在 24/41；沒過的 17 項都要等核准、建片後才能跑。

## 沒碰的

narration.md（你核過的稿）、SOURCES.md、其他片目錄、核准檔。沒上傳、沒發布、沒 commit。
