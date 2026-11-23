#!/usr/bin/env python3
"""公版文本庫：從維基文庫抓古籍笑話／寓言／軼事，拆成一則一筆，寫 refs/public-domain/<書>.jsonl。

  scripts/pd_texts.py            抓 WORKS 全部（已抓過的頁跳過）
  scripts/pd_texts.py --selftest 只跑拆則自檢，不連網

為什麼（2026-10-20）：對談片要「兩人一來一往＋最後一句翻盤」的結構。《笑林廣記》《艾子雜說》
一則就是這種結構，作者死了幾百年，屬公有領域，可以直接引用或改編，不受「台詞非照抄」門限制。
來源走維基文庫官方 API（prop=extracts 純文字），不寫爬蟲。零 token。
"""
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://zh.wikisource.org/w/api.php"
OUT = Path(__file__).resolve().parent.parent / "refs" / "public-domain"
UA = "vibe-shorts pd_texts (royalskynet)"
# 書名 → 是否有子頁。笑話集全收；子書只收寓言多的。
WORKS = {"笑林廣記": True, "艾子雜說": False, "笑府": False, "世說新語": True,
         "韓非子": True, "列子": True, "莊子": True, "呂氏春秋": True}
MIN_LEN = 20   # 太短的是目錄、標題殘片


def api(**q):
    q |= {"format": "json", "variant": "zh-tw"}
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(q), headers={"User-Agent": UA})
    for wait in (10, 30, 90, None):  # 2026-10-20 實測連打約 15 頁就 429
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code != 429 or wait is None:
                raise
            time.sleep(int(e.headers.get("Retry-After") or wait))


def subpages(work):
    d = api(action="query", list="prefixsearch", pssearch=work + "/", pslimit=100)
    return [x["title"] for x in d["query"]["prefixsearch"]]


def extract(title):
    d = api(action="query", prop="extracts", explaintext=1, titles=title)
    return next(iter(d["query"]["pages"].values())).get("extract", "")


def split_entries(text):
    """「== 標題 ==」切則；沒有標題的頁按空行段落切。回 [(標題, 內文)]。"""
    parts = re.split(r"^==+\s*(.+?)\s*==+\s*$", text, flags=re.M)
    out = []
    if len(parts) > 1:
        for t, body in zip(parts[1::2], parts[2::2]):
            body = re.sub(r"\s+", "", body)
            if len(body) >= MIN_LEN:
                out.append((t, body))
    else:
        for i, p in enumerate(re.split(r"\n\s*\n", text)):
            p = re.sub(r"\s+", "", p)
            if len(p) >= MIN_LEN:
                out.append((f"第{i + 1}段", p))
    return out


def selftest():
    t = "\n\n== 辭朝 ==\n　　一教官辭朝見象，低徊留之不忍去。人問其故，答曰：「我想祭丁的豬羊。」\n\n== 短 ==\n太短\n"
    e = split_entries(t)
    assert e == [("辭朝", "一教官辭朝見象，低徊留之不忍去。人問其故，答曰：「我想祭丁的豬羊。」")], e
    e2 = split_entries("甲段落有二十個字以上的內容在這裡啊啊啊啊\n\n短\n\n乙段落也要二十個字以上的內容才收啊啊啊啊啊")
    assert [x[0] for x in e2] == ["第1段", "第3段"], e2
    print("✅ pd_texts selftest 全過")
    return 0


def main():
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    if sys.argv[1:]:  # --help 之類的未知旗標不能落到真實抓取（fix 10432 類型）
        print(__doc__, file=sys.stderr)
        return 0 if sys.argv[1] in ("-h", "--help") else 2
    OUT.mkdir(parents=True, exist_ok=True)
    for work, has_sub in WORKS.items():
        f = OUT / f"{work}.jsonl"
        done = {json.loads(line)["page"] for line in f.open(encoding="utf-8")} if f.exists() else set()
        pages = subpages(work) if has_sub else [work]
        n = 0
        with f.open("a", encoding="utf-8") as w:
            for p in pages:
                if p in done:
                    continue
                for title, body in split_entries(extract(p)):
                    w.write(json.dumps({"work": work, "page": p, "title": title, "text": body,
                                        "url": "https://zh.wikisource.org/wiki/" + urllib.parse.quote(p)},
                                       ensure_ascii=False) + "\n")
                    n += 1
                time.sleep(2)  # 維基 API 禮貌間隔
        print(f"{work}：+{n} 則（{len(pages)} 頁）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
