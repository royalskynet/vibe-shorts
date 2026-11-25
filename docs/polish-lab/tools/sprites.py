import sys, colorsys, numpy as np
from PIL import Image
from scipy import ndimage as ndi
src, outdir, names = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
im = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
dist = np.sqrt(((255 - im) ** 2).sum(2))
fg = dist > 28
fg = ndi.binary_closing(fg, iterations=2)
lab, n = ndi.label(fg)
sizes = ndi.sum(fg, lab, range(1, n + 1))
keep = [i + 1 for i in np.argsort(sizes)[::-1][:len(names)]]
boxes = []
for k in keep:
    sl = ndi.find_objects(lab == k)[0]
    boxes.append((sl[0].start, sl[1].start, sl))
# 排序：先上排（y 近似）再左到右
rows = sorted(boxes, key=lambda b: b[0] // 300 * 10000 + b[1])
for (y0, x0, sl), name, k in zip(rows, names, [keep[[b[2] for b in boxes].index(r[2])] for r in rows]):
    pad = 6
    ys = slice(max(sl[0].start - pad, 0), sl[0].stop + pad); xs = slice(max(sl[1].start - pad, 0), sl[1].stop + pad)
    comp = ndi.binary_fill_holes(lab[ys, xs] == k)
    rgb = im[ys, xs]
    d = dist[ys, xs]
    alpha = np.clip((d - 14) / 30, 0, 1) * comp
    h, w = comp.shape
    # 外套：橘紅、飽和度高、亮度中高
    r, g, b = rgb[..., 0] / 255, rgb[..., 1] / 255, rgb[..., 2] / 255
    mx, mn = np.maximum.reduce([r, g, b]), np.minimum.reduce([r, g, b])
    sat = (mx - mn) / np.maximum(mx, 1e-6)
    coat = (sat > 0.55) & (mx > 0.45) & (r > g) & (g > b * 0.9) & comp
    coat = ndi.binary_opening(coat, iterations=1)
    cm = ndi.gaussian_filter(coat.astype(np.float32), 0.8)
    rest_a = alpha * (1 - cm)
    coat_a = alpha * cm
    # 外套明暗圖：以亮度除以基準橘亮度，供相乘上色
    lum = (0.3 * r + 0.59 * g + 0.11 * b)
    base = lum[coat].mean() if coat.any() else 0.5
    shade = np.clip(lum / base, 0, 1.3) / 1.3
    def save(arr_rgb, a, path):
        out = np.dstack([arr_rgb, a * 255]).astype(np.uint8); Image.fromarray(out, 'RGBA').save(path)
    save(rgb, alpha, f'{outdir}/{name}.png')
    save(rgb, rest_a, f'{outdir}/{name}_rest.png')
    sh = np.repeat((shade * 255)[..., None], 3, 2)
    save(sh, coat_a, f'{outdir}/{name}_coat.png')
    print(name, w, h, 'coat%', round(100 * coat.sum() / comp.sum()))
