"""内容质量门：确保每个故障是"真的好"。

   - task.yaml 可解析、字段齐全
   - buggy.py 必须抛出 task.yaml 里声明的 expected_error
   - fixed.py + tests.py 必须全部通过
   - law / story 文件存在

跑法：  python scripts/validate_content.py
这是维护的超级武器：新增或 AI 生成的故障，先过这道门才允许上架。
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

# expected_error 对逻辑型故障是可选的（没有它就用隐藏测试判故障是否成立）
REQUIRED_FIELDS = ("id", "title", "customer", "law", "law_statement")


def run(args, timeout=10.0, cwd=None):
    return subprocess.run(list(args), capture_output=True, text=True, timeout=timeout, cwd=cwd)


def check_fixed_passes(fid, d):
    """把 fixed.py 当 solution.py 跑 tests.py，必须全过。"""
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        shutil.copy(d / "fixed.py", td / "solution.py")
        shutil.copy(d / "tests.py", td / "tests.py")
        r = run([sys.executable, "tests.py"], cwd=td)
        if r.returncode != 0:
            return f"[{fid}] fixed.py 没能通过 tests.py:\n{r.stderr[:400]}"
    return None


def check_code_fails_tests(fid, d, filename):
    """逻辑型故障：把指定文件当 solution 跑 tests.py，必须判失败。"""
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        shutil.copy(d / filename, td / "solution.py")
        shutil.copy(d / "tests.py", td / "tests.py")
        r = run([sys.executable, "tests.py"], cwd=td)
        if r.returncode == 0:
            return f"[{fid}] {filename} 竟然通过了 tests.py —— 故障不成立"
    return None


def main() -> int:
    errors: list[str] = []
    checked = 0

    for d in sorted((CONTENT / "faults").glob("*")):
        tf = d / "task.yaml"
        if not tf.exists():
            continue
        checked += 1
        try:
            task = yaml.safe_load(tf.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            errors.append(f"[{d.name}] task.yaml 解析失败: {e}")
            continue

        fid = str(task.get("id", d.name)).zfill(3)
        for field in REQUIRED_FIELDS:
            if not task.get(field):
                errors.append(f"[{fid}] task.yaml 缺字段: {field}")

        if not (d / "law.md").exists():
            errors.append(f"[{fid}] 缺 law.md")
        if not (d / "story.md").exists():
            errors.append(f"[{fid}] 缺 story.md")

        # 崩溃型故障：buggy.py 必须报预期的错；逻辑型故障：buggy 必须通不过测试
        expected = task.get("expected_error", "")
        if expected:
            r = run([sys.executable, str(d / "buggy.py")])
            if r.returncode == 0:
                errors.append(f"[{fid}] buggy.py 没有报错 —— 故障根本没坏")
            elif expected not in r.stderr:
                errors.append(f"[{fid}] buggy.py 报的不是 {expected}:\n{r.stderr[:300]}")
        else:
            err = check_code_fails_tests(fid, d, "buggy.py")
            if err:
                errors.append(err)

        err = check_fixed_passes(fid, d)
        if err:
            errors.append(err)

    print(f"检查了 {checked} 个故障，{len(errors)} 个问题。")
    for e in errors:
        print("  ✗ " + e)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
