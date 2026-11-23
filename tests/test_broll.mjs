import assert from 'node:assert/strict';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SRC = path.join(ROOT, 'assets', 'broll', 'broll.mjs');

const { frameIndex, coverRect, framePath, drawBroll } = await import(SRC);

const clip = { dir: 'broll/a', start: 1, fps: 30, count: 60 };

assert.equal(frameIndex(0.5, clip), -1);
assert.equal(frameIndex(1, clip), 0);
assert.equal(frameIndex(1.5, clip), 15);
assert.equal(frameIndex(3, clip), -1);
assert.equal(frameIndex(1.02, clip), 0, 'floor 不是 ceil');
assert.equal(frameIndex(2.99, clip), 59);
const clip0 = { dir: 'broll/a', start: 0, fps: 30, count: 60 };
assert.equal(frameIndex(-0.1, clip0), -1, '負時間不畫');
assert.equal(frameIndex(0, clip0), 0);

const rect = coverRect(1920, 1080, 1080, 1920);
assert.equal(rect.h, 1920);
assert.ok(Math.abs(rect.w - 3413.3333333333335) < 1e-6, `w=${rect.w}`);
assert.ok(Math.abs(rect.x + 1166.6666666666667) < 1e-6, `x=${rect.x}`);
assert.equal(rect.y, 0);

const same = coverRect(960, 540, 1920, 1080);
assert.deepEqual(same, { x: 0, y: 0, w: 1920, h: 1080 });

// 比畫布更瘦長的直式圖：等寬放大、上下裁，不准拉伸
assert.deepEqual(coverRect(1080, 2400, 1080, 1920), { x: 0, y: -240, w: 1080, h: 2400 });

assert.equal(framePath({ dir: 'broll/a' }, 0), 'broll/a/0001.jpg');
assert.equal(framePath({ dir: 'broll/a' }, 41), 'broll/a/0042.jpg');

function fakeCtx() {
  const log = [];
  return new Proxy({}, {
    get(_, k) {
      if (k === 'log') return log;
      return (...a) => log.push([k, a]);
    },
    set() { return true; },
  });
}

const img = { width: 1920, height: 1080 };
const load = async (p) => img;

const ctxIn = fakeCtx();
await drawBroll(ctxIn, clip, 1, { W: 1080, H: 1920, load });
const diIn = ctxIn.log.filter((e) => e[0] === 'drawImage');
assert.equal(diIn.length, 1, 'in range should draw once');
assert.deepEqual(diIn[0][1], [img, rect.x, rect.y, rect.w, rect.h]);

for (const t of [0.5, 3]) {
  const ctxOut = fakeCtx();
  await drawBroll(ctxOut, clip, t, { W: 1080, H: 1920, load });
  assert.equal(ctxOut.log.filter((e) => e[0] === 'drawImage').length, 0, `t=${t} should not draw`);
}

console.log('ok test_broll');
