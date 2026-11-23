"""營銷號通知：走 `hermes send --to telegram`（Coco profile 憑證、零 token）送到使用者 Telegram，bot 名只當標題。
OpenBot 已於 2026-11-15 移除，原 omb_post 的 hermes 送法搬到這裡。去重由呼叫端負責；失敗回 (False, 說明)，不吞。"""
import os
import shutil
import subprocess

TARGET = os.environ.get("ALERT_HERMES_TARGET", "telegram")


def _bin():
    return os.environ.get("FLEET_HERMES_BIN") or shutil.which("hermes") or os.path.expanduser("~/.local/bin/hermes")


def post(bot, key, text, timeout=30):
    try:
        r = subprocess.run([_bin(), "send", "--to", TARGET, "-q", "-s", bot],
                           input=text, text=True, capture_output=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        return False, f"hermes failed: {type(e).__name__}"
    if r.returncode != 0:
        return False, f"hermes failed: rc={r.returncode} {(r.stderr or '').strip()[:200]}"
    return True, "hermes ok"


def notify(key, title, body, agent="Marketer"):
    text = body.strip()
    if not text:
        return True, "quiet"
    return post(agent, f"notify:{key}", f"{title}\n\n{text}")
