@echo off
chcp 65001 >nul
echo ============================================================
echo 🌍 硅基世界 2 - 三天工作任务
echo ============================================================
echo.
echo 启动时间：%date% %time%
echo.
echo 任务说明:
echo   Day 1: 世界启动 + 基础互动验证
echo   Day 2: 深化互动 + 协作任务
echo   Day 3: 自主演化 + 成果展示
echo.
echo 预计时长：10-15 分钟
echo.
echo ============================================================
echo.

cd /d "%~dp0"

python run_3days_mission.py

echo.
echo ============================================================
echo 任务完成！
echo ============================================================
echo.
echo 输出文件:
echo   - reports/day1_report.md
echo   - reports/day2_report.md
echo   - reports/day3_final_report.md
echo   - reports/knowledge_graph.md
echo   - reports/stories.md
echo.
pause
