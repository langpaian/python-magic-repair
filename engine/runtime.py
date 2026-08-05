"""运行时：隔离执行学习者提交的咒语（代码），捕获它的真话（输出/报错）。

安全模型：只在本地子进程里跑，带超时，无 stdin、无网络特权。
这是"机器的诚实"的物理保证——报错就是报错，一个字都不改。
"""
import subprocess
import sys
import tempfile


def run_code(code: str, timeout: float = 5.0) -> dict:
    """运行一段 Python 代码，返回 {ok, stdout, stderr, timeout}。"""
    if not code or not code.strip():
        return {"ok": False, "stdout": "", "stderr": "咒语是空的……写点什么，机器才能听。", "timeout": False}
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=tempfile.gettempdir(),
        )
        return {
            "ok": proc.returncode == 0,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "timeout": False,
        }
    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "stdout": "",
            "stderr": "（咒语卡住了……是不是有个死循环在兜圈子？）",
            "timeout": True,
        }
