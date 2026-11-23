#!/usr/bin/env python3
"""產一個隨機的公開路徑 token，寫進 <片子>/meta/public-path.txt。

用法：python3 scripts/publish/public_path.py films/flt-11days

為什麼不用片名當路徑：IG 和 Threads 發片時 Meta 會自己來下載影片，
所以 mp4 必須先放在公開網址上。用 flt-11days.mp4 這種路徑，別人猜得到，
也能順著猜其他片子。隨機 token 讓這段公開期間只有拿到網址的人找得到。

每次發布都重新產一個。舊 token 失效不用管，反正發完就關。
"""
import secrets
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    film = Path(sys.argv[1]).resolve()
    if not film.is_dir():
        print(f"找不到 {film}")
        return 2

    meta = film / "meta"
    meta.mkdir(exist_ok=True)
    token = secrets.token_hex(16)
    out = meta / "public-path.txt"
    out.write_text(token + "\n", encoding="utf-8")
    print(f"{out}  {token}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
