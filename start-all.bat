@echo off
chcp 65001 >nul
echo ============================================================
echo 硅基世界 2 - 完整启动脚本
echo ============================================================
echo.
echo 即将启动:
echo   1. 世界引擎（后台运行）
echo   2. Web 观察服务（http://localhost:8080）
echo.
echo 按任意键继续...
pause >nul
echo.

cd /d "%~dp0"

echo [1/3] 启动世界引擎...
start "硅基世界 2 - 引擎" python run_world_enhanced.py --duration 600

timeout /t 3 /nobreak >nul

echo [2/3] 启动 Web 服务...
start "硅基世界 2 - Web" cmd /k "cd web && python server.py"

timeout /t 5 /nobreak >nul

echo [3/3] 打开浏览器...
start http://localhost:8080

echo.
echo ============================================================
echo 硅基世界 2 已启动！
echo ============================================================
echo.
echo 服务状态:
echo   ✅ 世界引擎 - 运行中（600 秒）
echo   ✅ Web 服务 - http://localhost:8080
echo.
echo 停止服务:
echo   - 关闭引擎窗口停止世界运行
echo   - 关闭 Web 窗口停止 Web 服务
echo.
echo 查看报告:
echo   - reports/final_report.md
echo   - reports/stats_report.md
echo.
echo ============================================================
echo.
pause
