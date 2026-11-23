import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "publish"))
from prune_replies import run, summary, PAGE

ok = True
def check(name, got, want):
    global ok
    if got != want:
        ok = False
        print("FAIL", name, got, want)

# 已清空 → 停
check("empty stops", run(lambda: [], lambda ids: True, pause=0), (0, True, None))

# 列表 500 → 不可停（舊版 bug：印 deleted 0 誤觸停止），且原因要帶出來
n, stop, err = run(lambda: (_ for _ in ()).throw(RuntimeError("HTTP 500")), lambda ids: True, pause=0)
check("list error keeps going", (n, stop), (0, False))
check("list error reason", "抓清單失敗" in (err or "") and "500" in (err or ""), True)

# 有刪到東西、下一頁空 → 不停，明天再確認一次
pages = [["a", "b"], []]
check("deleted some keeps going", run(lambda: pages.pop(0), lambda ids: True, pause=0), (2, False, None))

# 上限截斷
check("cap", run(lambda: ["x"] * 10, lambda ids: True, cap=5, pause=0), (5, False, None))

# 刪除失敗 → 原因是限速
check("delete fail keeps going", run(lambda: ["a"], lambda ids: False, pause=0), (0, False, "刪除被拒，多半是被限速"))

# /me/replies limit>=6 必 500，頁大小不准調高（2026-10-17/18 連兩天沒刪成的根因）
check("page size", PAGE <= 5, True)

# 摘要：沒刪成時要寫真正的原因，不可一律說被限速
check("sum done", "全部刪完" in summary(0, True, 0, True), True)
check("sum days", "約 3 天" in summary(95, False, 200, True), True)
check("sum at least", "至少 275" in summary(95, False, 275, False), True)
check("sum zero left", "約 0 天" not in summary(5, False, 0, True) and "全部刪完" in summary(5, False, 0, True), True)
check("sum blocked reason", "抓清單失敗：HTTP 500" in summary(0, False, None, False, err="抓清單失敗：HTTP 500"), True)
check("sum blocked no rate-limit guess", "限速" not in summary(0, False, None, False, err="抓清單失敗：HTTP 500"), True)

def test_all():  # pytest 收集時不能在頂層 sys.exit（會 INTERNALERROR 中斷整套）
    assert ok


if __name__ == "__main__":
    print("ALL PASS" if ok else "FAILED")
    sys.exit(0 if ok else 1)
