// Model sheet — 林昭 / 假面騎士（概念腰帶）
// 依 cel-anime-80s/STYLE.md §2：球＋下巴頭型、杏仁眼、厚上睫毛、高橢圓虹膜＋兩點高光、
// 分層髮綹＋zigzag 下緣的 angel ring、平塗＋硬邊影＋硬邊光＋有色描邊（非純黑）。
// 契約：window.READY / window.render(t) / window.DUR。靜幀用：--q page=..&cell=..
import { clamp, lerp, seg, eio, eo, mulberry, TAU } from '/core/lib.js';

const W = 1920, H = 1080;
const PAGE = new URLSearchParams(location.search).get('page') || 'all';
const CELL = parseInt(new URLSearchParams(location.search).get('cell') || '-1', 10);
const EXPR = new URLSearchParams(location.search).get('expr') || '';

// 停止條件用：all 頁 DUR=1，render(0) 即出圖
window.DUR = 1;

/* ── 色指定（逐光源一組，不套濾鏡）─────────────────────────
   daylight 為基準；其餘由 fill / shadow / line 分別推導。 */
const P = {
  skin:   '#f7d9c0', skinSh: '#dfa98a', skinLine: '#8a4a3c',
  hair:   '#241d33', hairSh: '#151024', hairHi: '#6d5f9e', hairLine: '#120e1e',
  eye:    '#3f7ac4', eyeDeep:'#1d3f74',
  white:  '#fdfaf4', whiteSh: '#d9d2c6',
  scarf:  '#c8342f', scarfSh:'#8d1f1c', scarfHi:'#f2716a',
  coat:   '#3a3f57', coatSh: '#262a3c', coatHi: '#6a7191',
  belt:   '#d9d3c4', beltSh: '#9c968a', beltLine:'#3a3630',
  core:   '#ff4459', coreHi: '#ffd166',
  bg:     '#1a1c26', bg2: '#262a3c', ink: '#e8e3d6',
  accent: '#ff4459',
};

const rnd = mulberry(20261018);
const noise = [];
for (let i = 0; i < 4096; i++) noise.push(rnd());

/* ── 畫布工具 ─────────────────────────────────────────────── */
function path(ctx, f, close = true) { ctx.beginPath(); f(ctx); if (close) ctx.closePath(); }

// 平塗 → 硬邊影 → 硬邊光 → 有色描邊（順序照 STYLE §2）
function cel(ctx, shape, { fill, sh, hi, line, ink = 2.6, dx = -0.30, dy = -0.34, glow = 0 }) {
  const off = 13;
  ctx.save();
  path(ctx, shape);
  ctx.fillStyle = fill; ctx.fill();

  // 硬邊影：shape − (shape 往光源反方向位移)，even-odd
  if (sh) {
    ctx.save();
    path(ctx, shape); ctx.clip('evenodd');
    ctx.beginPath(); path(ctx, shape);
    ctx.save();
    ctx.translate(-dx * off, -dy * off);
    path(ctx, shape);
    ctx.restore();
    ctx.fillStyle = sh; ctx.fill('evenodd');
    ctx.restore();
  }
  // 硬邊光：同法、往光源方向位移
  if (hi) {
    ctx.save();
    path(ctx, shape); ctx.clip('evenodd');
    ctx.beginPath();
    ctx.save(); ctx.translate(dx * off, dy * off); path(ctx, shape); ctx.restore();
    ctx.fillStyle = hi; ctx.globalAlpha = 0.75; ctx.fill('evenodd');
    ctx.restore();
  }
  if (glow) { ctx.globalAlpha = glow; ctx.fillStyle = P.accent; ctx.fill(); ctx.globalAlpha = 1; }

  if (line) { path(ctx, shape); ctx.lineWidth = ink; ctx.strokeStyle = line; ctx.lineJoin = 'round'; ctx.stroke(); }
  ctx.restore();
}

/* ── 頭部構造（唯一來源；每個鏡頭都從這裡畫）───────────────
   turn: -1 全側(左) … 0 正 … +1 全側(右)；0 與 ±.5 為 3/4。 */
const HEAD = { r: 78, jaw: 96, chin: 44 };

function headShape(cx, cy, turn, scale = 1, jawOpen = 0) {
  const R = HEAD.r * scale, J = (HEAD.jaw + jawOpen * 22) * scale, C = HEAD.chin * scale;
  // 靠近鏡頭側的眼位移（3/4 透視）
  const front = Math.sign(turn) || 1;
  const ex = -turn * R * 0.30;           // 臉部特徵整體往轉向側滑
  return {
    R, J, C, ex, front,
    path(ctx) {
      ctx.beginPath();
      ctx.moveTo(cx - R, cy - R * 0.10);
      ctx.bezierCurveTo(cx - R, cy - R * 1.02, cx - R * 0.52, cy - R * 1.30, cx + ex * 0.5, cy - R * 1.28);
      ctx.bezierCurveTo(cx + R * 0.58, cy - R * 1.26, cx + R, cy - R * 0.98, cx + R, cy - R * 0.10);
      ctx.bezierCurveTo(cx + R, cy + R * 0.62, cx + R * 0.62, cy + J * 0.86, cx + ex * 0.35, cy + C + J * 0.30);
      ctx.bezierCurveTo(cx - R * 0.30, cy + J * 0.96, cx - R * 0.84, cy + J * 0.52, cx - R, cy - R * 0.10);
    },
  };
}

// 杏仁眼：厚上睫毛線外甩、高橢圓虹膜、兩點高光
function eye(ctx, x, y, w, h, turn, blink = 0, tear = 0) {
  if (blink > 0.85) {
    ctx.beginPath(); ctx.moveTo(x - w, y + h * 0.2); ctx.quadraticCurveTo(x, y - h * 0.25 * (1 - blink), x + w, y + h * 0.2);
    ctx.lineWidth = 6; ctx.lineCap = 'round'; ctx.strokeStyle = P.hairLine; ctx.stroke(); return;
  }
  const hh = h * (1 - blink * 0.92);
  const lash = Math.sign(turn) || 1;
  // 眼白
  path(ctx, c => {
    c.moveTo(x - w, y);
    c.quadraticCurveTo(x, y - hh * 1.35, x + w, y - hh * 0.10);
    c.quadraticCurveTo(x, y + hh * 0.98, x - w, y);
  });
  ctx.fillStyle = P.white; ctx.fill();
  ctx.save(); ctx.clip();
  ctx.fillStyle = P.whiteSh; ctx.beginPath(); ctx.rect(x - w, y - hh * 0.2, w * 2.2, hh * 2); ctx.fill();
  // 虹膜（高橢圓）
  const irx = w * 0.62, iry = hh * 1.02;
  ctx.beginPath(); ctx.ellipse(x + w * 0.06, y + hh * 0.06, irx, iry, 0, 0, TAU);
  ctx.fillStyle = P.eyeDeep; ctx.fill();
  ctx.beginPath(); ctx.ellipse(x + w * 0.06, y + hh * 0.14, irx * 0.74, iry * 0.74, 0, 0, TAU);
  ctx.fillStyle = P.eye; ctx.fill();
  // 瞳孔
  ctx.beginPath(); ctx.ellipse(x + w * 0.06, y + hh * 0.06, irx * 0.34, iry * 0.40, 0, 0, TAU);
  ctx.fillStyle = '#0d1330'; ctx.fill();
  // 兩點高光
  ctx.fillStyle = '#ffffff';
  ctx.beginPath(); ctx.ellipse(x - w * 0.22, y - hh * 0.42, irx * 0.30, iry * 0.30, -0.4, 0, TAU); ctx.fill();
  ctx.beginPath(); ctx.arc(x + w * 0.36, y + hh * 0.52, irx * 0.15, 0, TAU); ctx.fill();
  if (tear > 0) {
    ctx.fillStyle = 'rgba(255,255,255,.9)';
    ctx.beginPath(); ctx.ellipse(x + w * 0.10, y + hh * 0.55, irx * 0.5, iry * 0.55, 0, 0, TAU); ctx.fill();
    ctx.globalAlpha = 0.55; ctx.strokeStyle = '#cfe6ff'; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(x - w * 0.6, y + hh * (0.8 + tear * 0.5));
    ctx.quadraticCurveTo(x + w * 0.4, y + hh * (1.1 + tear * 0.5), x + w * 0.8, y + hh * (0.7 + tear)); ctx.stroke();
    ctx.globalAlpha = 1;
  }
  ctx.restore();
  // 下眼線（細，有色）
  ctx.beginPath();
  ctx.moveTo(x - w * 0.86, y + hh * 0.12);
  ctx.quadraticCurveTo(x, y + hh * 1.06, x + w * 0.9, y + hh * 0.06);
  ctx.lineWidth = 2.4; ctx.strokeStyle = P.skinLine; ctx.globalAlpha = 0.8; ctx.stroke(); ctx.globalAlpha = 1;
  // 厚上睫毛線（外甩）
  ctx.beginPath();
  ctx.moveTo(x - w * 1.02, y - hh * 0.05);
  ctx.quadraticCurveTo(x - w * 0.1, y - hh * 1.5, x + w * 1.02, y - hh * 0.02);
  ctx.lineWidth = 7.5 * (1 - blink); ctx.lineCap = 'round'; ctx.strokeStyle = P.hairLine; ctx.stroke();
  // 外眼角睫毛（往轉向側甩）
  ctx.beginPath();
  ctx.moveTo(x + w * 1.02, y - hh * 0.02);
  ctx.quadraticCurveTo(x + w * (1.16 + lash * 0.18), y - hh * 0.30, x + w * (1.30 + lash * 0.22), y - hh * (0.30 + lash * 0.24));
  ctx.lineWidth = 5 * (1 - blink); ctx.stroke();
}

// 眉：情緒主要載體
function brow(ctx, x, y, w, tilt, lift) {
  ctx.beginPath();
  ctx.moveTo(x - w, y + tilt * w * 0.55 + lift);
  ctx.quadraticCurveTo(x, y - w * 0.42 + lift, x + w, y + tilt * w * 0.18 + lift);
  ctx.lineWidth = 6.5; ctx.lineCap = 'round'; ctx.strokeStyle = P.hairLine; ctx.stroke();
}

// 鼻：一個陰影面＋一筆
function nose(ctx, x, y, s = 1) {
  ctx.beginPath();
  ctx.moveTo(x - 7 * s, y + 26 * s); ctx.quadraticCurveTo(x - 1 * s, y + 34 * s, x + 9 * s, y + 30 * s);
  ctx.quadraticCurveTo(x + 2 * s, y + 26 * s, x - 7 * s, y + 26 * s);
  ctx.closePath(); ctx.fillStyle = P.skinSh; ctx.globalAlpha = .85; ctx.fill(); ctx.globalAlpha = 1;
  ctx.beginPath(); ctx.moveTo(x - 2 * s, y + 6 * s); ctx.quadraticCurveTo(x + 6 * s, y + 20 * s, x + 8 * s, y + 29 * s);
  ctx.lineWidth = 3; ctx.strokeStyle = P.skinLine; ctx.globalAlpha = .7; ctx.stroke(); ctx.globalAlpha = 1;
}

// 嘴：情態
function mouth(ctx, x, y, w, kind, open = 0) {
  ctx.lineWidth = 4; ctx.lineCap = 'round'; ctx.strokeStyle = P.skinLine;
  const teeth = () => { ctx.fillStyle = P.white; ctx.fill(); };
  ctx.beginPath();
  switch (kind) {
    case 'smile': ctx.moveTo(x - w, y); ctx.quadraticCurveTo(x, y + w * 0.75, x + w, y); break;
    case 'grin':
      ctx.moveTo(x - w * 1.15, y - w * 0.15); ctx.quadraticCurveTo(x, y + w * 1.15 + open * 14, x + w * 1.15, y - w * 0.15);
      ctx.quadraticCurveTo(x, y + w * 0.20 + open * 6, x - w * 1.15, y - w * 0.15); teeth(); break;
    case 'flat': ctx.moveTo(x - w * 0.8, y); ctx.lineTo(x + w * 0.8, y); break;
    case 'open':
      ctx.moveTo(x - w * 0.85, y - w * 0.1); ctx.quadraticCurveTo(x, y + w * (1.5 + open), x + w * 0.85, y - w * 0.1);
      ctx.quadraticCurveTo(x, y + w * 0.1, x - w * 0.85, y - w * 0.1); teeth(); break;
    case 'shout':
      ctx.moveTo(x - w * 0.7, y - w * 0.3); ctx.quadraticCurveTo(x, y + w * (2.0 + open * 0.5), x + w * 0.7, y - w * 0.3);
      ctx.quadraticCurveTo(x - w * 0.1, y + w * 0.15, x - w * 0.7, y - w * 0.3);
      ctx.fillStyle = '#5e2a2c'; ctx.fill();
      ctx.fillStyle = P.white; ctx.beginPath();
      ctx.moveTo(x - w * 0.66, y - w * 0.28); ctx.quadraticCurveTo(x, y + w * 0.2, x + w * 0.66, y - w * 0.28); ctx.fill();
      break;
    case 'cat':
      ctx.moveTo(x - w, y + w * 0.2); ctx.quadraticCurveTo(x - w * 0.45, y - w * 0.2, x, y + w * 0.1);
      ctx.quadraticCurveTo(x + w * 0.45, y - w * 0.2, x + w, y + w * 0.2); break;
  }
  ctx.stroke();
}

// 髮：整顆頭是一條連續外輪廓。相位固定 ph 0 = 頭頂（sin 的 -π/2），
// 0.25 = 右側、0.5 = 下巴、0.75 = 左側。上緣與下襬各自用平滑函式，
// 不加逐槽鋸齒（那會變星芒）——不齊感改由「方向性法線抖動」給。
const HAIR = { rx: 1.19, ry: 1.30, cy: 0.10 };

const ph2a = ph => ph * TAU - Math.PI / 2;   // ph 0 → 頭頂

function slotPt(cx, cy, R, ph, bump) {
  const a = ph2a(ph);
  const rx = R * HAIR.rx, ry = R * HAIR.ry;
  const nx = Math.cos(a) / rx, ny = Math.sin(a) / ry;
  const nl = Math.hypot(nx, ny) || 1;
  const k = 1 + bump / (nl * Math.max(rx, ry));
  return [cx + rx * Math.cos(a) * k, cy + R * HAIR.cy + ry * Math.sin(a) * k];
}

// 平滑髮形：上緣澎、下襬長、頂點略塌，全為 ph 的連續函式
function hairBump(ph, o = {}) {
  const { flow = 0, claw = 0, wobble = 1 } = o;
  const crown = Math.pow(Math.cos(ph * TAU), 2);          // 1 在頭頂與下巴
  const hang = Math.pow(1 - Math.abs(Math.sin(ph * TAU)), 2); // 1 在左右兩側
  let b = 0.30 * hang + 0.16 * crown - 0.06;
  b += wobble * 0.030 * Math.sin(ph * TAU * 3 + flow);    // 髮流
  b += wobble * 0.018 * Math.sin(ph * TAU * 7 + flow * 1.7);
  if (claw > 0) b += claw * 0.26 * Math.pow(Math.abs(Math.sin(ph * TAU)), 3) * (Math.cos(ph * TAU) > 0 ? 1 : 0.3);
  return b;
}

function hairOutline(ctx, cx, cy, R) {
  return (o = {}) => {
    const N = 64;
    ctx.beginPath();
    for (let i = 0; i <= N; i++) {
      const ph = i / N;
      const [x, y] = slotPt(cx, cy, R, ph, hairBump(ph, o));
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.closePath();
  };
}

// angel ring：連續高光帶，下緣鋸齒，跨在顱頂弧上
function angelRing(ctx, cx, cy, R, a0, a1, zig = 9, amp = 9, w = 15) {
  const pts = [];
  const n = 46;
  for (let i = 0; i <= n; i++) { const a = lerp(a0, a1, i / n); pts.push([cx + Math.cos(a) * R, cy + Math.sin(a) * R]); }
  ctx.beginPath();
  ctx.moveTo(pts[0][0], pts[0][1] - w * 0.5);
  for (let i = 0; i <= n; i++) { const [x, y] = pts[i]; ctx.lineTo(x, y - w * 0.5 - Math.sin(i / n * Math.PI) * amp * 0.6); }
  for (let i = n; i >= 0; i--) {
    const [x, y] = pts[i];
    const z = (i % zig < zig / 2 ? 1 : -1) * amp;
    ctx.lineTo(x, y + w * 0.6 + z);
  }
  ctx.closePath();
  ctx.fillStyle = P.hairHi; ctx.globalAlpha = .92; ctx.fill(); ctx.globalAlpha = 1;
}

// 內輪廓（挖臉）：只在「下巴段」把外輪廓往內拉成臉型橢圓，
// 端點（額頭、頭頂）回到外輪廓上，因此瀏海與鬢髮自然連成一條線。
// 幾何取自實測：外輪廓 y −134…+150，臉橢圓 y −64…+112、x ±62。
function faceHole(ctx, cx, cy, R, s, turn, facing) {
  const N = 44;
  const frx = R * 0.80, fry = R * 1.12, fcy = cy + R * 0.31;
  ctx.beginPath();
  for (let i = 0; i <= N; i++) {
    const ph = i / N;
    const t = Math.max(0, Math.min(1, (ph - 0.28) / 0.44));
    const act = Math.sin(t * Math.PI);
    const [ox, oy] = slotPt(cx, cy, R, ph, hairBump(ph));
    // 目標點：臉橢圓上與外輪廓同相位的點
    const a = ph2a(ph);
    const tx = cx + frx * Math.cos(a), ty = fcy + fry * Math.sin(a);
    const x = ox + (tx - ox) * act, y = oy + (ty - oy) * act;
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  }
  ctx.closePath();
}

function hairBack(ctx, cx, cy, tv, s = 1, flow = 0, claw = 0) {
  const R = HEAD.r * s;
  hairOutline(ctx, cx, cy, R)({ flow, claw });
  ctx.fillStyle = P.hairSh; ctx.fill();
  ctx.lineWidth = 3; ctx.strokeStyle = P.hairLine; ctx.lineJoin = 'round'; ctx.stroke();
}

// 頭（正／3-4／側／背皆由此繪）。turn 的意義＝鼻子往哪一側轉（負＝左）。
function drawHead(ctx, cx, cy, o = {}) {
  const { turn = 0, s = 1, expr = 'neutral', blink = 0, t = 0, tear = 0 } = o;
  const back = Math.abs(turn) > 1.45;
  const tv = back ? (turn > 0 ? 1 : -1) : turn;      // 背面畫成反向的側臉底，再讓後髮蓋掉
  const hd = headShape(cx, cy, tv, s, expr === 'shout' ? 0.5 : 0);
  const R = hd.R, ex = hd.ex, side = Math.abs(tv);
  const sn = Math.sign(tv);                          // 轉向
  const facing = 1 - side;                           // 1 正面 → 0 全側
  const farSd = sn >= 0 ? -1 : 1;                    // 哪一眼是遠眼（同符號一側是近眼）

  if (!window.NOBACK) hairBack(ctx, cx, cy, tv, s, Math.sin(t * 2) * 0.4, expr === 'shout' || expr === 'smug' ? 1 : 0);
  // 臉
  cel(ctx, hd.path, { fill: P.skin, sh: P.skinSh, line: P.skinLine, ink: 2.6 * s, hi: null });
  // 耳：鼻尖偏離中心的 45% 處
  if (!back) {
    const ex0 = cx + sn * R * (0.44 * side + (1 - side) * 1.02);
    cel(ctx, c => {
      c.moveTo(ex0 - sn * R * 0.06, cy - R * 0.20);
      c.bezierCurveTo(ex0 + sn * R * 0.20, cy - R * 0.26, ex0 + sn * R * 0.20, cy + R * 0.16, ex0 - sn * R * 0.04, cy + R * 0.22);
    }, { fill: P.skin, sh: P.skinSh, line: P.skinLine, ink: 2.4 * s });
  }

  // 眼：鼻尖處為 origin，近眼在逺側、遠眼近中心且壓縮
  const eyeY = cy - R * 0.06;
  const sep = R * (0.50 * facing + 0.02);
  const ew = R * (0.31 * facing + 0.015) * (1 - side * 0.35);
  const eh = R * 0.19;
  const bl = (expr === 'blink' || (!back && blink > 0.9)) ? 1 : blink;
  if (!back) {
    const nearX = cx + sn * (sep * 0.58) + ex * 0.32;
    const farX = cx - sn * (sep * 0.60) - ex * 0.68;
    if (side > 0.88) {
      eye(ctx, nearX, eyeY, ew * 1.02, eh, tv, bl, tear);
    } else {
      eye(ctx, farX, eyeY, ew * 0.76, eh * 0.94, tv, bl, tear);
      eye(ctx, nearX, eyeY, ew * 1.02, eh, tv, bl, tear);
    }
  }
  // 眉
  const bt = { neutral: 0.06, happy: -0.10, angry: 0.30, shock: -0.20, smug: -0.16, tear: -0.22, shout: 0.24, blink: 0.06, grin: -0.04 }[expr] ?? 0.06;
  const blift = { neutral: 0, happy: -3, angry: 5, shock: -10, smug: -2, tear: -4, shout: 4, blink: 0, grin: -2 }[expr] ?? 0;
  if (!back) {
    const nearX = cx + sn * (sep * 0.58) + ex * 0.32;
    const farX = cx - sn * (sep * 0.60) - ex * 0.68;
    if (side > 0.88) brow(ctx, nearX, eyeY - eh * 2.3, ew * 0.98, bt, blift * s);
    else {
      brow(ctx, farX, eyeY - eh * 2.3, ew * 0.70, bt * 0.4 * -sn, blift * s - 2);
      brow(ctx, nearX, eyeY - eh * 2.3, ew * 0.98, bt * 0.5 + bt * 0.5 * sn, blift * s);
    }
  }
  // 鼻、嘴（鼻尖 = 面部朝向）
  if (!back) {
    nose(ctx, cx + sn * R * 0.36 * side + ex * 0.3, cy + R * 0.30, s * (1 - side * 0.35));
    const mk = { neutral: 'flat', happy: 'smile', angry: 'flat', shock: 'open', smug: 'cat', tear: 'cat', shout: 'shout', blink: 'flat', grin: 'grin' }[expr] || 'flat';
    mouth(ctx, cx + sn * R * 0.30 * side + ex * 0.35, cy + R * 0.58, R * (0.15 * facing + 0.02), mk, expr === 'shout' ? 0.35 : 0);
    // 腮紅
    ctx.save(); ctx.globalAlpha = .5; ctx.fillStyle = P.scarfHi;
    for (const sd of side < 0.6 ? [-sn, sn] : [sn]) {
      ctx.beginPath();
      ctx.ellipse(cx + sd * sep * 0.86 + ex * 0.2, cy + R * 0.26, R * 0.14 * (sd === sn ? 1 : 0.72), R * 0.07, sd * 0.1, 0, TAU);
      ctx.fill();
    }
    ctx.restore();
  }

  // 前髮：以 even-odd 挖臉，只留瀏海與鬢髮；單一路徑 → 不會產生反向洞
  if (!window.NOFRINGE) {
  path(ctx, c => { hairOutline(c, cx, cy, R)({ flow: Math.sin(t * 2) * 0.4 }); faceHole(c, cx, cy, R, s, tv, facing); });
  ctx.fillStyle = P.hair; ctx.fill('evenodd');
  ctx.lineWidth = 3; ctx.strokeStyle = P.hairLine; ctx.lineJoin = 'round'; ctx.stroke();
  }

  // angel ring：正面／3-4 走橫帶，全側走縱帶（背面不畫）
  if (!back) {
    if (side < 0.8) angelRing(ctx, cx + ex * 0.5, cy - R * 0.10, R * 1.18, Math.PI * 1.14, Math.PI * 1.88, 9, 8 * s, 15 * s);
    else angelRing(ctx, cx + ex * 0.5, cy - R * 0.10, R * 1.16, Math.PI * 0.86, Math.PI * 1.32, 5, 7 * s, 13 * s);
  }
}

/* ── 全身：騎士甲（人形比例，非機械）─────────────────────── */
function drawBody(ctx, cx, cy, o = {}) {
  const { s = 1, t = 0, pose = 'stand' } = o;
  const g = s;
  const sw = Math.sin(t * 1.6) * 2 * g;
  // 圍巾（在身體後面先畫一層，飄帶）
  ctx.save();
  path(ctx, c => {
    c.moveTo(cx - 46 * g, cy - 250 * g);
    c.quadraticCurveTo(cx - 150 * g - sw * 6, cy - 210 * g + sw * 4, cx - 190 * g, cy - 96 * g + sw * 10);
    c.lineTo(cx - 118 * g, cy - 128 * g + sw * 8);
    c.quadraticCurveTo(cx - 96 * g, cy - 196 * g, cx - 20 * g, cy - 240 * g);
  });
  ctx.fillStyle = P.scarfSh; ctx.fill();
  ctx.lineWidth = 3 * g; ctx.strokeStyle = '#5c1210'; ctx.stroke();
  ctx.restore();

  // 腿
  for (const sd of [-1, 1]) {
    cel(ctx, c => {
      const x = cx + sd * 24 * g, kx = cx + sd * (30 + (pose === 'action' ? sd * 22 : 0)) * g;
      c.moveTo(x - 22 * g, cy + 4 * g);
      c.quadraticCurveTo(kx - 20 * g, cy + 130 * g, kx - 17 * g, cy + 244 * g);
      c.lineTo(kx + 19 * g, cy + 246 * g);
      c.quadraticCurveTo(kx + 24 * g, cy + 128 * g, x + 24 * g, cy + 6 * g);
    }, { fill: P.coatSh, sh: '#191c2a', hi: P.coat, line: P.hairLine, ink: 3 * g });
    // 靴
    cel(ctx, c => {
      const kx = cx + sd * (30 + (pose === 'action' ? sd * 22 : 0)) * g;
      c.moveTo(kx - 22 * g, cy + 226 * g);
      c.quadraticCurveTo(kx - 26 * g, cy + 288 * g, kx + (sd > 0 ? 34 : 26) * g, cy + 292 * g);
      c.quadraticCurveTo(kx + 30 * g, cy + 240 * g, kx + 22 * g, cy + 226 * g);
    }, { fill: P.coat, sh: P.coatSh, hi: P.belt, line: P.hairLine, ink: 3 * g });
  }
  // 軀幹
  cel(ctx, c => {
    c.moveTo(cx - 54 * g, cy - 232 * g);
    c.bezierCurveTo(cx - 66 * g, cy - 150 * g, cx - 50 * g, cy - 40 * g, cx - 46 * g, cy + 10 * g);
    c.lineTo(cx + 46 * g, cy + 10 * g);
    c.bezierCurveTo(cx + 50 * g, cy - 40 * g, cx + 66 * g, cy - 150 * g, cx + 54 * g, cy - 232 * g);
    c.bezierCurveTo(cx + 20 * g, cy - 246 * g, cx - 20 * g, cy - 246 * g, cx - 54 * g, cy - 232 * g);
  }, { fill: P.coat, sh: P.coatSh, hi: P.coatHi, line: P.hairLine, ink: 3.2 * g });
  // 胸甲切口（亮面）
  cel(ctx, c => {
    c.moveTo(cx - 40 * g, cy - 214 * g); c.lineTo(cx + 40 * g, cy - 214 * g);
    c.lineTo(cx + 26 * g, cy - 132 * g); c.lineTo(cx - 26 * g, cy - 132 * g);
  }, { fill: P.coatHi, sh: P.coat, line: P.hairLine, ink: 2.4 * g });
  // 軀幹中央紅線（腰帶的能量走向）
  ctx.save(); ctx.globalAlpha = .85; ctx.beginPath();
  ctx.moveTo(cx, cy - 196 * g); ctx.lineTo(cx, cy - 30 * g);
  ctx.lineWidth = 7 * g; ctx.strokeStyle = P.accent; ctx.lineCap = 'round'; ctx.stroke(); ctx.restore();

  // 手臂
  for (const sd of [-1, 1]) {
    const act = pose === 'action' && sd > 0;
    const shx = cx + sd * 56 * g, shy = cy - 214 * g;
    const ex2 = cx + sd * (72 + (act ? 40 : 6)) * g, ey2 = cy - (act ? 300 : 92) * g;
    const hx = cx + sd * (act ? 30 : 70) * g, hy = cy - (act ? 400 : 18) * g;
    cel(ctx, c => {
      c.moveTo(shx - 20 * g, shy); c.quadraticCurveTo(sd * 4 + (shx + ex2) / 2 - 18 * g, (shy + ey2) / 2 + 16 * g, ex2 - 15 * g, ey2);
      c.quadraticCurveTo(ex2 + 8 * g, ey2 + 26 * g, hx + 14 * g, hy - (act ? 6 : 12) * g);
      c.lineTo(hx - 16 * g, hy + 8 * g);
      c.quadraticCurveTo(ex2 - 30 * g, ey2 + 8 * g, shx - 30 * g, shy + 14 * g);
    }, { fill: P.coat, sh: P.coatSh, hi: act ? P.coatHi : null, line: P.hairLine, ink: 3 * g });
    // 手套
    cel(ctx, c => {
      c.ellipse(hx, hy + (act ? 10 : 16) * g, 20 * g, 26 * g, sd * 0.2, 0, TAU);
    }, { fill: P.coatSh, sh: '#151824', hi: P.coat, line: P.hairLine, ink: 2.6 * g });
  }

  // 腰帶（主角／變身後同構，僅核心亮度不同）
  const bY = cy - 6 * g;
  cel(ctx, c => { c.roundRect(cx - 62 * g, bY - 30 * g, 124 * g, 60 * g, 10 * g); },
    { fill: P.belt, sh: P.beltSh, hi: '#f2ede0', line: P.beltLine, ink: 3.4 * g });
  const glow = 0.55 + 0.45 * Math.sin(t * 6);
  const cg = ctx.createRadialGradient(cx, bY, 2, cx, bY, 74 * g);
  cg.addColorStop(0, P.coreHi); cg.addColorStop(0.35, P.core); cg.addColorStop(1, 'rgba(255,68,89,0)');
  ctx.save(); ctx.globalAlpha = 0.5 + glow * 0.5; ctx.fillStyle = cg;
  ctx.beginPath(); ctx.arc(cx, bY, 74 * g, 0, TAU); ctx.fill(); ctx.restore();
  cel(ctx, c => { c.ellipse(cx, bY, 26 * g, 26 * g, 0, 0, TAU); },
    { fill: P.core, sh: '#a01f34', hi: P.coreHi, line: P.beltLine, ink: 3 * g });
  ctx.beginPath(); ctx.arc(cx, bY, 11 * g, 0, TAU); ctx.fillStyle = '#fff2c8'; ctx.fill();

  // 圍巾（前段壓在胸前）
  cel(ctx, c => {
    c.moveTo(cx - 44 * g, cy - 244 * g);
    c.quadraticCurveTo(cx, cy - 226 * g, cx + 42 * g, cy - 246 * g);
    c.quadraticCurveTo(cx + 10 * g, cy - 268 * g, cx - 44 * g, cy - 244 * g);
  }, { fill: P.scarf, sh: P.scarfSh, hi: P.scarfHi, line: '#5c1210', ink: 3 * g });
  ctx.restore();
}

/* ── 背景：淨色＋細網格，讓 cel 邊緣可讀 ─────────────────── */
function bg(ctx, t, tint = P.bg) {
  ctx.fillStyle = tint; ctx.fillRect(0, 0, W, H);
  const g = ctx.createLinearGradient(0, 0, 0, H);
  g.addColorStop(0, 'rgba(255,255,255,.05)'); g.addColorStop(1, 'rgba(0,0,0,.22)');
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  ctx.strokeStyle = 'rgba(255,255,255,.045)'; ctx.lineWidth = 1;
  for (let x = 0; x < W; x += 60) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); }
  for (let y = 0; y < H; y += 60) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); }
}

function title(ctx, x, y, big, small, t = 0) {
  ctx.textBaseline = 'top';
  ctx.fillStyle = P.ink; ctx.font = `400 ${big}px "ZCOOL KuaiLe"`;
  ctx.fillText(small, x, y);
  ctx.fillStyle = 'rgba(232,227,214,.45)'; ctx.font = `400 ${Math.round(big * 0.40)}px "ZCOOL KuaiLe"`;
  ctx.fillText('  MODEL SHEET — 一模'); // placeholder, replaced below
}

/* ── 版面：靜幀用網格（cell 0..11），另有 4 個整頁模式 ───── */
const CELLS = [
  ['TURN', '正面', 0.00, 'neutral', 0, 'bust'],
  ['TURN', '3/4', 0.52, 'neutral', 20, 'bust'],
  ['TURN', '側面', 0.96, 'neutral', 40, 'bust'],
  ['TURN', '背面', 1.75, 'neutral', 60, 'bust'],

  ['EXPR', '無表情', -0.40, 'neutral', 0, 'bust'],
  ['EXPR', '笑容', 0.55, 'happy', 0, 'bust'],
  ['EXPR', '怒', -0.55, 'angry', 0, 'bust'],
  ['EXPR', '震驚', 0.45, 'shock', 0, 'bust'],

  ['EXPR2', '認真', -0.45, 'smug', 0, 'bust'],
  ['EXPR2', '憋淚', -0.50, 'tear', 0.15, 'bust'],
  ['EXPR2', '喊', 0.50, 'shout', 0, 'bust'],
  ['EXPR2', '眨眼', 0.00, 'blink', 0, 'bust'],

  ['POSE', '立姿', 0.18, 'neutral', 0, 'full'],
  ['POSE', '變身動作', 0.62, 'angry', 0, 'full'],
  ['POSE', '側身', 0.30, 'neutral', 30, 'full'],
  ['PAL', '色票', 0, 'neutral', 0, 'pal'],
];

function drawCell(ctx, x, y, w, h, cell, t) {
  ctx.save();
  ctx.translate(x, y);
  // 框
  ctx.fillStyle = 'rgba(255,255,255,.028)'; ctx.fillRect(0, 0, w, h);
  ctx.strokeStyle = 'rgba(255,255,255,.10)'; ctx.lineWidth = 2; ctx.strokeRect(1, 1, w - 2, h - 2);
  ctx.save(); ctx.beginPath(); ctx.rect(0, 0, w, h); ctx.clip();

  const [grp, label, turn, expr, tilt, kind] = cell;
  const cx = w / 2, cy = kind === 'full' ? h * 0.30 : h * 0.46;
  if (kind === 'pal') {
    let px = 40, py = h * 0.36;
    ctx.textBaseline = 'top';
    for (const [k, v] of Object.entries(P)) {
      ctx.fillStyle = v; ctx.fillRect(px, py, 96, 96);
      ctx.strokeStyle = 'rgba(0,0,0,.5)'; ctx.lineWidth = 2; ctx.strokeRect(px, py, 96, 96);
      ctx.fillStyle = P.ink; ctx.font = '400 20px "ZCOOL KuaiLe"';
      ctx.fillText(k, px, py + 104);
      ctx.fillStyle = 'rgba(232,227,214,.5)'; ctx.font = '400 16px "ZCOOL KuaiLe"';
      ctx.fillText(v, px, py + 128);
      px += 118; if (px > w - 130) { px = 40; py += 172; }
    }
  } else if (kind === 'full') {
    ctx.save(); ctx.translate(cx, cy + h * 0.32); ctx.rotate((tilt || 0) * Math.PI / 180 * 0.12);
    const s = 0.72;
    ctx.beginPath(); ctx.ellipse(0, 20, 130 * s, 34 * s, 0, 0, TAU);
    ctx.fillStyle = 'rgba(0,0,0,.30)'; ctx.fill();
    drawBody(ctx, 0, 0, { s, t, pose: grp === 'POSE' && label === '變身動作' ? 'action' : 'stand' });
    ctx.restore();
    drawHead(ctx, cx, cy - h * 0.10, { turn: turn * 2 - 1, s: 0.56, expr, t, blink: 0 });
  } else {
    drawHead(ctx, cx, cy, { turn, s: 1.0, expr, t, blink: expr === 'blink' ? 1 : 0 });
  }
  ctx.restore();

  // 標籤
  ctx.textBaseline = 'top';
  ctx.fillStyle = P.accent; ctx.font = '400 24px "ZCOOL KuaiLe"';
  ctx.fillText(grp, 24, 18);
  ctx.fillStyle = P.ink; ctx.font = '400 40px "ZCOOL KuaiLe"';
  ctx.fillText(label, 24, 46);
  ctx.restore();
}

/* ── 整頁模式 ─────────────────────────────────────────────── */
function pageAll(ctx, t) {
  bg(ctx, t);
  ctx.textBaseline = 'top';
  ctx.fillStyle = P.ink; ctx.font = '400 46px "ZCOOL KuaiLe"';
  ctx.fillText('林昭 / 假面騎士腰帶 — 角色設定集', 60, 40);
  ctx.fillStyle = 'rgba(232,227,214,.5)'; ctx.font = '400 26px "ZCOOL KuaiLe"';
  ctx.fillText('《邪神給的腰帶》— cel-anime-80s 色指定 / 逐格由同一 head() 繪製', 60, 98);
  ctx.fillStyle = P.accent; ctx.fillRect(60, 138, 180, 6);

  const gx = 60, gy = 172, gw = (W - 120 - 3 * 16) / 4, gh = (H - 172 - 60 - 3 * 16) / 4;
  const start = CELL < 0 ? 0 : CELL, end = CELL < 0 ? CELLS.length : CELL + 1;
  // all 頁只排 12 格（palette 併入最後一列），避免超出畫布
  for (let i = start; i < end; i++) {
    if (CELL < 0 && i >= 12) break;
    const col = i % 4, row = (i / 4) | 0;
    drawCell(ctx, gx + col * (gw + 16), gy + row * (gh + 16), gw, gh, CELLS[i], t);
  }
  if (CELL < 0) {
    const i = 15, col = 3, row = 2;
    ctx.save();
    ctx.translate(gx + col * (gw + 16), gy + row * (gh + 16));
    drawCell(ctx, 0, 0, gw, gh, ['PAL', '色票', 0, 'neutral', 0, 'pal'], t);
    ctx.restore();
  }
  ctx.fillStyle = 'rgba(0,0,0,.35)'; ctx.fillRect(0, H - 44, W, 44);
  ctx.fillStyle = 'rgba(232,227,214,.55)'; ctx.font = '400 22px "ZCOOL KuaiLe"';
  ctx.fillText(EXPR ? `查詢：${EXPR}` : 'eyes: almond · thick upper lash · tall iris · 2 highlights · angel ring', 60, H - 34);
}

function pageTurn(ctx, t, turn) {
  bg(ctx, t);
  const cx = W / 2, cy = H * 0.54;
  drawHead(ctx, cx, cy, { turn, s: 3.2, expr: 'neutral', t });
  ctx.fillStyle = P.ink; ctx.font = '400 40px "ZCOOL KuaiLe"'; ctx.textBaseline = 'top';
  ctx.fillText(`turn = ${turn.toFixed(2)}   （正 → 3/4 → 側 → 背）`, 60, 40);
  ctx.fillStyle = 'rgba(232,227,214,.45)'; ctx.font = '400 24px "ZCOOL KuaiLe"';
  ctx.fillText('檢查：遠眼壓縮、臉型透視、angel ring 走向、耳位', 60, 96);
  ctx.strokeStyle = 'rgba(255,255,255,.14)'; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(W / 2, 0); ctx.lineTo(W / 2, H); ctx.stroke();
}

function pageClose(ctx, t) {
  bg(ctx, t, '#141622');
  const cx = W * 0.5, cy = H * 0.52;
  // 特寫：只畫頭的上半，眼放大
  ctx.save();
  ctx.translate(cx - W * 0.02, cy + H * 0.30);
  drawHead(ctx, 0, 0, { turn: 0.28, s: 5.0, expr: 'smug', t });
  ctx.restore();
  ctx.fillStyle = P.ink; ctx.font = '400 36px "ZCOOL KuaiLe"'; ctx.textBaseline = 'top';
  ctx.fillText('特寫 — 檢查虹膜層次、兩點高光、睫毛外甩、髮綹尖端', 60, 40);
}

function pagePoses(ctx, t) {
  bg(ctx, t);
  ctx.fillStyle = P.ink; ctx.font = '400 40px "ZCOOL KuaiLe"'; ctx.textBaseline = 'top';
  ctx.fillText('關鍵姿勢 — 立姿 / 變身動作 / 側身', 60, 40);
  const poses = [['stand', 0.18, 'stand'], ['action', 0.62, 'action'], ['stand', 0.30, 'stand']];
  poses.forEach(([pose, ph, lbl], i) => {
    const x = W * (0.22 + i * 0.28), y = H * 0.70;
    ctx.save(); ctx.translate(x, y);
    ctx.beginPath(); ctx.ellipse(0, 20, 150, 36, 0, 0, TAU); ctx.fillStyle = 'rgba(0,0,0,.30)'; ctx.fill();
    drawBody(ctx, 0, 0, { s: 0.95, t: t + i, pose });
    ctx.restore();
    drawHead(ctx, x + (i === 1 ? -14 : 0), y - H * 0.30, { turn: i === 2 ? 0.8 : i === 1 ? -0.3 : 0, s: 0.74, expr: i === 1 ? 'shout' : 'neutral', t: t + i });
    ctx.fillStyle = 'rgba(232,227,214,.5)'; ctx.font = '400 26px "ZCOOL KuaiLe"';
    ctx.fillText(lbl, x - 60, H - 90);
  });
}

/* ── 入口 ─────────────────────────────────────────────────── */
window.render = (t = 0) => {
  const c = document.getElementById('ov');
  const ctx = c.getContext('2d');
  ctx.save();
  if (['turn', 'close', 'poses'].includes(PAGE)) {
    if (PAGE === 'turn') pageTurn(ctx, t, 0.0);
    if (PAGE === 'close') pageClose(ctx, t);
    if (PAGE === 'poses') pagePoses(ctx, t);
  } else pageAll(ctx, t);
  ctx.restore();
};

const fonts = ['400 40px "ZCOOL KuaiLe"', '400 40px "Fredoka"', '400 40px "Lilita One"'];
Promise.all(fonts.map(f => document.fonts.load(f, '林昭假面騎士腰帶不公正邪'))).then(() => {
  window.render(0);
  window.READY = true;
});
