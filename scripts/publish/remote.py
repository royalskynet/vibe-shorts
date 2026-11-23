#!/usr/bin/env python3
"""手機遙控 Mac mini 上那個專用 Chrome（VNC 黑畫面時的替代路）。

  remote.py            在 tailnet 位址開一個網頁，手機打開就能看畫面、點、打字

只綁 Tailscale 位址，網址帶隨機路徑。你打的字（含密碼）經 HTTP 直接送進 Chrome，
不寫 log、不進對話。截圖只送到你的手機，不存檔。
單執行緒伺服器：Playwright sync API 不能跨執行緒，所以一次只處理一個請求。
"""
import json
import os
import secrets
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

import cdp

PORT = 8790
KEY = os.environ.get('REMOTE_KEY') or secrets.token_urlsafe(8)

PAGE = """<!doctype html><meta name=viewport content="width=device-width,initial-scale=1">
<style>body{margin:0;font:16px sans-serif;background:#111;color:#eee}
img{width:100%;display:block;touch-action:manipulation}
.bar{display:flex;gap:4px;padding:4px;flex-wrap:wrap}.bar *{font-size:16px;padding:8px}
input{flex:1;min-width:0}</style>
<div class=bar><input id=u placeholder="網址"><button onclick="go()">開</button></div>
<img id=s>
<div class=bar><input id=t placeholder="要打的字（點欄位後再送）" autocomplete=off>
<button onclick="post('type',{text:t.value});t.value=''">送</button></div>
<div class=bar><button onclick="key('Enter')">Enter</button><button onclick="key('Tab')">Tab</button>
<button onclick="key('Backspace')">⌫</button><button onclick="post('scroll',{dy:-500})">▲</button>
<button onclick="post('scroll',{dy:500})">▼</button><button onclick="post('back',{})">上一頁</button></div>
<script>
const b=location.pathname;let vw=1,vh=1;
async function post(a,d){await fetch(b+'/'+a,{method:'POST',body:JSON.stringify(d)});}
function key(k){post('key',{key:k})}
function go(){post('goto',{url:u.value})}
s.onclick=e=>{const r=s.getBoundingClientRect();
 post('click',{x:(e.clientX-r.left)/r.width*vw,y:(e.clientY-r.top)/r.height*vh})};
async function loop(){try{const r=await fetch(b+'/shot?'+Date.now(),{signal:AbortSignal.timeout(5000)});
 vw=+r.headers.get('x-vw');vh=+r.headers.get('x-vh');u.placeholder=r.headers.get('x-url')||'網址';
 const bl=await r.blob();const o=s.src;s.src=URL.createObjectURL(bl);if(o)URL.revokeObjectURL(o);}catch(e){}
 setTimeout(loop,600)}loop();
</script>"""


_armed = set()


def page():
    """每個分頁掛一個虛擬驗證器。Google 會要密碼金鑰，Chrome 跳的是原生對話框，
    截圖看不到、網頁點擊也被它擋住；掛上虛擬驗證器後請求直接失敗，頁面就能選「輸入密碼」。"""
    p = cdp.page()
    if id(p) not in _armed:
        s = p.context.new_cdp_session(p)
        s.send("WebAuthn.enable", {"enableUI": False})
        s.send("WebAuthn.addVirtualAuthenticator", {"options": {
            "protocol": "ctap2", "transport": "internal", "hasResidentKey": True,
            "hasUserVerification": True, "isUserVerified": True}})
        _armed.add(id(p))
    return p


def restart_if_driver_dead(e):
    """Playwright driver 死了就整個行程換新。
    兩個 CDP 客戶端（這裡和 cdp.py）同時接著時，頁面跳 JS 對話框兩邊都會去關，
    晚到的那邊拿到 'No dialog is showing'，driver 直接崩潰；之後每次截圖都是
    'Connection closed while reading from the driver'，手機只看到逾時。
    同一執行緒裡重開 sync_playwright 不可靠，所以 execv 自己（REMOTE_KEY 在環境變數裡，網址不變）。"""
    if "Connection closed" in str(e):
        print("driver 斷線，重啟", file=sys.stderr, flush=True)
        os.execv(sys.executable, [sys.executable, os.path.abspath(__file__)] + sys.argv[1:])


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):  # 不寫 log：POST 內容可能是密碼
        pass

    def _ok(self, path):
        # 只記來源 IP 與動作，不記內容
        print(self.client_address[0], self.command, self.path[len(KEY) + 1:].split("?")[0] or "/", file=sys.stderr, flush=True)
        if not self.path.startswith(f"/{KEY}"):
            self.send_error(404)
            return None
        return self.path[len(KEY) + 1:]

    def do_GET(self):
        sub = self._ok(self.path)
        if sub is None:
            return
        if sub.startswith("/shot"):
            try:
                p = page()
                img = p.screenshot(type="jpeg", quality=60)
                vs = p.evaluate("[innerWidth, innerHeight]")
            except Exception as e:  # noqa: BLE001
                self.send_error(503)
                restart_if_driver_dead(e)
                print("/shot", type(e).__name__, str(e).splitlines()[0][:200], file=sys.stderr, flush=True)
                return
            self.send_response(200)
            self.send_header("Content-Type", "image/jpeg")
            self.send_header("x-vw", str(vs[0]))
            self.send_header("x-vh", str(vs[1]))
            self.send_header("x-url", cdp.redact(p.url)[:200].encode("ascii", "ignore").decode())
            self.end_headers()
            self.wfile.write(img)
        else:
            body = PAGE.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(body)

    def do_POST(self):
        sub = self._ok(self.path)
        if sub is None:
            return
        d = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        try:
            p = page()
            if sub == "/click":
                p.mouse.click(d["x"], d["y"])
            elif sub == "/type":
                print("type len", len(d.get("text", "")), file=sys.stderr, flush=True)  # 只記長度
                p.keyboard.insert_text(d["text"])
            elif sub == "/key":
                p.keyboard.press(d["key"])
            elif sub == "/scroll":
                p.mouse.wheel(0, d["dy"])
            elif sub == "/back":
                p.go_back()
            elif sub == "/goto":
                url = d["url"] if "://" in d["url"] else "https://" + d["url"]
                p.goto(url, wait_until="domcontentloaded")
        except Exception as e:  # noqa: BLE001  頁面跳轉中點擊失敗很常見，不讓伺服器掛掉
            # /type 的錯誤訊息可能夾帶輸入內容（密碼），只印類型
            print(sub, type(e).__name__, "" if sub == "/type" else str(e).splitlines()[0][:200], file=sys.stderr, flush=True)
            if "Connection closed" in str(e):
                self.send_response(503)
                self.end_headers()
                restart_if_driver_dead(e)
        self.send_response(204)
        self.end_headers()


def main():
    ip = subprocess.run(["tailscale", "ip", "-4"], capture_output=True, text=True).stdout.split()[0]
    print(f"手機開：http://{ip}:{PORT}/{KEY}", flush=True)
    HTTPServer((ip, PORT), H).serve_forever()


if __name__ == "__main__":
    main()
