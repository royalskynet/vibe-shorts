#!/usr/bin/env python3
"""每日刪 @paradoxbar.tw 的 Threads 舊回覆，由 launchd com.51mini.threads-prune-replies 每天跑一次。

/me/replies 只有 limit<=5 會成功，limit>=6（含預設 25）一律回 HTTP 500；500 之後約幾秒內
再打還是 500，所以每個 GET 都要退避重試。每次抓一頁、刪完再抓。
官方上限 100 刪/天，這裡留 5 則餘裕。刪到 0 則（且列表沒出錯）就自己 bootout。
每次跑完用 hpush 送一則白話摘要到 Telegram。
"""
import json, os, subprocess, sys, time, urllib.parse, urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "publish"))
LABEL = "com.51mini.threads-prune-replies"
USER = "paradoxbar.tw"
DAILY_CAP = 95
PAGE = 5  # limit>=6 時 /me/replies 固定 500，別調高


def _get(params, tries=4, backoff=2.0):
    """打 /me/replies，500 退避重試；全部失敗就丟最後一個例外。"""
    import tokens
    q = dict(params, limit=PAGE, fields="id,username", access_token=tokens.read("THREADS_ACCESS_TOKEN"))
    url = "https://graph.threads.net/v1.0/me/replies?" + urllib.parse.urlencode(q)
    last = None
    for i in range(tries):
        try:
            return json.loads(urllib.request.urlopen(url, timeout=30).read())
        except Exception as e:
            last = e
            if i + 1 < tries:
                time.sleep(backoff * (i + 1))
    raise last


def list_mine():
    d = _get({})
    return [x["id"] for x in d.get("data", []) if x.get("username") == USER]


def count_mine(max_pages=200, pause=1):
    """翻頁數剩幾則，回傳 (幾則, 是否翻到底)；中途出錯就回 (至少幾則, False)。"""
    total, after = 0, None
    for _ in range(max_pages):
        try:
            d = _get({"after": after} if after else {})
        except Exception:
            return total, False
        total += sum(1 for x in d.get("data", []) if x.get("username") == USER)
        if "next" not in d.get("paging", {}):
            return total, True
        after = d["paging"]["cursors"]["after"]
        time.sleep(pause)
    return total, False


def summary(n, done, left, complete, cap=DAILY_CAP, err=None):
    if done:
        return "Threads 舊回覆清理：全部刪完，每日排程已自己停掉。"
    if n:
        head = f"Threads 舊回覆清理：今天刪了 {n} 則。"
    else:
        head = f"Threads 舊回覆清理：今天沒刪成（{err or '原因不明'}），明天 18:35 再試。"
    if left is None:
        return head + "剩幾則這次查不到。"
    if complete and left == 0:
        return head + "已經全部刪完，明天排程跑一次確認後會自己停掉。"
    if complete:
        days = -(-left // cap)
        return head + f"還剩 {left} 則，照每天 {cap} 則約 {days} 天刪完。"
    return head + f"還剩至少 {left} 則（API 後面幾頁會出錯，實際可能更多）。"


def delete(ids):
    r = subprocess.run([sys.executable, "scripts/publish/social.py", "delete", "threads", *ids, "--yes"],
                       capture_output=True, text=True, cwd=ROOT)
    print((r.stdout.splitlines() or [""])[0], r.stderr.strip()[-200:], flush=True)
    return r.returncode == 0


def run(list_fn, delete_fn, cap=DAILY_CAP, pause=3):
    """回傳 (刪除數, 是否該停止排程, 停下的原因)。只有列表正常且第一輪就 0 則才停。"""
    n = 0
    while n < cap:
        try:
            ids = list_fn()[:cap - n]
        except Exception as e:
            print("list err", e, flush=True)
            return n, False, f"抓清單失敗：{e}"
        if not ids:
            return n, n == 0, None
        if not delete_fn(ids):
            return n, False, "刪除被拒，多半是被限速"
        n += len(ids)
        time.sleep(pause)
    return n, False, None


if __name__ == "__main__":
    n, done, err = run(list_mine, delete)
    print(datetime.now().strftime("%F %T"), "deleted", n, "done" if done else "", err or "", flush=True)
    try:
        left, complete = count_mine()
    except Exception:
        left, complete = None, False
    msg = summary(n, done, left, complete, err=err)
    print(msg, flush=True)
    subprocess.run([os.path.expanduser("~/.local/bin/hpush"), msg])
    if done:
        # ponytail: plist 留在 LaunchAgents，重開機會再載入一次、刪 0 則後再 bootout；要永久移除就刪 plist
        subprocess.run(["launchctl", "bootout", f"gui/{os.getuid()}/{LABEL}"])
