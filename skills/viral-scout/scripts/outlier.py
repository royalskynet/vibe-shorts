#!/usr/bin/env python3
"""帳號內離群倍數：單支播放 ÷ 該帳號近 N 支播放中位數。零 token、免 key，只靠 yt-dlp。

  python3 scripts/outlier.py <@handle|帳號頁 URL> [N=20]   取近 N 支，依倍數由高到低印表
  python3 scripts/outlier.py --selftest                    只跑公式自檢，不連網

@handle 視為 TikTok。YouTube 給 `https://www.youtube.com/channel/<UC…>/shorts`（yt-dlp 2026.11.23
起可用；舊版回空）。
ponytail: 最新幾支播放還沒累積，會拉低中位數、墊高倍數；之後用發布時間排除太新的片。
判定門檻沿用 SKILL.md：倍數 ≥5 離群、2–5 偏強，其餘一般。中位數不用平均，免得一支爆款墊高基線。
借鏡 ScrapeCreators outlier-post-finder（MIT）的公式。
"""
import json
import statistics
import subprocess
import sys

OUTLIER_X = 5.0
STRONG_X = 2.0
MIN_POSTS = 8  # 少於此數基線不可信，照印但標警示


def score(entries):
    """entries: [{url, view_count}] → (中位數, [(倍數, 標籤, entry)] 倍數由高到低)。無播放數的略過。"""
    rows = [e for e in entries if isinstance(e.get("view_count"), (int, float)) and e["view_count"] >= 0]
    if not rows:
        return 0, []
    med = statistics.median(e["view_count"] for e in rows)
    out = []
    for e in rows:
        x = e["view_count"] / med if med else 0.0
        label = "離群" if x >= OUTLIER_X else "偏強" if x >= STRONG_X else "一般"
        out.append((x, label, e))
    out.sort(key=lambda t: t[0], reverse=True)
    return med, out


def fetch(target, n):
    url = f"https://www.tiktok.com/{target}" if target.startswith("@") else target
    p = subprocess.run(
        ["yt-dlp", "--flat-playlist", "--playlist-items", f"1:{n}", "-J", url],
        capture_output=True, text=True, timeout=180,
    )
    try:
        return json.loads(p.stdout).get("entries", [])  # stderr 不併入，否則 JSON 壞
    except json.JSONDecodeError:
        sys.exit(f"yt-dlp 沒回 JSON（exit {p.returncode}）：{p.stderr.strip()[-300:]}")


def selftest():
    # 基線 100 萬；一支 600 萬（6×）離群、一支 250 萬偏強；一支爆 1 億不能把基線墊高（中位數不變）
    views = [1_000_000] * 7 + [6_000_000, 2_500_000, 100_000_000]
    med, out = score([{"url": f"u{i}", "view_count": v} for i, v in enumerate(views)])
    assert med == 1_000_000, med
    assert [t[1] for t in out[:3]] == ["離群", "離群", "偏強"], out[:3]
    assert out[0][2]["view_count"] == 100_000_000
    assert score([{"url": "a", "view_count": None}, {"url": "b"}]) == (0, [])
    assert score([]) == (0, [])
    print("ok")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--selftest":
        return selftest()
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    entries = fetch(sys.argv[1], n)
    med, out = score(entries)
    if not out:
        sys.exit("沒有任何帶播放數的項目")
    note = f"（只 {len(out)} 支，基線不可信）" if len(out) < MIN_POSTS else ""
    print(f"中位數 {int(med):,}｜{len(out)} 支{note}")
    for x, label, e in out:
        print(f"{x:6.1f}×｜{label}｜{int(e['view_count']):,}｜{(e.get('title') or '')[:40]}｜{e.get('url')}")


if __name__ == "__main__":
    main()
