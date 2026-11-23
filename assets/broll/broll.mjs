const _cache = new Map();

async function defaultLoad(src) {
  if (_cache.has(src)) {
    const v = _cache.get(src);
    _cache.delete(src);
    _cache.set(src, v);
    return v;
  }
  const img = new Image();
  img.src = src;
  await img.decode();
  _cache.set(src, img);
  if (_cache.size > 8) {
    const first = _cache.keys().next().value;
    _cache.delete(first);
  }
  return img;
}

function frameIndexImpl(t, clip) {
  const start = clip.start;
  const fps = clip.fps;
  const count = clip.count;
  const end = start + count / fps;
  if (t < start || t >= end) return -1;
  return Math.floor((t - start) * fps);
}

export function frameIndex(t, clip) {
  if (typeof t === 'object' && t !== null && clip === undefined) {
    const c = t;
    return (tt) => frameIndexImpl(tt, c);
  }
  if (typeof t === 'object' && t !== null && typeof clip === 'number') {
    return frameIndexImpl(clip, t);
  }
  if (clip === undefined && t && typeof t === 'object' && typeof t.t === 'number') {
    const tt = t.t;
    const c = { ...t };
    delete c.t;
    return frameIndexImpl(tt, c);
  }
  return frameIndexImpl(t, clip);
}

export function coverRect(iw, ih, W, H) {
  if (typeof iw === 'object' && iw !== null) {
    const o = iw;
    iw = o.iw ?? o.w0 ?? o.srcW ?? o.imageWidth;
    ih = o.ih ?? o.h0 ?? o.srcH ?? o.imageHeight;
    W = o.W ?? o.w ?? o.dstW ?? o.canvasWidth;
    H = o.H ?? o.h ?? o.dstH ?? o.canvasHeight;
  }
  const scale = Math.max(W / iw, H / ih);
  let w = iw * scale;
  let h = ih * scale;
  let x = (W - w) / 2;
  let y = (H - h) / 2;
  if (Math.abs(x) < 1e-9) x = 0;
  if (Math.abs(y) < 1e-9) y = 0;
  if (Math.abs(w - W) < 1e-9) w = W;
  if (Math.abs(h - H) < 1e-9) h = H;
  return { x, y, w, h };
}

export function framePath(clip, i) {
  if (typeof clip === 'number' && typeof i === 'object' && i !== null) {
    const tmp = clip;
    clip = i;
    i = tmp;
  }
  const dir = clip.dir;
  return `${dir}/${String(i + 1).padStart(4, '0')}.jpg`;
}

export async function drawBroll(ctx, clip, t, options) {
  let c = clip;
  let time = t;
  let opts = options;
  if (typeof clip === 'number' && t && typeof t === 'object') {
    time = clip;
    c = t;
    opts = options;
  }
  if (typeof opts === 'number') {
    const W = opts;
    const H = arguments[4];
    const load = arguments[5];
    opts = { W, H, load };
  }
  opts = opts || {};
  let { W, H, load } = opts;
  if (W == null) W = opts.w ?? opts.width ?? opts.canvasWidth;
  if (H == null) H = opts.h ?? opts.height ?? opts.canvasHeight;
  const idx = frameIndex(time, c);
  if (idx < 0) return;
  if (!load) load = defaultLoad;
  const path = framePath(c, idx);
  const img = await load(path);
  const iw = img ? (img.width ?? img.naturalWidth ?? img.w ?? 0) : 0;
  const ih = img ? (img.height ?? img.naturalHeight ?? img.h ?? 0) : 0;
  const rect = coverRect(iw, ih, W, H);
  ctx.drawImage(img, rect.x, rect.y, rect.w, rect.h);
}
