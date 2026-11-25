# Handoff：接上 Threads 刪除權限，清掉轉貼

交接日期 2026-10-13。寫給另一個已經處理過 Threads 登入的 session。
你要做的只有「拿到一個含 `threads_delete` 的權杖」，工具端已經寫好並驗證過。

## 一、我這邊已經完成的（不用重做）

- 新檔 `/Users/51mini/dev/vibe-shorts-pipeline/scripts/publish/social.py`
  三平台統一 CLI，複用既有 `tokens.py` 的憑證與續期，只用標準函式庫。
- 改 `/Users/51mini/dev/vibe-shorts-pipeline/scripts/publish/tokens.py`
  `META["threads"]["scope"]` 加上 `threads_delete`（原本只有 `threads_basic,threads_content_publish`）。
- 新檔 `/Users/51mini/dev/vibe-shorts-pipeline/tests/test_social.py`
  11 項全過，且做過變異測試（把轉貼篩選反掉、把 IG 改成可刪，兩次都如期 exit=1）。
- 實測過 `list yt`（真的回一筆私人影片）、`list ig`（0 筆）、`delete ig`（如期被擋 exit=1）。

查證結論，別再查一遍：

- Threads 刪貼文 `DELETE https://graph.threads.net/v1.0/{media_id}?access_token=`，
  要 `threads_basic` + `threads_delete`，官方上限 **100 刪/天/帳號**。
- 轉貼在 `GET /v1.0/me/threads` 裡的 `media_type` 是 `REPOST_FACADE`。
- **官方文件沒有寫 `REPOST_FACADE` 能不能 DELETE**，reposts 頁也沒有 unrepost 端點。
  所以第一次一定要先刪一筆試，不要直接批次跑。
- IG 在我們這條路（Instagram Login / `graph.instagram.com`）**不能刪媒體**。
  官方 media reference 的 DELETE 區塊寫「This api only supports Instagram API with
  Facebook login only」，要 `graph.facebook.com` + `instagram_manage_contents`。
  `social.py` 已經在送出請求前就擋掉，不要試圖繞過。

## 二、現況：本機沒有 Threads 權杖

```
$ python3 /Users/51mini/dev/vibe-shorts-pipeline/scripts/publish/tokens.py status
  yt       已登入  refresh token 長期有效，上次換新 2026-10-13
  ig       已登入  還有 59 天（2026-12-12）
  threads  未登入  —
```

`creds has THREADS_ACCESS_TOKEN` 回 `no`（注意：`creds has` 永遠 rc=0，要讀 stdout
不要看 exit code）。`THREADS_CLIENT_ID`／`CLIENT_SECRET`／`REDIRECT_URI` 三個都在。

所以你那邊的「已登入」是下面哪一種，先確認：

1. 在 M2 或別台機器登入的 → 權杖在那台的 `~/.creds/kv/`，這台用不到。
2. 用別的工具（瀏覽器 session、別的腳本）登入的 → 不是 `tokens.py` 的權杖。
3. 剛登入還沒寫檔 → 重跑一次 `tokens.py login threads` 即可。

**不管是哪一種都要重新授權一次**，因為 `threads_delete` 這個 scope 是今天才加進
`tokens.py` 的，你手上那個權杖不可能含它。

## 三、你要做的三步

### 第 1 步：Meta App Dashboard 加權限

到 Threads app 的 use case 設定裡把 `threads_delete` 加進去。
沒加就授權，`threads.net/oauth/authorize` 會直接回 invalid scope。

驗收：授權網址開得起來、同意畫面上看得到刪除相關的項目。

### 第 2 步：授權

```bash
python3 /Users/51mini/dev/vibe-shorts-pipeline/scripts/publish/tokens.py login threads
```

它會印一個授權網址，開完同意後瀏覽器會跳到一個連不上的頁面（正常）。
把網址列整串複製，腳本從**剪貼簿**讀授權碼。
授權碼是憑證值，不要貼進對話。

驗收（兩條都要過）：

```bash
python3 .../tokens.py status | grep threads    # 要顯示「已登入」加剩餘天數
python3 .../tokens.py whoami threads           # 確認是對的帳號，不是別的
```

### 第 3 步：先刪一筆試，再批次

```bash
cd /Users/51mini/dev/vibe-shorts-pipeline
# 先看有幾筆轉貼（唯讀，不會動任何東西）
python3 scripts/publish/social.py list threads --type repost --limit 100
# 挑清單裡第一筆的 ID，單筆試刪（這一步不可逆）
python3 scripts/publish/social.py delete threads <那個ID> --yes
# 成功就批次；不帶 --yes 只會印出會刪哪些
python3 scripts/publish/social.py prune threads --reposts --limit 50 --yes
```

超過 100 筆的話 `prune` 會直接擋下來叫你分天跑，這是平台的每日上限不是程式限制。

## 四、單筆試刪失敗的話

如果 `DELETE` 對 `REPOST_FACADE` 回 400 或權限錯誤，那就是平台不給刪轉貼。
把原始錯誤訊息整段貼回來，**不要改程式去繞**，也不要去裝那些逆向的
`threads-api`（junhoyeo、Danie1 都已 archived，逆向私有 API 有封號風險）。
那種情況下轉貼只能在 App 裡手動取消，請回報結論並跑 `/fi` 記一筆。

## 五、做完回報

一行結論：清掉幾筆轉貼、剩幾筆、單筆試刪的原始回應是什麼。
決策紀錄已經在 `~/.wheel/registry.tsv`（2026-10-13 那一筆），不用再登記。
