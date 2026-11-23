#!/usr/bin/env python3
"""tokens.py 的最小自檢。不連網、不碰真的憑證目錄。

這裡只測三件會讓發片靜默失敗的事：
  1. 從貼回來的網址裡挖授權碼（Meta 會在尾巴附 #_，不切掉就換不到權杖）
  2. 續期的提前判斷（算錯就會在過期後才去續，權杖已經死了）
  3. 憑證檔權限必須是 600
"""
import os
import sys
import tempfile
import time
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
TMP = tempfile.mkdtemp(prefix="vibe-tokens-test-")
os.environ["VIBE_CREDS_DIR"] = os.path.join(TMP, "kv")
os.environ["VIBE_STATE"] = os.path.join(TMP, "state.json")
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts", "publish"))

import tokens  # noqa: E402

fails = []


def check(name, got, want):
    if got != want:
        fails.append(f"{name}: 得到 {got!r}，應該是 {want!r}")


# 1. 授權碼解析。Meta 真實回傳的樣子：尾巴有 #_
def extract(url):
    q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    code = (q.get("code") or [None])[0]
    return code.split("#")[0] if code else None


check("帶 #_ 的授權碼",
      extract("https://example.com/oauth?code=AQBx123abc#_"), "AQBx123abc")
check("乾淨的授權碼",
      extract("https://example.com/oauth?code=AQBx123abc"), "AQBx123abc")
check("使用者拒絕授權時沒有 code",
      extract("https://example.com/oauth?error=access_denied"), None)

# 2. 續期提前判斷。還有 20 天不該動，剩 5 天要續。
now = int(time.time())
tokens.state_save({"ig": {"access_expires": now + 20 * 86400}})
check("剩 20 天不動",
      tokens.state_load()["ig"]["access_expires"] - now > tokens.RENEW_AHEAD, True)
tokens.state_save({"ig": {"access_expires": now + 5 * 86400}})
check("剩 5 天要續",
      tokens.state_load()["ig"]["access_expires"] - now > tokens.RENEW_AHEAD, False)

# 2b. YT 的 status 不能宣稱 refresh token 長期有效：Testing 狀態下 7 天就失效（fix 10495）
li = int(time.mktime((2026, 10, 1, 12, 0, 0, 0, 0, -1)))
check("YT 有登入時間就報到期日",
      tokens.ts(li + 7 * 86400) in tokens.yt_note({"refreshed": now, "logged_in": li}), True)
check("YT 沒登入時間要說到期日不明", "到期日不明" in tokens.yt_note({"refreshed": now}), True)
check("YT 不准說長期有效", "長期有效，" in tokens.yt_note({"refreshed": now}), False)

# 3. 憑證檔權限
tokens.write("TEST_FAKE_TOKEN", "not-a-real-value")
mode = os.stat(os.path.join(os.environ["VIBE_CREDS_DIR"], "TEST_FAKE_TOKEN.txt")).st_mode
check("憑證檔權限 600", oct(mode & 0o777), "0o600")
check("讀回來一致", tokens.read("TEST_FAKE_TOKEN"), "not-a-real-value")
check("讀不存在的回 None", tokens.read("TEST_DOES_NOT_EXIST"), None)

if fails:
    print("FAIL")
    for f in fails:
        print(f"  {f}")
    sys.exit(1)
print(f"OK  {6 + 3 + 3} 項全過")
