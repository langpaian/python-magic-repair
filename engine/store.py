"""进度存储：本地 SQLite，记录已化解的故障（法则）与学习者的修复代码。"""
import pathlib
import sqlite3
from contextlib import closing

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "progress.db"


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS solved ("
        "fault_id TEXT PRIMARY KEY, solution TEXT DEFAULT '', "
        "solved_at TEXT DEFAULT CURRENT_TIMESTAMP)"
    )
    # 老库升级：补上 solution 列
    cols = [row[1] for row in conn.execute("PRAGMA table_info(solved)")]
    if "solution" not in cols:
        conn.execute("ALTER TABLE solved ADD COLUMN solution TEXT DEFAULT ''")
        conn.commit()
    return conn


def mark_solved(fault_id: str, solution: str = "", solved_at: str = "") -> None:
    """记录化解。solved_at 由浏览器本机时间提供，避免 UTC 时区差。"""
    with closing(_conn()) as c:
        if solved_at:
            c.execute(
                "INSERT INTO solved (fault_id, solution, solved_at) VALUES (?, ?, ?) "
                "ON CONFLICT(fault_id) DO UPDATE SET solution=excluded.solution, solved_at=excluded.solved_at",
                (fault_id, solution, solved_at),
            )
        else:
            c.execute(
                "INSERT INTO solved (fault_id, solution) VALUES (?, ?) "
                "ON CONFLICT(fault_id) DO UPDATE SET solution=excluded.solution",
                (fault_id, solution),
            )
        c.commit()


def solved_list() -> list[str]:
    with closing(_conn()) as c:
        return [r[0] for r in c.execute("SELECT fault_id FROM solved ORDER BY fault_id")]


def solved_records() -> list[tuple[str, str, str]]:
    """返回 [(fault_id, solution, solved_at)]，按化解时间排序。"""
    with closing(_conn()) as c:
        return list(c.execute("SELECT fault_id, solution, solved_at FROM solved ORDER BY solved_at"))


def is_solved(fault_id: str) -> bool:
    with closing(_conn()) as c:
        return c.execute("SELECT 1 FROM solved WHERE fault_id=?", (fault_id,)).fetchone() is not None


def solution_for(fault_id: str) -> str:
    with closing(_conn()) as c:
        row = c.execute("SELECT solution FROM solved WHERE fault_id=?", (fault_id,)).fetchone()
        return row[0] if row else ""


def solved_at_for(fault_id: str) -> str:
    with closing(_conn()) as c:
        row = c.execute("SELECT solved_at FROM solved WHERE fault_id=?", (fault_id,)).fetchone()
        return row[0] if row else ""
