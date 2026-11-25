// AI 生成的小人精靈圖：同一份 person(g, o) 介面，外套用明暗圖相乘上色，動作仍是 t 的純函數。
const POSES = ['stand', 'armsUp', 'point', 'think', 'shrug', 'walk'];
const VARIANT = { worried: ['stand', 'think', 'shrug'].map(p => p + '_w'), none: ['stand', 'armsUp', 'point'].map(p => p + '_n') };
const FILES = [...POSES, ...VARIANT.worried, ...VARIANT.none];
const SUF = { worried: '_w', none: '_n' };
const PROPIMG = {}, AI_PROPS = ['bulb', 'document', 'flag', 'speech', 'crown', 'gear'];
const IMG = {}, TINT = new Map();
export async function loadSprites(base, propBase = base.replace(/sprites\/$/, 'props/')) {
  await Promise.all(AI_PROPS.map(async n => { const im = new Image(); im.src = `${propBase}${n}.png`; await im.decode(); PROPIMG[n] = im; }));
  await Promise.all(FILES.flatMap(p => ['', '_rest', '_coat'].map(async s => {
    const im = new Image(); im.src = `${base}${p}${s}.png`; await im.decode(); IMG[p + s] = im;
  })));
}
const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
function tinted(pose, col) {
  const key = pose + col; let c = TINT.get(key);
  if (c) return c;
  const im = IMG[pose + '_coat'], rest = IMG[pose + '_rest'];
  c = document.createElement('canvas'); c.width = im.naturalWidth; c.height = im.naturalHeight;
  const x = c.getContext('2d'), [r, g, b] = hex(col).map(v => Math.min(255, v * 1.3));
  x.fillStyle = `rgb(${r | 0},${g | 0},${b | 0})`; x.fillRect(0, 0, c.width, c.height);
  x.globalCompositeOperation = 'multiply'; x.drawImage(im, 0, 0);
  x.globalCompositeOperation = 'destination-in'; x.drawImage(im, 0, 0);
  x.globalCompositeOperation = 'source-over'; x.drawImage(rest, 0, 0);
  if (TINT.size > 600) TINT.clear();
  TINT.set(key, c); return c;
}
export function person(g, o = {}) {
  let pose = POSES.includes(o.pose) ? o.pose : 'stand';
  const v = pose + (SUF[o.face] || '');
  if (IMG[v]) pose = v;
  const im = IMG[pose], H = im.naturalHeight, Wd = im.naturalWidth, k = (o.s || 100) / (H - 12);
  const t = o.t || 0;
  g.save(); g.translate(o.x || 0, o.y || 0);
  if (o.alpha != null) g.globalAlpha *= o.alpha;
  if (o.shadow !== false) {
    const rx = Wd * k * 0.42; g.save(); g.scale(1, 0.16);
    const gr = g.createRadialGradient(0, 0, 0, 0, 0, rx);
    gr.addColorStop(0, 'rgba(70,45,30,0.38)'); gr.addColorStop(1, 'rgba(70,45,30,0)');
    g.fillStyle = gr; g.beginPath(); g.arc(0, 0, rx, 0, 7); g.fill(); g.restore();
  }
  if (pose === 'walk') { g.translate(0, -Math.abs(Math.cos(t * 9)) * 4 * k); g.rotate(Math.sin(t * 9) * 0.02); }
  if (o.tilt) g.rotate(o.tilt);
  if ((o.dir ?? 1) < 0) g.scale(-1, 1);
  g.scale(k, k); g.translate(-Wd / 2, -(H - 6));
  g.drawImage(o.body ? tinted(pose, o.body) : im, 0, 0);
  g.restore();
}

const GLOW = (g, t, on) => {
  const gl = g.createRadialGradient(0, -16, 4, 0, -16, 62);
  gl.addColorStop(0, `rgba(240,196,92,${0.55 * on})`); gl.addColorStop(1, 'rgba(240,196,92,0)');
  g.fillStyle = gl; g.beginPath(); g.arc(0, -16, 62, 0, 7); g.fill();
};
export function propSprite(g, name, o = {}, fallback) {
  const im = PROPIMG[name];
  if (!im) return fallback(g, name, o);
  g.save(); g.translate(o.x || 0, o.y || 0);
  const k = (o.s || 100) / 100; g.scale(k, k);
  if (o.alpha != null) g.globalAlpha *= o.alpha;
  const W = im.naturalWidth, H = im.naturalHeight;
  if (name === 'bulb') {
    const on = o.on ?? 1; if (on > 0) GLOW(g, o.t || 0, on * (0.8 + 0.2 * Math.sin((o.t || 0) * 3)));
    const h = 72, w = W * h / H; g.drawImage(im, -w / 2, -16 - h / 2, w, h);
  } else if (name === 'document') {
    const h = 104, w = W * h / H; g.drawImage(im, -w / 2, -h / 2, w, h);
  } else if (name === 'flag') {
    const sw = Math.sin((o.t || 0) * 2.6) * 0.04, h = 104, w = W * h / H;
    g.save(); g.scale(1, 0.18); g.fillStyle = 'rgba(70,45,30,0.3)'; g.beginPath(); g.arc(0, 0, 12, 0, 7); g.fill(); g.restore();
    g.translate(0, 0); g.rotate(sw); g.drawImage(im, -w * 0.12, -h, w, h);
  } else if (name === 'speech') {
    const w = 120, h = H * w / W;
    if ((o.tail ?? 'left') === 'right') g.scale(-1, 1);
    g.drawImage(im, -w / 2, -h / 2, w, h);
    g.scale((o.tail ?? 'left') === 'right' ? -1 : 1, 1);
    g.fillStyle = '#6b5a4e'; for (let i = -1; i <= 1; i++) { g.beginPath(); g.arc(i * 17, -6, 5, 0, 7); g.fill(); }
  }
  g.restore();
}

export function crownSprite(g, x, y, s) {
  const im = PROPIMG.crown, h = s * im.naturalHeight / im.naturalWidth;
  g.drawImage(im, x - s / 2, y - h, s, h);
}
export function gearSprite(g, x, y, r, rot = 0) {
  const im = PROPIMG.gear, d = r * 2.6;
  g.save(); g.translate(x, y); g.rotate(rot); g.drawImage(im, -d / 2, -d / 2, d, d); g.restore();
}
