@echo off
REM 硅基世界 2 - 快速启动脚本 (Windows Batch)
REM Author: 三二 🐱
REM Date: 2026-03-19

echo ========================================
echo   🌍 硅基世界 2 (Silicon World 2)
echo   多 AI 代理协作应用平台
echo ========================================
echo.

REM 检查 Python
echo [1/4] 检查 Python 环境...
python --version
if errorlevel 1 (
    echo   ❌ 未找到 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)
echo   ✅ Python 环境正常

REM 检查虚拟环境
echo.
echo [2/4] 检查虚拟环境...
if exist "venv" (
    echo   ✅ 虚拟环境已存在
) else (
    echo   ⚠️  虚拟环境不存在，创建中...
    python -m venv venv
    echo   ✅ 虚拟环境创建完成
)

REM 激活虚拟环境
echo.
echo [3/4] 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
if exist "requirements.txt" (
    echo   安装依赖中...
    pip install -r requirements.txt -q
    echo   ✅ 依赖安装完成
)

REM 启动服务
echo.
echo [4/4] 启动服务...
echo.
echo ========================================
echo   服务启动信息:
echo   - API 文档：http://localhost:8000/docs
echo   - Web UI:   http://localhost:3000
echo   - WebSocket: ws://localhost:8000/ws
echo ========================================
echo.
echo 按 Ctrl+C 停止服务
echo.

REM 启动 API 服务
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

pause
