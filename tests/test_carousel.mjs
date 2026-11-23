// 輪播頁規則：用 films/codex 的真 timeline 斷言固定頁數，且原台詞不漏不重、照順序。
// 跑：node tests/test_carousel.mjs
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { buildPages } = require('../scripts/carousel/pages.js');

global.window = global;
require('../films/codex/timeline.js');
const TL = global.TL;

// 1) codex：鉤子2／衝突12／轉折4／落點2／提問1＋收尾1 → 封面、衝突拆 6+6、轉折、落點、提問＋收尾 = 6 頁
const pages = buildPages(TL);
assert.equal(pages.length, 6, 'codex 應為 6 頁');
assert.deepEqual(pages.map(p => p.lines.length), [2, 6, 6, 4, 2, 2]);
assert.ok(pages[0].cover && pages[0].account, '第 0 頁是封面且有帳號名');
assert.equal(pages[0].lines[0].text, TL.lines[0].text, '封面第一句＝鉤子第一句');
assert.ok(pages.at(-1).cta, '最後一頁有 CTA');
assert.ok(pages.every(p => p.lines.length > 0), '沒有空頁');

// 2) 原台詞按序各出現恰一次（帳號名、CTA 不在 lines 裡）
assert.deepEqual(pages.flatMap(p => p.lines.map(l => l.text)), TL.lines.map(l => l.text));

// 3) AI 角色顯示名叫 Claude
for (const l of pages.flatMap(p => p.lines)) if (l.who === 'clawd') assert.equal(l.name, 'Claude');

// 4) 拆頁邊界：6 句不拆，7 句拆成 2 頁
const fake = n => ({ lines: [...Array(n)].map((_, i) => ({ section: '衝突', text: `第${i}句`, who: i % 2 ? 'clawd' : 'host' })) });
assert.equal(buildPages(fake(6)).length, 1);
assert.deepEqual(buildPages(fake(7)).map(p => p.lines.length), [4, 3]);

console.log('test_carousel ok');
