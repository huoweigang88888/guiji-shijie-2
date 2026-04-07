@echo off
chcp 65001 >nul
echo ============================================================
echo 硅基世界 2 - Web 观察服务
echo ============================================================
echo.
echo 正在启动 Web 服务器...
echo.

cd /d "%~dp0"

start http://localhost:8080
python server.py

echo.
echo 服务已停止
echo.
pause
