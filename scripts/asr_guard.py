"""whisper 幻聽守門：段落大半落在真實靜音裡就丟。

whisper 對數位靜音會吐固定句（例：「请不吝点赞 订阅 转发 打赏支持明镜与点点栏目」），
11-10 實測該段 no_speech_prob=0、avg_logprob=-0.1，模型自評抓不到，hallucination_silence_threshold 也沒擋；
所以改量音訊本身：ffmpeg silencedetect 給靜音區間，用重疊比例判斷。
ponytail: 只擋靜音上的幻聽；純配樂段的幻聽（音量不低）擋不到，要擋就換 VAD（silero）。
"""
import re
import subprocess

NOISE_DB = -50      # 低於這個音量算靜音
MIN_SILENCE = 0.3   # 秒，短於這個的停頓不算
MAX_QUIET = 0.8     # 段落靜音占比達到這個就丟


def silences(path):
    """回傳 [(起, 訖)] 靜音區間（秒）；檔尾靜音沒有 silence_end，訖記成 inf。"""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
                        "-af", f"silencedetect=n={NOISE_DB}dB:d={MIN_SILENCE}", "-f", "null", "-"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"silencedetect 失敗：{r.stderr.strip()[-300:]}")
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: (-?[\d.]+)", r.stderr)]
    ends += [float("inf")] * (len(starts) - len(ends))
    return list(zip(starts, ends))


def voiced(segments, quiet_spans, max_quiet=MAX_QUIET):
    """留下靜音占比 < max_quiet 的 whisper 段落（看 start／end 欄）。"""
    keep = []
    for s in segments:
        dur = s["end"] - s["start"]
        quiet = sum(max(0.0, min(s["end"], b) - max(s["start"], a)) for a, b in quiet_spans)
        if dur <= 0 or quiet / dur < max_quiet:
            keep.append(s)
    return keep
