# 最小逆向腳本 scripts/reverse.py（2026-11-10）

## 為什麼

HyperFrames 的 `/reverse-any-video` 是付費層，CLI 只是打 HeyGen 雲端 `api2…/v1/hyperframes/reverse/start`，fork 拿不到（wheel 卡 2026-11-10）。
本 repo 的 ② 拆解 `scripts/breakdown.py` 已有：下載、video-shots 切鏡、拼圖、mlx_whisper 逐字稿、前 3 秒鉤子。
缺：任意單支網址／本機檔入口、每鏡頭畫面字（OCR）、每鏡頭對到的口播、結構化輸出。

## 借鏡 wheel 逆向軸（REA 做法）

- 證據包整包落檔（`<out>/`：ref.mp4、shots/、transcript.json、evidence/frames/、reverse.json）。
- 只帶摘要回來：stdout 只印 REVERSE.md 路徑＋一行統計。
- 摘要固定三段：`## 觀察到`（量得到的事實）／`## 推斷`（由事實推的格式結論）／`## 未覆蓋`（沒量的東西，明列）。

## 規格

`.venv/bin/python scripts/reverse.py <YouTube 網址或本機 mp4> [--out <目錄>]`

1. 輸出目錄預設 `refs/rev-<影片 ID 或檔名主幹>`。本機檔先複製成 `<out>/ref.mp4`，再呼叫 `breakdown.process(d, 輸入)`（ref.mp4 已在就不下載）。
2. 每鏡頭取中點幀 `(start+end)/2` → `evidence/frames/<id>.png`（ffmpeg）。
3. OCR：`tesseract <png> - -l chi_tra+eng --psm 11`（參數同 precheck.py；預設 psm 對影片幀回 Empty page，11-10 實測）。只留中文字與數字，去空白。
4. 純函式（測試對象）：
   - `assign_speech(shots, segments)`：每個逐字稿段落歸給重疊秒數最多的鏡頭，回 `{shot_id: 文字}`。
   - `cjk_per_sec(text, seconds)`：中文字數／秒，seconds≤0 回 0。
5. 寫 `reverse.json`：`{source, duration, hook, shots:[{id,start,end,seconds,motion,ocr,speech}]}`。
6. 寫 `REVERSE.md`：三段標題（見上），觀察到含鏡頭表（id／秒數／畫面字／口播）；推斷含平均鏡長、整片字／秒、有畫面字的鏡頭比例；未覆蓋固定列：畫面元素與版面（看 shots/sheets 拼圖）、運鏡、配樂音效、可編輯專案重建、逐幀比對。

ponytail：零 token，不接視覺模型；之後要升級就在 `evidence/frames/*.png` 上加視覺描述一步、輸出寫進同一份 reverse.json。

## 驗收素材

`tests/fixtures/reverse-2shot.mp4`：4 秒 540×960，0–2 秒紅底「台灣冷知識」、2–4 秒藍底「第二鏡頭」，無聲。11-10 實測 video-shots 切成 S01 0–2／S02 2–4，psm 11 OCR 兩張都認得。

## 工單

`/Users/51mini/dev/vibe-shorts-pipeline/docs/workorders/20261110-reverse-video.md`
