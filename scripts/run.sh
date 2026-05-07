#!/bin/bash
# 启动 API 服务
cd "$(dirname "$0")/.."
pip install -r requirements.txt -q
uvicorn src.api.server:app --host 0.0.0.0 --port 8000 --reload
