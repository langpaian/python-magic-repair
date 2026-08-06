"""一次性生成 10 个更基础的故障（初级/中级/高级魔法）+ 10 条新法则。

主题：魔法材料世界。初级=材料与基础语法，中级=运算，高级=条件与循环。
生成后只需跑 validate_content 确认质量门。
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FAULTS = ROOT / "content" / "faults"

RU = {
    "syntax": "https://www.runoob.com/python3/python3-basic-syntax.html",
    "var": "https://www.runoob.com/python3/python3-variable-types.html",
    "str": "https://www.runoob.com/python3/python3-string.html",
    "ops": "https://www.runoob.com/python3/python3-operators.html",
    "cond": "https://www.runoob.com/python3/python3-conditional.html",
    "loop": "https://www.runoob.com/python3/python3-loop.html",
}

NEW = [
    # ---------------- 初级魔法：材料与基础语法 ----------------
    {
        "folder": "011-材料标签-名字没贴好",
        "task": dict(id="011", title="材料标签写岔了", customer="魔法学徒小奇",
                     law="标签要先贴好",
                     law_statement="机器说'这个名字我没听过'的时候，看看材料标签（变量名）是不是拼错了？",
                     difficulty=1, category="variables", expected_error="NameError", magic="初级魔法",
                     learn=dict(topic="变量与赋值", url=RU["var"],
                                note="用到的名字必须先被赋值（贴好标签）。机器不猜拼写——写岔一个字母，它就当是另一个人。")),
        "buggy": '# 魔法材料清单\nmaterial = "魔法石"\nprint("今天的材料是：" + materail)   # 标签拼错了\n',
        "tests": 'from solution import material\nassert material == "魔法石"\nprint("✓ 机器听懂你的意思了。")\n',
        "fixed": 'material = "魔法石"\nprint("今天的材料是：" + material)\n',
        "law": "# 标签要先贴好\n\n> 用到的名字，先写好标签（赋值），机器才认。\n\n给大人的话：NameError 是机器在说：'这个名字，你从没教过我。'变量拼写要前后一致——写岔一个字母，它当你是另一个人。\n",
        "story": "# 事故卷轴 · 贴错的标签\n\n学徒小奇把魔法石装进罐子，贴好标签 material。可念咒语时，他写的是 materail——一个从没贴过标签的名字。\n\n机器没有猜。它如实说：这个名字，我没见过。**它宁可停下来，也不猜。**\n\n---\n\n给大人的话：NameError 大多是拼写不一致。真实项目里，改过变量名却漏改其中一处，是最常见的翻车方式之一。\n",
    },
    {
        "folder": "012-报菜单-咒语没念完",
        "task": dict(id="012", title="报菜单的咒语念到一半断了", customer="占卜屋老板娘",
                     law="咒语必须念完整",
                     law_statement="机器说'这句话我没法读'的时候，看看括号、引号是不是没成双成对？",
                     difficulty=1, category="syntax", expected_error="SyntaxError", magic="初级魔法",
                     learn=dict(topic="基础语法", url=RU["syntax"],
                                note="括号和引号要成双成对——念到一半的咒语，机器听不懂。")),
        "buggy": '# 报菜单的咒语\nmenu = "魔法石 x 3"\nprint("今日菜单：" + menu   # 少了一个右括号\n',
        "tests": 'from solution import menu\nassert menu == "魔法石 x 3"\nprint("✓ 机器听懂你的意思了。")\n',
        "fixed": 'menu = "魔法石 x 3"\nprint("今日菜单：" + menu)\n',
        "law": "# 咒语必须念完整\n\n> 括号和引号要成双成对——念到一半的咒语不生效。\n\n给大人的话：SyntaxError 是机器在说：'这句话我没法读。'多半是少了右括号或引号，机器不会替你补。\n",
        "story": "# 事故卷轴 · 念到一半的咒语\n\n老板娘想让机器把今天的菜单念出来。她写了 print，话说到一半——右括号忘在了嘴里。\n\n机器等了一会儿，没有等到那句话说完。它如实说：**这句话，我没法读。**\n\n---\n\n给大人的话：SyntaxError 是语法层面的'话没说完'。真实项目里，写了一半被保存的文件，第一次跑就是这种报错。\n",
    },
    {
        "folder": "013-材料数量-拼不进句子",
        "task": dict(id="013", title="魔法石的数量拼不进句子", customer="宝库管理员",
                     law="数量要能写进话里",
                     law_statement="机器说'这两种东西不能相加'的时候，看看是不是数字要写进文字里？",
                     difficulty=1, category="types", expected_error="TypeError", magic="初级魔法",
                     learn=dict(topic="字符串 · 类型转换", url=RU["str"],
                                note="数字和文字是两种东西。把数字写进句子里，先 str() 转成文字，或直接 f-string。")),
        "buggy": '# 材料数量\nstones = 3\nprint("今天有" + stones + "块魔法石")   # 数字拼进句子\n',
        "tests": 'from solution import stones\nassert stones == 3\nprint("✓ 机器听懂你的意思了。")\n',
        "fixed": 'stones = 3\nprint("今天有" + str(stones) + "块魔法石")\n',
        "law": "# 数量要能写进话里\n\n> 数字要写进句子里，先 str() 转成文字。\n\n给大人的话：字符串和整数不能直接拼。str() 或 f-string，就是那道'把数字变成文字'的咒语。\n",
        "story": "# 事故卷轴 · 说不出口的数量\n\n宝库管理员想把'今天有 3 块魔法石'念出来。文字'今天有'和数字 3 被拼到了一起——机器愣住了。\n\n它不会悄悄把 3 变成文字。它如实说：**这两种东西，我拼不到一起。**\n\n---\n\n给大人的话：字符串 + 整数是新手第一高发的 TypeError。机器从不替你悄悄转换类型。\n",
    },
    {
        "folder": "014-真伪开关-念不出真伪",
        "task": dict(id="014", title="真伪开关念不出结果", customer="炼金术士",
                     law="真伪也能被念出",
                     law_statement="机器说'这两种东西不能相加'的时候，看看是不是想直接打印 True/False？",
                     difficulty=1, category="types", expected_error="TypeError", magic="初级魔法",
                     learn=dict(topic="布尔值 · print", url=RU["var"],
                                note="True/False 也是材料。拼进句子要 str()，或者用逗号分开打印。")),
        "buggy": 'is_ready = True\nprint("炉子准备好了：" + is_ready)   # 布尔拼进句子\n',
        "tests": 'from solution import is_ready\nassert is_ready == True\nprint("✓ 机器听懂你的意思了。")\n',
        "fixed": 'is_ready = True\nprint("炉子准备好了：", is_ready)\n',
        "law": "# 真伪也能被念出\n\n> True/False 也是材料——拼进句子也要转成文字，或用逗号分开打印。\n\n给大人的话：布尔值是一种类型。print 里直接用逗号传多个参数，就不必硬拼成字符串。\n",
        "story": "# 事故卷轴 · 念不出的真伪\n\n炼金术士给炉子装了个开关：准备好了，是 True；没准备好，是 False。可他想把这句话念出来时，机器又愣住了。\n\nTrue 不是文字，是'真'的开关状态。**机器不假装它是文字。**\n\n---\n\n给大人的话：布尔值、数字、文字都是不同的类型。print(\\\"炉子准备好了：\\\", is_ready) 用逗号，机器就懂。\n",
    },
    # ---------------- 中级魔法：运算 ----------------
    {
        "folder": "015-合成魔力-算错配方",
        "task": dict(id="015", title="合成魔力算错了配方", customer="炼金术士",
                     law="合成要按配方",
                     law_statement="答案不对劲的时候，看看运算写对了没有：该加的你写成了乘？",
                     difficulty=2, category="operators", expected_error="", magic="中级魔法",
                     learn=dict(topic="算术运算符", url=RU["ops"],
                                note="先想清楚语义：1 份火石 + 2 份风粉是相加，不是相乘。")),
        "buggy": '# 合成魔力值：火石 1 份 + 风粉 2 份，应该相加\nfire = 1\nwind = 2\ntotal = fire * wind     # 应该是 fire + wind\nprint("合成魔力：" + str(total))\n',
        "tests": 'from solution import total\nassert total == 3, "1 份火石 + 2 份风粉，合成魔力应该是 3"\nprint("✓ 机器听懂你的意思了。")\n',
        "fixed": 'fire = 1\nwind = 2\ntotal = fire + wind\nprint("合成魔力：" + str(total))\n',
        "law": "# 合成要按配方\n\n> 魔力值按配方算——加法还是乘法，机器照着来。\n\n给大人的话：先想清楚运算语义再写符号。1 + 2 写成了 1 * 2，机器不会提醒你配方错了。\n",
        "story": "# 事故卷轴 · 按错配方的炉子\n\n炼金术士的配方写得很清楚：一份火石，加两份风粉。可机器算出来的魔力不对。\n\n你低头一看——配方的'加'，被写成了'乘'。**机器只是照着执行，错的从来不是它。**\n\n---\n\n给大人的话：逻辑错（wrong answer, no crash）最难查，因为机器不报错。读懂'它算出了什么'，才能看出'该算什么'。\n",
    },
    {
        "folder": "016-魔石多少-箭头指反",
        "task": dict(id="016", title="魔石谁多谁少说反了", customer="魔法学徒小奇",
                     law="谁多谁少要看箭头",
                     law_statement="答案不对劲的时候，看看 > 和 < 是不是指反了方向？",
                     difficulty=2, category="comparison", expected_error="", magic="中级魔法",
                     learn=dict(topic="比较运算符", url=RU["ops"],
                                note="> 和 < 的开口朝向较大的数。3 > 5 是 False，5 > 3 才是 True。")),
        "buggy": '# 谁的魔石多？\nmine = 3\nyours = 5\nmore = mine > yours     # 应该是 yours > mine\nprint("你的魔石比我多吗？", more)\n',
        "tests": 'from solution import more\nassert more == True, "你有 5 块、我有 3 块，你的应该更多"\nprint("✓ 机器听懂你的意思了。")\n',
        "fixed": 'mine = 3\nyours = 5\nmore = yours > mine\nprint("你的魔石比我多吗？", more)\n',
        "law": "# 谁多谁少要看箭头\n\n> > 和 < 是指向多的一边的箭头，别指反。\n\n给大人的话：比较运算符的开口朝向较大的数。这是最容易被忽略的'看着对、实际反'的错。\n",
        "story": "# 事故卷轴 · 指向反了的箭头\n\n小奇有 3 块魔石，你比他多，有 5 块。他让机器判断'你的魔石比我多吗？'——机器想了想，说：不是。\n\n机器没错。他写成了 mine > yours（3 > 5），是 False。**箭头指向了少的那一边。**\n\n---\n\n给大人的话：> 的开口朝向较大的数。真实代码里，比较方向写反会造成静默的逻辑错误。\n",
    },
    {
        "folder": "017-平分魔石-整份零头搞混",
        "task": dict(id="017", title="平分魔石把整份和零头搞混", customer="占卜屋老板娘",
                     law="整份和零头要分开",
                     law_statement="分东西的答案不对时，看看 //（整份）和 %（零头）是不是用混了？",
                     difficulty=2, category="operators", expected_error="", magic="中级魔法",
                     learn=dict(topic="整除与取余", url=RU["ops"],
                                note="7 // 2 = 3（每人整份），7 % 2 = 1（剩下零头）。两个是不同的运算。")),
        "buggy": '# 7 块魔石分给 2 个学徒\nstones = 7\npeople = 2\neach = stones % people     # 应该是 //\nleft = stones // people    # 应该是 %\nprint("每人", each, "块，剩", left, "块")\n',
        "tests": 'from solution import each, left\nassert each == 3, "7 块分给 2 人，每人 3 块"\nassert left == 1, "剩下 1 块"\nprint("✓ 机器听懂你的意思了。")\n',
        "fixed": 'stones = 7\npeople = 2\neach = stones // people\nleft = stones % people\nprint("每人", each, "块，剩", left, "块")\n',
        "law": "# 整份和零头要分开\n\n> // 是整份，% 是零头，分材料别混。\n\n给大人的话：7 // 2 = 3、7 % 2 = 1。两个运算符服务不同的问题，用混了答案就差得远。\n",
        "story": "# 事故卷轴 · 分不清整份和零头\n\n老板娘要把 7 块魔石分给 2 个学徒。机器算出来'每人 1 块，剩 3 块'——把整份和零头弄反了。\n\n机器按你写的算：你先算了零头，再算了整份。**它不替你调换顺序。**\n\n---\n\n给大人的话：// 和 % 是'份数'和'余数'两件事。分东西、排队、循环分页，到处都用它们。\n",
    },
    # ---------------- 高级魔法：条件与循环 ----------------
    {
        "folder": "018-出门判断-条件说反",
        "task": dict(id="018", title="出门带伞的条件说反了", customer="魔法信使",
                     law="条件要对着想",
                     law_statement="条件的结果和你的意图反了时，看看 if 后面的判断是不是写反了？",
                     difficulty=2, category="condition", expected_error="", magic="高级魔法",
                     learn=dict(topic="条件控制 if/else", url=RU["cond"],
                                note="if 的条件为真才走里面。rainy == False 在真的下雨时反而走 else。")),
        "buggy": '# 下雨带伞\nrainy = True\nif rainy == False:     # 说反了，应该 if rainy:\n    advice = "带伞"\nelse:\n    advice = "不用带"\nprint(advice)\n',
        "tests": 'from solution import advice\nassert advice == "带伞", "下雨了应该带伞"\nprint("✓ 机器听懂你的意思了。")\n',
        "fixed": 'rainy = True\nif rainy:\n    advice = "带伞"\nelse:\n    advice = "不用带"\nprint(advice)\n',
        "law": "# 条件要对着想\n\n> if 的条件为真才走里面——把话说对。\n\n给大人的话：if rainy == False 在真的下雨时反而走 else。条件要对着你的意图写，别绕一个弯。\n",
        "story": "# 事故卷轴 · 说反的条件\n\n信使让机器决定带不带伞：如果下雨就带。机器看了看天——在下雨，却告诉他不用带。\n\n不是机器傻。他写的是 if rainy == False：下雨（True == False 不成立）→ 走 else。**条件对反了，结论就反了。**\n\n---\n\n给大人的话：条件判断是程序的分叉路口。一个 == False 的弯绕，让真实系统做出过完全相反的决定。\n",
    },
    {
        "folder": "019-数药水-多数少数",
        "task": dict(id="019", title="数药水多数了少数了", customer="卖魔药的老妇人",
                     law="数数别多数少数",
                     law_statement="数出来的数和实际的数不一样时，看看 range(起点, 终点) 的终点是不是不含它？",
                     difficulty=2, category="loop", expected_error="", magic="高级魔法",
                     learn=dict(topic="for 循环 · range", url=RU["loop"],
                                note="range(1, 3) 是 1、2 两个数；要数到 3，得写 range(1, 4)——终点不包含。")),
        "buggy": '# 数药水：3 瓶要数到 3\ncount = 0\nfor i in range(1, 3):     # 应该 range(1, 4)\n    count = count + 1\nprint("数了", count, "瓶")\n',
        "tests": 'from solution import count\nassert count == 3, "3 瓶药水要数到 3"\nprint("✓ 机器听懂你的意思了。")\n',
        "fixed": 'count = 0\nfor i in range(1, 4):\n    count = count + 1\nprint("数了", count, "瓶")\n',
        "law": "# 数数别多数少数\n\n> range(起点, 终点) 不含终点——数药水别多数少数。\n\n给大人的话：range(1, 3) 是 1、2 两个数。要 1、2、3，终点得写 4。off-by-one 是真实世界里最多见的循环错误。\n",
        "story": "# 事故卷轴 · 少数的那一瓶\n\n老妇人有 3 瓶药水，想让机器数一遍。机器数完说：2 瓶。\n\n不是它漏了。她写的是 range(1, 3)——机器数到 2 就停下，**因为终点那瓶它不数。**\n\n---\n\n给大人的话：range 的终点不含终点，这是新手第一道 off-by-one 关。真实系统里，这种'差一个'让火箭炸过、让卫星丢过。\n",
    },
    {
        "folder": "020-搅拌魔药-步子迈太大",
        "task": dict(id="020", title="搅拌魔药步子迈太大", customer="炼金术士",
                     law="搅拌要一步步来",
                     law_statement="循环跑的次数不对时，看看循环变量每次加的是不是 1？",
                     difficulty=2, category="loop", expected_error="", magic="高级魔法",
                     learn=dict(topic="while 循环", url=RU["loop"],
                                note="循环要记得让变量前进。一次加 2，5 下的活只干 3 下就停了。")),
        "buggy": '# 搅拌魔药 5 下\nstirs = 0\ntimes = 0\nwhile stirs < 5:\n    stirs = stirs + 2     # 一次迈两步，只搅了 3 下\n    times = times + 1\nprint("搅拌了", times, "下")\n',
        "tests": 'from solution import times\nassert times == 5, "应该搅拌 5 下"\nprint("✓ 机器听懂你的意思了。")\n',
        "fixed": 'stirs = 0\ntimes = 0\nwhile stirs < 5:\n    stirs = stirs + 1\n    times = times + 1\nprint("搅拌了", times, "下")\n',
        "law": "# 搅拌要一步步来\n\n> 循环要记得让变量前进，一步一个脚印。\n\n给大人的话：while 里不推进变量会死循环；推进太快（一次 +2）会少跑。步长要正好一步。\n",
        "story": "# 事故卷轴 · 迈了太大的步子\n\n炼金术士要搅拌魔药 5 下。机器搅了 3 下就停了——它每一步迈了两格。\n\n它没偷懒，是命令让它迈大步。**想让机器一步一步来，就给它一格的步子。**\n\n---\n\n给大人的话：while 循环的两大坑：忘记推进（死循环）和推进太快（少跑）。真实代码里，死循环会让程序卡死；步长错会让结果悄悄不对。\n",
    },
]

LAWS_ADD = """
  - id: tag-first
    name: 标签要先贴好
    error: NameError
    stage: 新手法师
    statement: "用到的名字，先写好标签（赋值），机器才认。"
    adult_note: "NameError 是机器在说：'这个名字，你从没教过我。'变量拼写要前后一致——写岔一个字母，它当你是另一个人。"

  - id: spell-complete
    name: 咒语必须念完整
    error: SyntaxError
    stage: 新手法师
    statement: "括号和引号要成双成对——念到一半的咒语不生效。"
    adult_note: "SyntaxError 是机器在说：'这句话我没法读。'多半是少了右括号或引号，机器不会替你补。"

  - id: count-in-sentence
    name: 数量要能写进话里
    error: TypeError
    stage: 新手法师
    statement: "数字要写进句子里，先 str() 转成文字。"
    adult_note: "字符串和整数不能直接拼。str() 或 f-string，就是那道'把数字变成文字'的咒语。"

  - id: truth-speakable
    name: 真伪也能被念出
    error: TypeError
    stage: 新手法师
    statement: "True/False 也是材料——拼进句子也要转成文字，或用逗号分开打印。"
    adult_note: "布尔值是一种类型。print 里直接用逗号传多个参数，就不必硬拼成字符串。"

  - id: recipe-math
    name: 合成要按配方
    error: ""
    stage: 见习维修师
    statement: "魔力值按配方算——加法还是乘法，机器照着来。"
    adult_note: "先想清楚运算语义再写符号。1 + 2 写成了 1 * 2，机器不会提醒你配方错了。"

  - id: arrow-compare
    name: 谁多谁少要看箭头
    error: ""
    stage: 见习维修师
    statement: "> 和 < 是指向多的一边的箭头，别指反。"
    adult_note: "比较运算符的开口朝向较大的数。这是最容易被忽略的'看着对、实际反'的错。"

  - id: whole-and-remainder
    name: 整份和零头要分开
    error: ""
    stage: 见习维修师
    statement: "// 是整份，% 是零头，分材料别混。"
    adult_note: "7 // 2 = 3、7 % 2 = 1。两个运算符服务不同的问题，用混了答案就差得远。"

  - id: condition-straight
    name: 条件要对着想
    error: ""
    stage: 熟练维修师
    statement: "if 的条件为真才走里面——把话说对。"
    adult_note: "if rainy == False 在真的下雨时反而走 else。条件要对着你的意图写，别绕一个弯。"

  - id: count-right
    name: 数数别多数少数
    error: ""
    stage: 熟练维修师
    statement: "range(起点, 终点) 不含终点——数药水别多数少数。"
    adult_note: "range(1, 3) 是 1、2 两个数。要 1、2、3，终点得写 4。off-by-one 是真实世界里最多见的循环错误。"

  - id: step-by-step
    name: 搅拌要一步步来
    error: ""
    stage: 熟练维修师
    statement: "循环要记得让变量前进，一步一个脚印。"
    adult_note: "while 里不推进变量会死循环；推进太快（一次 +2）会少跑。步长要正好一步。"
"""

# 已有故障的魔法等级
MAGIC_EXISTING = {
    "001": "中级魔法", "002": "高级魔法", "003": "初级魔法", "004": "初级魔法",
    "005": "高级魔法", "006": "初级魔法", "007": "大师魔法", "008": "大师魔法",
    "009": "大师魔法", "010": "中级魔法",
}


def main() -> None:
    for f in NEW:
        d = FAULTS / f["folder"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "task.yaml").write_text(_dump_task(f["task"]), encoding="utf-8")
        (d / "buggy.py").write_text(f["buggy"], encoding="utf-8")
        (d / "tests.py").write_text(f["tests"], encoding="utf-8")
        (d / "fixed.py").write_text(f["fixed"], encoding="utf-8")
        (d / "law.md").write_text(f["law"], encoding="utf-8")
        (d / "story.md").write_text(f["story"], encoding="utf-8")
        print("✓", f["folder"])

    # 给旧故障加 magic
    import yaml
    for p in FAULTS.glob("*/task.yaml"):
        t = p.read_text(encoding="utf-8")
        d = yaml.safe_load(t)
        fid = str(d["id"]).zfill(3)
        if fid in MAGIC_EXISTING and "magic" not in d:
            d["magic"] = MAGIC_EXISTING[fid]
            p.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False), encoding="utf-8")
            print(f"magic {fid} = {MAGIC_EXISTING[fid]}")

    # 追加新法则
    laws_path = ROOT / "content" / "laws.yaml"
    laws_path.write_text(laws_path.read_text(encoding="utf-8").rstrip() + "\n" + LAWS_ADD, encoding="utf-8")
    print("laws.yaml 已追加 10 条新法则")


def _dump_task(t: dict) -> str:
    import yaml
    return yaml.safe_dump(t, allow_unicode=True, sort_keys=False)


if __name__ == "__main__":
    main()
