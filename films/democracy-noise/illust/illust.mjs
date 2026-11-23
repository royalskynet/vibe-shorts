// 插畫庫：扁平小人與道具，畫風對標 IG @boundless__explorer（refs/boundless/ANALYSIS.md §3）。
// 片子不能讀片目錄外的檔（lemo core/render/serve.mjs 掛載根），用 scripts/illust_install.sh 複製進 films/<片>/illust/。
//
// 規矩：
// - 形狀存成 SVG path 字串，用 new Path2D(d) 畫；Path2D 物件按字串快取（同字串同形狀，不影響畫面）。
// - 每個函式都是參數的純函數：同參數同畫面，動畫只吃傳進來的 t（seek_check.mjs 會亂序比對）。
// - 每個函式開頭 g.save()、結尾 g.restore()，陰影、透明度、變形都不外漏。
// - 不寫死政黨色：人物 body、旗子 color 這類由呼叫端傳入；PALETTE 只放參考帳號四色與底色。
//
// 座標：person 的 (x, y) 是腳底中心、s 是全身高（px）；道具的 (x, y) 是中心（house、flag、balance 是地面中心）、s 是寬（px）。
// 內部都畫在 100 單位的格子裡再縮放。

export const PALETTE = {
  ink: '#3b2f2a',      // 深棕：頭、腿、字
  terra: '#c8674a',    // 陶土紅：重點
  sage: '#8fa98a',     // 鼠尾草綠
  mustard: '#d9a441',  // 芥末黃
  cream: '#f5efe6',    // 底色
  paper: '#fffaf2',    // 文件、卡片
  soft: '#ebe1d2',     // 卡片內底
  line: '#d6c8b4',     // 文件內文線
  mute: '#b3a797',     // 灰：不表態、次要
  coat: '#7a5a48',     // 人物預設身體色（參考帳號的棕外套）
};
const SHADOW = 'rgba(59,47,42,0.18)';
const FONT = '"PingFang TC"';

// ---------- 小工具 ----------
const cache = new Map();
function P(d) {
  let p = cache.get(d);
  if (!p) { if (cache.size > 4000) cache.clear(); p = new Path2D(d); cache.set(d, p); }
  return p;
}
const f2 = n => +n.toFixed(2);
// 圓角矩形的 path 字串（Path2D 吃 SVG 語法）
export function rrPath(x, y, w, h, r) {
  r = Math.min(r, w / 2, h / 2);
  return `M${f2(x + r)},${f2(y)}H${f2(x + w - r)}A${f2(r)},${f2(r)} 0 0 1 ${f2(x + w)},${f2(y + r)}V${f2(y + h - r)}` +
    `A${f2(r)},${f2(r)} 0 0 1 ${f2(x + w - r)},${f2(y + h)}H${f2(x + r)}A${f2(r)},${f2(r)} 0 0 1 ${f2(x)},${f2(y + h - r)}` +
    `V${f2(y + r)}A${f2(r)},${f2(r)} 0 0 1 ${f2(x + r)},${f2(y)}Z`;
}
const circlePath = (cx, cy, r) => `M${f2(cx - r)},${f2(cy)}A${f2(r)},${f2(r)} 0 1 0 ${f2(cx + r)},${f2(cy)}A${f2(r)},${f2(r)} 0 1 0 ${f2(cx - r)},${f2(cy)}Z`;
const fill = (g, d, col) => { g.fillStyle = col; g.fill(P(d)); };
function stroke(g, d, col, w) { g.strokeStyle = col; g.lineWidth = w; g.lineCap = 'round'; g.lineJoin = 'round'; g.stroke(P(d)); }
const seg = pts => 'M' + pts.map(([x, y]) => `${f2(x)},${f2(y)}`).join('L');
const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
export function shade(a, b, t) {
  const A = hex(a), B = hex(b);
  return '#' + A.map((v, i) => Math.round(v + (B[i] - v) * t).toString(16).padStart(2, '0')).join('');
}
// 柔和投影：只在 fn 裡生效；shadowBlur 不吃變形，所以乘上縮放 k
function soft(g, k, fn, blur = 16, dy = 5, col = SHADOW) {
  g.save(); g.shadowColor = col; g.shadowBlur = blur * k; g.shadowOffsetY = dy * k; fn(); g.restore();
}
function ground(g, rx, ry, a = 0.14) { g.fillStyle = `rgba(59,47,42,${a})`; g.beginPath(); g.ellipse(0, 0, rx, ry, 0, 0, Math.PI * 2); g.fill(); }
function label(g, s, x, y, px, col, w = 700, align = 'center') {
  g.font = `${w} ${px}px ${FONT}`; g.textAlign = align; g.textBaseline = 'middle'; g.fillStyle = col; g.fillText(s, x, y);
}
function begin(g, o) {
  g.save(); g.translate(o.x || 0, o.y || 0);
  const k = (o.s || 100) / 100; g.scale(k, k);
  if (o.alpha != null) g.globalAlpha *= o.alpha;
  return k;
}

// ---------- 人物 ----------
// 頭圓、身體一個上窄下寬的色塊、手腳是圓頭粗線。格子：腳底 y=0、頭頂 y=-96。
const HEAD = circlePath(0, -84, 12);
const BODY = 'M-10,-73H10Q13,-73 13.4,-69L15.2,-37Q15.4,-33 11.5,-33H-11.5Q-15.4,-33 -15.2,-37L-13.4,-69Q-13,-73 -10,-73Z';
const SH = [11.5, -67.5];   // 右肩；左肩鏡像
const HIP = [5, -35];

// 每個姿勢回傳右臂、左臂（肘、手）、兩腳腳底、身體位移；座標是「面向右」時的樣子
const POSES = {
  stand: () => ({ R: [[15.5, -53], [16.5, -39]], L: [[-15.5, -53], [-16.5, -39]], feet: [[-6, 0], [6, 0]] }),
  point: o => {
    const a = o.aim ?? -0.12;   // 指向角（弧度，0＝水平、負＝往上）
    const e = [SH[0] + 13 * Math.cos(a * 0.6), SH[1] + 13 * Math.sin(a * 0.6)];
    return { R: [e, [e[0] + 14 * Math.cos(a), e[1] + 14 * Math.sin(a)]], L: [[-15.5, -53], [-16.5, -39]], feet: [[-6, 0], [6, 0]] };
  },
  armsUp: () => ({ R: [[21, -80], [23, -95]], L: [[-21, -80], [-23, -95]], feet: [[-7, 0], [7, 0]] }),
  shrug: () => ({ R: [[22, -55], [29, -66]], L: [[-22, -55], [-29, -66]], feet: [[-6, 0], [6, 0]], dy: -1 }),
  think: () => ({ R: [[16, -50], [5, -71]], L: [[-14, -52], [12, -52]], feet: [[-6, 0], [6, 0]] }),
  walk: o => {
    const ph = Math.sin((o.t || 0) * Math.PI * 2 * (o.speed || 1.6));
    const bob = -Math.abs(Math.cos((o.t || 0) * Math.PI * 2 * (o.speed || 1.6))) * 1.6;
    // 側走：兩腿從髖部中間前後擺、雙手跟腿反向擺
    return { R: [[15.5 - 2 * ph, -53], [16.5 - 6 * ph, -39.5]], L: [[-15.5 - 2 * ph, -53], [-16.5 - 6 * ph, -39.5]],
      hips: [-2.5, 2.5], feet: [[-2.5 + 10 * ph, 0], [2.5 - 10 * ph, 0]], dy: bob };
  },
};
export const POSE_NAMES = Object.keys(POSES);
export const FACE_NAMES = ['none', 'smile', 'worried'];

export function person(g, o = {}) {
  const pose = o.pose || 'stand', face = o.face || 'none';
  if (!POSES[pose]) throw new Error(`illust.person: 不認得的 pose「${pose}」（可用 ${POSE_NAMES.join('、')}）`);
  if (!FACE_NAMES.includes(face)) throw new Error(`illust.person: 不認得的 face「${face}」（可用 ${FACE_NAMES.join('、')}）`);
  const body = o.body || PALETTE.coat, head = o.head || PALETTE.ink, leg = o.leg || PALETTE.ink;
  const q = POSES[pose](o), dy = q.dy || 0;
  begin(g, o);
  if (o.shadow !== false) ground(g, 21, 4.2);
  if (o.tilt) g.rotate(o.tilt);
  if ((o.dir ?? 1) < 0) g.scale(-1, 1);
  // 腿
  for (const [i, f] of q.feet.entries()) {
    const hx = q.hips ? q.hips[i] : i ? HIP[0] : -HIP[0];
    stroke(g, seg([[hx, HIP[1] + dy], [f[0], f[1] - 3.5]]), leg, 7.5);
  }
  g.translate(0, f2(dy));
  fill(g, BODY, body);
  // 手：袖子比身體深一點，手掌跟頭同色
  const arm = shade(body, PALETTE.ink, 0.22);
  for (const [side, [e, h]] of [[1, q.R], [-1, q.L]]) {
    stroke(g, seg([[side * SH[0], SH[1]], e, h]), arm, 6.2);
    fill(g, circlePath(h[0], h[1], 3.3), head);
  }
  fill(g, HEAD, head);
  if (face !== 'none') {
    const c = o.faceColor || PALETTE.cream, fx = 1.6;
    fill(g, circlePath(fx - 4.3, -85.5, 1.45), c); fill(g, circlePath(fx + 4.3, -85.5, 1.45), c);
    if (face === 'smile') stroke(g, `M${fx - 4.2},-81.2Q${fx},-77 ${fx + 4.2},-81.2`, c, 1.5);
    else {
      stroke(g, `M${fx - 7},-89.2L${fx - 2.6},-91`, c, 1.3); stroke(g, `M${fx + 7},-89.2L${fx + 2.6},-91`, c, 1.3);
      stroke(g, `M${fx - 3.4},-78.2Q${fx},-80.8 ${fx + 3.4},-78.2`, c, 1.4);
    }
  }
  g.restore();
}

// ---------- 道具 ----------
// 文件：折角＋內文線＋可選標題。(x, y) 中心，s 寬。
function documentProp(g, o = {}) {
  const k = begin(g, o);
  const sheet = 'M-38,-50H22L38,-34V46Q38,50 34,50H-34Q-38,50 -38,46V-46Q-38,-50 -34,-50Z';
  soft(g, k, () => fill(g, sheet, o.fill || PALETTE.paper));
  fill(g, 'M22,-50V-38Q22,-34 26,-34H38Z', '#e6d9c6');
  let y = -32;
  if (o.title) { label(g, o.title, -27, -33, o.titlePx || 10, PALETTE.ink, 700, 'left'); y = -16; }
  const n = o.lines ?? 6;
  for (let i = 0; i < n; i++) stroke(g, `M-27,${y + i * 9}H${i === n - 1 ? 6 : 26}`, o.lineColor || PALETTE.line, 3);
  if (o.cross) { stroke(g, 'M-24,-20L24,30', PALETTE.terra, 6); stroke(g, 'M24,-20L-24,30', PALETTE.terra, 6); }
  g.restore();
}

// 手機：螢幕內 2–4 列貼文（圓點頭像＋灰線）。hl＝要標紅的列號。
function phone(g, o = {}) {
  const rows = o.rows ?? 3;
  if (!(rows >= 2 && rows <= 4)) throw new Error(`illust.phone: rows 要 2–4，拿到 ${rows}`);
  const k = begin(g, o);
  soft(g, k, () => fill(g, rrPath(-30, -56, 60, 112, 9), o.body || '#5a463c'));
  fill(g, rrPath(-25.5, -48, 51, 94, 4), o.screen || '#f3ebdf');
  fill(g, rrPath(-6, -53, 12, 2.2, 1.1), PALETTE.ink);
  const cols = o.avatars || [PALETTE.terra, PALETTE.sage, PALETTE.mustard, PALETTE.terra];
  const rh = (94 - 6) / rows;
  for (let i = 0; i < rows; i++) {
    const y = -45 + i * rh, h = rh - 4;
    fill(g, rrPath(-22, y, 44, h, 3), i === o.hl ? '#f4d6c9' : '#e9dece');
    const cy = y + Math.min(8, h / 3);
    fill(g, circlePath(-15.5, cy, 3.6), cols[i % cols.length]);
    stroke(g, `M-8.5,${cy - 1.5}H15`, '#a89884', 2.4);
    stroke(g, `M-8.5,${cy + 4}H8`, '#cdbfac', 2.2);
    if (h > 18) stroke(g, `M-17,${y + h - 5}H15`, '#d9ccba', 2.2);
  }
  g.restore();
}

// 卡片：圓角＋柔和陰影的容器。(x, y) 中心，w／h 像素；content(g, w, h) 在卡片左上為原點的座標裡畫。
function card(g, o = {}) {
  const w = o.w || 400, h = o.h || 300, r = o.r ?? 28;
  g.save(); g.translate((o.x || 0) - w / 2, (o.y || 0) - h / 2);
  if (o.alpha != null) g.globalAlpha *= o.alpha;
  soft(g, 1, () => fill(g, rrPath(0, 0, w, h, r), o.fill || PALETTE.paper), 34, 10, 'rgba(59,47,42,0.16)');
  if (o.content) { g.save(); g.beginPath(); g.roundRect(0, 0, w, h, r); g.clip(); o.content(g, w, h); g.restore(); }
  g.restore();
}

// 燈泡：光暈＋玻璃＋燈座＋放射線。on 0–1 是亮度，t 讓光芒呼吸。
function bulb(g, o = {}) {
  const on = o.on ?? 1;
  begin(g, o);
  if (on > 0) {
    const gl = g.createRadialGradient(0, -16, 4, 0, -16, 62);
    gl.addColorStop(0, `rgba(240,196,92,${0.55 * on})`); gl.addColorStop(1, 'rgba(240,196,92,0)');
    g.fillStyle = gl; g.beginPath(); g.arc(0, -16, 62, 0, Math.PI * 2); g.fill();
    const pulse = 0.8 + 0.2 * Math.sin((o.t || 0) * 3);
    g.save(); g.globalAlpha *= on * pulse;
    for (let i = 0; i < 7; i++) {
      const a = -Math.PI + (i + 0.5) * Math.PI / 7;
      stroke(g, seg([[Math.cos(a) * 33, -16 + Math.sin(a) * 33], [Math.cos(a) * 42, -16 + Math.sin(a) * 42]]), PALETTE.mustard, 3.2);
    }
    g.restore();
  }
  fill(g, 'M-10,6C-10,-1 -24,-5 -24,-18A24,24 0 1 1 24,-18C24,-5 10,-1 10,6Z', on > 0 ? shade('#e9b850', '#cbbfae', 1 - on) : '#cbbfae');
  stroke(g, 'M-14,-26A15,15 0 0 1 -4,-34', 'rgba(255,250,240,0.7)', 3.2);
  fill(g, rrPath(-11, 7, 22, 5, 2), '#8c7b6b');
  fill(g, rrPath(-10, 13, 20, 5, 2), '#a99d8c');
  fill(g, rrPath(-5, 19, 10, 4, 2), PALETTE.ink);
  g.restore();
}

// 旗子：(x, y) 旗桿底，color 由呼叫端傳（政黨色不寫死），t 讓旗面飄。
function flag(g, o = {}) {
  begin(g, o);
  const w = Math.sin((o.t || 0) * 2.6) * 3;
  if (o.shadow !== false) ground(g, 12, 2.6);
  stroke(g, 'M0,0V-98', '#6b5a4e', 3.2);
  fill(g, circlePath(0, -99, 3.2), PALETTE.mustard);
  fill(g, `M1.5,-95Q22,${-99 + w} 46,-93L${44 + w * 0.3},-80L46,-67Q22,${-72 + w} 1.5,-68Z`, o.color || PALETTE.terra);
  if (o.label) label(g, o.label, 22, -81, o.labelPx || 10, o.labelColor || PALETTE.paper);
  g.restore();
}

// 房子：(x, y) 地面中心。
function house(g, o = {}) {
  const k = begin(g, o);
  if (o.shadow !== false) ground(g, 40, 5);
  fill(g, rrPath(16, -80, 9, 22, 1.5), o.roof || '#8a6a55');
  soft(g, k, () => fill(g, 'M-32,-48H32V0H-32Z', o.wall || '#e4d1b2'), 10, 3);
  fill(g, 'M-44,-44Q-45,-47 -42,-49L-2,-81Q0,-83 2,-81L42,-49Q45,-47 44,-44L42,-42H-42Z', o.roof || '#8a6a55');
  fill(g, rrPath(-8, -26, 16, 26, 3), o.door || '#6b4f3f');
  fill(g, rrPath(13, -36, 13, 12, 2), '#fbf3e4');
  stroke(g, 'M19.5,-36V-24M13,-30H26', o.roof || '#8a6a55', 1.6);
  g.restore();
}

// 對話泡泡：text 或三個點；tail＝'left'|'right'|'none'。(x, y) 泡泡中心。
function speech(g, o = {}) {
  const k = begin(g, o);
  const w = o.w || 100, h = o.h || 60, col = o.fill || '#ffffff';
  const tl = o.tail ?? 'left', sx = tl === 'right' ? 1 : -1;
  const body = rrPath(-w / 2, -h / 2, w, h, h / 2);
  const tail = `M${sx * w * 0.12},${h / 2 - 2}L${sx * w * 0.36},${h / 2 + 16}L${sx * w * 0.32},${h / 2 - 2}Z`;
  soft(g, k, () => { fill(g, body, col); if (tl !== 'none') fill(g, tail, col); }, 12, 4);
  if (o.stroke) { stroke(g, body, o.stroke, 2.4); }
  if (o.text) label(g, o.text, 0, 1, o.px || 20, o.color || PALETTE.ink);
  else for (let i = -1; i <= 1; i++) fill(g, circlePath(i * 16, 0, 5), o.color || PALETTE.ink);
  g.restore();
}

// 天秤：(x, y) 底座中心，tilt 弧度（正＝右邊下沉）；leftColor／rightColor 盤子顏色。
function balance(g, o = {}) {
  const k = begin(g, o), tilt = o.tilt || 0;
  if (o.shadow !== false) ground(g, 34, 4);
  soft(g, k, () => {
    fill(g, 'M-28,0H28L18,-9H-18Z', PALETTE.ink);
    fill(g, rrPath(-3, -90, 6, 84, 3), PALETTE.ink);
  }, 10, 3);
  const cx = Math.cos(tilt) * 48, cy = Math.sin(tilt) * 48;
  stroke(g, seg([[-cx, -88 - cy], [cx, -88 + cy]]), PALETTE.ink, 5.5);
  fill(g, circlePath(0, -92, 5.5), PALETTE.mustard);
  for (const [sx, col] of [[-1, o.leftColor || PALETTE.sage], [1, o.rightColor || PALETTE.terra]]) {
    const ex = sx * cx, ey = -88 + sx * cy, py = ey + 34;
    stroke(g, seg([[ex - 16, py], [ex, ey], [ex + 16, py]]), '#8c7b6b', 1.8);
    soft(g, k, () => fill(g, `M${ex - 21},${py}H${ex + 21}Q${ex + 16},${py + 11} ${ex},${py + 11}Q${ex - 16},${py + 11} ${ex - 21},${py}Z`, col), 8, 3);
  }
  g.restore();
}

// 大聲公：(x, y) 中心，喇叭口朝右（dir -1 朝左），t 讓聲波往外走。
function megaphone(g, o = {}) {
  const k = begin(g, o);
  if ((o.dir ?? 1) < 0) g.scale(-1, 1);
  if (o.waves !== false) {
    for (let i = 0; i < 3; i++) {
      const r = 16 + ((((o.t || 0) * 26 + i * 12) % 36) + 36) % 36;
      g.save(); g.globalAlpha *= 1 - (r - 16) / 36;
      g.strokeStyle = o.waveColor || PALETTE.terra; g.lineWidth = 3.5; g.lineCap = 'round';
      g.beginPath(); g.arc(26, 0, r, -0.6, 0.6); g.stroke();
      g.restore();
    }
  }
  soft(g, k, () => fill(g, 'M-30,-8V8H-18L24,27V-27L-18,-8Z', o.color || PALETTE.terra), 10, 3);
  g.save(); g.fillStyle = shade(o.color || PALETTE.terra, PALETTE.ink, 0.35); g.beginPath(); g.ellipse(24, 0, 5, 27, 0, 0, Math.PI * 2); g.fill(); g.restore();
  fill(g, rrPath(-15, 7, 8, 17, 3), PALETTE.ink);
  fill(g, rrPath(-34, -9, 6, 18, 3), PALETTE.ink);
  g.restore();
}

// 問號：粗線 path＋圓點。
function question(g, o = {}) {
  begin(g, o);
  stroke(g, 'M-16,-30C-16,-53 18,-53 18,-30C18,-14 0,-15 0,4', o.color || PALETTE.terra, 10);
  fill(g, circlePath(0, 22, 6.5), o.color || PALETTE.terra);
  g.restore();
}

export const PROPS = { document: documentProp, phone, card, bulb, flag, house, speech, balance, megaphone, question };
export const PROP_NAMES = Object.keys(PROPS);
export function prop(g, name, o) {
  const fn = PROPS[name];
  if (!fn) throw new Error(`illust.prop: 不認得的道具「${name}」（可用 ${PROP_NAMES.join('、')}）`);
  fn(g, o);
}
