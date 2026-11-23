# 品牌定位（2026-10-13，10-14 改爆款第一）

## 一句話

做爆款。題材不設限（地理、冷知識、社會議題都只是目前證據指向的題型），唯一標準是同題或同型已有爆款證據，且程式畫面做得出來。

2026-10-14 使用者定案：「爆款就好，不管什麼反直覺冷知識或地理，就是為了爆款。」收尾落人生道理、結尾提問是目前的格式假設，數據不支持就換。

## 依據

- 選題：爆款第一（PLAN.md「選題原則」2026-10-14）。題目只從已證實的爆款題型挑，證據記在 `refs/VIRAL-LEDGER.md`；中文地理冷知識頭部中位數 87 萬，防詐 3.4 萬（PLAN.md 同段）。沒有偏好主題。
- 收尾：DECISIONS.md §2（收尾落到人生道理；結尾提問拿到的留言多出幾十倍）。
- 平台分工：DECISIONS.md §1（IG Reels 主場、Threads 冷啟動、YouTube Shorts 第二落點）。
- 受眾：台灣，繁體中文旁白加字幕（VOICE.md）。

## 帳號

- YouTube：品牌帳戶 `UCZkzE-KXwTHZysZmpCfTx_A`，2026-10-13 由「東森精鷹Mil／@sskynet42」改為「悖論小酒館／@paradoxbar」（改名時 0 訂閱、0 影片；API 讀回已確認）。原名「東森精鷹Mil」含台灣媒體公司「東森」字樣，改掉以免被誤認。
- Instagram：沿用既有帳號，2026-10-13 由 `iris96284` 改為「悖論小酒館／@paradoxbar.tw」（`paradoxbar` 已被占用）；舊貼文已刪、轉創作者帳號（類別：數位創作者）、換大頭貼與簡介，公開頁讀回確認。
- 三平台用同一個名稱與同一句簡介。

## 名稱（已定：悖論小酒館 @paradoxbar）

### 當時的候選

YouTube 帳號代碼在 2026-10-13 用 `curl https://www.youtube.com/@<代碼>` 查，404＝沒人用。Threads／IG 不登入查不到，要開帳號時再確認。

| 名稱 | 代碼 | 代碼狀態 |
|---|---|---|
| 反直覺研究所 | `@counterintuitlab` | 404 可用 |
| 悖論小酒館 | `@paradoxbar` | 404 可用 |
| 局部最優 | `@localoptimum.tw` | 404 可用（`@localoptimum` 已被用） |

## 簡介（三平台共用）

> 每支兩分鐘，一個反直覺的冷知識，最後問你一個沒有標準答案的問題。

2026-10-14 前的舊版（10-13 設到平台上的那句）：「每支兩分鐘，一個反直覺的數學或哲學概念，最後問你一個沒有標準答案的問題。」平台上的簡介這次沒改。

## 限制

- YouTube 頻道名稱和帳號代碼各自 14 天內只能改 2 次（[YouTube 說明](https://support.google.com/youtube/answer/2657964)），選定後不要再換。
- 影片標註 AI 生成：上片時設 `status.containsSyntheticMedia`（YouTube Data API）。

## 吉祥物與視覺風格（2026-10-14 定）

**格式：深夜對談**（使用者 2026-10-14 定）。深夜房間的桌前，女主跟 Claude（Clawd Bot）一來一往對話，一句一卡字幕。依據：`refs/VIRAL-LEDGER.md`「人跟 AI 聊天的對話動畫」——夜景公寓、暖光、人＋Claude 吉祥物並肩、一句一卡口語字幕（IG @canwebuildthis 5.43 萬讚、@agentmorphy 5.69 萬讚）。

**畫風：low-poly 3D**（使用者 2026-10-15 改，取代 10-14 的 2D 扁平動漫；理由是爆款三支都是 low-poly 3D，2D 沒有證據）。實作走 three.js 進 lemo-opuscar 既有渲染鏈，材質與後製借內建風格 `lowpoly-island`（`flatShading: true` 無貼圖、GTAO 畫接縫陰影、夜晚只有暖色自發光）；**鏡頭不照它**：`lowpoly-island` 規定正交鏡頭，爆款是透視＋淺景深散景，所以換 `PerspectiveCamera`＋景深。角色用基本幾何組裝，姿態仍須是 `t` 的封閉式（`seek_check.mjs` 尋幀一致）。2D 資產（下面的 svg）保留當造型與色票參考。

兩個角色：

- **女主**：動漫少女（3D 版待建），橘髮（`#D97757` 系）、炭黑連帽衫，女聲旁白就是她。造型 `assets/mascot/host/host-a.svg`（`gen_host.py` 產生；b、c 兩款是當時的候選）。
- **Clawd Bot（智能機械蟹）**：Claude 本人，坐在桌上跟她對話。設計正本 `assets/mascot/clawd-bot/`（來源 `royalskynet/Ether-secrets:vibe-shorts/mascot-clawd-bot`，commit 870b741），不改。

色票：Claude 陶土橘（`#F29172`／`#D97757`／`#BC5C3E`）＋炭黑描邊（`#252422`）＋深色底（`#201F1D`）＋LED 綠金（`#68E399`／`#F6B966`）＋夜空藍（`#0F1424`→`#1E2A44`）。字幕說話者名字用角色色：女主橘、Clawd 綠。新片不再另調 rose／plum／teal。場景定格 `assets/mascot/scene/night.png`（`gen_night.py` 產生，`preview.sh` 不經 GPU 出圖）。

- **待定**：Clawd 的聲音。對話要兩個聲音，現在只有女主的 D 音色（VOICE.md）。
- 片子怎麼接、為什麼不直接用上游的 rig.js：`docs/MASCOT.md`。
- 已完成的 `films/dating-bill`、`films/scam-map` 不回頭改，從下一支片開始採用。
- 平台大頭貼 2026-11-11 起換成 Clawd Bot（使用者點頭，下節）。

## 大頭貼

現行（2026-11-11 起，使用者定）：`assets/brand/avatar-mascot.png`（900px）／`avatar-mascot-800.png`（上傳用）／`avatar-mascot.svg`。Clawd Bot 放大置中，深藍底 `#16233F`、圓形襯底 `#1E2F55`，拿掉地面陰影。不加「Paradox」字樣：頭貼顯示約 32–110px 且被裁成圓形，旁邊的字會糊掉或被裁，帳號名本來就排在頭貼旁。三平台共用同一張；頭貼沒有 API，走專用 Chrome（`scripts/publish/cdp.py launch`）網頁換，11-11 三平台個人頁截圖讀回確認。

舊版（2026-10-13 至 11-10）：`assets/brand/avatar.png`（900px）／`avatar-800.png`（上傳用）／`avatar.svg`。倒置的潘洛斯三角（不可能三角）當馬丁尼杯身：悖論＋酒館。深藍底、琥珀三色。
幾何取自 Wikimedia Commons `Penrose-dreieck.svg`（Tobias R.，Public domain），`gen_avatar.py` 重新上色、翻轉、加杯腳。2026-10-13 已上傳 YouTube，API 讀回縮圖確認。三平台共用同一張。
