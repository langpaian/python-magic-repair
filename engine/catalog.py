"""内容目录：读取 content/ 下所有"数据"（法则、启蒙仪式、故障）。

核心思想：增删内容 = 增删文件，引擎永远不用动。
"""
import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"


class Fault:
    def __init__(self, task: dict, dir: pathlib.Path):
        self.task = task
        self.dir = dir
        # YAML 会把 001 解析成整数 1，这里统一补零，保证 id 恒为三位
        self.id = str(task["id"]).zfill(3)
        self.title = task["title"]
        self.customer = task.get("customer", "一位神秘的客人")
        self.law_name = task["law"]
        self.law_statement = task.get("law_statement", "")
        self.difficulty = task.get("difficulty", 1)
        self.buggy_code = (dir / "buggy.py").read_text(encoding="utf-8")
        self.fixed_code = (dir / "fixed.py").read_text(encoding="utf-8") if (dir / "fixed.py").exists() else ""
        self.story_text = (dir / "story.md").read_text(encoding="utf-8") if (dir / "story.md").exists() else ""


def load_faults() -> list[Fault]:
    faults = []
    for d in sorted(CONTENT.glob("faults/*")):
        task_file = d / "task.yaml"
        if task_file.exists():
            task = yaml.safe_load(task_file.read_text(encoding="utf-8"))
            faults.append(Fault(task, d))
    return faults


def load_laws() -> list[dict]:
    data = yaml.safe_load((CONTENT / "laws.yaml").read_text(encoding="utf-8"))
    return data["laws"]


def laws_by_name() -> dict:
    return {law["name"]: law for law in load_laws()}


def load_initiation() -> dict:
    return yaml.safe_load((CONTENT / "initiation" / "scenes.yaml").read_text(encoding="utf-8"))


def load_ending() -> dict:
    return yaml.safe_load((CONTENT / "awakening.yaml").read_text(encoding="utf-8"))
