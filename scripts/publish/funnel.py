#!/usr/bin/env python3
"""發片時把 IG／Threads 要的 mp4 暫時放上公開網址，發完就關。

  funnel.py up films/flt-11days      開：印出 reels／threads 兩個公開網址（有 dist/<片名>-cover.jpg 再加一行 cover）
                                     （token 讀 meta/public-path.txt，每次發布前先跑 public_path.py 換新）
  funnel.py up films/x --carousel    改放 out/carousel/p_*.jpg（輪播圖），每張一行
  funnel.py down                     關（重複跑也安全）
  funnel.py status                   看現在開著沒

為什麼要公開網址：IG 和 Threads 發片時 Meta 自己來下載影片，不收上傳。
IG 的 resumable upload 只給 Facebook Login for Business，我們走 Instagram Login；
Threads 只收 video_url。業界排程器（Postiz）是把檔案永久放公開儲存，我們只開幾分鐘。

四個踩過的坑，改這支前先看：
  1. 不能用 443 埠。443 上有只對 tailnet 開放的 4177 服務，Funnel 是整個埠對外，
     開 443 會把它一起曝光。
  2. 絕不能用 `tailscale funnel reset`，它會把 4177 的設定一起清掉。
     關閉只關我們那個埠。
  3. Funnel 直接指檔案要 root（401 must be root），所以經本機只綁 127.0.0.1 的
     http.server 轉發。
  4. 不用 Funnel 的 --https。2026-10-13 tailscaled 內建的 TLS 終結整個壞掉
     （連 tailnet 內的 443 都 connection reset），沒有 sudo 重啟不了它。
     改用 --tcp 直通 10000 埠，TLS 由 _serve 自己做（憑證用 `tailscale cert` 拿，
     私鑰載入記憶體後立刻刪檔）。直通不剝路徑，所以 _serve 只認 /<token>/<檔名>，
     其他一律 404、不列目錄。

關的時機是兩平台的 container 都 PUBLISHED，不是建好 container 就關：
Meta 處理期間會不會再來抓沒有文件，發布失敗還要重建 container。

開的時候會留一個逾時守衛，時間到自動關，防止發片腳本中途掛掉、網址一直開著。
"""
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

PORT = 10000  # 見坑 1、4；Funnel 只開放 443／8443／10000
HOST = "<your-host>.ts.net"
HOME = Path(os.environ.get("VIBE_PUBLISH_DIR") or Path.home() / ".vibe-publish")
STATE = HOME / "funnel.json"
SERVE = HOME / "serve"
# ponytail: 固定 30 分鐘。Meta 建議輪詢 5 分鐘、大檔社群回報 10 分鐘以上；
# 真的發片常超時再改成發布流程每輪詢一次就延長。
TTL = int(os.environ.get("VIBE_FUNNEL_TTL", 30 * 60))

# Meta 要抓的只有這兩支（加上有的話 IG 封面 jpg）。shorts 走 YouTube 上傳，不需要公開。
LABELS = ("reels", "threads")


CAROUSEL_MAX = 10  # IG 輪播上限 10（Threads 20），取小的，兩邊共用同一組圖


def page_no(p):
    """p_3.00.jpg → 3。檔名格式來自 still.mjs --range。"""
    return int(float(p.name[2:-4]))


def served_files(film, carousel=False):
    """回傳 [(label, 原檔路徑)]。缺檔直接報錯，不要開一個抓不到東西的網址。"""
    film = Path(film).resolve()
    name = film.name
    if carousel:
        pages = sorted((film / "out" / "carousel").glob("p_*.jpg"), key=page_no)
        if not 2 <= len(pages) <= CAROUSEL_MAX:
            raise SystemExit(f"輪播要 2–{CAROUSEL_MAX} 張，現在 {len(pages)} 張；先跑 scripts/carousel.sh {film}")
        return [(p.name, p) for p in pages]
    out = []
    for label in LABELS:
        p = film / "dist" / f"{name}-{label}.mp4"
        if not p.is_file():
            raise SystemExit(f"找不到 {p}，先跑 scripts/deliver.sh")
        out.append((label, p))
    # IG 自訂封面（deliver.sh → cover.sh 產）。沒有就不放，IG 退回用第 0 幀
    cover = film / "dist" / f"{name}-cover.jpg"
    if cover.is_file():
        out.append(("cover", cover))
    return out


def film_token(film):
    """用 public_path.py 產的 token，precheck 閘門 6 驗的就是這個值，不要另產一個。"""
    p = Path(film).resolve() / "meta" / "public-path.txt"
    if not p.is_file():
        raise SystemExit(f"找不到 {p}，先跑 scripts/publish/public_path.py {film}")
    token = p.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"[0-9a-f]{16,}", token):
        raise SystemExit(f"{p} 不是隨機 token，重跑 public_path.py")
    return token


def url(token, filename):
    return f"https://{HOST}:{PORT}/{token}/{filename}"


def load():
    try:
        return json.loads(STATE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def ts(*args):
    return subprocess.run(["tailscale", "funnel", *args], capture_output=True, text=True)


def up(film, carousel=False):
    if load():
        raise SystemExit("已經開著，先跑 funnel.py down")
    files = served_files(film, carousel)

    token = film_token(film)
    d = SERVE / token
    d.mkdir(parents=True)
    for _, p in files:
        try:
            os.link(p, d / p.name)  # 同一顆碟，硬連結不佔空間
        except OSError:
            shutil.copy2(p, d / p.name)

    port = free_port()
    log = open(HOME / "funnel-http.log", "ab")
    srv = subprocess.Popen(
        [sys.executable, __file__, "_serve", str(SERVE), token, str(port)],
        stdout=log, stderr=log, start_new_session=True,
    )
    state = {"token": token, "port": port, "pid": srv.pid, "film": str(Path(film).resolve()),
             "opened": int(time.time()), "ttl": TTL}
    STATE.write_text(json.dumps(state, indent=2))

    r = ts("--bg", "--yes", f"--tcp={PORT}", f"tcp://127.0.0.1:{port}")
    if r.returncode != 0:
        down()
        raise SystemExit(f"tailscale funnel 失敗，已收回：\n{r.stdout}{r.stderr}")

    # 逾時守衛：脫離本行程獨立跑，token 對得上才關，避免關到下一次開的
    subprocess.Popen(
        [sys.executable, __file__, "_expire", token, str(TTL)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True,
    )

    for label, p in files:
        print(f"{label}\t{url(token, p.name)}")
    print(f"# {TTL // 60} 分鐘後自動關；發完請跑 funnel.py down", file=sys.stderr)


def down():
    st = load()
    if not st:
        print("沒開著")
        return
    r = ts(f"--tcp={PORT}", "off")
    try:
        os.kill(st["pid"], 15)
    except ProcessLookupError:
        pass
    shutil.rmtree(SERVE / st["token"], ignore_errors=True)
    STATE.unlink(missing_ok=True)
    if r.returncode != 0 and "not found" not in (r.stdout + r.stderr).lower():
        raise SystemExit(f"關 funnel 回報錯誤，請跑 funnel.py status 確認：\n{r.stdout}{r.stderr}")
    print("已關")


def status():
    st = load()
    if not st:
        print("沒開著")
    else:
        left = st["opened"] + st["ttl"] - int(time.time())
        print(f"開著：{st['film']}，token {st['token'][:6]}…，約 {max(left, 0) // 60} 分鐘後自動關")
    print(ts("status").stdout, end="")


def parse_range(header, size):
    """'bytes=a-b'／'bytes=a-'／'bytes=-n' → (start, end)；不認得或超出範圍回 None（當整檔送）。"""
    m = re.fullmatch(r"bytes=(\d*)-(\d*)", (header or "").strip())
    if not m or m.groups() == ("", ""):
        return None
    a, b = m.groups()
    if a == "":
        start, end = max(size - int(b), 0), size - 1
    else:
        start, end = int(a), min(int(b), size - 1) if b else size - 1
    return (start, end) if start <= end < size else None


def content_type(name):
    return "image/jpeg" if name.lower().endswith((".jpg", ".jpeg")) else "video/mp4"


def allowed(path, token, names):
    """直通不剝路徑（坑 4），只放行 /<token>/<要發的檔名>，其他都 404。"""
    parts = path.split("?", 1)[0].split("/")
    return len(parts) == 3 and parts[0] == "" and parts[1] == token and parts[2] in names


def tls_context():
    """憑證每次現拿（tailscaled 有快取，到期前自己續）。私鑰只在 0700 暫存目錄待到載入為止。"""
    import ssl
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        cert, key = f"{tmp}/c.pem", f"{tmp}/k.pem"
        r = subprocess.run(["tailscale", "cert", "--cert-file", cert, "--key-file", key, HOST],
                           capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f"tailscale cert 失敗：{r.stderr}")
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(cert, key)
    return ctx


def serve(root, token, port):
    """http.server 不支援 Range；Meta 抓檔會先試 Range: bytes=0-1 要 206（社群回報），所以補上。"""
    import http.server

    names = {p.name for p in (Path(root) / token).iterdir()}

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=root, **k)

        def log_message(self, fmt, *args):
            sys.stderr.write("%s [%s] %s ua=%s range=%s\n" % (
                self.address_string(), self.log_date_time_string(), fmt % args,
                self.headers.get("User-Agent"), self.headers.get("Range")))

        def send_head(self):
            if not allowed(self.path, token, names):
                self.send_error(404)
                return None
            path = Path(self.translate_path(self.path))
            size = path.stat().st_size
            rng = parse_range(self.headers.get("Range"), size)
            f = open(path, "rb")
            start, end = rng or (0, size - 1)
            self.send_response(206 if rng else 200)
            self.send_header("Content-Type", content_type(path.name))
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Length", str(end - start + 1))
            if rng:
                self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            self.end_headers()
            f.seek(start)
            self._left = end - start + 1
            return f

        def copyfile(self, src, dst):
            left = getattr(self, "_left", None)
            try:
                while left is None or left > 0:
                    buf = src.read(65536 if left is None else min(65536, left))
                    if not buf:
                        break
                    dst.write(buf)
                    if left is not None:
                        left -= len(buf)
            except (BrokenPipeError, ConnectionResetError):
                pass  # 對方只要前幾個 byte 就斷線是正常的，不要噴 traceback

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", int(port)), H)
    # 握手延到各自的處理執行緒，一個卡住的連線不會擋住 accept
    srv.socket = tls_context().wrap_socket(srv.socket, server_side=True, do_handshake_on_connect=False)
    srv.serve_forever()


def expire(token, seconds):
    time.sleep(int(seconds))
    st = load()
    if st and st["token"] == token:
        down()


def main():
    HOME.mkdir(parents=True, exist_ok=True)
    a = sys.argv[1:]
    if a[:1] == ["up"] and len(a) == 2:
        up(a[1])
    elif a[:1] == ["up"] and len(a) == 3 and a[2] == "--carousel":
        up(a[1], carousel=True)
    elif a == ["down"]:
        down()
    elif a == ["status"]:
        status()
    elif a[:1] == ["_serve"] and len(a) == 4:
        serve(a[1], a[2], a[3])
    elif a[:1] == ["_expire"] and len(a) == 3:
        expire(a[1], a[2])
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
