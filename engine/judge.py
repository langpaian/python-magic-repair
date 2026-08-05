"""判定器：跑隐藏测试。跑通 ≠ 修对，测试说了算。

把学习者代码写成 solution.py，与故障自带的 tests.py 一起在临时目录里执行。
tests.py 全过（退出码 0）才算"机器听懂了你的意思"。
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile


def run_hidden_tests(code: str, fault_dir: pathlib.Path, timeout: float = 10.0) -> dict:
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        (td / "solution.py").write_text(code, encoding="utf-8")
        shutil.copy(fault_dir / "tests.py", td / "tests.py")
        try:
            proc = subprocess.run(
                [sys.executable, "tests.py"],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=td,
            )
            return {"ok": proc.returncode == 0, "stdout": proc.stdout, "stderr": proc.stderr}
        except subprocess.TimeoutExpired:
            return {"ok": False, "stdout": "", "stderr": "（机器等太久了……它是不是在死循环里打转？）"}
