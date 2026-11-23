## 任務

工作目錄：`/Users/you/dev/vibe-shorts-pipeline`。做兩件事，不做其他事。

### 1. 改 `films/ai-oversold/index.html`
- 第 29 行 `DIM = '#8C7B6B'` 改成 `DIM = '#6F5F50'`，同一行其他常數不動。
- 第 414 行 `plain(`來源｜${cd.hud}`, 540, 1530, 28, DIM, { align: 'center', w: 500 });` 改成字級 32、字重 600：`plain(`來源｜${cd.hud}`, 540, 1530, 32, DIM, { align: 'center', w: 600 });`
- 第 322 行系列標籤不動。

### 2. 新增 `tests/test_dim_contrast.py`
用標準函式庫寫。讀 `films/ai-oversold/index.html`：
- 用 regex 抓 `DIM = '#xxxxxx'`，算它對奶油底 `#f5efe6` 的 WCAG 相對亮度對比（sRGB 線性化，公式 `(L1+0.05)/(L2+0.05)`），小於 4.5 就失敗。
- 用 regex 抓以 `來源｜` 開頭的 `plain(` 呼叫，取字級（第四個參數），小於 32 就失敗。
- 檔內放一個 `def test_dim_contrast()` 與 `if __name__ == '__main__'` 區塊；失敗印原因並 `sys.exit(1)`。

## 驗收

```bash
cd /Users/you/dev/vibe-shorts-pipeline
f=films/ai-oversold/index.html
cp "$f" /tmp/ai-oversold-index.new.html
sed -i '' "s/DIM = '#6F5F50'/DIM = '#8C7B6B'/" "$f"
if python3 tests/test_dim_contrast.py; then echo "負控制未失敗"; cp /tmp/ai-oversold-index.new.html "$f"; exit 1; fi
cp /tmp/ai-oversold-index.new.html "$f"
python3 tests/test_dim_contrast.py
grep -q "DIM = '#6F5F50'" "$f"
grep -q "32, DIM, { align: 'center', w: 600 }" "$f"
```

預期：負控制那步測試 exit 1 並輸出含 `3.56`，還原後測試 exit 0，兩個 grep 都有命中，整段 exit 0。

## 不動
`films/` 其他資料夾、`assets/illust/`、`scripts/precheck.py`、任何 gate 基準。

## 禁止
1. `launchctl bootout/bootstrap/kickstart` 必帶完整 service target `gui/$(id -u)/<label>`；裸 domain 與 `launchctl reboot` 禁止；載入回 141/125 立即停手回報。本單不涉及 launchd。
2. 無頭機：禁止回報「請使用者手動貼 token／授權／執行指令」；憑證讀不到＝停手回報阻斷點與需要的 key 名。
3. 不 render 影片、不執行 `build.sh`、不 git commit。
