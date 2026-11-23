# Handoff：跑通三平台發布全鏈路

交接日期 2026-10-13。接手先跑「零、驗證現況」，數字對不上就以實測為準。

**10-14 起流程改為對標驅動九段，正本在 `PLAN.md`「流程」表；下一步照 `PLAN.md`「下一步（2026-10-14 定案）」第 1 步做。**

## 零、驗證現況（唯讀，不會動任何東西）

```bash
cd /Users/you/dev/vibe-shorts-pipeline
python3 scripts/publish/tokens.py status        # yt/ig/threads 三個都要「已登入」
python3 scripts/publish/tokens.py whoami threads # 要是 paradoxbar.tw
python3 scripts/publish/social.py list yt        # 10-13 起 2I__EhCB2U0 費馬為 PUBLIC
cat films/flt-11days/meta/published.json         # ig／threads 已發的網址
ls films/flt-11days/dist/                        # shorts／reels／threads 三支 mp4
python3 scripts/publish/funnel.py status
```

## 一、已完成

- 成片：`films/flt-11days/dist/flt-11days-{shorts,reels,threads}.mp4`，閘門 24/24 過。
- **第一支片三平台已公開（2026-10-13 22:30）**，說明文字都補了結尾提問：
  - YouTube：`https://youtube.com/shorts/2I__EhCB2U0`（嵌入關閉，oembed 會回 401，不是沒公開）
  - IG：`https://www.instagram.com/reel/DecBpufjF8l/`
  - Threads：`https://www.threads.com/@paradoxbar.tw/post/DecBltXgYyf`
- 授權（權杖都在 `~/.creds/kv`，由 `tokens.py` 管理與續期）：
  - yt：refresh token 長期有效。
  - ig：到 2026-12-12。
  - threads：到 2026-12-12，scope 有 basic、content_publish、delete、read_replies。
- Meta 後台 app `paradoxbar-threads`（編號 1420971479569949）：三個回呼網址都已填，`@paradoxbar.tw` 是已接受的 Threads 測試人員。
- 公開網址：`funnel.py up|down|status` 在 10000 埠 TCP 直通、TLS 自己做，只放行 `/<token>/<檔名>`，已經公開 IP 驗證並實際發片成功。
- Threads 帳號清理：見 `docs/STATUS-threads-cleanup.md`。

## 二、還沒有的（要做的）

1. ~~IG／Threads 發片腳本~~ 10-13 完成：`scripts/publish/meta_publish.py`（兩平台共用一次 funnel，
   whoami 必須是 paradoxbar.tw，`meta/published.json` 防重發，不帶 `--yes` 只印計畫）。
   自檢 `tests/test_meta_publish.py`。10-13 真發成功。
2. ~~container 端點實打~~ 10-13 完成。失敗三次才通，原因與修法見 fix 10518（公開 DNS 延遲、
   交付檔 yuvj420p／edit list、tailscaled --https 壞掉改 TCP 直通）。Meta 抓檔沒用 Range。
3. ~~YouTube 轉公開~~ 10-13 完成，`yt_upload.py public films/<片> <影片ID>` 會一併更新標題說明。
4. 10-13 發現選題排程 `com.host.vibe-trends` 從沒裝進 LaunchAgents（10-11 後沒跑過），已補裝；
   Reddit RSS 配額降到每 60 秒 1 次，已修（fix 10517）。

## 三、必須先問使用者的（對外公開，不可逆）

公開發布前，用一句話確認「哪一支片、哪幾個平台、文案」。
建議先用 YT PRIVATE 那支確認畫面沒問題，IG／Threads 只能公開發，沒有私人模式。

## 四、已知的坑（別再踩）

- Funnel 用 `--tcp=10000` 直通。不要改回 `--https`：本機 tailscaled 的 HTTPS 終結 10-13 壞掉（連 tailnet 443 的 4177 也 reset），沒有 sudo 重啟不了。**禁用 `tailscale funnel reset`**，它會把 443 埠的 4177 serve 一起清掉。
- 驗公開網址用 M2：`m2ssh "curl --resolve <host>:10000:<公開IP> ..."`；本機 MagicDNS 永遠解得到，不代表外部解得到。
- 交付檔要 yuv420p 標準範圍、無 edit list，`deliver.sh` 已處理；precheck 有結尾提問門。
- Threads `/me/replies` 帶 `limit=100` 會回 500。Graph API 不要隨手調大 limit。
- 授權碼、權杖不進對話。`tokens.py login` 可以從 stdin 讀回呼網址。授權頁用 `cdp.py` 開 Chrome，再從 `Page.getNavigationHistory` 取回呼網址（回呼頁本身會連線失敗，這是正常的）。
- IG 走 Instagram Login，**不能刪媒體**（見 `social.py caps`）。
- 遇到阻礙先跑 `/wheel` 查官方文件、社群經驗、現成工具，不要直接自造。舊卡在 `~/.wheel/registry.tsv`（10-12 funnel 卡、10-13 social 卡）。

## 五、下一步

- 看 24–48 小時數據（留言數驗證結尾提問有沒有效），再做第二支片。

## 10-14 進度與下一步（對標→拆解→寫稿→配音）

已完成：
- 故事閘門（precheck 旁白稿結構／旁白進成片，`eafd839`，fix 10519）。費馬片 do-nothing 對照 FAIL；有旁白的片還沒有任何一支實際過門，0.85 門檻未校準。
- 對標清單 `scripts/benchmarks.py`＋`refs/BENCHMARKS.md`（`a3d55a3`）。結論：流量第一是知識冷知識格式（四處觀察中位數 87 萬、cheap 50 萬、四方異聞 44.5 萬且訂閱僅 4.7 萬），AI／區塊鏈／防詐帳號中位數都 ≤7.8 萬。
- 第一支 local-optimum 已刪（`d83d824`）。

輪子卡（10-14）：查流量改用 YouTube Data API `search.list order=viewCount videoDuration=short publishedAfter=90天`（既有 youtube OAuth，實測可用，search 100 units／日上限 10k），加中文比例過濾；離群值＝單支÷頻道中位數。

下一步（依序）：
1. benchmarks.py 的發現階段改走 search.list（取代 yt-dlp 相關度搜尋），補 AI 類大帳號；加離群值欄。
2. 拆前三名（四處觀察、四方異聞、cheap）各 3 支最高播放：video-shots＋mlx_whisper 逐字稿，確認格式與鉤子（目前「地圖動畫格式」只是從片名推測）。
3. 第二支片用該格式＋偏好主題（AI→區塊鏈→金融／防詐／台灣）寫 narration.md，過旁白稿結構門。
4. Qwen3-TTS 配音接進 mix.py，narration_check＋precheck 全過才發。
