"""引擎冒烟测试：运行、判定、内容加载。"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from engine import runtime  # noqa: E402
from engine.catalog import load_faults, load_initiation, load_laws  # noqa: E402
from engine.judge import run_hidden_tests  # noqa: E402


def test_cast_ok():
    r = runtime.run_code("print('hi')")
    assert r["ok"] and r["stdout"].strip() == "hi"


def test_cast_error_is_honest():
    r = runtime.run_code("1 / 0")
    assert not r["ok"] and "ZeroDivisionError" in r["stderr"]


def test_cast_timeout():
    r = runtime.run_code("while True: pass", timeout=1)
    assert r["timeout"]


def test_content_loads():
    assert len(load_faults()) == 21
    assert len(load_laws()) == 21
    assert len(load_initiation()["acts"]) == 3


def test_judge_rejects_buggy_accepts_fixed():
    """每个故障：坏代码必须判失败，参考解必须判通过。"""
    for f in load_faults():
        bad = run_hidden_tests(f.buggy_code, f.dir)
        good = run_hidden_tests(f.dir.joinpath("fixed.py").read_text(encoding="utf-8"), f.dir)
        assert not bad["ok"], f"{f.id} 的 buggy.py 不应通过隐藏测试"
        assert good["ok"], f"{f.id} 的 fixed.py 应通过隐藏测试"


def test_outcome_card_renders():
    from engine.outcomes import outcome_card_html

    f = load_faults()[0]
    card = outcome_card_html(
        f,
        "print('修好了')",
        {"name": "零的禁忌", "statement": "除法不接受零的拜访", "adult_note": "ZeroDivisionError 从不说谎"},
        date="2026-08-05",
    )
    assert "你读懂的报错" in card
    assert "零的禁忌" in card
    assert "修好了" in card  # 学习者自己的修复会被写进成果卡


def test_build_static_output_is_complete():
    """静态版构建产物：content.json 必须包含全部故障/法则/仪式/结尾。"""
    import json
    import pathlib
    import subprocess

    root = pathlib.Path(__file__).resolve().parent.parent
    subprocess.run([sys.executable, str(root / "scripts" / "build_static.py")], cwd=root, check=True)
    data = json.loads((root / "site" / "data" / "content.json").read_text(encoding="utf-8"))
    assert len(data["faults"]) == 21
    assert len(data["laws"]) == 21
    assert len(data["initiation"]["acts"]) == 3
    assert data["ending"]["title"]
    assert all(f.get("error_headline") for f in data["faults"])


def test_ending_loads_and_certificate_renders():
    from engine import lore
    from engine.catalog import load_ending

    e = load_ending()
    assert e["title"] == "觉醒 · 创造之权"
    assert len(e["epilogue"]) >= 3
    assert len(e["free_cast"]["success_lines"]) >= 1

    svg = lore.certificate_svg(["零的禁忌", "房间号必须存在", "名字必须先被念过"])
    assert "魔法维修师之证" in svg
    assert "零的禁忌" in svg
