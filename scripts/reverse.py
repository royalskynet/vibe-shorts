#!/usr/bin/env python3
"""③ 逆向短片：對標短片切鏡 → 畫面字 OCR → 口播歸屬 → 結構化輸出。
   只重用 breakdown.process 與 breakdown.hook，不改 breakdown.py。
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import breakdown as bp  # noqa: E402


def clean_ocr_text(text):
    """只留中文字與數字，去空白。"""
    return "".join(ch for ch in text if ("\u4e00" <= ch <= "\u9fff") or ch.isdigit())


def ocr_frames(paths):
    """Vision OCR（scripts/vocr.swift），一次批次跑完；回 JSON 陣列，一張一格。"""
    r = subprocess.run(["swift", str(SCRIPT_DIR / "vocr.swift"), *map(str, paths)],
                       capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        raise RuntimeError(f"vocr 失敗 rc={r.returncode}：{r.stderr.strip()[-300:]}")
    return [clean_ocr_text(x) for x in parse_vocr(r.stdout, len(paths))]


def parse_vocr(stdout, n):
    """vocr.swift 的 JSON 陣列 → n 格字串；格數不符或型別不對就丟錯，不讓幀與字錯位。"""
    texts = json.loads(stdout)
    if not isinstance(texts, list) or len(texts) != n or not all(isinstance(x, str) for x in texts):
        raise RuntimeError(f"vocr 輸出要 {n} 格字串陣列，拿到：{stdout[:200]!r}")
    return texts

def assign_speech(shots, segments):
    """把每段逐字稿歸給重疊秒數最多的鏡頭。傳回 {shot_id: 文字}"""
    shot_map = {}
    for seg in segments:
        t0, t1 = seg["t0"], seg["t1"]
        best_shot = None
        best_overlap = -1.0
        for shot in shots:
            s0, s1 = shot["start"], shot["end"]
            overlap = max(0.0, min(t1, s1) - max(t0, s0))
            if overlap > best_overlap:
                best_overlap = overlap
                best_shot = shot
        if best_shot is not None:
            sid = best_shot["id"]
            shot_map[sid] = shot_map.get(sid, "") + seg["text"]
    return shot_map

def cjk_per_sec(text, seconds):
    """中文字數／秒。seconds≤0 回 0。"""
    if seconds <= 0:
        return 0
    cjk = re.findall(r"[\u4e00-\u9fff]", text)
    return len(cjk) / seconds

def main():
    ap = argparse.ArgumentParser(description="逆向短片")
    ap.add_argument("input", help="YouTube 網址或本機 mp4 檔案")
    ap.add_argument("--out", default=None, help="輸出目錄（預設 refs/rev-<影片 ID 或檔名主幹>）")
    a = ap.parse_args()

    inp = a.input
    out_dir = Path(a.out) if a.out else None

    if out_dir is None:
        if inp.startswith("http"):
            import re
            m = re.search(r'(?:shorts/|watch\?v=)([^&/]+)', inp)
            vid = m.group(1) if m else "unknown"
        else:
            vid = Path(inp).stem
        out_dir = Path("refs") / f"rev-{vid}"
    else:
        out_dir = Path(out_dir)

    out_dir.mkdir(parents=True, exist_ok=True)

    # -----------------------------------------------------------------
    # 1. Prepare video file (download or copy)
    # -----------------------------------------------------------------
    video_path = out_dir / "ref.mp4"

    if inp.startswith("http"):
        cmd = [
            "yt-dlp",
            inp,
            "--no-warnings",
            "--merge-output-format", "mp4",
            "-o", str(video_path),
            "--write-info-json",
            "--no-write-playlist-metafiles",
            "-f", "bv*[height<=1920]+ba/b"
        ]
        subprocess.run(cmd, check=True, timeout=600)
    else:
        shutil.copy2(inp, video_path)

    # -----------------------------------------------------------------
    # 2. Run breakdown.process (reuses existing logic)
    # -----------------------------------------------------------------
    bp.process(out_dir, str(video_path))

    # -----------------------------------------------------------------
    # 3. Load shots and transcript
    # -----------------------------------------------------------------
    shots_path = out_dir / "shots" / "shots.json"
    with open(shots_path, "r", encoding="utf-8") as f:
        shots_doc = json.load(f)
    shots_data = shots_doc["shots"]

    tr_path = out_dir / "transcript.json"
    with open(tr_path, "r", encoding="utf-8") as f:
        tr_data = json.load(f)

    segments = tr_data.get("segments", [])
    words = tr_data.get("words", [])

    # -----------------------------------------------------------------
    # 4. Extract middle frame for each shot and OCR
    # -----------------------------------------------------------------
    evidence_dir = out_dir / "evidence" / "frames"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    frames = []
    for shot in shots_data:
        mid = (shot["start"] + shot["end"]) / 2.0
        frame_path = evidence_dir / f"{shot['id']}.png"
        subprocess.run(
            ["ffmpeg", "-y", "-ss", f"{mid:.3f}", "-i", str(video_path), "-vframes", "1", str(frame_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        frames.append(frame_path)
    for shot, text in zip(shots_data, ocr_frames(frames)):
        shot["ocr"] = text

    # -----------------------------------------------------------------
    # 5. Assign speech per shot
    # -----------------------------------------------------------------
    speech_map = assign_speech(shots_data, segments)

    # -----------------------------------------------------------------
    # 6. Compute cjk_per_sec per shot
    # -----------------------------------------------------------------
    for shot in shots_data:
        shot["cjk_per_sec"] = cjk_per_sec(shot.get("ocr", ""), shot["seconds"])

    # -----------------------------------------------------------------
    # 6. Assign speech to each shot (already done above)
    # -----------------------------------------------------------------
    for shot in shots_data:
        shot["speech"] = speech_map.get(shot["id"], "")

    # -----------------------------------------------------------------
    # 7. Build reverse.json
    # -----------------------------------------------------------------
    duration = shots_doc.get("meta", {}).get("durationSeconds", 0)
    hook_text = bp.hook(words)

    reverse_shots = []
    for shot in shots_data:
        reverse_shots.append({
            "id": shot["id"],
            "start": shot["start"],
            "end": shot["end"],
            "seconds": shot["seconds"],
            "motion": shot.get("motion", 0),
            "ocr": shot.get("ocr", ""),
            "speech": shot.get("speech", ""),
        })

    reverse_data = {
        "source": inp,
        "duration": duration,
        "hook": hook_text,
        "shots": reverse_shots,
    }

    with open(out_dir / "reverse.json", "w", encoding="utf-8") as f:
        json.dump(reverse_data, f, ensure_ascii=False, indent=1)

    # -----------------------------------------------------------------
    # 8. Write REVERSE.md
    # -----------------------------------------------------------------
    md_lines = []
    md_lines.append("## 觀察到")
    for shot in shots_data:
        md_lines.append(
            f"- {shot['id']}: {shot['seconds']:.1f}s, 畫面文字: {shot.get('ocr','')} , 口播: {shot.get('speech','')}"
        )

    md_lines.append("## 推斷")
    avg_seconds = sum(s["seconds"] for s in shots_data) / len(shots_data) if shots_data else 0
    md_lines.append(f"- 平均鏡長: {avg_seconds:.1f}s")
    total_ocr_text = "".join(shot.get("ocr", "") for shot in shots_data)
    overall_cjk_per_sec = cjk_per_sec(total_ocr_text, sum(s["seconds"] for s in shots_data))
    md_lines.append(f"- 整體字/秒: {overall_cjk_per_sec:.1f}")
    shots_with_ocr = sum(1 for s in shots_data if s.get("ocr"))
    pct_ocr = (shots_with_ocr / len(shots_data)) * 100 if shots_data else 0
    md_lines.append(f"- 有畫面文字的鏡頭比例: {pct_ocr:.1f}%")

    md_lines.append("## 未覆蓋")
    md_lines.extend([
        "- 畫面元素與版面（看 shots/sheets 拼圖）",
        "- 運鏡",
        "- 配樂音效",
        "- 可編輯專案重建",
        "- 逐幀比對",
    ])

    (out_dir / "REVERSE.md").write_text("\n".join(md_lines), encoding="utf-8")
    print(f"Written {out_dir / 'reverse.json'} and {out_dir / 'REVERSE.md'}")

if __name__ == "__main__":
    main()