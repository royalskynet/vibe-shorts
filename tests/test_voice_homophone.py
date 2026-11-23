"""單句核稿比拼音：Whisper 吐簡體字與同音字不算念錯（11-07 mrt-escalator 第 16 句、taipei-childcare 第 25 句）。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from voice import similarity as sim

ok = 0
def check(name, cond, detail=""):
    global ok
    if not cond:
        print("FAIL", name, detail); sys.exit(1)
    ok += 1

# 正例：簡體＋同音字（兜战／都站、再到／載到）念對了就要過門檻
s = sim("改成兩邊都站，載到一萬六千兩百二十人，多了快三成。",
        "改成两边兜战再到16220人多了快三成")
check("mrt 第16句 同音字過門檻", s >= 0.90, f"{s:.3f}")
s = sim("市府估計，每週要四十一萬小時臨托，", "是否估计每周要41万小时临拖")
check("childcare 第25句 同音字過門檻", s >= 0.90, f"{s:.3f}")

# 反例：念音明顯不同就要擋下來，不能因為改比拼音就放寬
s = sim("改成兩邊都站，載到一萬六千兩百二十人，多了快三成。",
        "今天天氣很好我們去公園散步")
check("完全不同的句子擋下來", s < 0.90, f"{s:.3f}")
s = sim("市府估計，每週要四十一萬小時臨托，", "市政府說今年預算要刪掉一半")
check("講錯內容擋下來", s < 0.90, f"{s:.3f}")

print(f"ALLPASS {ok}")
