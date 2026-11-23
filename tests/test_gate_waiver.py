import sys, tempfile, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from precheck import gate_waived, parse_narration, story_problems, contrast_problems

with tempfile.TemporaryDirectory() as t:
    film = Path(t)
    narr = film / "narration.md"
    narr.write_text("## 卡1\n我覺得這件事不是壞事，而是一個很長很長很長很長很長很長很長很長很長很長很長的句子。\n", encoding="utf-8")
    assert story_problems(parse_narration(narr.read_text(encoding="utf-8"))) and contrast_problems(narr.read_text(encoding="utf-8"))
    assert not gate_waived(film)
    (film / "audit").mkdir()
    sha = hashlib.sha256(narr.read_bytes()).hexdigest()
    w = film / "audit" / "gate-waiver.md"
    w.write_text(f"narration_sha: {sha}\n放行：使用者原話\n", encoding="utf-8")
    assert gate_waived(film)
    w.write_text(f"narration_sha: {sha}\n", encoding="utf-8")
    assert not gate_waived(film), "沒有使用者原話不得放行"
    w.write_text(f"narration_sha: {sha}\n放行：使用者原話\n", encoding="utf-8")
    narr.write_text(narr.read_text(encoding="utf-8") + "改稿\n", encoding="utf-8")
    assert not gate_waived(film), "改稿後豁免必須失效"
print("GATE_WAIVER_OK")
