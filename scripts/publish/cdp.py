#!/usr/bin/env python3
"""接上 Mac mini 螢幕上那個 Chrome，替你點三平台後台。登入由你自己做（螢幕共享）。

  cdp.py launch                 開一個專用 Chrome（獨立設定檔，開 127.0.0.1:9333 除錯埠）
  cdp.py goto <url>             目前分頁開網址
  cdp.py text [N]               印目前頁面文字（遮掉像憑證的字串），預設前 4000 字
  cdp.py click <selector>       Playwright selector，例如 'text=建立用戶端'、'role=button[name="Save"]'
  cdp.py fill <selector> <值>   填非機密欄位（網址、名稱）
  cdp.py grab <selector> <NAME> 讀欄位值或文字，直接寫進 ~/.creds/kv/<NAME>.txt，只印字元數
  cdp.py shot <png>             截圖；頁面上有像憑證的字串就拒絕

憑證值只走 grab，不經過 text／shot 的輸出，所以不會進對話紀錄。
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
import tokens  # noqa: E402

PORT = 9333
PROFILE = os.path.expanduser("~/.vibe-publish/chrome-profile")
CHROME = "/Applications/Google Chrome.app"

# ponytail: 用樣式猜憑證，猜不到的長字串一律遮；新平台的權杖格式不同時再加樣式
SECRETISH = re.compile(
    r"GOCSPX-[\w-]+"            # Google 用戶端密鑰
    r"|\b[0-9a-f]{32}\b"        # Meta app secret
    r"|(?:EAA|IGAA|IGQ|TH)[\w-]{20,}"  # Meta 權杖
    r"|(?<=code=)[^&\s#]+"      # 授權碼
    r"|[\w-]{40,}"              # 其餘長隨機字串
)


def redact(s):
    return SECRETISH.sub("[遮]", s)


_browser = None


def page():
    """最新開的那個分頁。連線留著重用，remote.py 每 0.6 秒會叫一次。"""
    global _browser
    if _browser is None or not _browser.is_connected():
        from playwright.sync_api import sync_playwright
        _browser = sync_playwright().start().chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    b = _browser
    pages = [p for c in b.contexts for p in c.pages if not p.url.startswith(("devtools://", "chrome://"))]
    if not pages:
        sys.exit("Chrome 沒有分頁，先跑 cdp.py launch")
    return pages[-1]


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return
    cmd = a[0]
    if cmd == "launch":
        os.makedirs(PROFILE, exist_ok=True)
        subprocess.run(["open", "-na", CHROME, "--args",
                        f"--user-data-dir={PROFILE}",
                        f"--remote-debugging-port={PORT}",
                        "--remote-debugging-address=127.0.0.1",
                        "--no-first-run", "about:blank"], check=True)
        print("已開。Mac mini 螢幕上那個 Chrome 就是它。")
        return
    p = page()
    if cmd == "goto":
        p.goto(a[1], wait_until="domcontentloaded")
        print(redact(p.url))
    elif cmd == "text":
        n = int(a[1]) if len(a) > 1 else 4000
        print(redact(p.url))
        print(redact(p.inner_text("body"))[:n])
    elif cmd == "click":
        p.locator(a[1]).first.click(timeout=10000)
        p.wait_for_timeout(1500)
        print(redact(p.url))
    elif cmd == "fill":
        p.locator(a[1]).first.fill(a[2], timeout=10000)
        print("已填")
    elif cmd == "grab":
        el = p.locator(a[1]).first
        v = (el.input_value(timeout=10000) if el.evaluate("e => 'value' in e")
             else el.inner_text(timeout=10000)).strip()
        if not v:
            sys.exit("欄位是空的")
        if not a[2].replace("_", "").isalnum():
            sys.exit(f"憑證名稱只能用英數和底線：{a[2]}")
        tokens.write(a[2], v)
        print(f"已存 {a[2]}（{len(v)} 個字元，值沒有印出來）")
    elif cmd == "shot":
        if SECRETISH.search(p.inner_text("body") + p.url):
            sys.exit("頁面上有像憑證的字串，不截圖。改用 cdp.py text")
        p.screenshot(path=a[1])
        print(a[1])
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
