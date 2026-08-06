"""给全部故障加上"属性"(魔法材料系)：精神/火/冰/空间/时间，并补一个元组(时间系)故障 021。

属性 → 施法特效颜色：
  精神(标量/基础/逻辑)=暖金  火(字符串)=橙红  冰(列表)=冰蓝  空间(字典)=深紫  时间(元组/固定)=银金
"""
import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
FAULTS = ROOT / "content" / "faults"

ATTR = {
    "001": "精神", "002": "冰", "003": "精神", "004": "火", "005": "空间",
    "006": "精神", "007": "冰", "008": "时间", "009": "精神", "010": "精神",
    "011": "精神", "012": "精神", "013": "火", "014": "精神", "015": "精神",
    "016": "精神", "017": "精神", "018": "精神", "019": "精神", "020": "精神",
    "021": "时间",
}

F021 = {
    "folder": "021-固定配方-时间定格",
    "task": dict(id="021", title="固定配方不能改", customer="炼金术士",
                 law="时间定格的配方",
                 law_statement="机器说'元组不支持修改'的时候，想想：有些东西定下来就是定下来了。",
                 difficulty=2, category="tuple", expected_error="TypeError", magic="高级魔法", attr="时间",
                 learn=dict(topic="元组 tuple", url="https://www.runoob.com/python3/python3-tuple.html",
                            note="元组 ( ) 是固定不变的配方，不能改其中一个材料。要变，就换个新配方。")),
    "buggy": '# 固定配方：元组定下来就不改\nrecipe = ("火石", "风粉")\nrecipe[0] = "水珠"     # 元组不能改！\nprint("配方：", recipe)\n',
    "tests": 'from solution import recipe\nassert recipe == ("火石", "风粉"), "固定配方应该保持原样"\nprint("✓ 机器听懂你的意思了。")\n',
    "fixed": 'recipe = ("火石", "风粉")\nprint("配方：", recipe)\n',
    "law": "# 时间定格的配方\n\n> 元组 ( ) 定下来就不改——时间把它定格了。\n\n给大人的话：元组不可变。想改其中一个元素？不行。要么换列表，要么新建一个元组。\n",
    "story": "# 事故卷轴 · 定格的配方\n\n炼金术士的祖传配方用括号订成一卷，定下来就再没改过。他想把'火石'换成'水珠'——卷轴纹丝不动。\n\n**时间把这份配方定格了。**不是机器刻板，是元组生来就不许变。\n\n---\n\n给大人的话：元组（tuple）是不可变序列。它比列表安全——不怕别人偷偷改。真实代码里，坐标、配置、固定集合都用元组。\n",
}

LAW_021 = """
  - id: tuple-frozen
    name: 时间定格的配方
    error: TypeError
    stage: 熟练维修师
    statement: "元组 ( ) 定下来就不改——时间把它定格了。"
    adult_note: "元组不可变。想改其中一个元素？不行。要么换列表，要么新建一个元组。"
"""


def main() -> None:
    # 1) 创建 021
    d = FAULTS / F021["folder"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "task.yaml").write_text(yaml.safe_dump(F021["task"], allow_unicode=True, sort_keys=False), encoding="utf-8")
    (d / "buggy.py").write_text(F021["buggy"], encoding="utf-8")
    (d / "tests.py").write_text(F021["tests"], encoding="utf-8")
    (d / "fixed.py").write_text(F021["fixed"], encoding="utf-8")
    (d / "law.md").write_text(F021["law"], encoding="utf-8")
    (d / "story.md").write_text(F021["story"], encoding="utf-8")
    print("✓ 021-固定配方-时间定格")

    # 2) 给全部故障加 attr
    for p in FAULTS.glob("*/task.yaml"):
        t = yaml.safe_load(p.read_text(encoding="utf-8"))
        fid = str(t["id"]).zfill(3)
        if fid in ATTR:
            t["attr"] = ATTR[fid]
            p.write_text(yaml.safe_dump(t, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print("✓ 全部故障已标属性")

    # 3) 追加法则
    lp = ROOT / "content" / "laws.yaml"
    lp.write_text(lp.read_text(encoding="utf-8").rstrip() + "\n" + LAW_021, encoding="utf-8")
    print("✓ 追加法则: 时间定格的配方")


if __name__ == "__main__":
    main()
