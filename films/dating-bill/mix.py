"""你覺得台灣人單身，是因為沒錢嗎 — 旁白＋配樂＋音效。
旁白：out/voice/lines.json（scripts/voice.py 產生，每句在片中的 t0）。
音效：events.json（頁面匯出的 window.EV）。
配樂讓位給旁白：旁白有聲的地方配樂壓低 DUCK_DB（側鏈閃避），句與句之間再浮回來。
用法：LIB=~/dev/lemo-opuscar $LIB/.venv/bin/python mix.py
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.environ.get('LIB') or os.path.expanduser('~/dev/lemo-opuscar')
sys.path.insert(0, os.path.join(LIB, 'core', 'audio'))
from sfx import SR, add, bp, lp, hp, noise, limit, click, clack, thump, whoosh, pop, t_, env_exp  # noqa: E402
import soundfile as sf  # noqa: E402

EV = json.load(open(os.path.join(HERE, 'events.json'), encoding='utf-8'))
LINES = json.load(open(os.path.join(HERE, 'out', 'voice', 'lines.json'), encoding='utf-8'))
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)

DUR = EV['dur']
N = int(DUR * SR)
music = np.zeros((N, 2), np.float32)
fx = np.zeros((N, 2), np.float32)
voice = np.zeros((N, 2), np.float32)

BPM = 120.0          # 跟 index.html 的 BPM 一致：圖案帶每拍跳四分之一格
BEAT = 60.0 / BPM
BAR = BEAT * 4
VOICE_GAIN = 1.0
MUSIC_GAIN = 0.55
DUCK_DB = -11.0      # 旁白講話時配樂壓多少


def kick(v=1.0):
    d = 0.28
    tt = t_(d)
    f = 110 * np.exp(-tt / 0.03) + 46
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(d, 0.08) * v


def hat(v=1.0, d=0.05):
    return hp(noise(d), 7500) * env_exp(d, 0.014) * v * 0.35


def bass(d, f, v=1.0):
    tt = t_(d)
    x = np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * f * 2 * tt)
    e = np.minimum(1, tt / 0.008) * env_exp(d, d * 0.5)
    return lp(x, 600) * e * v * 0.5


def pad(d, freqs, v=1.0):
    tt = t_(d)
    x = sum(np.sin(2 * np.pi * f * tt + i * 0.7) * (0.85 ** i) for i, f in enumerate(freqs))
    e = np.minimum(1, tt / 0.5) * np.minimum(1, (d - tt) / 0.6)
    return lp(x, 1500) * e * v * 0.2


def pluck(d, f, v=1.0):
    tt = t_(d)
    x = np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * f * 3.99 * tt) * np.exp(-tt / 0.05)
    return x * env_exp(d, 0.18) * v * 0.45


def bell(f, v=1.0):
    d = 1.4
    tt = t_(d)
    x = np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 2.76 * tt)
    return x * env_exp(d, 0.4) * v * 0.4


# —— 1. 配樂：F 大調 F–Am–Dm–Bb 循環，暖色、不懸疑；脈動低音＋輕鼓 ——
F2, A2, D3, Bb2 = 87.3, 110.0, 146.8, 116.5
C4, D4, E4, F4, G4, A4, Bb4, C5, D5, E5, F5 = 261.6, 293.7, 329.6, 349.2, 392.0, 440.0, 466.2, 523.3, 587.3, 659.3, 698.5
PROG = [(F2 * 2, [F4, A4, C5]), (A2 * 2, [E4, A4, C5]), (D3, [D4, F4, A4]), (Bb2 * 2, [D4, F4, Bb4])]
for b in range(int(DUR / BAR) + 1):
    t0 = b * BAR
    root, notes = PROG[b % 4]
    add(music, pad(BAR, notes, 0.5), t0, pan=0.05)
    for i in range(8):
        add(music, bass(BEAT * 0.4, root / 2 * (2 if i % 4 == 3 else 1), 0.5), t0 + i * BEAT / 2, pan=-0.06)
    if b >= 1:
        for i in range(4):
            add(music, kick(0.4 if i in (0, 2) else 0.18), t0 + i * BEAT)
        for i in range(8):
            add(music, hat(0.28 if i % 2 else 0.4), t0 + i * BEAT / 2, pan=0.18)
    if b % 2 == 0:
        for i, n in enumerate([C5, A4, F5, E5]):
            add(music, pluck(BEAT * 0.9, n, 0.28), t0 + i * BEAT * 0.75, pan=-0.14)

# —— 2. 音效 ——
for e in EV['ev']:
    t, k, L = float(e['t']), e['type'], float(e.get('len', 0) or 0)
    if k == 'whoosh':
        add(fx, whoosh(0.32, 0.28), t)
    elif k == 'turn':                       # 換卡：一聲輕撥弦（F4），取代刷聲（使用者 10-14 嫌刺耳）
        add(fx, lp(pluck(0.6, 349.2, 0.5), 3000), t)
    elif k == 'pop':
        add(fx, pop(0.22), t)
    elif k == 'ticks':                      # 計數器跑動
        n = int(L / 0.06)
        for i in range(n):
            add(fx, click(1.4 + 0.5 * i / n, 0.08), t + i * 0.06, pan=0.14)
    elif k == 'stamp':
        add(fx, thump(0.7, 52), t)
        add(fx, clack(0.65, 0.32), t + 0.004)
    elif k == 'swish':                      # 鈔票被抽走
        n = int(L / 0.09)
        for i in range(n):
            add(fx, lp(whoosh(0.14, 0.08), 2200), t + i * 0.09, pan=-0.3 + 0.6 * (i % 2))
    elif k == 'bell':
        for i, n in enumerate([F5, C5, A4 * 2]):
            add(fx, bell(n, 0.4 - i * 0.07), t + i * 0.16, pan=0.1 * i)
    elif k == 'bed':
        pass
    else:
        raise SystemExit(f'未知的事件類型 {k}（頁面 EV 跟 mix.py 對不上）')

# —— 3. 旁白 ——
for ln in LINES['lines']:
    x, sr = sf.read(os.path.join(HERE, 'out', 'voice', ln['file']), dtype='float32', always_2d=True)
    if sr != SR:
        raise SystemExit(f'{ln["file"]} 取樣率 {sr}，要 {SR}（重跑 scripts/voice.py）')
    s = int(ln['t0'] * SR)
    e = min(N, s + len(x))
    voice[s:e] += x[:e - s, :2] * VOICE_GAIN

# 側鏈閃避：旁白包絡（10ms 起、250ms 放）→ 配樂增益
env = np.abs(voice).max(axis=1)
att, rel = np.exp(-1 / (0.01 * SR)), np.exp(-1 / (0.25 * SR))
follow = np.zeros(N, np.float32)
lvl = 0.0
for i in range(0, N, 64):                   # 每 64 個樣本算一次，夠細且快
    v = env[i:i + 64].max()
    lvl = v + (lvl - v) * (att ** 64 if v > lvl else rel ** 64)
    follow[i:i + 64] = lvl
duck = 10 ** (DUCK_DB / 20 * np.clip(follow / 0.05, 0, 1))
music *= (MUSIC_GAIN * duck)[:, None]
# 提問句講完配樂就收掉：片尾 1 秒多的純配樂會讓 Whisper 幻聽出「明镜与点点栏目」，旁白核對判片尾不是提問句。
END = int(LINES['lines'][-1]['t1'] * SR)
music[END:] *= np.linspace(1, 0, N - END)[:, None] ** 3

buf = music + fx * 0.8 + voice


def fade(x, a, b):
    y = x.copy()
    ia, ib = int(a * SR), int(b * SR)
    y[:ia] *= np.linspace(0, 1, ia)
    y[len(y) - ib:] *= np.linspace(1, 0, ib)
    return y


for c in range(2):
    buf[:, c] = fade(buf[:, c], 0.02, 0.8)
    buf[:, c] = limit(np.tanh(buf[:, c] * 1.1) * 0.9, 0.5)   # 0.89 時 mux 拉到 -14 LUFS 峰值 -0.8 dB，超過 -1.2 上限

peak = float(np.abs(buf).max())
rms = float(np.sqrt((buf ** 2).mean()))
vr = float(np.sqrt((voice ** 2).mean()))
mr = float(np.sqrt((music ** 2).mean()))
out = os.path.join(HERE, 'out', 'mix.wav')
sf.write(out, buf, SR)
print(f'{out}  {len(buf) / SR:.2f}s  peak {peak:.3f}  rms {rms:.4f}  旁白/配樂 {20 * np.log10(vr / mr):+.1f} dB')
