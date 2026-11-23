import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts" / "publish"))
import yt_upload  # noqa: E402

yt_upload.check_channel(yt_upload.CHANNEL_ID)
try:
    yt_upload.check_channel("UCLJ4s0a-0FWRxGIU8SPVJxw")
except SystemExit:
    pass
else:
    raise AssertionError("個人頻道應被擋")
print("ok")
