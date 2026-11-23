"""bakeoff 計分：換位一致才算贏、不一致與缺票算和局；verdict 取最後一行。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import bakeoff as b

ok = 0
def check(name, cond):
    global ok
    if not cond:
        print("FAIL", name); sys.exit(1)
    ok += 1

check("x 換位兩次都贏", b.pair_result("A", "B") == "x")
check("y 換位兩次都贏", b.pair_result("B", "A") == "y")
check("位置偏誤（都選 A）＝和", b.pair_result("A", "A") is None)
check("缺票＝和", b.pair_result(None, "B") is None)
s = b.tally(["p", "q", "r"], [("j", "p", "q", "A", "B"), ("j", "p", "r", "A", "A"), ("j", "q", "r", "B", "A")])
check("計分", s == {"p": 1.5, "q": 0.0, "r": 1.5})
check("verdict 取最後一個", b.verdict("WINNER: A 舉例\n理由\nWINNER: TIE") == "TIE")
check("verdict 沒有＝None", b.verdict("我覺得 A 比較好") is None)
check("clean 去 fence 與前言", b.clean("好的，以下是稿：\n```markdown\n## 鉤子\n你好？\n```").startswith("## 鉤子"))
b.RETRY_WAIT = 0
calls = []
def flaky(engine, prompt, cwd):
    calls.append(1)
    if len(calls) < 3:
        raise RuntimeError("deepseek rc=1 Error: the server is overloaded; retry shortly")
    return "WINNER: A"
b.run_once = flaky
check("上游忙會重試到成功", b.run("deepseek", "p", ".") == "WINNER: A" and len(calls) == 3)
def hard(engine, prompt, cwd):
    calls.append(1)
    raise RuntimeError("codex rc=1 not logged in")
calls.clear(); b.run_once = hard
try:
    b.run("codex", "p", "."); check("非忙碌錯誤要丟", False)
except RuntimeError:
    check("非忙碌錯誤不重試", len(calls) == 1)


# ---- TOP.json：機器只讀這個，同分照 codex 評審分 ----
import json, tempfile  # noqa: E402
from pathlib import Path  # noqa: E402

def film_with(tmp, writers):
    film = Path(tmp) / "films" / "t"
    (film / "bakeoff").mkdir(parents=True)
    (film / "FACTS.md").write_text("## 題目\nx\n")
    for w in writers:
        (film / "bakeoff" / f"{w}.md").write_text(f"## 鉤子\n{w.upper()} 稿？\n## 機制\n甲。\n## 轉折\n但乙。\n## 落點\n丙。\n")
    return film

def fake_run(engine, prompt, cwd):
    a = prompt.split("# 稿 A\n", 1)[1].split("# 稿 B\n", 1)[0]
    fav = "opus" if engine == "codex" else "codex"  # 兩個評審各有偏誤，總分一樣
    return "WINNER: A" if fav in a.lower() else "WINNER: B"

with tempfile.TemporaryDirectory() as t:
    film = film_with(t, ["codex", "opus"])
    b.run = fake_run
    check("judge 正常回 0", b.judge(film) == 0)
    top = json.loads((film / "bakeoff/TOP.json").read_text())
    check("TOP 總分相同", {r["name"]: r["total"] for r in top["rank"]} == {"codex": 1.0, "opus": 1.0})
    check("同分照 codex 評審分排", top["top2"] == ["opus", "codex"])
    check("TOP 記各評審分", top["rank"][0]["per_judge"] == {"codex": 1.0, "deepseek": 0.0})
    check("TOP 無缺票", top["missing"] == 0 and top["pairs"] == 4)

with tempfile.TemporaryDirectory() as t:
    film = film_with(t, ["codex", "opus"])
    def half(engine, prompt, cwd):
        if engine == "deepseek":
            return ""  # 沒給 WINNER＝缺票
        return fake_run(engine, prompt, cwd)
    b.run = half
    check("缺票回 3", b.judge(film) == 3)
    top = json.loads((film / "bakeoff/TOP.json").read_text())
    check("TOP 記缺票數", top["missing"] == 2 and top["pairs"] == 4)
    check("缺票仍給前兩名", top["top2"] == ["opus", "codex"])

with tempfile.TemporaryDirectory() as t:
    film = film_with(t, ["opus"])
    check("只有一份稿回 2", b.judge(film) == 2)
    top = json.loads((film / "bakeoff/TOP.json").read_text())
    check("一份稿也寫 TOP", top["top2"] == ["opus"] and len(top["rank"]) == 1)

print(f"OK bakeoff 自檢 {ok}/{ok}")
