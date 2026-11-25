// 內頁大標取樣：開片子頁面，取首卡之後每張卡的尾幀，回報 window.TEXTS 的文字框。precheck.py「內頁大標」門呼叫它。
// 用法：node scripts/headline_check.mjs films/<name> [--size 1920x1080]   → stdout 一行 JSON：{cards:[{card, t, boxes:[{id,text,h}]}]}
// --size 預設 1080x1920；meta/format.json 存在時以它為準（橫式片）。
// 卡＝timeline.js 的一句（TL.lines，單人旁白片一句一卡）；尾幀＝下一句開始前 0.3 秒，最後一卡取片尾前 0.7 秒（含片尾系列卡）。
// 頁面沒有 window.TEXTS 或 TL 時 exit 3（precheck 判不適用前就先檢查過，這裡是保險）。
import path from 'path';
import { readFileSync, existsSync } from 'fs';
const LIB = process.env.LIB || path.join(process.env.HOME, 'dev/lemo-opuscar');
const { openDemo, closeServer } = await import(path.join(LIB, 'core/render/page.mjs'));
const dir = process.argv[2];
const si = process.argv.indexOf('--size');
let w = 1080, h = 1920;
if (si > 0) [w, h] = process.argv[si + 1].split('x').map(Number);
else if (existsSync(path.join(dir, 'meta/format.json'))) ({ w, h } = JSON.parse(readFileSync(path.join(dir, 'meta/format.json'), 'utf8')));
const { browser, page } = await openDemo(dir, { w, h });
const has = await page.evaluate(() => typeof window.TEXTS === 'function' && !!window.TL?.lines?.length);
if (!has) { await browser.close(); closeServer(); console.error('頁面沒有 window.TEXTS 或 window.TL'); process.exit(3); }
const times = await page.evaluate(() => {
  const L = TL.lines, out = [];
  for (let i = 1; i < L.length; i++) out.push({ card: i + 1, t: i + 1 < L.length ? L[i + 1].t0 - 0.3 : L[i].t1 + 0.1 });
  out.push({ card: 'end', t: window.DUR - 0.7 });
  return out;
});
const cards = [];
for (const c of times) {
  const boxes = await page.evaluate(async t => { const b = window.TEXTS(t); await window.render(t); return b; }, c.t);
  cards.push({ ...c, t: +c.t.toFixed(3), boxes: boxes.map(b => ({ id: b.id, text: b.text, h: +(b.y1 - b.y0).toFixed(1) })) });
}
await browser.close(); closeServer();
console.log(JSON.stringify({ cards }));
