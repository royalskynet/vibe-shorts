// 把 Clawd Bot 做成 AgentPet（Codex pet 格式）寵物：pet.json + 8×9 格、每格 192×208 的透明 spritesheet.webp。
// 用法：node scripts/agentpet_build.mjs [--install]   （--install 再複製到 ~/.agentpet/pets/clawd-bot/）
// 造型與 applyPose 直接用 assets/mascot/clawd-bot.svg、clawd-bot-shot.mjs，不另畫；這裡只負責每列動作的 pose。
// 列序與每列格數照 Codex pet 規格（對照 ~/.agentpet/pets/boba 實測）：
//   idle 6, running-right 8, running-left 8, waving 4, jumping 5, failed 8, waiting 6, running 6, review 6
import { readFileSync, mkdirSync, copyFileSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { homedir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const OUT = join(ROOT, 'assets/mascot/agentpet/clawd-bot');
const CELL_W = 192, CELL_H = 208, COLS = 8;
const ROWS = [['idle', 6], ['running-right', 8], ['running-left', 8], ['waving', 4], ['jumping', 5],
  ['failed', 8], ['waiting', 6], ['running', 6], ['review', 6]];
// ponytail: playwright-core 借 lemo-opuscar 的 node_modules；那邊移走就改這行或在本 repo 裝一份
const { chromium } = createRequire('/Users/51mini/dev/lemo-opuscar/package.json')('playwright-core');
const CHROME = process.env.PLAYWRIGHT_CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

const svg = readFileSync(join(ROOT, 'assets/mascot/clawd-bot/clawd-bot.svg'), 'utf8')
  .replace(/viewBox="[^"]*"/, 'viewBox="-104 -118 208 225"')   // 留上方給跳躍與特效，比例 = 192:208
  .replace(/width="\d+" height="\d+"/, `width="${CELL_W}" height="${CELL_H}"`)
  .replace(/ id="clawd-bot-svg"/, '');
const shot = readFileSync(join(ROOT, 'assets/mascot/clawd-bot-shot.mjs'), 'utf8').replace(/^export /gm, '');

// 每格的 pose：θ 走一整圈，讓每列首尾接得上。欄位同 poseAt 的回傳，另加 lean／legs／fx。
function frame(row, i, n) {
  const th = 2 * Math.PI * i / n, s = Math.sin(th);
  const p = {
    state: 'idle', bobY: s * 4.5, scaleX: 1 + s * 0.03, scaleY: 1 - s * 0.03,
    face: { x: 0, y: 0 }, sparkRot: 90 * i / n,
    clawL: { x: -66, y: 2 + s * 4, rot: s * 6 }, clawR: { x: 66, y: 2 + s * 4, rot: -s * 6 },
    lean: 0, legs: 0, fx: null,
  };
  if (row === 'running-right' || row === 'running-left') {
    const dir = row === 'running-right' ? 1 : -1;
    p.bobY = -Math.abs(s) * 9; p.lean = 7 * dir; p.legs = s * 16; p.face = { x: 7 * dir, y: 0 };
    p.clawL = { x: -62, y: 2 + s * 7, rot: 10 * dir }; p.clawR = { x: 62, y: 2 - s * 7, rot: 10 * dir };
    p.sparkRot = 180 * i / n;
  } else if (row === 'waving') {
    p.state = 'happy';
    p.clawR = { x: 66, y: -26, rot: -30 - s * 28 };
  } else if (row === 'jumping') {
    const bob = [3, -18, -32, -18, 3][i], squash = [0.08, -0.04, -0.02, -0.04, 0.08][i];
    p.state = 'happy'; p.bobY = bob; p.scaleX = 1 + squash; p.scaleY = 1 - squash;
    const up = bob < 0;
    p.clawL = { x: -64, y: up ? -14 : 6, rot: up ? 35 : -8 }; p.clawR = { x: 64, y: up ? -14 : 6, rot: up ? -35 : 8 };
    p.legs = up ? -10 : 0; p.fx = '';
  } else if (row === 'failed') {
    const k = Math.min(1, i / 4);             // 前半段垮下去，後半段趴著喘
    p.state = 'sleep'; p.bobY = 2 + k * 8 + (i >= 4 ? Math.sin(th * 2) * 1.2 : 0);
    p.scaleX = 1 + k * 0.05; p.scaleY = 1 - k * 0.05; p.face = { x: 0, y: 2 };
    p.clawL = { x: -66 + k * 10, y: 4 + k * 12, rot: -k * 20 }; p.clawR = { x: 66 - k * 10, y: 4 + k * 12, rot: k * 20 };
    p.sparkRot = 0;
    p.fx = i < 4 ? '<g transform="translate(58, -66)"><circle r="14" fill="#FFF" stroke="#252422" stroke-width="2.5"/>'
      + '<text y="6" font-size="17" font-weight="bold" text-anchor="middle" fill="#FF8577">!</text></g>' : '';
  } else if (row === 'waiting') {
    p.bobY = s * 3; p.face = { x: 4, y: -4 }; p.sparkRot = 45 * i / n;
    p.fx = '<g transform="translate(58, -66)"><circle r="15" fill="#FFF" stroke="#252422" stroke-width="2.5"/>'
      + `<text y="6" font-size="17" font-weight="bold" text-anchor="middle" fill="#D97757">${['?', '?', '?', '…', '…', '…'][i]}</text></g>`;
  } else if (row === 'running') {               // 工作中：沿用 thinking 的敲鍵盤
    p.state = 'thinking'; p.bobY = Math.sin(th * 2) * 4.5; p.sparkRot = 360 * i / n;
    p.clawL = { x: -58, y: 2 + Math.sin(th * 2) * 6, rot: 15 }; p.clawR = { x: 58, y: 2 - Math.sin(th * 2) * 6, rot: -15 };
  } else if (row === 'review') {                // 審查：一螯托腮、視線左右掃
    p.state = 'thinking'; p.bobY = s * 2; p.face = { x: s * 7, y: 1 };
    p.clawR = { x: 52, y: -8, rot: -40 }; p.fx = '';
  }
  return p;
}

const cells = [];
ROWS.forEach(([row, n], r) => { for (let i = 0; i < n; i++) cells.push({ r, c: i, pose: frame(row, i, n) }); });

const html = `<!doctype html><html><body style="margin:0;background:transparent">
<div id="sheet" style="position:relative;width:${CELL_W * COLS}px;height:${CELL_H * ROWS.length}px"></div>
<script>${shot}
const cells = ${JSON.stringify(cells)}, sheet = document.getElementById('sheet');
for (const { r, c, pose } of cells) {
  const box = document.createElement('div');
  box.style.cssText = 'position:absolute;left:' + c * ${CELL_W} + 'px;top:' + r * ${CELL_H} + 'px';
  box.innerHTML = ${JSON.stringify(svg)};
  sheet.appendChild(box);
  const root = box.querySelector('svg');
  pose.shadowRx = 50 - pose.bobY * 0.35;
  applyPose(root, pose);
  const actor = root.querySelector('#actor');
  actor.setAttribute('transform', 'rotate(' + pose.lean + ' 0 60) ' + actor.getAttribute('transform'));
  if (pose.legs) for (const [id, sign] of [['leg-l-1', 1], ['leg-r-2', 1], ['leg-r-1', -1], ['leg-l-2', -1]]) {
    const leg = root.querySelector('#' + id);
    leg.setAttribute('transform', leg.getAttribute('transform').replace(/rotate\\((-?[\\d.]+)/, (m, a) => 'rotate(' + (+a + sign * pose.legs)));
  }
  if (pose.fx !== null) root.querySelector('#fx').innerHTML = pose.fx;
}
window.READY = true;
</script></body></html>`;

mkdirSync(OUT, { recursive: true });
const browser = await chromium.launch({ executablePath: CHROME, args: ['--force-color-profile=srgb'] });
try {
  const page = await browser.newPage({ viewport: { width: CELL_W * COLS, height: CELL_H * ROWS.length } });
  const errors = [];
  page.on('pageerror', e => errors.push(e));
  await page.setContent(html);
  await page.waitForFunction('window.READY === true', null, { timeout: 10000 });
  if (errors.length) throw errors[0];
  await page.locator('#sheet').screenshot({ path: join(OUT, 'spritesheet.png'), omitBackground: true });
} finally { await browser.close(); }

execFileSync('cwebp', ['-quiet', '-lossless', '-exact', join(OUT, 'spritesheet.png'), '-o', join(OUT, 'spritesheet.webp')]);
// 預覽動圖給 README：每列循環兩次、10fps，透明底
const frames = [];
ROWS.forEach(([, n], r) => { for (let k = 0; k < 2; k++) for (let i = 0; i < n; i++) frames.push(`${CELL_W}x${CELL_H}+${i * CELL_W}+${r * CELL_H}`); });
execFileSync('magick', ['-dispose', 'background', '-delay', '10',
  ...frames.flatMap(g => ['(', join(OUT, 'spritesheet.png'), '-crop', g, '+repage', ')']),
  '-loop', '0', join(OUT, 'preview.gif')]);
writeFileSync(join(OUT, 'pet.json'), JSON.stringify({
  id: 'clawd-bot', displayName: 'Clawd Bot',
  description: '短影音頻道的智能機械蟹吉祥物：陶土橘機甲、LED 面罩、星芒天線。',
  spritesheetPath: 'spritesheet.webp', category: 'creature',
}, null, 2) + '\n');
console.log('built', OUT);

if (process.argv.includes('--install')) {
  const dst = join(homedir(), '.agentpet/pets/clawd-bot');
  mkdirSync(dst, { recursive: true });
  for (const f of ['pet.json', 'spritesheet.webp']) copyFileSync(join(OUT, f), join(dst, f));
  console.log('installed', dst);
}
