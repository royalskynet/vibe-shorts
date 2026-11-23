"""card_sheet.card_end_times：每張卡取在結束前 0.2 秒，不落到下一張卡。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import card_sheet as cs  # noqa: E402

tl = {"dur": 10.0, "lines": [{"t0": 0.3}, {"t0": 4.25}, {"t0": 7.25}]}
got = cs.card_end_times(tl)
fails = []
if got != [3.8, 6.8, 9.8]:
    fails.append(f"取樣時間 {got} != [3.8, 6.8, 9.8]")
# 每個取樣點都要落在自己那張卡裡（起點 ≤ t < 下一張起點）
starts = [0.0, 4.0, 7.0, 10.0]
if not all(starts[i] <= t < starts[i + 1] for i, t in enumerate(got)):
    fails.append("取樣點跑到別張卡")
short = cs.card_end_times({"dur": 1.0, "lines": [{"t0": 0.0}, {"t0": 0.3}]})
if not all(t >= 0 for t in short) or short[1] < 0.05:
    fails.append(f"極短卡取樣 {short} 不該早於卡起點")
# 有片尾系列卡（末句 t1 後 0.3 秒進場）：末卡取樣要在片尾卡之前
end = cs.card_end_times({"dur": 83.572, "lines": [{"t0": 0.3, "t1": 70.0}, {"t0": 76.115, "t1": 80.072}]})
if not (75.865 <= end[-1] < 80.372):
    fails.append(f"末卡取樣 {end[-1]} 落到片尾系列卡（應 < 80.372）")
if fails:
    print("FAIL\n  " + "\n  ".join(fails)); sys.exit(1)
print("OK card_sheet 自檢")
