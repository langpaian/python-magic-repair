// 共享逻辑：加载内容、本地进度、SVG 徽章、学习成果 HTML、下载。
const App = (() => {
  const OUTCOME_CSS = `
  * { box-sizing: border-box; }
  body { margin: 0; min-height: 100vh; display: flex; flex-direction: column;
    align-items: center; justify-content: center; gap: 18px; padding: 30px 14px 70px;
    font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; color: #3a3126;
    background:
      radial-gradient(900px 520px at 18% -6%, rgba(217,164,65,.20), transparent),
      radial-gradient(720px 480px at 86% 8%, rgba(194,87,27,.10), transparent),
      #f6efdf;
    overflow-x: hidden; }
  .stars { position: fixed; inset: 0; pointer-events: none; opacity: .5;
    background-image:
      radial-gradient(1.5px 1.5px at 12% 22%, rgba(164,118,63,.5), transparent 60%),
      radial-gradient(1px 1px at 34% 8%, rgba(217,164,65,.55), transparent 60%),
      radial-gradient(1.5px 1.5px at 58% 34%, rgba(194,87,27,.35), transparent 60%),
      radial-gradient(1px 1px at 76% 14%, rgba(164,118,63,.45), transparent 60%),
      radial-gradient(1px 1px at 88% 42%, rgba(217,164,65,.4), transparent 60%),
      radial-gradient(1.5px 1.5px at 22% 66%, rgba(201,151,46,.5), transparent 60%),
      radial-gradient(1px 1px at 46% 82%, rgba(164,118,63,.4), transparent 60%);
    animation: twinkle 7s ease-in-out infinite alternate; }
  @keyframes twinkle { from { opacity: .3; } to { opacity: .6; } }

  .grid { display: flex; flex-wrap: wrap; gap: 28px; justify-content: center; max-width: 1400px; }
  .scene { perspective: 1500px; width: 430px; max-width: 92vw; animation: float 7s ease-in-out infinite; }
  @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
  .card { position: relative; width: 100%; height: 570px; transform-style: preserve-3d;
    transition: transform 1s cubic-bezier(.4,.2,.2,1); }
  .scene:hover .card { transform: rotateY(180deg); }
  .face { position: absolute; inset: 0; backface-visibility: hidden; -webkit-backface-visibility: hidden;
    border-radius: 22px; padding: 28px 30px;
    background: linear-gradient(160deg, #fbf4e3, #efe2c6);
    border: 1px solid rgba(164,118,63,.55);
    box-shadow: 0 0 70px rgba(201,151,46,.35), inset 0 0 60px rgba(255,240,210,.35); overflow: hidden; }
  .front { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
  .front::before { content: ""; position: absolute; top: -40%; left: -60%; width: 55%; height: 220%;
    background: linear-gradient(115deg, transparent, rgba(255,255,255,.35), transparent);
    transform: rotate(22deg); animation: shine 4.5s ease-in-out infinite; }
  @keyframes shine { 0%, 55% { left: -60%; } 100% { left: 160%; } }
  .back { transform: rotateY(180deg); overflow-y: auto; }
  .back::-webkit-scrollbar { width: 6px; }
  .back::-webkit-scrollbar-thumb { background: rgba(164,118,63,.4); border-radius: 3px; }

  .kicker { color: #9c8f76; font-size: 13px; letter-spacing: 3px; margin-bottom: 18px; }
  .badge svg { width: 175px; filter: drop-shadow(0 0 24px rgba(201,151,46,.5));
    animation: pulse 3s ease-in-out infinite; }
  @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.07); } }
  .big { margin: 14px 0 4px; color: #8a6a34; font-size: 30px;
    font-family: Georgia, "Songti SC", serif; letter-spacing: 2px; }
  .sub { color: #9c8f76; font-size: 13px; margin: 0; }
  .hint { color: #9c8f76; font-size: 12px; margin-top: 18px; }

  h2 { margin: 0 0 4px; font-size: 20px; }
  h3 { margin: 16px 0 6px; color: #a4763f; font-size: 13px; letter-spacing: 1px; }
  .customer { color: #9c8f76; font-size: 13px; margin: 0; }
  .stmt { color: #5a4a2e; line-height: 1.7; }
  .adult { color: #9c8f76; font-size: 13px; line-height: 1.7; }
  pre { background: #2b2620; border: 1px solid rgba(207,224,192,.18); border-radius: 10px; padding: 12px;
    font-family: Menlo, Consolas, monospace; font-size: 12px; white-space: pre-wrap; word-break: break-word;
    color: #e8dcc8; line-height: 1.55; }
  pre.err { color: #ffb49a; }
  .story { color: #3a3126; line-height: 1.8; }
  .story b { color: #a4763f; }
  .story p { margin: 0 0 8px; }
  .cert-wrap { text-align: center; margin-top: 40px; }
  .cert-wrap svg { max-width: 92vw; height: auto; filter: drop-shadow(0 0 30px rgba(201,151,46,.35)); }
  .foot { position: fixed; bottom: 14px; width: 100%; text-align: center; color: #9c8f76; font-size: 12px; opacity: .8; }
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

  // 浏览器本机时间（避免 UTC 时区差 8 小时）
  function localStamp() {
    const d = new Date();
    const p = (n) => String(n).padStart(2, "0");
    return d.getFullYear() + "-" + p(d.getMonth() + 1) + "-" + p(d.getDate()) + " " + p(d.getHours()) + ":" + p(d.getMinutes());
  }
  function localDate() {
    const d = new Date();
    const p = (n) => String(n).padStart(2, "0");
    return d.getFullYear() + "-" + p(d.getMonth() + 1) + "-" + p(d.getDate());
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
    p[id] = { solution, date: localStamp() };  // 浏览器本机时间
    saveProgress(p);
  }
  function solutionFor(id) { const p = progress(); return p[id] ? p[id].solution : ""; }
  function solvedList() { return Object.keys(progress()).sort(); }

  // ---- SVG 徽章 / 证书（移植自 engine/lore.py）----
  function badgeSVG(lawName, date) {
    const d = date || localDate();
    const name = esc(lawName);
    return '<svg xmlns="http://www.w3.org/2000/svg" width="300" height="360" viewBox="0 0 300 360">'
      + '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#fbf4e3"/><stop offset="100%" stop-color="#efe2c6"/></linearGradient>'
      + '<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#d9a441"/><stop offset="100%" stop-color="#a4763f"/></linearGradient></defs>'
      + '<rect width="300" height="360" rx="18" fill="url(#bg)"/>'
      + '<path d="M150 40 L250 90 L250 190 Q250 250 150 310 Q50 250 50 190 L50 90 Z" fill="none" stroke="url(#gold)" stroke-width="3"/>'
      + '<text x="150" y="175" text-anchor="middle" font-family="Georgia,serif" font-size="22" fill="#8a6a34">已化解</text>'
      + '<text x="150" y="225" text-anchor="middle" font-family="Georgia,serif" font-size="19" fill="#3a3126">' + name + "</text>"
      + '<text x="150" y="338" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#9c8f76">' + d + "</text></svg>";
  }

  function certSVG(lawNames, date) {
    const d = date || localDate();
    const laws = esc((lawNames || []).join(" · ") || "（法则待填）");
    return '<svg xmlns="http://www.w3.org/2000/svg" width="620" height="440" viewBox="0 0 620 440">'
      + '<defs><linearGradient id="cbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#fbf4e3"/><stop offset="100%" stop-color="#efe2c6"/></linearGradient>'
      + '<linearGradient id="cgold" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#d9a441"/><stop offset="100%" stop-color="#a4763f"/></linearGradient></defs>'
      + '<rect width="620" height="440" rx="20" fill="url(#cbg)"/>'
      + '<rect x="14" y="14" width="592" height="412" rx="14" fill="none" stroke="url(#cgold)" stroke-width="2" stroke-dasharray="6 4"/>'
      + '<text x="310" y="86" text-anchor="middle" font-family="Georgia,serif" font-size="34" fill="#8a6a34" letter-spacing="6">魔法维修师之证</text>'
      + '<text x="310" y="130" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#9c8f76">—— 授予一名学会了倾听机器真话的人 ——</text>'
      + '<text x="310" y="200" text-anchor="middle" font-family="sans-serif" font-size="17" fill="#6b5f4c">已化解法则：</text>'
      + '<text x="310" y="252" text-anchor="middle" font-family="Georgia,serif" font-size="22" fill="#3a3126">' + laws + "</text>"
      + '<text x="310" y="330" text-anchor="middle" font-family="sans-serif" font-size="13" fill="#9c8f76">' + d + "</text></svg>";
  }

  // ---- 学习成果（移植自 engine/outcomes.py）----
  function cardMarkup(fault, solution, law, date) {
    const stars = "★".repeat(fault.difficulty || 1);
    return '<div class="scene"><div class="card">'
      + '<div class="face front">'
      + '<div class="kicker">魔法维修 · 学习成果</div>'
      + '<div class="badge">' + badgeSVG(fault.law, date) + "</div>"
      + '<div class="big">' + esc(fault.law) + "</div>"
      + '<div class="sub">化解日期 ' + esc(date || "") + " · 难度 " + stars + "</div>"
      + '<div class="hint">悬停翻转 · 看这单的报错与你写的修复</div>'
      + "</div>"
      + '<div class="face back">'
      + "<h2>" + esc(fault.title) + "</h2>"
      + '<p class="customer">客人：' + esc(fault.customer) + "</p>"
      + "<h3>法则</h3>"
      + '<p class="stmt">' + esc(law.statement || "") + "</p>"
      + '<p class="adult">' + esc(law.adult_note || "") + "</p>"
      + "<h3>你读懂的报错</h3>"
      + '<pre class="err">' + esc(fault.error_headline || "") + "</pre>"
      + "<h3>你的修复 · 你写下的咒语</h3>"
      + "<pre>" + esc(solution || "（你的修复当时没有被保存下来。）") + "</pre>"
      + "<h3>事故卷轴</h3>"
      + '<div class="story">' + storyHTML(fault.story) + "</div>"
      + "</div>"
      + "</div></div>";
  }

  function pageShell(title, body) {
    return '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><title>' + esc(title) + "</title>"
      + '<style>' + OUTCOME_CSS + "</style></head><body>"
      + '<div class="stars"></div>'
      + body
      + '<div class="foot">「机器不会撒谎，它只是比你诚实。」—— 魔法维修铺</div>'
      + "</body></html>";
  }

  function outcomeCardHTML(fault, solution, law, date) {
    return pageShell("学习成果 · " + fault.law, cardMarkup(fault, solution, law, date));
  }

  function portfolioHTML(content, records) {
    const cards = records.map((r) => {
      const f = content.faults.find((x) => x.id === r.fid);
      return f ? cardMarkup(f, r.solution, content.laws[f.law] || {}, r.date) : "";
    }).join("");
    const date = new Date().toISOString().slice(0, 10);
    const solvedLaws = records.map((r) => content.faults.find((x) => x.id === r.fid)).filter(Boolean).map((f) => f.law);
    const cert = solvedLaws.length === content.faults.length && solvedLaws.length
      ? '<div class="cert-wrap">' + certSVG(solvedLaws, date) + "</div>"
      : "";
    return pageShell("我的魔法维修 · 学习档案", '<div class="grid">' + cards + "</div>" + cert);
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
