// 用 lemo 的靜態服務＋playwright 開某目錄裡的任意 html（openDemo 只認 index.html），等 window.READY。
// 給 scripts/illust_preview.mjs 與 tests/test_illust.mjs 用。
import path from 'path';
export async function openPage(LIB, dir, file, { w = 1080, h = 1920 } = {}) {
  const { serve, pageURL } = await import(path.join(LIB, 'core/render/serve.mjs'));
  const { EXE, ARGS } = await import(path.join(LIB, 'core/render/browser.mjs'));
  const { chromium } = await import(path.join(LIB, 'node_modules/playwright-core/index.mjs'));
  const srv = await serve(LIB);
  const url = pageURL(LIB, srv.port, dir).replace(/index\.html$/, encodeURIComponent(file));
  const browser = await chromium.launch({ executablePath: EXE, args: ARGS });
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  await page.goto(url);
  try { await page.waitForFunction(() => window.READY === true, null, { timeout: 30000 }); }
  catch (e) { await browser.close(); srv.server.close(); throw new Error(`${file} 沒等到 READY：${errs.join('；') || e.message}`); }
  if (errs.length) { await browser.close(); srv.server.close(); throw new Error(`${file} 頁面錯誤：${errs.join('；')}`); }
  return { page, close: async () => { await browser.close(); srv.server.close(); } };
}
