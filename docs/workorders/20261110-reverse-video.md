## 任務

工作目錄 REPO_ROOT。照計畫 REPO_ROOT/docs/plans/2026-11-10-reverse-video.md 的「規格」段實作，先讀計畫、scripts/breakdown.py、tests/test_breakdown.py。

### 1. 新增 scripts/reverse.py
重用 breakdown.process 與 breakdown.hook，不改 breakdown.py。Python 用 .venv/bin/python（已裝 mlx-whisper、whisper 模型已快取）。

### 2. 新增 tests/test_reverse.py
照 tests/test_breakdown.py 寫法（純 stdlib、python3 可跑、失敗 exit 1）：測 assign_speech 歸給重疊最多的鏡頭、cjk_per_sec 算法與 seconds≤0 回 0。邏輯改錯要 fail。

writes!: scripts/reverse.py tests/test_reverse.py
regress: for t in tests/test_breakdown.py tests/test_cover_text.py; do python3 "$t" >/dev/null 2>&1; echo "$? $(basename "$t")"; done

## 驗收

```bash
cd REPO_ROOT
python3 tests/test_reverse.py
python3 tests/test_breakdown.py
rm -rf /tmp/rev-acc
.venv/bin/python scripts/reverse.py tests/fixtures/reverse-2shot.mp4 --out /tmp/rev-acc
python3 -c "import json;d=json.load(open('/tmp/rev-acc/reverse.json'));s=d['shots'];assert len(s)==2,s;assert '台灣冷知識' in s[0]['ocr'],s[0];assert '第二鏡頭' in s[1]['ocr'],s[1]"
python3 -c "import json;d=json.load(open('/tmp/rev-acc/reverse.json'));assert d['hook']=='' and all(x['speech']=='' for x in d['shots']),d"
grep -q '^## 觀察到' /tmp/rev-acc/REVERSE.md
grep -q '^## 推斷' /tmp/rev-acc/REVERSE.md
grep -q '^## 未覆蓋' /tmp/rev-acc/REVERSE.md
```

預期：全部 exit 0；reverse.json 兩鏡頭、畫面字各含「台灣冷知識」「第二鏡頭」；REVERSE.md 三段標題都在。

## 禁止

- 禁止改 scripts/breakdown.py、tests/fixtures/、驗收區塊。
- 禁止 pip／uv 安裝新套件；缺套件就停手回報套件名。
- launchctl 一律不碰；無頭機，禁止回報「請使用者手動執行」，卡住就回報阻斷點。
