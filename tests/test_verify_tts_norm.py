"""verify_tts.norm：opencc 不轉的「著」、Whisper 同音挑字「止」，念對的句子要比得上。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from verify_tts import norm

assert norm("投完，還要有人看著。") == norm("投完还要有人看着"), "著／着 沒歸一"
assert norm("這不只發生在德國。") == norm("这不止发生在德国"), "只／止 沒歸一"
assert norm("二〇一七年還有兩萬六千多個，") == norm("2017年还有26000多个"), "萬位數字沒轉"
assert norm("剩兩千兩百多個。") == norm("剩2200多个"), "兩千／二千 沒歸一"
assert norm("多一萬零五百個") == norm("多10500个"), "萬位後補零錯"
assert norm("兩個寶寶") != norm("二个宝宝"), "「兩個」不該被換成二"
assert norm("市府估計") != norm("是否估计"), "一般字不能被放過"
print("ok")
