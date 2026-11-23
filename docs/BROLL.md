# B-roll 接入

1. 搜尋素材：`python scripts/broll.py search <關鍵字>`
2. 抓取並切幀：`python scripts/broll.py fetch <url> --out films/<片>/broll/<名> --license <授權> --credit <作者> --sources films/<片>/SOURCES.md`
3. 複製引擎：`cp assets/broll/broll.mjs films/<片>/broll/broll.mjs`
4. `index.html`：`import { drawBroll } from './broll/broll.mjs'`
5. 在 `async render(t)` 裡：`await drawBroll(ctx, clip, t, { W, H, load })`
6. 出處寫入 `SOURCES.md`（CC BY 必須署名）
7. 本機預覽需 `serve` 掛載片目錄為根
8. clip.json 由 fetch 寫入，含 count/fps/w/h
9. drawBroll 範圍外不畫，不需手動判斷
10. 參考 assets/broll/broll.mjs 與 tests/test_broll.mjs
