"""进度存储：本地 SQLite，记录已化解的故障（法则）。"""
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
        "fault_id TEXT PRIMARY KEY, solved_at TEXT DEFAULT CURRENT_TIMESTAMP)"
    )
    return conn


def mark_solved(fault_id: str) -> None:
    with closing(_conn()) as c:
        c.execute("INSERT OR IGNORE INTO solved (fault_id) VALUES (?)", (fault_id,))
        c.commit()


def solved_list() -> list[str]:
    with closing(_conn()) as c:
        return [r[0] for r in c.execute("SELECT fault_id FROM solved ORDER BY fault_id")]


def is_solved(fault_id: str) -> bool:
    with closing(_conn()) as c:
        return c.execute("SELECT 1 FROM solved WHERE fault_id=?", (fault_id,)).fetchone() is not None
