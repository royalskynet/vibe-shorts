# Clawd Bot — 片子裡怎麼用

常駐吉祥物／主持人：智能機械蟹 Clawd Bot。設計正本（色票、座標、狀態機公式）在 `assets/mascot/clawd-bot/README.md`，2026-10-14 由使用者交付，來源 `royalskynet/Ether-secrets:vibe-shorts/mascot-clawd-bot`（commit 870b741）。

## 檔案分工

| 檔案 | 角色 | 可不可以改 |
|---|---|---|
| `assets/mascot/clawd-bot/*`（README、svg、rig.js、preview.html） | 設計正本，上游交付原樣 | 不改。要改先改上游 repo 再同步 |
| `assets/mascot/clawd-bot-shot.mjs` | 影片用的決定性姿態層 | 這裡改 |
| `assets/mascot/index.html` | lookdev 測試台（`core/render/video.mjs` 可直接渲） | 這裡改 |
| `films/<名稱>/mascot/*` | 片子自己的副本，由 `scripts/mascot_install.sh` 複製 | 不手改，改正本再重裝 |

## 為什麼不直接用上游的 `clawd-bot-rig.js`

`rig.js` 的 `smoothLook` 與 `pokeAmount` 是「每呼叫一次就乘一次」的累積狀態。`core/render/video.mjs` 會開多個 worker、各自從不同的起始 frame 往下渲，片子還會在 `window.READY` 前預熱幾幀，累積狀態在這種呼叫順序下會漂 → 同一個 `t` 兩次渲出不同畫面，`scripts/seek_check.mjs`（尋幀一致）會擋下來。

`clawd-bot-shot.mjs` 把同樣的公式改寫成 `t` 的封閉式：視線阻尼用 `(1-0.12)^(Δt*fps)`、poke 用 `0.88^(Δt*fps)`，動作與座標一字不改照 README §4。`tests/test_mascot_pose.mjs` 驗兩件事：亂序呼叫同 `t` 得同 pose、封閉式與原本逐幀迭代的結果一致（誤差 < 1e-6）。

## 接進一支片

```bash
bash scripts/mascot_install.sh films/<名稱>
```

片子的 `index.html`（canvas 之外再疊一層 DOM SVG，`page.screenshot` 截整頁，兩層都會進畫面）：

```html
<div id="stage" style="position:relative;width:1080px;height:1920px">
  <canvas id="c" width="1080" height="1920" style="position:absolute;left:0;top:0"></canvas>
  <div id="mascot" style="position:absolute;left:0;top:0;width:1080px;height:1920px"></div>
</div>
<script type="module">
import { poseAt, applyPose } from './mascot/clawd-bot-shot.mjs';
const track = {
  fps: 30,
  states: [{ t: 0, state: 'idle' }, { t: 12.4, state: 'thinking' }, { t: 95, state: 'happy' }],
  looks: [{ t: 0, x: 0, y: 0 }, { t: 30, x: 0.6, y: -0.3 }],
  pokes: [],
};
const root = /* fetch('./mascot/clawd-bot.svg') 注進 #mascot，取不到就 throw */;
// 片子原本的 render(t) 最後加一行：
applyPose(root, poseAt(t, track));
</script>
```

規矩：

- **`track` 的時間點對齊 `timeline.js` 的句子起點**，不要另外寫一套秒數。`thinking` 配數據段、`happy` 配結論、`sleep` 只給「壞掉／沒救」那種語意，別亂切。
- **狀態一句話最多切一次**。四個狀態的速度倍率差到 2.8 倍，切太密在 9:16 小畫面上只會看起來在抽動。
- **SVG 取不到要 throw**，不要默默出一支沒有主持人的片（`page.mjs` 只對 script／document 的 404 致命，`fetch` 的 404 只警告一行）。
- **不要放大到超過 800×800**：描邊寬度是為 240 單位的 viewBox 調的，再大線條會顯得空。
- 吉祥物層在 DOM、不在 canvas：`scripts/textless_check.mjs`（藏字檢查）與 `scripts/seek_check.mjs` 都看整頁截圖，所以兩個檢查都照常涵蓋它。`happy` / `sleep` 的特效用的是 `✨ ♥ Z` 這類字元，第一支用吉祥物的片要看一次 `out/textless/` 的樣張確認沒被當成字幕。

## 色票（給片子的 canvas 用同一套）

| 用途 | 色碼 |
|---|---|
| 機甲亮部／標題 | `#F29172` |
| 機甲主色（Claude 陶土橘） | `#D97757` |
| 機甲暗部 | `#BC5C3E` |
| 描邊／四足 | `#252422` |
| 面罩底／全片底色 | `#201F1D`（內框 `#3A3632`） |
| 天線星芒／思考態 | `#F6B966` |
| LED 正常／開心 | `#68E399` |
| LED 腮紅 | `#FF856D` |
| LED 休眠／錯誤 | `#FF8577` |

## 看樣片

```bash
node $LIB/core/render/video.mjs assets/mascot --fps 30 --size 1080x1920 --workers 2 --out assets/mascot/out/lookdev.mp4
```

八秒，`idle → thinking → happy → sleep` 各兩秒，含一次 `poke` 果凍縮放與視線追蹤。
