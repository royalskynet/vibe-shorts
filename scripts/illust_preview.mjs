// 把 assets/illust/preview.html 截成 assets/illust/preview.png（插畫庫總覽）。
// 用法：LIB=~/dev/lemo-opuscar node scripts/illust_preview.mjs [輸出.png]
import path from 'path'; import { fileURLToPath } from 'url';
const LIB = process.env.LIB || path.join(process.env.HOME, 'dev/lemo-opuscar');
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const { openPage } = await import(path.join(ROOT, 'scripts/illust_page.mjs'));
const out = process.argv[2] || path.join(ROOT, 'assets/illust/preview.png');
const { page, close } = await openPage(LIB, path.join(ROOT, 'assets/illust'), 'preview.html', { w: 1080, h: 1920 });
await page.screenshot({ path: out, type: 'png' });
await close();
console.log('寫好', out);
