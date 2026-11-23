// 輪播頁規則（node 與瀏覽器共用）：timeline.js 的 TL → 頁陣列。
// 第 0 頁＝封面（第一段＋帳號名）；之後每段一頁，超過 MAX 句平均拆頁；提問與收尾併成最後一頁＋CTA。
// lines 只放原台詞（測試靠這點核對不漏不重），帳號名與 CTA 放在 account／cta 欄。
(function (root) {
  const MAX = 6;
  const NAME = { clawd: 'Claude', host: '她' };   // AI 角色叫 Claude，不叫小爪
  const TAIL = ['提問', '收尾'];

  function chunk(lines) {
    const k = Math.ceil(lines.length / MAX), size = Math.ceil(lines.length / k), out = [];
    for (let i = 0; i < lines.length; i += size) out.push(lines.slice(i, i + size));
    return out;
  }

  function buildPages(TL, { account = '@paradoxbar 悖論小酒館', cta = '留言告訴我' } = {}) {
    const order = [], by = {};
    for (const l of TL.lines) {
      const s = TAIL.includes(l.section) ? '提問' : l.section;
      if (!by[s]) { by[s] = []; order.push(s); }
      by[s].push({ who: l.who, name: NAME[l.who] || l.who, text: l.text });
    }
    const pages = [];
    for (const s of order) for (const lines of chunk(by[s])) pages.push({ section: s, lines });
    if (!pages.length) return pages;
    pages[0].cover = true; pages[0].account = account;
    const last = pages[pages.length - 1];
    if (last.section === '提問') last.cta = cta;
    return pages;
  }

  root.buildPages = buildPages;
  if (typeof module !== 'undefined') module.exports = { buildPages, MAX };
})(typeof globalThis !== 'undefined' ? globalThis : this);
