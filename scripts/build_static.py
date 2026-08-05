"""把 content/ 编译成 GitHub Pages 用的静态数据（site/data/content.json）。

用法： python scripts/build_static.py
会在 site/ 下生成 data/content.json，并同步 site/css/style.css。
之后 site/ 就是可以被 GitHub Pages 托管的纯静态站点。
"""
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine.catalog import load_ending, load_faults, load_initiation, load_laws  # noqa: E402
from engine.outcomes import error_headline  # noqa: E402

SITE = ROOT / "site"


def main() -> None:
    faults = []
    for f in load_faults():
        faults.append(
            {
                "id": f.id,
                "title": f.title,
                "customer": f.customer,
                "law": f.law_name,
                "law_statement": f.law_statement,
                "difficulty": f.difficulty,
                "category": f.task.get("category", ""),
                "buggy_code": f.buggy_code,
                "fixed_code": f.fixed_code,
                "tests_code": (f.dir / "tests.py").read_text(encoding="utf-8"),
                "story": f.story_text,
                "error_headline": error_headline(f.buggy_code),
            }
        )

    data = {
        "faults": faults,
        "laws": {law["name"]: law for law in load_laws()},
        "initiation": load_initiation(),
        "ending": load_ending(),
    }

    (SITE / "data").mkdir(parents=True, exist_ok=True)
    (SITE / "css").mkdir(parents=True, exist_ok=True)
    (SITE / "js").mkdir(parents=True, exist_ok=True)
    (SITE / "data" / "content.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    shutil.copy(ROOT / "web/static/style.css", SITE / "css/style.css")
    shutil.copy(ROOT / "web/static/editor.js", SITE / "js/editor.js")
    print(f"✓ 编译 {len(faults)} 个故障 → site/data/content.json")


if __name__ == "__main__":
    main()
