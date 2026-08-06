"""学习成果：把化解过的故障变成可下载的成果档案。

一张会旋转的动态卡片——正面是法则徽章，悬停翻转，背面是你读懂的报错、
你写下的修复与事故卷轴。自带星空、漂浮、光泽扫过、徽章呼吸等动画。
"""
import html
from datetime import datetime

from engine import lore, runtime

_OUTCOME_CSS = """
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
"""


def _esc(s) -> str:
    return html.escape(str(s))


def _md_bold(text: str) -> str:
    parts = _esc(text).split("**")
    out = []
    for i, part in enumerate(parts):
        out.append(f"<b>{part}</b>" if i % 2 == 1 else part)
    return "".join(out)


def _story_html(story_text: str) -> str:
    paras = [p.strip() for p in story_text.split("\n\n") if p.strip()]
    return "".join(f"<p>{_md_bold(p)}</p>" for p in paras)


def error_headline(buggy_code: str) -> str:
    """跑一遍坏代码，取出报错最后一行——这就是学习者读懂的"真话"。"""
    r = runtime.run_code(buggy_code)
    if not r["ok"]:
        lines = [ln for ln in r["stderr"].strip().splitlines() if ln.strip()]
        return lines[-1] if lines else "（机器说了些什么，但没留下字。）"
    return "（它居然没报错？那问题藏在'答错了'里。）"


def _card_markup(fault, learner_solution: str, law: dict, date: str = "") -> str:
    stars = "★" * int(fault.difficulty or 1)
    badge = lore.badge_svg(fault.law_name)
    return f"""<div class="scene"><div class="card">
  <div class="face front">
    <div class="kicker">魔法维修 · 学习成果</div>
    <div class="badge">{badge}</div>
    <div class="big">{_esc(fault.law_name)}</div>
    <div class="sub">化解日期 {_esc(date)} · 难度 {stars}</div>
    <div class="hint">悬停翻转 · 看这单的报错与你写的修复</div>
  </div>
  <div class="face back">
    <h2>{_esc(fault.title)}</h2>
    <p class="customer">客人：{_esc(fault.customer)}</p>
    <h3>法则</h3>
    <p class="stmt">{_esc(law.get("statement", ""))}</p>
    <p class="adult">{_esc(law.get("adult_note", ""))}</p>
    <h3>你读懂的报错</h3>
    <pre class="err">{_esc(error_headline(fault.buggy_code))}</pre>
    <h3>你的修复 · 你写下的咒语</h3>
    <pre>{_esc(learner_solution or "（你的修复当时没有被保存下来。）")}</pre>
    <h3>事故卷轴</h3>
    <div class="story">{_story_html(fault.story_text)}</div>
  </div>
</div></div>"""


def _page(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>{_esc(title)}</title>
<style>{_OUTCOME_CSS}</style></head>
<body>
<div class="stars"></div>
{body}
<div class="foot">「机器不会撒谎，它只是比你诚实。」—— 魔法维修铺</div>
</body></html>"""


def outcome_card_html(fault, learner_solution: str, law: dict, date: str = "") -> str:
    """单张学习成果：一张旋转的动态卡片。"""
    return _page("学习成果 · " + fault.law_name, _card_markup(fault, learner_solution, law, date))


def portfolio_html(faults, records, laws, all_done: bool) -> str:
    """全部学习成果：一排会翻转的卡片；全部化解时末尾附维修师之证。"""
    cards: list[str] = []
    solved_ids: set[str] = set()
    for fid, solution, solved_at in records:
        solved_ids.add(fid)
        f = next((x for x in faults if x.id == fid), None)
        if f:
            cards.append(_card_markup(f, solution, laws.get(f.law_name, {}), str(solved_at)[:10]))

    date = datetime.now().strftime("%Y-%m-%d")
    cert = ""
    if all_done and cards:
        solved_laws = [f.law_name for f in faults if f.id in solved_ids]
        cert = f'<div class="cert-wrap">{lore.certificate_svg(solved_laws, date)}</div>'

    body = f'<div class="grid">{"".join(cards)}</div>{cert}'
    return _page("我的魔法维修 · 学习档案", body)
