@echo off
echo ====================================
echo   TradingAgents Web Demo 启动脚本
echo ====================================
echo.

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)

:: 检查 Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Node.js，请先安装 Node.js 18+
    pause
    exit /b 1
)

echo [1/4] 安装后端依赖...
pip install -r b_backend\requirements.txt

echo.
echo [2/4] 安装前端依赖...
cd b_frontend
call npm install
cd ..

echo.
echo [3/4] 启动后端服务...
start "TradingAgents Backend" cmd /k "python -m b_backend.main"

echo.
echo [4/4] 启动前端服务...
cd b_frontend
start "TradingAgents Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ====================================
echo   服务已启动！
echo   后端: http://localhost:8000
echo   前端: http://localhost:3000
echo   API文档: http://localhost:8000/docs
echo ====================================
echo.
echo 按任意键打开浏览器...
pause >nul

start http://localhost:3000
