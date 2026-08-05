// 共享逻辑：加载内容、本地进度、SVG 徽章、学习成果 HTML、下载。
const App = (() => {
  const PORTFOLIO_CSS = `
    * { box-sizing: border-box; }
    body { margin: 0; background: #0e0a22; color: #ede7ff; font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; padding: 40px 20px; }
    .doc { max-width: 700px; margin: 0 auto; }
    h1 { color: #f5d98a; letter-spacing: 3px; margin: 0 0 4px; font-size: 24px; }
    h2 { color: #ede7ff; margin: 0 0 6px; font-size: 20px; }
    h3 { color: #c49a3c; letter-spacing: 2px; margin: 20px 0 8px; font-size: 13px; }
    .meta, .customer { color: #a79fc8; font-size: 13px; margin: 2px 0 0; }
    .stmt { color: #e3daff; line-height: 1.7; }
    .adult { color: #a79fc8; font-size: 13px; line-height: 1.7; }
    pre { background: #0b0818; border: 1px solid rgba(212,175,55,.25); border-radius: 10px; padding: 14px; font-family: Menlo, Consolas, monospace; font-size: 12.5px; white-space: pre-wrap; word-break: break-word; color: #d6ecff; line-height: 1.55; }
    .err pre { color: #ff8a7a; }
    .story { color: #d8d0f0; line-height: 1.8; }
    .story b { color: #f5d98a; }
    .story p { margin: 0 0 8px; }
    .badge { text-align: center; margin-top: 12px; }
    .card { background: #1a1130; border: 1px solid rgba(212,175,55,.4); border-radius: 16px; padding: 28px 30px; margin-bottom: 26px; }
    .foot { text-align: center; color: #a79fc8; font-size: 12px; margin-top: 30px; }
  `;
  let content = null;
  let loading = null;

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function mdBold(text) {
    return esc(text).split("**").map((p, i) => (i % 2 ? "<b>" + p + "</b>" : p)).join("");
  }
  function storyHTML(story) {
    return String(story).split("\n\n").map((p) => "<p>" + mdBold(p) + "</p>").join("");
  }

  function ready() {
    if (content) return Promise.resolve(content);
    if (loading) return loading;
    loading = fetch("data/content.json").then((r) => r.json()).then((d) => { content = d; return d; });
    return loading;
  }

  // ---- 进度（localStorage）----
  function progress() {
    try { return JSON.parse(localStorage.getItem("mr_progress") || "{}"); } catch (e) { return {}; }
  }
  function saveProgress(p) { localStorage.setItem("mr_progress", JSON.stringify(p)); }
  function isSolved(id) { return !!progress()[id]; }
  function markSolved(id, solution) {
    const p = progress();
    p[id] = { solution, date: new Date().toISOString().slice(0, 16).replace("T", " ") };
    saveProgress(p);
  }
  function solutionFor(id) { const p = progress(); return p[id] ? p[id].solution : ""; }
  function solvedList() { return Object.keys(progress()).sort(); }

  // ---- SVG 徽章 / 证书（移植自 engine/lore.py）----
  function badgeSVG(lawName, date) {
    const d = date || new Date().toISOString().slice(0, 10);
    const name = esc(lawName);
    return '<svg xmlns="http://www.w3.org/2000/svg" width="300" height="360" viewBox="0 0 300 360">'
      + '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#1a1030"/><stop offset="100%" stop-color="#0d0a1f"/></linearGradient>'
      + '<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#f5d98a"/><stop offset="100%" stop-color="#c49a3c"/></linearGradient></defs>'
      + '<rect width="300" height="360" rx="18" fill="url(#bg)"/>'
      + '<path d="M150 40 L250 90 L250 190 Q250 250 150 310 Q50 250 50 190 L50 90 Z" fill="none" stroke="url(#gold)" stroke-width="3"/>'
      + '<text x="150" y="175" text-anchor="middle" font-family="Georgia,serif" font-size="22" fill="#f5d98a">已化解</text>'
      + '<text x="150" y="225" text-anchor="middle" font-family="Georgia,serif" font-size="19" fill="#e8e0ff">' + name + "</text>"
      + '<text x="150" y="338" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#8a7fb8">' + d + "</text></svg>";
  }

  function certSVG(lawNames, date) {
    const d = date || new Date().toISOString().slice(0, 10);
    const laws = esc((lawNames || []).join(" · ") || "（法则待填）");
    return '<svg xmlns="http://www.w3.org/2000/svg" width="620" height="440" viewBox="0 0 620 440">'
      + '<defs><linearGradient id="cbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#1c1436"/><stop offset="100%" stop-color="#0e0a22"/></linearGradient>'
      + '<linearGradient id="cgold" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#f5d98a"/><stop offset="100%" stop-color="#b98f2f"/></linearGradient></defs>'
      + '<rect width="620" height="440" rx="20" fill="url(#cbg)"/>'
      + '<rect x="14" y="14" width="592" height="412" rx="14" fill="none" stroke="url(#cgold)" stroke-width="2" stroke-dasharray="6 4"/>'
      + '<text x="310" y="86" text-anchor="middle" font-family="Georgia,serif" font-size="34" fill="#f5d98a" letter-spacing="6">魔法维修师之证</text>'
      + '<text x="310" y="130" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#a79fc8">—— 授予一名学会了倾听机器真话的人 ——</text>'
      + '<text x="310" y="200" text-anchor="middle" font-family="sans-serif" font-size="17" fill="#ede7ff">已化解法则：</text>'
      + '<text x="310" y="252" text-anchor="middle" font-family="Georgia,serif" font-size="22" fill="#d8d0f0">' + laws + "</text>"
      + '<text x="310" y="330" text-anchor="middle" font-family="sans-serif" font-size="13" fill="#8a7fb8">' + d + "</text></svg>";
  }

  // ---- 学习成果（移植自 engine/outcomes.py）----
  function outcomeCardHTML(fault, solution, law, date) {
    const stars = "★".repeat(fault.difficulty || 1);
    return '<div class="card">'
      + "<h2>" + esc(fault.title) + "</h2>"
      + '<p class="customer">客人：' + esc(fault.customer) + " · 化解日期：" + esc(date || "") + " · 难度 " + stars + "</p>"
      + "<h3>法则 · " + esc(law.name || "") + "</h3>"
      + '<p class="stmt">' + esc(law.statement || "") + "</p>"
      + '<p class="adult">' + esc(law.adult_note || "") + "</p>"
      + "<h3>你读懂的报错</h3>"
      + '<pre class="err">' + esc(fault.error_headline || "") + "</pre>"
      + "<h3>你的修复 · 你写下的咒语</h3>"
      + "<pre>" + esc(solution || "（你的修复当时没有被保存下来。）") + "</pre>"
      + "<h3>事故卷轴</h3>"
      + '<div class="story">' + storyHTML(fault.story) + "</div>"
      + '<div class="badge">' + badgeSVG(fault.law, date) + "</div>"
      + "</div>";
  }

  function portfolioHTML(content, records) {
    const cards = records.map((r) => {
      const f = content.faults.find((x) => x.id === r.fid);
      return f ? outcomeCardHTML(f, r.solution, content.laws[f.law] || {}, r.date) : "";
    }).join("");
    const date = new Date().toISOString().slice(0, 10);
    const solvedLaws = records.map((r) => content.faults.find((x) => x.id === r.fid)).filter(Boolean).map((f) => f.law);
    const cert = solvedLaws.length === content.faults.length && solvedLaws.length
      ? '<div class="card" style="text-align:center"><h3>维修师之证</h3>' + certSVG(solvedLaws, date) + "</div>"
      : "";
    return '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><title>我的魔法维修 · 学习档案</title>'
      + '<style>' + PORTFOLIO_CSS + "</style></head><body><div class=\"doc\">"
      + "<h1>我的魔法维修 · 学习档案</h1>"
      + '<p class="meta">化解法则 ' + records.length + " 条 · 记录于 " + date + "</p>"
      + cards + cert
      + '<p class="foot">「机器不会撒谎，它只是比你诚实。」—— 魔法维修铺</p>'
      + "</div></body></html>";
  }

  function download(filename, text) {
    const blob = new Blob([text], { type: "text/html;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 200);
  }

  return { ready, esc, mdBold, storyHTML, progress, isSolved, markSolved, solutionFor, solvedList, badgeSVG, certSVG, outcomeCardHTML, portfolioHTML, download };
})();
