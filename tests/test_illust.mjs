// 插畫庫 assets/illust/illust.mjs：純函數（同參數同畫面）、walk 跟 t 走、未知 pose／道具丟錯、save／restore 成對、片內副本跟正本一致。
// 跑：node tests/test_illust.mjs（瀏覽器那段要 $LIB，預設 ~/dev/lemo-opuscar）
import assert from 'node:assert/strict';
import fs from 'node:fs'; import path from 'node:path'; import crypto from 'node:crypto'; import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SRC = path.join(ROOT, 'assets/illust/illust.mjs');

// ---------- 1) node 裡用記錄型假 context 跑：呼叫序列就是畫面 ----------
globalThis.Path2D = class { constructor(d) { this.d = d; } toJSON() { return this.d; } };
function fakeCtx() {
  const log = [], st = { globalAlpha: 1, depth: 0, saves: 0, restores: 0 };
  const g = new Proxy({}, {
    get(_, k) {
      if (k === 'log') return log;
      if (k === 'st') return st;
      if (k in st) return st[k];
      return (...a) => {
        if (k === 'save') { st.depth++; st.saves++; }
        if (k === 'restore') { st.depth--; st.restores++; assert.ok(st.depth >= 0, 'restore 比 save 多'); }
        log.push([k, a.map(x => typeof x === 'function' ? 'fn' : x)]);
        if (k === 'createRadialGradient') return { addColorStop: (...b) => log.push(['stop', b]) };
      };
    },
    set(_, k, v) { st[k] = v; log.push(['=' + String(k), v]); return true; },
  });
  return g;
}
const { person, prop, POSE_NAMES, FACE_NAMES, PROP_NAMES, PALETTE } = await import(SRC);
const draw = (fn) => { const g = fakeCtx(); fn(g); return { g, s: JSON.stringify(g.log) }; };

for (const pose of ['stand', 'point', 'armsUp', 'shrug', 'think', 'walk']) assert.ok(POSE_NAMES.includes(pose), `少了 pose ${pose}`);
for (const n of ['document', 'phone', 'card', 'bulb', 'flag', 'house', 'speech', 'balance', 'megaphone', 'question'])
  assert.ok(PROP_NAMES.includes(n), `少了道具 ${n}`);
for (const c of ['#3b2f2a', '#c8674a', '#8fa98a', '#d9a441', '#f5efe6']) assert.ok(Object.values(PALETTE).includes(c), `PALETTE 少了 ${c}`);

// 每個 pose × face、每個道具：save／restore 成對；同參數畫兩次呼叫序列一樣
for (const pose of POSE_NAMES) for (const face of FACE_NAMES) for (const dir of [1, -1]) {
  const o = { x: 300, y: 900, s: 200, pose, face, dir, t: 1.234, body: '#6f8fb0', tilt: 0.1 };
  const a = draw(g => person(g, o)), b = draw(g => person(g, { ...o }));
  assert.equal(a.g.st.depth, 0, `${pose}/${face} save／restore 沒成對`);
  assert.ok(a.g.st.saves > 0, `${pose} 沒有 save`);
  assert.equal(a.s, b.s, `${pose}/${face} 同參數畫兩次不一樣`);
}
for (const n of PROP_NAMES) {
  const o = { x: 500, y: 800, s: 300, w: 300, h: 200, t: 0.7, title: '研究', label: '自己', text: '溫和', content: g => g.fillRect(0, 0, 10, 10) };
  const a = draw(g => prop(g, n, o)), b = draw(g => prop(g, n, { ...o }));
  assert.equal(a.g.st.depth, 0, `道具 ${n} save／restore 沒成對`);
  assert.equal(a.s, b.s, `道具 ${n} 同參數畫兩次不一樣`);
}
// walk：腿跟 t 走；stand：t 不影響
const walkAt = t => draw(g => person(g, { x: 0, y: 0, s: 100, pose: 'walk', t })).s;
// 腿＝最先畫的兩筆 stroke（髖→腳）
// 只比腳底端點（path 的 L 後面），身體上下晃不算
const legsAt = t => { const g = fakeCtx(); person(g, { pose: 'walk', t }); return g.log.filter(e => e[0] === 'stroke').slice(0, 2).map(e => e[1][0].d.split('L')[1]).join(' '); };
assert.notEqual(legsAt(0), legsAt(0.15), 'walk 在 t=0 與 t=0.15 腿位置一樣（腿沒動）');
assert.equal(walkAt(0.15), walkAt(0.15 + 1 / 1.6), 'walk 不是 t 的週期函數（有累積狀態？）');
assert.equal(draw(g => person(g, { pose: 'stand', t: 0 })).s, draw(g => person(g, { pose: 'stand', t: 9 })).s, 'stand 不該隨 t 變');
// 未知 pose／face／道具要丟錯，且丟錯前沒畫任何東西
assert.throws(() => person(fakeCtx(), { pose: 'dance' }), /dance/);
assert.throws(() => person(fakeCtx(), { face: 'angry' }), /angry/);
assert.throws(() => prop(fakeCtx(), 'rocket', {}), /rocket/);
assert.throws(() => prop(fakeCtx(), 'phone', { rows: 5 }), /rows/);
{ const g = fakeCtx(); try { person(g, { pose: 'dance' }); } catch {} assert.equal(g.log.length, 0, '未知 pose 丟錯前已經畫了東西'); }

// ---------- 2) 真瀏覽器：像素層級 ----------
const LIB = process.env.LIB || path.join(process.env.HOME, 'dev/lemo-opuscar');
const { openPage } = await import(path.join(ROOT, 'scripts/illust_page.mjs'));
const { page, close } = await openPage(LIB, path.join(ROOT, 'assets/illust'), 'preview.html', { w: 400, h: 400 });
try {
  const r = await page.evaluate(async () => {
    const L = await import('./illust.mjs');
    const c = Object.assign(document.createElement('canvas'), { width: 300, height: 300 }), g = c.getContext('2d');
    const shot = (fn) => { g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.fillStyle = '#f5efe6'; g.fillRect(0, 0, 300, 300); fn(); return c.toDataURL(); };
    const walk = t => shot(() => L.person(g, { x: 150, y: 280, s: 250, pose: 'walk', t, face: 'smile' }));
    const scene = () => shot(() => {
      L.person(g, { x: 80, y: 280, s: 200, pose: 'point', face: 'worried', body: '#6f8fb0' });
      for (const n of L.PROP_NAMES) L.prop(g, n, { x: 200, y: 150, s: 120, w: 120, h: 90, t: 0.4, title: '研究' });
    });
    const a = scene(), b = scene();
    // 狀態還原：畫完後 transform、alpha、陰影都回到原樣
    g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.shadowBlur = 0;
    for (const n of L.PROP_NAMES) L.prop(g, n, { x: 100, y: 100, s: 80, t: 0.2 });
    L.person(g, { x: 100, y: 200, s: 80, pose: 'think', dir: -1, tilt: 0.2 });
    const m = g.getTransform();
    return { same: a === b, walkDiff: walk(0) !== walk(0.15), walkSame: walk(0.3) === walk(0.3),
      restored: m.a === 1 && m.b === 0 && m.c === 0 && m.d === 1 && m.e === 0 && m.f === 0 && g.globalAlpha === 1 && g.shadowBlur === 0 };
  });
  assert.ok(r.same, '同參數畫兩次像素不同');
  assert.ok(r.walkDiff, 'walk 在不同 t 像素一樣');
  assert.ok(r.walkSame, 'walk 同 t 像素不同');
  assert.ok(r.restored, '畫完沒還原 transform／alpha／陰影');
} finally { await close(); }

// ---------- 3) 片內副本要跟正本一致（scripts/illust_install.sh） ----------
const sha = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
for (const f of fs.readdirSync(path.join(ROOT, 'films'))) {
  const copy = path.join(ROOT, 'films', f, 'illust/illust.mjs');
  if (fs.existsSync(copy)) assert.equal(sha(copy), sha(SRC), `films/${f}/illust/illust.mjs 跟正本不一致，重跑 bash scripts/illust_install.sh films/${f}`);
}
console.log('ok test_illust');
