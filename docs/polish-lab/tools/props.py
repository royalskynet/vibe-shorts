import sys, numpy as np
from PIL import Image
from scipy import ndimage as ndi
src, outdir, names = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
im = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
d = np.sqrt(((255 - im) ** 2).sum(2))
fg = ndi.binary_closing(d > 22, iterations=3)
lab, n = ndi.label(fg)
sizes = ndi.sum(fg, lab, range(1, n + 1))
keep = list(np.argsort(sizes)[::-1][:len(names)] + 1)
objs = [(k, ndi.find_objects(lab == k)[0]) for k in keep]
objs.sort(key=lambda o: ((o[1][0].start + o[1][0].stop) // 2) // 360 * 10000 + o[1][1].start)
for (k, sl), name in zip(objs, names):
    comp = ndi.binary_fill_holes(lab[sl] == k)
    a = np.clip(ndi.gaussian_filter(comp.astype(np.float32), 0.9) * 1.4 - 0.2, 0, 1)
    out = np.dstack([im[sl], a * 255]).astype(np.uint8)
    Image.fromarray(out).save(f'{outdir}/{name}.png')
    print(name, comp.shape[1], comp.shape[0])
