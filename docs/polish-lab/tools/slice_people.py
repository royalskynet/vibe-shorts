import sys, glob, numpy as np
from PIL import Image
from scipy import ndimage as ndi
POSES = ['stand','armsUp','point','think','shrug','worry']
def run(src, who, outdir):
    im = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
    dist = np.sqrt(((255 - im) ** 2).sum(2))
    fg = ndi.binary_closing(dist > 28, iterations=3)
    lab, n = ndi.label(fg)
    sizes = ndi.sum(fg, lab, range(1, n + 1))
    keep = [i + 1 for i in np.argsort(sizes)[::-1][:6]]
    objs = []
    for k in keep:
        sl = ndi.find_objects(lab == k)[0]
        objs.append(((sl[0].start+sl[0].stop)/2, (sl[1].start+sl[1].stop)/2, k, sl))
    objs.sort(key=lambda o: o[0]); objs = sorted(objs[:3], key=lambda o: o[1]) + sorted(objs[3:], key=lambda o: o[1])
    crops = []
    for (_, _, k, sl) in objs:
        pad = 6
        ys = slice(max(sl[0].start - pad, 0), sl[0].stop + pad); xs = slice(max(sl[1].start - pad, 0), sl[1].stop + pad)
        comp = ndi.binary_fill_holes(lab[ys, xs] == k)
        rgb = im[ys, xs]; d = dist[ys, xs]
        a = np.clip((d - 14) / 30, 0, 1) * comp
        a_safe = np.maximum(a, 1e-3)[..., None]
        col = np.clip((rgb - 255 * (1 - a[..., None])) / a_safe, 0, 255)
        crops.append(np.dstack([col, a * 255]).astype(np.uint8))
    H = max(c.shape[0] for c in crops); Wd = max(c.shape[1] for c in crops)
    for name, c in zip(POSES, crops):
        canvas = np.zeros((H, Wd, 4), np.uint8)
        h, w = c.shape[:2]
        canvas[H - h:, (Wd - w) // 2:(Wd - w) // 2 + w] = c
        Image.fromarray(canvas).save(f'{outdir}/{who}_{name}.png')
    print(who, 'canvas', Wd, H, 'n', len(crops))
for who in 'ABC':
    run(glob.glob(f'/tmp/agnes/out/ch{who}/*.png')[0], who, '/tmp/mr/people')
