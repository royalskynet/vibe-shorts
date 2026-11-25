// 場景層：紙質底、光、遠景、塵粒、鏡頭推進。全部是 t 的純函數；顆粒圖只在載入時畫一次（固定種子）。
const W = 1080, H = 1920;
function rng(seed) { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

let grain = null, paper = null;
function mk(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
function buildGrain() {
  const c = mk(540, 960), x = c.getContext('2d'), r = rng(7);
  const im = x.createImageData(540, 960);
  for (let i = 0; i < im.data.length; i += 4) {
    const v = r() < 0.5 ? 0 : 255, a = Math.floor(r() * 16);
    im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = a;
  }
  x.putImageData(im, 0, 0);
  x.globalAlpha = 0.05; x.strokeStyle = '#8c7b6b'; x.lineWidth = 1;
  for (let i = 0; i < 420; i++) { const px = r() * 540, py = r() * 960, a = r() * 6.28, l = 6 + r() * 16; x.beginPath(); x.moveTo(px, py); x.lineTo(px + Math.cos(a) * l, py + Math.sin(a) * l); x.stroke(); }
  return c;
}
function buildPaper(top, mid, bot) {
  const c = mk(W, H), x = c.getContext('2d');
  const lg = x.createLinearGradient(0, 0, 0, H);
  lg.addColorStop(0, top); lg.addColorStop(0.45, mid); lg.addColorStop(1, bot);
  x.fillStyle = lg; x.fillRect(0, 0, W, H);
  const rg = x.createRadialGradient(W * 0.5, H * 0.42, 120, W * 0.5, H * 0.42, 1250);
  rg.addColorStop(0, 'rgba(255,248,232,0.55)'); rg.addColorStop(0.55, 'rgba(255,248,232,0)'); rg.addColorStop(1, 'rgba(120,92,70,0.22)');
  x.fillStyle = rg; x.fillRect(0, 0, W, H);
  return c;
}

export function backdrop(g, o = {}) {
  const tone = o.tone || { top: '#fbf4e8', mid: '#f5ebdb', bot: '#eadcc6' };
  const key = tone.top + tone.mid + tone.bot;
  if (!paper || paper.key !== key) paper = { key, c: buildPaper(tone.top, tone.mid, tone.bot) };
  g.drawImage(paper.c, 0, 0);
  const gl = o.glow || { x: 300, y: 520, r: 760, col: '255,226,170' };
  const rg = g.createRadialGradient(gl.x, gl.y, 0, gl.x, gl.y, gl.r);
  rg.addColorStop(0, `rgba(${gl.col},0.42)`); rg.addColorStop(1, `rgba(${gl.col},0)`);
  g.fillStyle = rg; g.fillRect(0, 0, W, H);
}

export function finishGrade(g) {
  if (!grain) grain = buildGrain();
  g.save(); g.globalCompositeOperation = 'multiply'; g.globalAlpha = 0.55; g.drawImage(grain, 0, 0, W, H); g.restore();
  g.save(); g.globalAlpha = 0.5; g.drawImage(grain, 0, 0, W, H); g.restore();
}

export function hills(g, o) {
  const { gy, t = 0, cols = ['#eadcc0', '#e0cda6', '#d6bf93'], amp = [70, 55, 40], speed = [4, 9, 16] } = o;
  cols.forEach((col, i) => {
    const y = gy - 40 - (cols.length - 1 - i) * 52, off = -((t * speed[i]) % 540);
    g.save(); g.fillStyle = col; g.beginPath(); g.moveTo(-10, H);
    for (let x = -10; x <= W + 10; x += 20) g.lineTo(x, y - Math.sin((x + off) / 540 * Math.PI * 2 + i * 1.7) * amp[i] * 0.5 - Math.sin((x + off) / 210 * Math.PI * 2 + i) * amp[i] * 0.18);
    g.lineTo(W + 10, H); g.closePath(); g.fill(); g.restore();
  });
}

export function floor(g, o) {
  const { gy, top = '#e9d7b0', bot = '#eadcc6' } = o;
  const lg = g.createLinearGradient(0, gy - 30, 0, gy + 300);
  lg.addColorStop(0, top); lg.addColorStop(0.5, '#e4d0a8'); lg.addColorStop(1, bot);
  g.save(); g.fillStyle = lg; g.fillRect(0, gy - 30, W, H - gy + 30);
  const mist = g.createLinearGradient(0, gy - 90, 0, gy + 12);
  mist.addColorStop(0, 'rgba(255,246,228,0)'); mist.addColorStop(1, 'rgba(255,246,228,0.5)');
  g.fillStyle = mist; g.fillRect(0, gy - 90, W, 102);
  g.restore();
}

export function motes(g, t, o = {}) {
  const n = o.n ?? 26, r = rng(o.seed ?? 3);
  g.save();
  for (let i = 0; i < n; i++) {
    const x0 = r() * W, y0 = r() * 1250 + 250, sp = 8 + r() * 14, ph = r() * 6.28, sz = 2 + r() * 4.5;
    const x = (x0 + t * sp + Math.sin(t * 0.7 + ph) * 18 + W * 4) % W, y = y0 - ((t * (3 + sp * 0.25)) % 220) + 110 * Math.sin(ph);
    g.globalAlpha = (0.25 + 0.25 * Math.sin(t * 1.6 + ph)) * (o.alpha ?? 1);
    g.fillStyle = o.col || '#fff3d2'; g.beginPath(); g.arc(x, y, sz, 0, 7); g.fill();
  }
  g.restore();
}

export function godray(g, o) {
  const { x = 280, y = -60, w = 360, len = 1500, a = 0.2, t = 0 } = o;
  const sway = Math.sin(t * 0.5) * 10;
  g.save(); g.globalCompositeOperation = 'screen';
  const lg = g.createLinearGradient(x, y, x + 260, y + len);
  lg.addColorStop(0, `rgba(255,236,190,${a})`); lg.addColorStop(1, 'rgba(255,236,190,0)');
  g.fillStyle = lg; g.beginPath(); g.moveTo(x - w * 0.15 + sway, y); g.lineTo(x + w * 0.15 + sway, y);
  g.lineTo(x + 260 + w * 0.6, y + len); g.lineTo(x + 260 - w * 0.6, y + len); g.closePath(); g.fill(); g.restore();
}

export function camera(g, p, o = {}) {
  const { amt = 0.035, cx = 540, cy = 900 } = o;
  const s = 1 + amt * p;
  g.translate(cx, cy); g.scale(s, s); g.translate(-cx, -cy);
}

// AI 背景板：src 地平線在 hz（0–1，圖高比例），貼到畫面 gy
export async function loadPlate(url) { const im = new Image(); im.src = url; await im.decode(); return im; }
export function plate(g, im, o = {}) {
  const { hz = 0.55, gy = 1250 } = o, sh = im.naturalHeight, sw = im.naturalWidth, cut = sh * hz;
  g.drawImage(im, 0, 0, sw, cut, 0, 0, W, gy);
  g.drawImage(im, 0, cut, sw, sh - cut, 0, gy - 1, W, H - gy + 1);
}
