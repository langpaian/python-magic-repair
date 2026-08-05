#!/usr/bin/env bash
# 一条命令开铺
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  echo "首次运行：创建环境…"
  python3 -m venv .venv
fi
.venv/bin/pip install --quiet -r requirements.txt
exec .venv/bin/python run.py
