#!/usr/bin/env python3
"""三平台發布權杖：一次登入，之後自動續期。

只用標準函式庫。三個平台的續期各自只是一個 HTTP 端點，不值得為它裝套件；
真正麻煩的分段上傳到實際發片時才需要，那時再決定要不要引入 google-api-python-client。

  tokens.py status              看三個平台的權杖還有多久
  tokens.py login yt            YouTube 走裝置流程（手機或電腦都能授權）
  tokens.py login ig            Instagram：印出授權網址，把跳轉後的網址貼回來
  tokens.py login threads       Threads：同上
  tokens.py refresh             續期全部（launchd 每天跑，零 token）
  tokens.py whoami ig|threads   權杖對應哪個帳號（發片前確認）
  tokens.py save <NAME>         把剪貼簿的內容存成憑證（值不會印出來）

憑證一律走剪貼簿進來，不要貼進對話。用戶端密鑰和授權碼都是憑證值，
進了對話就等於外洩，事後輪替也補不回來。

憑證值寫在 ~/.creds/kv/<NAME>.txt，一個檔一個值，chmod 600。
到期時間這類非機密的狀態寫在 ~/.vibe-publish/state.json。
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

CREDS = os.environ.get("VIBE_CREDS_DIR") or os.path.expanduser("~/.creds/kv")
STATE = os.environ.get("VIBE_STATE") or os.path.expanduser("~/.vibe-publish/state.json")

# Meta 的長期權杖是 60 天。提前 10 天續，留足夠的失敗重試空間。
META_TTL = 60 * 86400
RENEW_AHEAD = 10 * 86400
# Google OAuth 同意畫面在 Testing＋External 時，refresh token 7 天過期。
YT_TESTING_TTL = 7 * 86400

PLATFORMS = ("yt", "ig", "threads")


# ---------- 憑證存取 ----------

def read(name):
    p = os.path.join(CREDS, f"{name}.txt")
    if not os.path.exists(p):
        return None
    with open(p) as f:
        v = f.read().strip()
    return v or None


def write(name, value):
    os.makedirs(CREDS, exist_ok=True)
    p = os.path.join(CREDS, f"{name}.txt")
    with open(p, "w") as f:
        f.write(value)
    os.chmod(p, 0o600)


def state_load():
    try:
        with open(STATE) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def state_save(d):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    tmp = STATE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(d, f, indent=2, sort_keys=True)
    os.replace(tmp, STATE)


def state_set(platform, **kv):
    s = state_load()
    s.setdefault(platform, {}).update(kv)
    state_save(s)


# ---------- HTTP ----------

def http(url, data=None, method=None):
    """回傳解析後的 JSON。失敗時把平台的原始錯誤訊息一起丟出來，不要吞掉。"""
    body = urllib.parse.urlencode(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method or ("POST" if body else "GET"))
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        raise RuntimeError(f"HTTP {e.code} {url.split('?')[0]}\n{raw}") from None


# ---------- YouTube ----------
# 裝置流程。授權的人不必跟這台機器在同一個地方，手機開 google.com/device 輸入代碼就行。
# 裝置流程只開放 youtube 這個大範圍（youtube.upload 不在允許清單），而 videos.insert 接受它。

YT_SCOPE = "https://www.googleapis.com/auth/youtube"


def yt_login():
    cid, secret = read("YT_CLIENT_ID"), read("YT_CLIENT_SECRET")
    if not cid or not secret:
        die("缺 YT_CLIENT_ID 或 YT_CLIENT_SECRET。先在 Google Cloud Console 建一個"
            "「電視與有限輸入裝置」類型的 OAuth 用戶端，見 docs/PUBLISH-SETUP.md")

    d = http("https://oauth2.googleapis.com/device/code",
             {"client_id": cid, "scope": YT_SCOPE})
    print(f"\n  開這個網址：{d['verification_url']}")
    print(f"  輸入這組代碼：{d['user_code']}")
    print(f"\n  （{d['expires_in'] // 60} 分鐘內有效，我在這裡等你完成）\n", flush=True)

    interval = d.get("interval", 5)
    deadline = time.time() + d["expires_in"]
    while time.time() < deadline:
        time.sleep(interval)
        try:
            t = http("https://oauth2.googleapis.com/token", {
                "client_id": cid, "client_secret": secret,
                "device_code": d["device_code"],
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            })
        except RuntimeError as e:
            if "authorization_pending" in str(e):
                continue
            if "slow_down" in str(e):
                interval += 5
                continue
            raise
        write("YT_REFRESH_TOKEN", t["refresh_token"])
        write("YT_ACCESS_TOKEN", t["access_token"])
        state_set("yt", access_expires=int(time.time() + t["expires_in"]),
                  refreshed=int(time.time()), logged_in=int(time.time()))
        print("  YouTube 授權完成。refresh token 已存，之後我自己換新的。")
        return
    die("等太久了，授權碼過期。再跑一次 login yt")


def yt_refresh():
    rt, cid, secret = read("YT_REFRESH_TOKEN"), read("YT_CLIENT_ID"), read("YT_CLIENT_SECRET")
    if not (rt and cid and secret):
        return "未登入"
    t = http("https://oauth2.googleapis.com/token", {
        "client_id": cid, "client_secret": secret,
        "refresh_token": rt, "grant_type": "refresh_token",
    })
    write("YT_ACCESS_TOKEN", t["access_token"])
    state_set("yt", access_expires=int(time.time() + t["expires_in"]),
              refreshed=int(time.time()))
    return "已換新"


# ---------- Meta（Instagram 與 Threads 同一個形狀）----------
# 兩邊的流程一樣：授權碼 → 短期權杖 → 換成 60 天長期權杖 → 之後定期自己續。
# 差別只在網域、scope 和 grant_type 的前綴。

META = {
    "ig": {
        "name": "Instagram",
        "authorize": "https://www.instagram.com/oauth/authorize",
        "exchange": "https://api.instagram.com/oauth/access_token",
        "graph": "https://graph.instagram.com",
        # instagram_business_manage_insights 讓 /{media}/insights 抓得到播放數。
        "scope": "instagram_business_basic,instagram_business_content_publish,"
                 "instagram_business_manage_insights",
        "prefix": "ig",
    },
    "threads": {
        "name": "Threads",
        "authorize": "https://threads.net/oauth/authorize",
        "exchange": "https://graph.threads.net/oauth/access_token",
        "graph": "https://graph.threads.net",
        # threads_delete 是刪貼文的權限；threads_read_replies 讓 /me/replies 列得出自己的回覆；
        # threads_manage_insights 讓 /{media}/insights 抓得到播放數。
        "scope": "threads_basic,threads_content_publish,threads_delete,threads_read_replies,"
                 "threads_manage_insights",
        "prefix": "th",
    },
}


def meta_login(p):
    cfg = META[p]
    up = p.upper()
    cid, secret, redirect = read(f"{up}_CLIENT_ID"), read(f"{up}_CLIENT_SECRET"), read(f"{up}_REDIRECT_URI")
    if not (cid and secret and redirect):
        die(f"缺 {up}_CLIENT_ID、{up}_CLIENT_SECRET 或 {up}_REDIRECT_URI，"
            f"見 docs/PUBLISH-SETUP.md")

    url = cfg["authorize"] + "?" + urllib.parse.urlencode({
        "client_id": cid, "redirect_uri": redirect,
        "scope": cfg["scope"], "response_type": "code",
    })
    print(f"\n  開這個網址授權 {cfg['name']}：\n\n{url}\n")
    print("  授權完瀏覽器會跳到一個連不上的頁面。那是正常的。")
    print("  複製網址列那一整串，然後讓我繼續（授權碼從剪貼簿讀，不進對話）。")
    piped = "" if sys.stdin.isatty() else sys.stdin.read()
    pasted = (piped or clipboard()).strip()
    if not pasted:
        die("剪貼簿是空的，複製網址列那一整串再試")

    q = urllib.parse.parse_qs(urllib.parse.urlparse(pasted).query)
    code = (q.get("code") or [None])[0]
    if not code:
        err = (q.get("error_description") or q.get("error") or ["網址裡沒有 code 參數"])[0]
        die(f"拿不到授權碼：{err}")
    code = code.split("#")[0]  # Meta 會在尾巴附一個 #_

    short = http(cfg["exchange"], {
        "client_id": cid, "client_secret": secret,
        "grant_type": "authorization_code",
        "redirect_uri": redirect, "code": code,
    })
    long = http(f"{cfg['graph']}/access_token?" + urllib.parse.urlencode({
        "grant_type": f"{cfg['prefix']}_exchange_token",
        "client_secret": secret,
        "access_token": short["access_token"],
    }))
    write(f"{up}_ACCESS_TOKEN", long["access_token"])
    exp = int(time.time()) + int(long.get("expires_in", META_TTL))
    state_set(p, access_expires=exp, refreshed=int(time.time()),
              user_id=short.get("user_id"))
    print(f"  {cfg['name']} 授權完成。長期權杖到 {ts(exp)}，我會提前續。")


def meta_refresh(p):
    cfg = META[p]
    tok = read(f"{p.upper()}_ACCESS_TOKEN")
    if not tok:
        return "未登入"
    exp = state_load().get(p, {}).get("access_expires", 0)
    if exp and exp - time.time() > RENEW_AHEAD:
        return f"還有 {int((exp - time.time()) / 86400)} 天，不動"
    r = http(f"{cfg['graph']}/refresh_access_token?" + urllib.parse.urlencode({
        "grant_type": f"{cfg['prefix']}_refresh_token", "access_token": tok,
    }))
    write(f"{p.upper()}_ACCESS_TOKEN", r["access_token"])
    exp = int(time.time()) + int(r.get("expires_in", META_TTL))
    state_set(p, access_expires=exp, refreshed=int(time.time()))
    return f"已續到 {ts(exp)}"


# ---------- 指令 ----------

def clipboard():
    """讀剪貼簿。憑證值靠這條路進來，才不會留在對話紀錄裡。"""
    import subprocess
    try:
        return subprocess.run(["pbpaste"], capture_output=True, text=True,
                              timeout=5).stdout
    except (OSError, subprocess.SubprocessError):
        return ""


def cmd_save(name):
    v = clipboard().strip()
    if not v:
        die("剪貼簿是空的")
    if not name.replace("_", "").isalnum():
        die(f"憑證名稱只能用英數和底線：{name}")
    write(name, v)
    print(f"  已存 {name}（{len(v)} 個字元，值沒有印出來）")


def ts(epoch):
    return time.strftime("%Y-%m-%d", time.localtime(epoch)) if epoch else "不知道"


def die(msg):
    print(f"  {msg}", file=sys.stderr)
    sys.exit(1)


def yt_note(info):
    """OAuth 同意畫面還在 Testing 時，refresh token 從登入算起 7 天失效（fix 10495）。
    從這裡看不出應用程式是不是已發布，所以照最壞情況報到期日。"""
    base = f"上次換新 {ts(info.get('refreshed'))}"
    li = info.get("logged_in")
    if not li:
        return f"{base}；登入時間沒記錄，Testing 狀態下 7 天就失效，到期日不明"
    return f"{base}；Testing 狀態下 {ts(li + YT_TESTING_TTL)} 失效（應用程式發布後才長期有效）"


def cmd_status():
    s = state_load()
    rows = []
    for p in PLATFORMS:
        up = p.upper()
        tok = read("YT_REFRESH_TOKEN" if p == "yt" else f"{up}_ACCESS_TOKEN")
        if not tok:
            rows.append((p, "未登入", "—"))
            continue
        info = s.get(p, {})
        if p == "yt":
            rows.append((p, "已登入", yt_note(info)))
        else:
            exp = info.get("access_expires", 0)
            left = int((exp - time.time()) / 86400) if exp else -1
            rows.append((p, "已登入", f"還有 {left} 天（{ts(exp)}）" if left >= 0 else "到期日不明"))
    w = max(len(r[0]) for r in rows)
    for p, st, note in rows:
        print(f"  {p:<{w}}  {st}  {note}")


def cmd_whoami(p):
    """權杖對應哪個帳號。發片前確認不會發到別的帳號。"""
    if p not in META:
        die(f"whoami 只支援 {', '.join(META)}")
    tok = read(f"{p.upper()}_ACCESS_TOKEN")
    if not tok:
        die(f"{p} 未登入")
    fields = "user_id,username,account_type" if p == "ig" else "id,username"
    me = http(f"{META[p]['graph']}/me?" + urllib.parse.urlencode({"fields": fields, "access_token": tok}))
    print("  " + "  ".join(f"{k}={v}" for k, v in me.items()))


def cmd_refresh():
    fails = []
    for p in PLATFORMS:
        try:
            r = yt_refresh() if p == "yt" else meta_refresh(p)
            print(f"  {p}: {r}")
        except Exception as e:                      # noqa: BLE001
            fails.append(p)
            print(f"  {p}: 失敗\n{e}", file=sys.stderr)
    if fails:
        sys.exit(f"續期失敗：{', '.join(fails)}")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    if args[0] == "status":
        cmd_status()
    elif args[0] == "refresh":
        cmd_refresh()
    elif args[0] == "whoami" and len(args) == 2:
        cmd_whoami(args[1])
    elif args[0] == "save" and len(args) == 2:
        cmd_save(args[1])
    elif args[0] == "login" and len(args) == 2:
        p = args[1]
        if p == "yt":
            yt_login()
        elif p in META:
            meta_login(p)
        else:
            die(f"不認得 {p}，只有 yt、ig、threads")
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
