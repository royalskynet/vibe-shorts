#!/usr/bin/env python3
"""Threads 文字貼排程佇列：queue/threads/*.md 到點且核准過就發，發完搬進 sent/。

  threads_post.py list         列佇列（時間、核准、引用、前 30 字）
  threads_post.py run          發所有到點且 approved: yes 的；launchd 每 30 分鐘跑一次
  threads_post.py run --dry    只印會發哪幾則，不連 Meta

佇列檔格式（--- 上面是表頭，下面是貼文，≤500 字）：

  at: 2026-10-21 20:30
  approved: yes
  quote: codex/threads
  ---
  貼文內容

- approved：對外發布要人點頭（CLAUDE.md），使用者在對話裡說好才改成 yes。
- quote：選填。`<片名>/<published.json 的鍵>` 引用自己發過的片（套娃自轉），
  或直接給 Threads 媒體 ID。他人貼文拿不到 ID（keyword_search 未過審），不支援。
- 官方：POST me/threads media_type=TEXT text=… [quote_post_id=…] → threads_publish。
  https://developers.facebook.com/docs/threads/posts/quote-posts
"""
import json
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import meta_publish as mp  # noqa: E402

QUEUE = ROOT / "queue" / "threads"
LIMIT = 500


def parse(path):
    """回傳 dict(at, approved, quote, text)。格式錯直接報錯，不要默默跳過一則。"""
    raw = Path(path).read_text(encoding="utf-8")
    if "\n---\n" not in raw:
        raise ValueError(f"{path.name} 缺 --- 分隔線")
    head, text = raw.split("\n---\n", 1)
    meta = {}
    for line in head.splitlines():
        if line.strip():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    text = text.strip()
    if not text:
        raise ValueError(f"{path.name} 沒有內文")
    # ponytail: 官方 emoji 按 UTF-8 位元組計，這裡只數字元；稿子常用 emoji 再改
    if len(text) > LIMIT:
        raise ValueError(f"{path.name} {len(text)} 字，超過 {LIMIT}")
    return {
        "at": datetime.strptime(meta["at"], "%Y-%m-%d %H:%M"),
        "approved": meta.get("approved") == "yes",
        "quote": meta.get("quote") or None,
        "text": text,
    }


def resolve_quote(q):
    """codex/threads → published.json 裡的 id；純數字照用。"""
    if q is None or q.isdigit():
        return q
    film, _, key = q.partition("/")
    f = ROOT / "films" / film / "meta" / "published.json"
    done = json.loads(f.read_text()) if f.is_file() else {}
    if key not in done:
        raise ValueError(f"引用 {q} 找不到（{f} 沒有 {key}）")
    return done[key]["id"]


def due(now=None):
    """到點、核准過、還沒發的佇列檔，照時間排。"""
    now = now or datetime.now()
    out = []
    for f in sorted(QUEUE.glob("*.md")):
        d = parse(f)
        if d["approved"] and d["at"] <= now:
            out.append((f, d))
    return sorted(out, key=lambda x: x[1]["at"])


def post(d):
    params = {"media_type": "TEXT", "text": d["text"]}
    qid = resolve_quote(d["quote"])
    if qid:
        params["quote_post_id"] = qid
    cid = mp.call("threads", "me/threads", params)["id"]
    mp.wait_finished("threads", [cid])
    m = mp.call("threads", "me/threads_publish", {"creation_id": cid})
    link = mp.call("threads", f"{m['id']}?fields=permalink").get("permalink", "-")
    return m["id"], link


def preview(d):
    return d["text"][:30].replace("\n", " ")


def cmd_run(dry):
    jobs = due()
    if not jobs:
        return 0
    if not dry and mp.whoami("threads") != mp.ACCOUNT:
        raise SystemExit(f"Threads 權杖不是 {mp.ACCOUNT}，不發")
    fails = 0
    for f, d in jobs:
        if dry:
            print(f"會發 {f.name}：{preview(d)}")
            continue
        try:
            mid, link = post(d)
        except (RuntimeError, ValueError) as e:
            print(f"失敗 {f.name}：{e}", file=sys.stderr)
            fails += 1
            continue
        sent = QUEUE / "sent"
        sent.mkdir(exist_ok=True)
        dst = sent / f.name
        shutil.move(f, dst)
        with dst.open("a", encoding="utf-8") as fh:
            fh.write(f"\n\n<!-- sent {time.strftime('%F %T')} id={mid} {link} -->\n")
        print(f"已發 {f.name} {link}")
    return 1 if fails else 0


def cmd_list():
    for f in sorted(QUEUE.glob("*.md")):
        d = parse(f)
        flag = "核准" if d["approved"] else "待核"
        q = f" 引用 {d['quote']}" if d["quote"] else ""
        print(f"{d['at']:%m-%d %H:%M} {flag}{q} {f.name}：{preview(d)}")


def main():
    a = sys.argv[1:]
    if a == ["list"]:
        cmd_list()
        return 0
    if a in (["run"], ["run", "--dry"]):
        return cmd_run("--dry" in a)
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
