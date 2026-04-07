@echo off
chcp 65001 >nul
REM 硅基世界 2 - 自动提交脚本
REM 每天自动提交更改到 GitHub

echo ========================================
echo   硅基世界 2 - 自动提交到 GitHub
echo   时间：%date% %time%
echo ========================================
echo.

cd /d "%~dp0"

REM 检查是否有更改
git status --porcelain > temp_status.txt
set /p HAS_CHANGES=<temp_status.txt
del temp_status.txt

if "%HAS_CHANGES%"=="" (
    echo [INFO] 没有需要提交的更改
    echo.
    echo ✅ 所有更改已同步
    goto :EOF
)

echo [INFO] 发现未提交的更改：
git status --short
echo.

REM 添加所有更改
echo [STEP 1] 添加所有更改...
git add -A
if errorlevel 1 (
    echo [ERROR] git add 失败
    goto :EOF
)

REM 提交更改
echo [STEP 2] 提交更改...
set COMMIT_MSG=🤖 自动提交 - %date:~0,4%-%date:~5,2%-%date:~8,2% %time:~0,2%:%time:~3,2%

git commit -m "%COMMIT_MSG%"
if errorlevel 1 (
    echo [ERROR] git commit 失败
    goto :EOF
)

echo.
echo [INFO] 提交成功：%COMMIT_MSG%

REM 推送到 GitHub
echo [STEP 3] 推送到 GitHub...
git push origin main
if errorlevel 1 (
    echo [ERROR] git push 失败
    echo [INFO] 本地提交已完成，推送失败（可能需要手动推送）
    goto :EOF
)

echo.
echo ========================================
echo   ✅ 自动提交完成！
echo   时间：%date% %time%
echo ========================================
