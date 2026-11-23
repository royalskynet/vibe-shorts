#!/usr/bin/env python3
"""三平台換大頭貼。平台沒有換頭貼的 API，走 cdp.py 那個已登入的專用 Chrome 點網頁。

  avatar.py <png>                    YouTube、IG、Threads 都換（對外改動，跑之前要確認）
  avatar.py <png> yt ig              只換列出的平台（yt／ig／threads）
  avatar.py <png> --dry-run          只開編輯頁、確認上傳欄位找得到，不上傳

換完重新載入個人頁截圖到 /tmp/vibe-avatar-<平台>.png，要看過圖才算換成功。
Chrome 沒開先跑 cdp.py launch。系統 python3 跑（.venv 沒裝 playwright）。

2026-11-11 實測的坑：YouTube「自訂相片」的「完成」鈕在 shadow DOM 深處，
get_by_role／has_text 都找不到，只能走訪 shadowRoot 取座標再用滑鼠點。
ponytail: 選擇器綁平台現在的中文介面；改版或換語系會壞，壞了照截圖重找。
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cdp  # noqa: E402
from yt_upload import CHANNEL_ID  # noqa: E402

HANDLE = "paradoxbar.tw"
YT_EDIT = f"https://studio.youtube.com/channel/{CHANNEL_ID}/editing/profile"

# 走訪所有 shadowRoot，找文字剛好是「完成」的按鈕，回傳最後一個的中心座標
FIND_DONE = """() => {
  const out = [];
  const walk = (r) => { for (const e of r.querySelectorAll('*')) {
    if (e.shadowRoot) walk(e.shadowRoot);
    if (/^(BUTTON|YTCP-BUTTON)$/.test(e.tagName) && e.textContent.trim() === '完成') {
      const b = e.getBoundingClientRect();
      if (b.width) out.push([b.x + b.width / 2, b.y + b.height / 2]);
    } } };
  walk(document);
  return out.length ? out[out.length - 1] : null;
}"""


def shot(p, name):
    path = f"/tmp/vibe-avatar-{name}.png"
    p.screenshot(path=path, clip={"x": 0, "y": 0, "width": 1100, "height": 420})
    print(f"  {name}：截圖 {path}")


def yt(p, png, dry):
    p.goto(YT_EDIT, wait_until="domcontentloaded")
    p.wait_for_timeout(8000)
    btn = p.locator("ytcp-profile-image-upload ytcp-button:visible", has_text="變更").first
    if dry:
        print(f"  yt：變更鈕 {btn.count()} 個")
        return
    with p.expect_file_chooser(timeout=10000) as fc:
        btn.click()
    fc.value.set_files(png)
    p.wait_for_timeout(5000)
    xy = p.evaluate(FIND_DONE)
    if not xy:
        raise SystemExit("yt：裁切框的「完成」鈕找不到")
    p.mouse.click(*xy)
    p.wait_for_timeout(4000)
    pub = p.locator("#publish-button").first
    if pub.get_attribute("disabled") is not None:
        raise SystemExit("yt：「發布」鈕還是停用，頭貼沒進編輯狀態")
    pub.click()
    p.wait_for_timeout(10000)
    p.reload(wait_until="domcontentloaded")
    p.wait_for_timeout(8000)
    shot(p, "yt")


def ig(p, png, dry):
    p.goto("https://www.instagram.com/accounts/edit/", wait_until="domcontentloaded")
    p.wait_for_timeout(6000)
    inp = p.locator("input[type=file]")
    if dry:
        print(f"  ig：上傳欄位 {inp.count()} 個")
        return
    inp.first.set_input_files(png)
    p.wait_for_timeout(8000)
    p.goto(f"https://www.instagram.com/{HANDLE}/", wait_until="domcontentloaded")
    p.wait_for_timeout(6000)
    shot(p, "ig")


def threads(p, png, dry):
    url = f"https://www.threads.com/@{HANDLE}"
    p.goto(url, wait_until="domcontentloaded")
    p.wait_for_timeout(6000)
    p.get_by_text("編輯個人檔案", exact=True).first.click(timeout=10000)
    p.wait_for_timeout(3000)
    inp = p.locator("input[type=file]")
    if dry:
        print(f"  threads：上傳欄位 {inp.count()} 個")
        p.keyboard.press("Escape")
        return
    inp.first.set_input_files(png)
    p.wait_for_timeout(6000)
    p.locator("[role=dialog]").last.get_by_text("完成", exact=True).first.click(timeout=10000)
    p.wait_for_timeout(6000)
    p.goto(url, wait_until="domcontentloaded")
    p.wait_for_timeout(6000)
    shot(p, "threads")


STEPS = {"yt": yt, "ig": ig, "threads": threads}


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    if not args or not Path(args[0]).is_file():
        print(__doc__)
        sys.exit(2)
    png = str(Path(args[0]).resolve())
    names = args[1:] or list(STEPS)
    bad = [n for n in names if n not in STEPS]
    if bad:
        raise SystemExit(f"不認得的平台：{' '.join(bad)}（只有 yt／ig／threads）")
    p = cdp.page()
    for n in names:
        STEPS[n](p, png, dry)


if __name__ == "__main__":
    main()
