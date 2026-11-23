#!/usr/bin/env python3
"""social.py 的最小自檢。不連網、不碰真的憑證目錄。

只測三件錯了會真的弄壞東西的事：
  1. 轉貼篩選。篩錯就會把自己寫的貼文一起刪掉，而刪掉不可復原。
  2. IG 不能刪必須在送請求前就擋下來，不是等平台回 400。
  3. 沒有 --yes 時 delete 與 prune 一筆都不能送出去。
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TMP = tempfile.mkdtemp(prefix="vibe-social-test-")
os.environ["VIBE_CREDS_DIR"] = os.path.join(TMP, "kv")
os.environ["VIBE_STATE"] = os.path.join(TMP, "state.json")
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts", "publish"))

import social  # noqa: E402

fails = []


def check(name, got, want):
    if got != want:
        fails.append(f"{name}: 得到 {got!r}，應該是 {want!r}")


def raises(name, fn, needle):
    try:
        fn()
    except SystemExit as e:
        if needle not in str(e):
            fails.append(f"{name}: 擋下來了但訊息是 {e}，裡面沒有 {needle!r}")
        return
    fails.append(f"{name}: 應該要擋下來，卻直接跑完")


# 1. 轉貼篩選
rows = [
    {"id": "1", "type": "REPOST_FACADE", "date": "2026-10-01T00:00:00+0000", "url": "u1", "text": ""},
    {"id": "2", "type": "TEXT_POST", "date": "2026-10-02T00:00:00+0000", "url": "u2", "text": "自己寫的"},
    {"id": "3", "type": "REPOST_FACADE", "date": "2026-10-03T00:00:00+0000", "url": "u3", "text": ""},
]
check("只留轉貼", [r["id"] for r in social.pick(rows, "repost")], ["1", "3"])
check("all 全留", [r["id"] for r in social.pick(rows, "all")], ["1", "2", "3"])

# 2. 能力表在送請求前就擋
raises("IG 不能刪", lambda: social.can("ig", "delete"), "不支援 DELETE")
check("IG 能列", social.can("ig", "list"), True)
check("Threads 能刪", social.can("threads", "delete"), True)
raises("不認得的平台", lambda: social.can("x", "delete"), "不認得平台")

# 3. 沒有 --yes 一筆都不送
sent = []
social.DELETERS["threads"] = lambda i: sent.append(i)
social.delete_many("threads", social.pick(rows, "repost"), yes=False)
check("沒 --yes 不送請求", sent, [])
social.delete_many("threads", social.pick(rows, "repost"), yes=True)
check("有 --yes 才送，且只送轉貼", sent, ["1", "3"])

# 4. 輸出壓成單行，不會把 tab 分隔弄亂
check("換行壓掉", social.one_line("第一行\n第二行"), "第一行 第二行")
check("超長截斷", len(social.one_line("字" * 100)), social.TEXT_WIDTH)
check("None 當空字串", social.one_line(None), "")

if fails:
    print("FAIL")
    for f in fails:
        print(f"  {f}")
    sys.exit(1)
print(f"OK  {11} 項全過")
