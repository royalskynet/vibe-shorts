# 三平台發布：電腦前操作手冊

你在電腦前做一次（約 40–60 分鐘），之後權杖由這台機器自己續。

2026-10-12 依官方文件重寫，介面名稱以當天官方文件為準。按鈕名稱跟畫面對不上時，先找意思相近的那個，不要停下來。

---

## 0. 開始前要備好

| 項目 | 確認方式 |
|---|---|
| 一台**電腦**，瀏覽器已登入你要發片的 Google 帳號 | Meta、Google 後台在手機上很難操作 |
| 這台電腦**能把剪貼簿傳給 Mac mini** | 見下方「剪貼簿怎麼過去」 |
| 有一個 Claude session 開著，我能跑指令 | 「跟我說一聲」就是對那個 session 說 |
| IG 帳號已切成**專業帳號**（商業或創作者都可以） | IG App → 設定 → 帳號類型和工具 |
| Threads 帳號跟那個 IG 綁同一個人 | 有 Threads 帳號就行 |
| Facebook 帳號能登入 Meta for Developers | 第一次用會要求註冊成開發者，要驗證手機 |

### 剪貼簿怎麼過去

`tokens.py save` 讀的是 **Mac mini 的剪貼簿**（`pbpaste`），讀不到你手上那台裝置的剪貼簿。兩個做法擇一：

- **直接在 Mac mini 上操作**（螢幕共享或接螢幕）：複製就在 Mac mini 本機，最穩。
- **用同 Apple ID 的 Mac 或 iPhone**，開「接力」和藍牙，人在 Mac mini 附近：通用剪貼簿會同步過去。每次複製完等 2–3 秒再說「複製好了」。

我讀到之後只印字元數，不印值。字元數不對，我會叫你重複製。

### 規則：憑證不進對話

用戶端密鑰、授權碼、授權後的網址列都是憑證。一律複製，跟我說「複製好了」。**不要貼進對話**，貼進來就等於外洩，事後輪替也補不回來。

---

## 1. YouTube（約 15 分鐘）

### 1-1 建專案、開 API

1. 開 <https://console.cloud.google.com>，右上帳號確認是要發片的那個 Google 帳號。
2. 頂部專案選單 → **新增專案**，名稱填 `vibe-shorts`，建立，然後切換到這個專案。
3. 開 <https://console.cloud.google.com/apis/library/youtube.googleapis.com>，按**啟用**（YouTube Data API v3）。

### 1-2 Google Auth Platform

4. 開 <https://console.cloud.google.com/auth/overview>，有「開始使用」就按。
5. **Audience（目標對象）**：使用者類型選**外部**，儲存。
6. **Branding（品牌宣傳）**：應用程式名稱 `vibe-shorts`，支援電子郵件和開發人員聯絡資訊都填你的信箱，儲存。不用填網域和 logo。
7. **Audience → 測試使用者**：新增你自己的 Gmail。

### 1-3 建用戶端

8. 開 <https://console.cloud.google.com/auth/clients> → **建立用戶端**。
9. 應用程式類型選**電視和受限輸入裝置**，名稱 `vibe-shorts-mini`，建立。

   一定要選這個類型。它走裝置代碼流程，不需要重新導向網址，這台機器不用對外開任何埠。

10. 彈窗裡複製**用戶端 ID** → 跟我說「複製好了」→ 我跑 `tokens.py save YT_CLIENT_ID`。
11. 複製**用戶端密鑰** → 跟我說 → 我跑 `tokens.py save YT_CLIENT_SECRET`。

    彈窗關掉後密鑰可能不再完整顯示。沒複製到，就在用戶端頁面新增一組密鑰。

### 1-4 授權

12. 我跑 `tokens.py login yt`，印出網址（`google.com/device`）和一組代碼。
13. 你開網址、輸入代碼、選帳號。會看到「Google 尚未驗證這個應用程式」→ 按**進階** → **前往 vibe-shorts（不安全）** → 允許。這是你自己的應用程式，這個警告是正常的。
14. 我這邊顯示「YouTube 授權完成」就結束。這一步手機也可以做。

### 1-5 發布成正式版（不做的話七天後失效）

15. 回 **Audience** → 發布狀態按**發布應用程式**，確認。

    原因：應用程式在「測試」狀態時，Google 發的 refresh token **7 天就過期**（官方原文寫明）。切成「正式版」後就沒有這個限制。我們只授權你自己的帳號，不需要送驗證。代價是授權畫面會一直顯示「未驗證」警告。

    **還沒實證**：切成正式版之後，Google 有可能因為 `youtube` 屬於敏感範圍而要求送驗證。真的被擋的話，退路是停留在測試狀態，每 7 天重做一次第 12–14 步。

16. 發布後我再跑一次 `tokens.py login yt`。測試狀態下拿到的 refresh token 還是只有 7 天效期，要重拿一次。

**這段的產出**：`YT_CLIENT_ID`、`YT_CLIENT_SECRET`、`YT_REFRESH_TOKEN`（第 16 步自動產生）。

---

## 2. Instagram（約 15 分鐘）

### 2-1 建應用程式

1. 開 <https://developers.facebook.com/apps> → **建立應用程式**。
2. 應用程式名稱填 `vibe-shorts-ig`，聯絡信箱填你的。
3. 使用案例選**管理 Instagram 上的訊息和內容**（Manage messaging & content on Instagram）。
4. 問要不要連結商家管理組合（business portfolio）時，選**暫時不連結**。
5. 一路下一步到建立完成。

### 2-2 商家登入設定

6. 左側 **Instagram → API setup with Instagram login**（或在使用案例裡按「自訂」）。
7. 找到 **3. Set up Instagram business login** → **Business login settings**。
8. **OAuth redirect URIs** 填這一行，儲存：

   ```
   https://host.tailnet.ts.net/oauth
   ```

   儲存後回頭看一眼。後台有時會自動在尾巴加 `/`，有加的話跟我說，我這邊要存成一模一樣的。

9. 同一頁複製**Instagram App ID** → 跟我說 → `tokens.py save IG_CLIENT_ID`。
10. 複製**Instagram App Secret** → 跟我說 → `tokens.py save IG_CLIENT_SECRET`。

    同一個應用程式還有另一組「應用程式編號」（在 設定 → 基本資料）。**不要拿那組**，要拿 Instagram 登入設定頁上的這組。

11. 把上面那行重新導向網址也複製一次 → 跟我說 → `tokens.py save IG_REDIRECT_URI`。

    `tokens.py` 換授權碼時要帶這個值，而且要跟後台一字不差。它不是機密，但目前程式從憑證檔讀它，所以一樣走剪貼簿。

### 2-3 把自己加成測試者，並接受邀請

12. 左側 **App roles → Roles** → **Add People** → 選 **Instagram Tester** → 輸入你的 IG 帳號名稱。
13. 開 <https://www.instagram.com/accounts/manage_access/>（設定 → 應用程式和網站 → **測試人員邀請**）→ 接受。

    沒接受邀請，授權會失敗。

### 2-4 授權

14. 我跑 `tokens.py login ig`，印出授權網址。
15. 你在**同一台能傳剪貼簿的裝置**上開它，登入 IG，按允許。
16. 瀏覽器跳到 `…ts.net/oauth?code=…`，頁面顯示連不上。**這是正常的**。
17. 複製**網址列整串** → 跟我說 → 我讀剪貼簿，換成 60 天的長期權杖。

    授權碼 **1 小時內有效，只能用一次**。第 16 步之後不要拖。失敗了就從第 14 步重來。

**這段的產出**：`IG_CLIENT_ID`、`IG_CLIENT_SECRET`、`IG_REDIRECT_URI`、`IG_ACCESS_TOKEN`（60 天，自動續）。

---

## 3. Threads（約 10 分鐘）

### 3-1 建應用程式

1. 回 <https://developers.facebook.com/apps> → **建立應用程式**，**另開一個**，名稱 `vibe-shorts-threads`。
2. 使用案例選 **Access the Threads API**（存取 Threads API）。商家管理組合一樣選暫時不連結。

   不要掛在 IG 那個應用程式上。官方文件只寫「建立應用程式時選 Threads 使用案例」。

### 3-2 權限與網址

3. 左側**使用案例** → 點 Threads 那個 → 權限清單裡 `threads_basic`、`threads_content_publish` 旁邊按**新增**。
4. 左側**設定**（Threads 使用案例的設定頁）：
   - **重新導向回呼網址**（Client OAuth Settings）填同一行 `https://host.tailnet.ts.net/oauth`。
   - **解除授權回呼網址**、**資料刪除要求網址**：沒填不給儲存的話，兩格都填同一行網址。
   - 按**儲存**。
5. 同一頁有 **Threads app ID** 和 **Threads app secret**。
   - 複製 Threads app ID → 跟我說 → `tokens.py save THREADS_CLIENT_ID`
   - 複製 Threads app secret → 跟我說 → `tokens.py save THREADS_CLIENT_SECRET`

   **坑**：這個應用程式有**兩組**編號和密鑰。拿 Meta 的那組（在 應用程式設定 → 基本資料），授權那一步會失敗。

6. 重新導向網址複製一次 → 跟我說 → `tokens.py save THREADS_REDIRECT_URI`。

### 3-3 測試者

7. 設定頁按 **Add or Remove Threads Test Users** → **Add People** → **Threads Tester** → 輸入你的 Threads 帳號。
8. 開 Threads（網頁版或 App）→ **設定 → 帳號 → 網站權限 → 邀請** → 接受。

### 3-4 授權

9. 我跑 `tokens.py login threads`，後面跟 Instagram 的第 15–17 步一樣。

**這段的產出**：`THREADS_CLIENT_ID`、`THREADS_CLIENT_SECRET`、`THREADS_REDIRECT_URI`、`THREADS_ACCESS_TOKEN`（60 天，自動續）。

---

## 4. 收尾驗收

我跑 `tokens.py status`，三行都要是「已登入」（日期是示意）：

```
  yt       已登入  refresh token 長期有效，上次換新 2026-10-xx
  ig       已登入  還有 59 天（2026-12-xx）
  threads  已登入  還有 59 天（2026-12-xx）
```

再跑一次 `tokens.py refresh`。yt 要顯示「已換新」，證明 refresh token 真的能用。ig 和 threads 顯示「還有 N 天，不動」是正常的，Meta 的權杖要滿 24 小時才能續。

**全部產出一覽**（都在 `~/.creds/kv/`，一個檔一個值，權限 600）：

| 你複製的（8 個） | 機器自己產生的（4 個） |
|---|---|
| `YT_CLIENT_ID`、`YT_CLIENT_SECRET` | `YT_REFRESH_TOKEN`、`YT_ACCESS_TOKEN` |
| `IG_CLIENT_ID`、`IG_CLIENT_SECRET`、`IG_REDIRECT_URI` | `IG_ACCESS_TOKEN` |
| `THREADS_CLIENT_ID`、`THREADS_CLIENT_SECRET`、`THREADS_REDIRECT_URI` | `THREADS_ACCESS_TOKEN` |

後台另外要留在這個狀態：Google 應用程式是「正式版」；IG 和 Threads 的測試者邀請都已接受。

---

## App Review：不用（2026-10-11 查證）

Meta 把權限分兩級。**Standard Access** 給「只有應用程式裡有角色的人會用」的應用程式，不需要 App Review，也不需要企業驗證。要發到別人的帳號才需要 Advanced Access。我們只發自己的帳號，Standard Access 就夠。

關鍵動作是**把自己加成 Tester，而且去接受邀請**。沒接受，權限不會生效。

## 已知風險

- **端點沒實際跑過。** 三個平台的端點是照官方文件寫的。跑錯會把平台的原始錯誤訊息整段印出來，不會假裝成功。
- **Threads 網域。** 官方文件現在寫 `threads.com/oauth/authorize`，`tokens.py` 用的是 `threads.net`。舊網域應該會轉址過去。授權頁打不開的話，先改這裡。
- **YouTube 上片不再強制私人。** 官方文件現行寫法是「未驗證 API 專案上傳的影片不再限制為私人」。2020 年起的那條限制已經拿掉。

## 影片的公開網址（10-12 已解決）

IG 和 Threads 發片時，Meta 自己去下載影片檔，不收上傳。做法是 Tailscale Funnel 只在 8443 埠開那支 mp4 的隨機路徑，發完就關，30 分鐘逾時自動關。腳本是 `scripts/publish/funnel.py`，已外部驗證。YouTube 收檔案上傳，沒這個問題。

## 之後怎麼看狀態

```
tokens.py status
```

排程每天 05:40 跑 `tokens.py refresh`，紀錄在 `logs/token-refresh.log`。
