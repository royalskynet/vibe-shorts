# 一次複製清單

你在電腦前照這張單走一次，之後權杖我自己續，不用再找你。

**規則先講**：密鑰和授權碼不要貼進對話。複製起來就好，跟我說「複製好了」，我從剪貼簿讀。貼進對話等於外洩，事後換掉也補不回來。

每一項都是「複製 → 跟我說一聲 → 我存檔 → 換下一項」。一次一項，因為剪貼簿只有一格。

---

## 要建三個應用程式

| 平台 | 在哪建 | 要選什麼 |
|---|---|---|
| YouTube | Google Cloud Console | OAuth 用戶端類型選**電視和受限輸入裝置** |
| Instagram | Meta for Developers | 用途**其他** → 類型**商家** → 加 Instagram 產品 |
| Threads | Meta for Developers | 另開一個，用途選 **Threads** |

Threads 要另開一個應用程式。官方文件只寫「建立應用程式並選 Threads 用途」，沒有說現有的 IG 應用程式能加掛。

詳細步驟在 `PUBLISH-SETUP.md`，這張單只是順序和要複製的東西。

---

## 複製順序

六個值，一個一個來。

1. `YT_CLIENT_ID` — Google Cloud 的 OAuth 用戶端編號
2. `YT_CLIENT_SECRET` — 同一個用戶端的密鑰
3. `IG_CLIENT_ID` — **Instagram** 應用程式編號
4. `IG_CLIENT_SECRET` — Instagram 應用程式密鑰
5. `THREADS_CLIENT_ID` — **Threads** 應用程式編號
6. `THREADS_CLIENT_SECRET` — Threads 應用程式密鑰

**第 5、6 項有坑。** Threads 應用程式會給你兩組編號和密鑰。要複製的是「Threads 應用程式編號」那一組，不是「Meta 應用程式編號」那一組。拿錯會在授權那步失敗。

---

## 兩個網址要填

IG 和 Threads 的 **OAuth 重新導向 URI** 都填這一個：

```
https://host.tailnet.ts.net/oauth
```

這是這台機器的 Tailscale 網址，只有你的裝置連得到。授權完瀏覽器會說連不上，那是正常的——授權碼就在網址列裡。

YouTube 不用填，受限輸入裝置流程會直接給你一組代碼。

---

## 兩個邀請要接受

這兩步不做，發片會被拒。

- **Instagram**：應用程式後台 App roles → Roles 把自己加成 Instagram Tester，然後開 instagram.com 網頁版，設定 → 應用程式和網站，接受邀請。
- **Threads**：同樣加成 Threads Tester，然後開 Threads 設定 → 網站權限，接受邀請。

加成 Tester 之後就停在 Standard Access，不需要 App Review，也不需要企業驗證。Meta 的文件寫 Standard Access 就是給「只有應用程式裡有角色的人會用」的應用程式。我們只發自己的帳號，這一級夠。

---

## 三次授權

六個值都存好以後，我印三個授權網址給你。每一個你開、按同意、複製網址列整串，跟我說一聲。

之後每天 05:40 的排程會檢查到期日，剩不到 10 天自動續。續期不需要你。

---

## 公開網址（10-12 已同意並完成，不用再做）

IG 和 Threads 發片時，Meta 是**自己去下載影片檔**，不收上傳，所以影片要先放在公開網址上。YouTube 收檔案上傳，沒這個問題。

做法：Tailscale Funnel 只在 8443 埠開那支 mp4 的隨機路徑，兩平台發布完成就關，30 分鐘逾時自動關。funnel 權限已開通，腳本 `scripts/publish/funnel.py` 已外部驗證過。
