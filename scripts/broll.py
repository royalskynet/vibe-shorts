#!/usr/bin/env python3
"""B-roll 素材搜尋與擷取。Commons 免 key；Pexels 需 PEXELS_API_KEY。"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

UA = "vibe-shorts-broll/0.1 (royalskynet)"

# 白名單整串比對：未知或附加條款的授權一律不收（codex 11-10 審查：子字串比對會放過「CC BY mystery」）。
# Pexels License 可商用免署名，Pexels 結果一律標這個值。
OK_LICENSE = re.compile(r"cc0(?: 1\.0)?|public domain|pexels|cc by(?: [1-4]\.0| 2\.5)?")


def license_ok(name):
    return bool(name) and OK_LICENSE.fullmatch(" ".join(str(name).lower().split())) is not None


def _duration(item):
    d = item.get("duration")
    if d is None:
        return 0.0
    try:
        return float(d)
    except Exception:
        return 0.0


def _is_portrait(item):
    try:
        return int(item.get("height") or 0) > int(item.get("width") or 0)
    except Exception:
        return False


def _ratio_score(item):
    try:
        w = float(item.get("width") or 0)
        h = float(item.get("height") or 0)
        if w <= 0 or h <= 0:
            return 10**9
        target = 9.0 / 16.0
        r = w / h
        return abs(r - target)
    except Exception:
        return 10**9


def rank(items, min_sec):
    out = []
    for it in items:
        if _duration(it) < float(min_sec):
            continue
        out.append(it)
    out.sort(key=lambda x: (0 if _is_portrait(x) else 1, _ratio_score(x), -_duration(x)))
    return out


def _request_json(url, headers=None, timeout=30):
    h = {"User-Agent": UA}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", "ignore")
        except Exception:
            pass
        msg = f"HTTP {e.code} {e.reason} {url}\n{body}"
        for v in (headers or {}).values():   # 上游可能回顯 Authorization，key 不准出現在錯誤裡
            msg = msg.replace(v, "***")
        raise RuntimeError(msg) from None
    except urllib.error.URLError as e:
        raise RuntimeError(f"URL error {url}: {e}") from e
    except Exception as e:
        raise RuntimeError(f"request failed {url}: {e}") from e
    try:
        return json.loads(data.decode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"JSON decode failed {url}: {e}") from e


def _search_commons(keyword, limit, min_sec):
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"filetype:video {keyword}",
        "gsrnamespace": "6",
        "gsrlimit": str(max(int(limit) * 5, 20)),
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "iiextmetadatafilter": "LicenseShortName|Artist",
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    data = _request_json(url)
    pages = (data.get("query") or {}).get("pages") or {}
    items = []
    for page in pages.values():
        iis = page.get("imageinfo") or []
        if not iis:
            continue
        ii = iis[0]
        meta = ii.get("extmetadata") or {}
        lic = (meta.get("LicenseShortName") or {}).get("value") or ""
        if not license_ok(lic):
            continue
        artist = (meta.get("Artist") or {}).get("value") or ""
        dur = ii.get("duration") or 0
        item = {
            "source": "commons",
            "url": ii.get("url"),
            "page": ii.get("descriptionurl") or "",
            "width": ii.get("width") or 0,
            "height": ii.get("height") or 0,
            "duration": dur,
            "license": lic,
            "artist": re.sub("<[^>]+>", "", artist),
        }
        if not item["url"]:
            continue
        items.append(item)
    return rank(items, min_sec)[: int(limit)]


def _search_pexels(keyword, limit, min_sec):
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        raise SystemExit(2)
    params = {
        "query": keyword,
        "per_page": str(max(int(limit) * 5, 20)),
        "orientation": "portrait",
    }
    url = "https://api.pexels.com/videos/search?" + urllib.parse.urlencode(params)
    data = _request_json(url, headers={"Authorization": key})
    items = []
    for v in data.get("videos") or []:
        files = v.get("video_files") or []
        chosen = None
        for f in files:
            w = f.get("width") or 0
            h = f.get("height") or 0
            link = f.get("link")
            if not link:
                continue
            if h > w:
                chosen = f
                break
            if chosen is None:
                chosen = f
        if not chosen:
            continue
        lic = "Pexels"
        item = {
            "source": "pexels",
            "url": chosen.get("link"),
            "page": v.get("url") or "",
            "width": chosen.get("width") or v.get("width") or 0,
            "height": chosen.get("height") or v.get("height") or 0,
            "duration": v.get("duration") or 0,
            "license": lic,
            "artist": (v.get("user") or {}).get("name") or "",
        }
        if not license_ok(lic):
            continue
        items.append(item)
    return rank(items, min_sec)[: int(limit)]


def cmd_search(args):
    if getattr(args, "pexels", False) and not os.environ.get("PEXELS_API_KEY"):
        print("PEXELS_API_KEY", file=sys.stderr)
        return 2
    try:
        items = _search_commons(args.keyword, args.limit, args.min_sec)
        if os.environ.get("PEXELS_API_KEY"):
            items = rank(items + _search_pexels(args.keyword, args.limit, args.min_sec), args.min_sec)[: args.limit]
        if args.json:
            print(json.dumps(items, ensure_ascii=False))
        else:
            for it in items:
                print(f"{it['source']}\t{it['duration']}\t{it['width']}x{it['height']}\t{it['license']}\t{it['url']}")
        return 0
    except SystemExit:
        raise
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1


def cmd_fetch(args):
    out = Path(args.out)
    try:
        out.mkdir(parents=True, exist_ok=True)
        # 先抽進暫存，成功才替換：重抽失敗時舊幀與 clip.json 保持原狀（codex 11-10 複審 P1）
        tmp = Path(tempfile.mkdtemp(dir=out, prefix=".fetch-"))
        try:
            return _fetch(args, out, tmp)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1


def _fetch(args, out, tmp):
    vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    if args.start is not None:
        cmd += ["-ss", str(args.start)]
    cmd += ["-i", args.src]
    if args.secs is not None:
        cmd += ["-t", str(args.secs)]
    cmd += ["-vf", vf, "-r", str(args.fps), str(tmp / "%04d.jpg")]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr.strip() or "ffmpeg failed", file=sys.stderr)
        return 1
    files = sorted(tmp.glob("*.jpg"))
    if not files:
        print(f"ffmpeg 沒抽出任何幀：{args.src}", file=sys.stderr)
        return 1
    if args.sources:   # 出處先記，寫不進去就不動既有素材
        sp = Path(args.sources)
        sp.parent.mkdir(parents=True, exist_ok=True)
        with sp.open("a", encoding="utf-8") as f:
            f.write(f"{args.src}\t{args.license or ''}\t{args.credit or ''}\n")
    # ponytail: 刪舊幀到換新幀之間不是原子操作，中途磁碟出錯會遺失舊幀。
    # 幀是從原片抽的衍生檔，重跑 fetch 即可復原；要原子就改成整個目錄 rename 換版。
    for old in out.glob("*.jpg"):
        old.unlink()
    for f in files:
        f.replace(out / f.name)
    clip = {
        "count": len(files),
        "fps": int(args.fps),
        "w": 1080,
        "h": 1920,
        "src": args.src,
        "license": args.license or "",
        "credit": args.credit or "",
    }
    (out / "clip.json").write_text(json.dumps(clip, ensure_ascii=False), encoding="utf-8")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("search")
    sp.add_argument("keyword")
    sp.add_argument("--limit", type=int, default=5)
    sp.add_argument("--min-sec", type=float, default=3)
    sp.add_argument("--json", action="store_true")
    sp.add_argument("--pexels", action="store_true")
    sp.set_defaults(func=cmd_search)

    fp = sub.add_parser("fetch")
    fp.add_argument("src")
    fp.add_argument("--out", required=True)
    fp.add_argument("--start", type=float, default=0)
    fp.add_argument("--secs", type=float, default=4.0)
    fp.add_argument("--fps", type=int, default=30)
    fp.add_argument("--license", default="")
    fp.add_argument("--credit", default="")
    fp.add_argument("--sources", default=None)
    fp.set_defaults(func=cmd_fetch)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
