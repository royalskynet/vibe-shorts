#!/usr/bin/env python3
"""⑨ 復盤初記補數：refs/postmortem.md 裡標「初記」的片，上架滿 120h 就換成新數字、拿掉「初記」。

  postmortem_refresh.py [--dry-run]

片與平台 ID 對照在 refs/postmortem-ids.tsv。數字來自 stats.py。教訓（下次要改）不動，只在段尾加一行提醒重看。
有更新就 git commit refs/postmortem.md 並印出更新的片名；沒有就安靜退出。零 token，由 daily-trends.sh 呼叫。
"""
import csv
import io
import os
import re
import subprocess
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MD = os.path.join(ROOT, "refs", "postmortem.md")
IDS = os.path.join(ROOT, "refs", "postmortem-ids.tsv")
FULL_H = 120
PLATFORMS = ("yt", "ig", "threads")


# ---------- 純函數（tests/test_postmortem_refresh.py 測）----------

def parse_stats(tsv):
    """stats.py 輸出 → {ID: row}。"""
    return {r["ID"]: r for r in csv.DictReader(io.StringIO(tsv), delimiter="\t") if r.get("ID")}


def refresh(md, stats, ids, today):
    """回傳 (新 md, 更新的片名[])。只動含「初記」且 yt 上架 ≥120h 的段；缺任一平台數字就整段不動。"""
    parts = re.split(r"(?m)^(?=## )", md)
    done = []
    for i, seg in enumerate(parts):
        m = re.match(r"## (\S+)\n", seg)
        if not m or m.group(1) not in ids or "初記" not in seg:
            continue
        film = m.group(1)
        rows = {p: stats.get(ids[film][p]) for p in PLATFORMS}
        if not all(rows.values()):
            continue
        hours = int(rows["yt"]["上架"].rstrip("h"))
        if hours < FULL_H:
            continue
        seg = re.sub(r"(?m)^- 上架：.*$", f"- 上架：{hours}h（{today} 更新）", seg)
        for p, r in rows.items():
            seg = re.sub(rf"(?m)^- {p}：.*$", f"- {p}：播放 {r['播放']}／讚 {r['讚']}／留言 {r['留言']}", seg)
        seg = seg.rstrip("\n") + "\n- 重看：教訓是用 120h 前的舊數字寫的，數字已更新，要不要改教訓看上面三行。\n\n"
        parts[i] = seg
        done.append(film)
    return "".join(parts).rstrip("\n") + "\n", done


# ---------- 執行 ----------

def main():
    args = sys.argv[1:]
    if args == ["--help"] or args == ["-h"]:
        print(__doc__.strip())
        return
    unknown = [a for a in args if a != "--dry-run"]
    if unknown:
        sys.exit(f"不認得的旗標 {unknown}；只接受 --dry-run（fix 10432：旗標被默默忽略會跑成真實執行）")
    dry = "--dry-run" in args
    md = open(MD, encoding="utf-8").read()
    if "初記" not in md:
        return
    ids = {r["片"]: r for r in csv.DictReader(open(IDS, encoding="utf-8"), delimiter="\t")}
    out = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "publish", "stats.py"), "--limit", "30"],
                         capture_output=True, text=True, timeout=180)
    if out.returncode:
        sys.exit(f"stats.py rc={out.returncode}: {out.stderr.strip()[:300]}")
    new, done = refresh(md, parse_stats(out.stdout), ids, date.today().strftime("%m-%d"))
    if not done:
        return
    if dry:
        print(new)
        return
    open(MD, "w", encoding="utf-8").write(new)
    subprocess.run(["git", "-C", ROOT, "add", MD], check=True)
    subprocess.run(["git", "-C", ROOT, "commit", "-q", "-m", f"refs/postmortem.md：初記補數（{'、'.join(done)}）"], check=True)
    print("、".join(done))


if __name__ == "__main__":
    main()
