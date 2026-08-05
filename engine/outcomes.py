"""学习成果：把化解过的故障变成可下载的成果档案。

让学习留下看得见的东西——每修完一单，你都能带走一张"成果卡"：
上面有你读懂的报错、你写下的修复、你掌握的法则。全部学完，还有一整份学习档案。
"""
import html
from datetime import datetime

from engine import lore, runtime


def _md_bold(text: str) -> str:
    """把 **加粗** 转成 <b>（先转义防注入）。"""
    parts = html.escape(text).split("**")
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


_STYLES = """
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
"""


def outcome_card_html(fault, learner_solution: str, law: dict, date: str = "") -> str:
    title = html.escape(fault.title)
    customer = html.escape(fault.customer)
    law_name = html.escape(law.get("name", ""))
    statement = html.escape(law.get("statement", ""))
    adult = html.escape(law.get("adult_note", ""))
    err = html.escape(error_headline(fault.buggy_code))
    sol = html.escape(learner_solution or "（你的修复当时没有被保存下来。）")
    stars = "★" * int(fault.difficulty)
    badge = lore.badge_svg(fault.law_name)
    return f"""<div class="card">
  <h2>{title}</h2>
  <p class="customer">客人：{customer} · 化解日期：{date} · 难度 {stars}</p>
  <h3>法则 · {law_name}</h3>
  <p class="stmt">{statement}</p>
  <p class="adult">{adult}</p>
  <h3>你读懂的报错</h3>
  <pre class="err">{err}</pre>
  <h3>你的修复 · 你写下的咒语</h3>
  <pre>{sol}</pre>
  <h3>事故卷轴</h3>
  <div class="story">{_story_html(fault.story_text)}</div>
  <div class="badge">{badge}</div>
</div>"""


def portfolio_html(faults, records, laws, all_done: bool) -> str:
    """全部学习成果；若全部化解，末尾附维修师之证。"""
    cards = []
    solved_ids = set()
    for fid, solution, solved_at in records:
        solved_ids.add(fid)
        f = next((x for x in faults if x.id == fid), None)
        if not f:
            continue
        cards.append(outcome_card_html(f, solution, laws.get(f.law_name, {}), date=str(solved_at)[:10]))

    date = datetime.now().strftime("%Y-%m-%d")
    cert = ""
    if all_done and cards:
        solved_laws = [f.law_name for f in faults if f.id in solved_ids]
        cert = (
            '<div class="card" style="text-align:center">'
            f"<h3>维修师之证</h3>{lore.certificate_svg(solved_laws, date)}</div>"
        )

    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>我的魔法维修 · 学习档案</title>
<style>{_STYLES}</style></head>
<body><div class="doc">
  <h1>我的魔法维修 · 学习档案</h1>
  <p class="meta">化解法则 {len(cards)} 条 · 记录于 {date}</p>
  {''.join(cards)}
  {cert}
  <p class="foot">「机器不会撒谎，它只是比你诚实。」—— 魔法维修铺</p>
</div></body></html>"""
