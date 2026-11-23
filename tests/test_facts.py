"""facts.py check：缺段、條數不足、缺 URL、有數字沒口徑都要擋；合格表要過。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import facts as f

ok = 0
def check(name, cond):
    global ok
    if not cond:
        print("FAIL", name); sys.exit(1)
    ok += 1

line = "{n}. 尖峰兩側站載客較多｜16,220 vs 12,745（口徑：一座梯、一週五個早上尖峰合計）｜https://tfl.gov.uk/x（2016-03）｜「approximately 16,220」"
good = "## 題目\nx\n## 已查證事實\n" + "\n".join(line.format(n=i) for i in range(1, 9)) + \
       "\n## 反直覺候選\n- a｜第 1 條\n## 參考爆款\n- YouTube｜1 播放\n## 未查證／查不到\n- 無\n"
check("合格表過", f.problems(good) == [])
check("缺段擋", any("缺段" in p for p in f.problems(good.replace("## 參考爆款", "## 爆款"))))
check("條數不足擋", any("至少" in p for p in f.problems(good.replace(line.format(n=8) + "\n", ""))))
check("沒口徑擋", any("口徑" in p for p in f.problems(good.replace("（口徑：一座梯、一週五個早上尖峰合計）", "", 1))))
check("沒 URL 擋", any("URL" in p for p in f.problems(good.replace("https://tfl.gov.uk/x", "TfL", 1))))
check("數字欄無數字免口徑", f.problems(good.replace("16,220 vs 12,745（口徑：一座梯、一週五個早上尖峰合計）", "—", 1)) == [])
check("不到四欄擋", any("四欄" in p for p in f.problems(good.replace(line.format(n=3), "3. 只有一欄", 1))))
print(f"OK facts 自檢 {ok}/{ok}")
