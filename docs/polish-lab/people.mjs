// AI 生成的三位角色（髮型、臉、服裝各不同）：A 黃外套長髮女、B 綠背心眼鏡男、C 紅長外套銀髮女。
// 每人 6 個姿勢，畫布高度一致（腳底對齊），所以同一個 s 下三人與各姿勢大小一致。動作仍是 t 的純函數。
const WHO = ['A', 'B', 'C'], POSES = ['stand', 'armsUp', 'point', 'think', 'shrug', 'worry'];
const IMG = {};
export async function loadPeople(base) {
  await Promise.all(WHO.flatMap(w => POSES.map(async p => {
    const im = new Image(); im.src = `${base}${w}_${p}.png`; await im.decode(); IMG[`${w}_${p}`] = im;
  })));
}
export function person(g, o = {}) {
  const who = WHO.includes(o.who) ? o.who : 'A';
  let pose = POSES.includes(o.pose) ? o.pose : 'stand';
  if (pose === 'stand' && o.face === 'worried') pose = 'worry';
  const im = IMG[`${who}_${pose}`], H = im.naturalHeight, Wd = im.naturalWidth, k = (o.s || 100) / (H - 12);
  g.save(); g.translate(o.x || 0, o.y || 0);
  if (o.alpha != null) g.globalAlpha *= o.alpha;
  if (o.shadow !== false) {
    const rx = Wd * k * 0.42; g.save(); g.scale(1, 0.16);
    const gr = g.createRadialGradient(0, 0, 0, 0, 0, rx);
    gr.addColorStop(0, 'rgba(70,45,30,0.38)'); gr.addColorStop(1, 'rgba(70,45,30,0)');
    g.fillStyle = gr; g.beginPath(); g.arc(0, 0, rx, 0, 7); g.fill(); g.restore();
  }
  if (o.tilt) g.rotate(o.tilt);
  if ((o.dir ?? 1) < 0) g.scale(-1, 1);
  g.scale(k, k); g.translate(-Wd / 2, -(H - 6));
  g.drawImage(im, 0, 0);
  g.restore();
}
