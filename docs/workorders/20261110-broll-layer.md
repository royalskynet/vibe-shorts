## 任務

工作目錄 /Users/51mini/dev/vibe-shorts-pipeline。照計畫 /Users/51mini/dev/vibe-shorts-pipeline/docs/plans/2026-11-10-broll-dedup.md 的「B. 引擎圖層」段實作，先讀計畫、assets/illust/illust.mjs、tests/test_illust.mjs（假 context 寫法）、scripts/illust_install.sh。

### 1. 新增 assets/broll/broll.mjs
ES module，匯出 frameIndex、coverRect、framePath、drawBroll，規格照計畫 B 段。無外部依賴。

### 2. 新增 tests/test_broll.mjs
`node tests/test_broll.mjs` 可跑，失敗 exit 1（node:assert/strict）：
- frameIndex({start:1,fps:30,count:60})：t=0.5→-1、t=1→0、t=1.5→15、t=3→-1。
- coverRect(1920,1080,1080,1920)：h=1920、w≈3413.33、x≈-1166.67、y=0；同比例時回 {0,0,W,H}。
- framePath({dir:'broll/a'},0) === 'broll/a/0001.jpg'。
- drawBroll 用注入的假 load 與記錄型假 ctx：在範圍內呼叫一次 drawImage 且參數等於 coverRect；範圍外不呼叫。

### 3. 新增 docs/BROLL.md
≤30 行：search→fetch→複製 broll.mjs 進片目錄→index.html import 並在 async render(t) 裡 await drawBroll；出處寫 SOURCES.md。

writes!: assets/broll/broll.mjs tests/test_broll.mjs docs/BROLL.md
regress: for t in tests/test_illust.mjs tests/test_mascot_pose.mjs; do node "$t" >/dev/null 2>&1; echo "$? $(basename "$t")"; done

## 驗收

```bash
cd /Users/51mini/dev/vibe-shorts-pipeline
node tests/test_broll.mjs
node -e "import('./assets/broll/broll.mjs').then(m=>{for(const k of ['frameIndex','coverRect','framePath','drawBroll'])if(typeof m[k]!=='function')process.exit(1)})"
grep -q 'drawBroll' docs/BROLL.md
test "$(wc -l < docs/BROLL.md)" -le 30
```

預期：全部 exit 0。

## 禁止

- 禁止改 assets/illust/、films/、驗收區塊。
- 禁止 npm 安裝套件。
- launchctl 一律不碰；無頭機，禁止回報「請使用者手動執行」，卡住就回報阻斷點。
