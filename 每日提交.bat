@echo off
chcp 65001 >nul
title 硅基世界 2 - 每日提交
color 0A

echo.
echo ========================================
echo    硅基世界 2 - 每日自动提交
echo ========================================
echo.

cd /d "%~dp0"

REM 检查 Git 是否可用
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未找到 Git，请先安装 Git
    pause
    exit /b 1
)

REM 检查是否有更改
git status --porcelain > temp_status.txt
set /p HAS_CHANGES=<temp_status.txt
del temp_status.txt

if "%HAS_CHANGES%"=="" (
    echo [信息] 没有需要提交的更改
    echo.
    echo ✓ 所有更改已同步到 GitHub
    echo.
    pause
    exit /b 0
)

echo [信息] 发现以下更改：
echo ----------------------------------------
git status --short
echo ----------------------------------------
echo.

set /p CONFIRM="是否提交这些更改？(Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo.
    echo [已取消] 未提交更改
    pause
    exit /b 0
)

echo.
echo [步骤 1/3] 添加所有更改...
git add -A

echo.
echo [步骤 2/3] 提交更改...
set COMMIT_MSG=📝 每日提交 - %date:~0,4%-%date:~5,2%-%date:~8,2%
git commit -m "%COMMIT_MSG%"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [错误] 提交失败
    pause
    exit /b 1
)

echo.
echo [步骤 3/3] 推送到 GitHub...
git push origin main

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [警告] 推送失败，但本地提交已完成
    echo [提示] 请检查网络连接后手动执行：git push
    pause
    exit /b 1
)

echo.
echo ========================================
echo    ✓ 提交成功！
echo ========================================
echo.
echo 提交消息：%COMMIT_MSG%
echo.

pause
