"""魔法维修铺 —— FastAPI 应用。

铺子大厅 / 启蒙仪式 / 任务卡 / 法则图鉴 / 徽章。
一切内容来自 content/ 目录，引擎代码不随内容变动。
"""
import pathlib

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from engine import lore, runtime
from engine.catalog import load_ending, load_faults, load_initiation, laws_by_name
from engine.judge import run_hidden_tests
from engine.outcomes import error_headline, outcome_card_html, portfolio_html
from engine.store import is_solved, mark_solved, solved_list, solved_records, solution_for

WEB_DIR = pathlib.Path(__file__).resolve().parent

app = FastAPI(title="Python 魔法维修铺")
app.mount("/static", StaticFiles(directory=WEB_DIR / "static"), name="static")
templates = Jinja2Templates(directory=WEB_DIR / "templates")

FAULTS = load_faults()
LAWS = laws_by_name()
INIT = load_initiation()
ENDING = load_ending()


@app.middleware("http")
async def no_cache(request: Request, call_next):
    """开发期不让浏览器缓存，避免旧 CSS/HTML 造成的"看着没修好"问题。"""
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store"
    return response


def _fault(fid: str):
    # 容错：/ticket/1 与 /ticket/001 都能找到同一单（id 统一补零）
    for candidate in (fid, fid.zfill(3)):
        f = next((f for f in FAULTS if f.id == candidate), None)
        if f:
            return f
    return None


def _next_unsolved(exclude: str | None = None):
    solved = solved_list()
    for f in FAULTS:
        if f.id not in solved and f.id != exclude:
            return f
    return None


def _all_solved() -> bool:
    return len(solved_list()) >= len(FAULTS) and len(FAULTS) > 0


@app.get("/", response_class=HTMLResponse)
def hall(request: Request):
    solved = solved_list()
    next_id = _next_unsolved()
    next_fid = next_id.id if next_id else None
    return templates.TemplateResponse(
        request,
        "hall.html",
        {
            "faults": FAULTS,
            "solved": solved,
            "solved_count": len(solved),
            "total_count": len(FAULTS),
            "next_fid": next_fid,
        },
    )


@app.get("/initiation", response_class=HTMLResponse)
def initiation(request: Request):
    return templates.TemplateResponse(request, "initiation.html", {"init": INIT})


@app.post("/cast")
def cast(code: str = Form("")):
    return JSONResponse(runtime.run_code(code))


@app.get("/ticket/{fid}", response_class=HTMLResponse)
def ticket(request: Request, fid: str):
    fault = _fault(fid)
    if fault is None:
        return HTMLResponse(
            '<div style="padding:60px;text-align:center;font-family:sans-serif;color:#a79fc8">'
            "<p>这个任务单不存在——它可能还没被写进 <code>content/</code> 目录。</p>"
            '<p><a href="/">← 回大厅</a></p></div>',
            status_code=404,
        )
    law = LAWS.get(fault.law_name, {})
    solved_set = set(solved_list())
    others_solved = all(f.id in solved_set for f in FAULTS if f.id != fid)
    return templates.TemplateResponse(
        request,
        "ticket.html",
        {
            "fault": fault,
            "law": law,
            "already_solved": is_solved(fid),
            "next_fault": _next_unsolved(exclude=fid),
            "others_solved": others_solved,
        },
    )


@app.post("/ticket/{fid}/run")
def ticket_run(fid: str, code: str = Form("")):
    return JSONResponse(runtime.run_code(code))


@app.post("/ticket/{fid}/submit")
def ticket_submit(fid: str, code: str = Form("")):
    fault = _fault(fid)
    if fault is None:
        return JSONResponse({"ok": False, "stderr": "没有这个任务单。"})
    result = run_hidden_tests(code, fault.dir)
    if result["ok"]:
        mark_solved(fid, code)  # 记下学习者自己的修复，供学习成果使用
        law = LAWS.get(fault.law_name, {})
        return JSONResponse(
            {
                "ok": True,
                "law_name": law.get("name", ""),
                "law_statement": law.get("statement", ""),
                "adult_note": law.get("adult_note", ""),
                "badge_url": f"/badge/{fault.law_name}",
                "story": fault.story_text,
                "out": result["stdout"],
            }
        )
    return JSONResponse({"ok": False, "out": result["stdout"], "stderr": result["stderr"]})


@app.get("/badge/{law_name}", response_class=Response)
def badge(law_name: str):
    return Response(content=lore.badge_svg(law_name), media_type="image/svg+xml")


@app.get("/awakening", response_class=HTMLResponse)
def awakening(request: Request):
    if not _all_solved():
        nxt = _next_unsolved()
        return templates.TemplateResponse(
            request,
            "awakening.html",
            {"ending": ENDING, "locked": True, "next_fid": nxt.id if nxt else None},
        )
    return templates.TemplateResponse(
        request,
        "awakening.html",
        {"ending": ENDING, "locked": False, "next_fid": None},
    )


@app.get("/certificate", response_class=Response)
def certificate():
    if not _all_solved():
        return Response("还没修完所有故障，毕业证还拿不了。", status_code=403)
    solved = set(solved_list())
    laws = [f.law_name for f in FAULTS if f.id in solved]
    return Response(content=lore.certificate_svg(laws), media_type="image/svg+xml")


@app.get("/outcomes", response_class=HTMLResponse)
def outcomes(request: Request):
    records = []
    for fid, _solution, solved_at in solved_records():
        f = _fault(fid)
        if not f:
            continue
        records.append(
            {
                "fid": fid,
                "fault": f,
                "law_name": f.law_name,
                "date": str(solved_at)[:10],
                "error_headline": error_headline(f.buggy_code),
            }
        )
    return templates.TemplateResponse(request, "outcomes.html", {"records": records})


@app.get("/outcomes/{fid}/download", response_class=Response)
def outcome_download(fid: str):
    fault = _fault(fid)
    if fault is None or not is_solved(fid):
        return HTMLResponse("先化解这一单，才能下载学习成果。", status_code=404)
    doc = outcome_card_html(fault, solution_for(fid), LAWS.get(fault.law_name, {}), date="")
    return Response(
        doc,
        media_type="text/html",
        headers={"Content-Disposition": f'attachment; filename="magic-repair-outcome-{fid}.html"'},
    )


@app.get("/outcomes/download", response_class=Response)
def outcomes_download():
    doc = portfolio_html(FAULTS, solved_records(), LAWS, all_done=_all_solved())
    return Response(
        doc,
        media_type="text/html",
        headers={"Content-Disposition": 'attachment; filename="my-magic-repair-learning-portfolio.html"'},
    )


@app.get("/lore", response_class=HTMLResponse)
def lore_page(request: Request):
    solved = solved_list()
    solved_laws = {f.law_name for f in FAULTS if f.id in solved}
    return templates.TemplateResponse(
        request,
        "lore.html",
        {
            "laws": list(LAWS.values()),
            "solved_laws": solved_laws,
            "solved_count": len(solved_laws),
        },
    )
