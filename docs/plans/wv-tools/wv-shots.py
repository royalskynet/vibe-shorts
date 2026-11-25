import sys, subprocess
v, thr = sys.argv[1], float(sys.argv[2])
W, H = 96, 34
raw = subprocess.run(["ffmpeg","-v","error","-i",v,"-vf","fps=1,crop=iw:ih*0.68:0:ih*0.1,scale=96:34,format=gray","-f","rawvideo","-"],capture_output=True).stdout
fr = [raw[i:i+W*H] for i in range(0, len(raw)-W*H+1, W*H)]
anchor, start, shots, gaps = fr[0], 0, [0], []
for i, f in enumerate(fr):
    d = sum(abs(a-b) for a, b in zip(f, anchor)) / (W*H)
    if d > thr:
        gaps.append((i-start, start)); anchor, start = f, i; shots.append(i)
gaps.append((len(fr)-start, start))
g, at = max(gaps)
print(f"{len(shots)} {g} {at}")
