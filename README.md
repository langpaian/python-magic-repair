# 🔮 Python 魔法维修铺

> 这个世界只有一条真理：**机器不会撒谎，它只是比你诚实。**

游戏化 Python 学习项目。你扮演一位魔法维修师，在 AI 维修精灵的陪伴下，
修复一台台"被诅咒的"程序——从报错中学会读代码、定位问题、验证修复。

## 一条命令开铺

```bash
./run.sh          # 首次运行会自动建 venv 装依赖
# 或手动：
# python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
# .venv/bin/python run.py
```

然后浏览器打开 **http://127.0.0.1:8000**，从「启蒙仪式」开始。

## 你会在里面遇到什么

- **启蒙仪式**：三段微型实验——先看世界听你的话，再看机器对你说真话，然后修好第一单。
- **任务单**：客人送来的坏咒语。读报错 → 改代码 → 提交修复 → 隐藏测试判对错。
- **法则图鉴**：每化解一单，点亮一条"机器说的真话"，收到一枚 Python 生成的 SVG 徽章。

## 项目结构

```
engine/           引擎：隔离执行、隐藏测试、图鉴/徽章、SQLite 进度
web/              FastAPI + Jinja2 + 原生 JS（零构建前端）
content/          ★ 内容 = 数据（法则 / 启蒙仪式 / 故障文件夹）
scripts/          validate_content.py —— 内容质量门
```

## 加一个新故障（不改引擎代码）

```bash
mkdir content/faults/004-我的故障
# 放进去：
#   task.yaml   元数据（id/title/customer/law/expected_error…）
#   buggy.py    故意写坏的代码（必须报 expected_error）
#   tests.py    隐藏测试（= 正确行为规格）
#   fixed.py    参考答案
#   law.md      法则卡     story.md   幕后故事（双声道）
python scripts/validate_content.py   # 过质量门
```

## 理念（给成年人读的话）

初学者觉得报错是"坏"；工程师知道，报错是机器在说真话。
这个项目想让人先**感觉到**那件事——然后再系统地学会怎么听。

## 安全说明

学习者代码只在本地子进程里跑（带超时、无网络特权）。不要直接把公网部署成
"服务器跑任意代码"——公开部署需要沙箱（见设计文档）。

## 公开试用版（GitHub Pages 静态版）

`site/` 是一个**纯静态版本**：学习者代码通过 Pyodide 在**访问者自己的浏览器**里跑，
不经过任何服务器，因此可以安全地放上 GitHub Pages 公开分享。

- 重新编译静态数据：`python scripts/build_static.py`（生成 `site/data/content.json`）
- 本地预览：`cd site && python -m http.server 8001`
- 部署：推送到 GitHub 后，`.github/workflows/pages.yml` 会自动把 `site/` 发布到 Pages
  （首次需在仓库 Settings → Pages 把 Source 设为 **GitHub Actions**）
- 多 CDN 自动回退：Pyodide 从 jsdelivr / fastly / unpkg 依次加载，对国内访问更稳
