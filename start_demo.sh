#!/bin/bash

echo "===================================="
echo "  TradingAgents Web Demo 启动脚本"
echo "===================================="
echo

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 Python，请先安装 Python 3.10+"
    exit 1
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "[错误] 未找到 Node.js，请先安装 Node.js 18+"
    exit 1
fi

echo "[1/4] 安装后端依赖..."
pip3 install -r b_backend/requirements.txt

echo
echo "[2/4] 安装前端依赖..."
cd b_frontend
npm install
cd ..

echo
echo "[3/4] 启动后端服务..."
python3 -m b_backend.main &
BACKEND_PID=$!

echo
echo "[4/4] 启动前端服务..."
cd b_frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo
echo "===================================="
echo "  服务已启动！"
echo "  后端: http://localhost:8000"
echo "  前端: http://localhost:3000"
echo "  API文档: http://localhost:8000/docs"
echo "===================================="
echo
echo "按 Ctrl+C 停止服务"

# 等待进程
wait $BACKEND_PID $FRONTEND_PID
