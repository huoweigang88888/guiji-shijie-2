# 硅基世界 2 - 快速启动脚本 (Windows)
# Author: 三二 🐱
# Date: 2026-03-19

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🌍 硅基世界 2 (Silicon World 2)" -ForegroundColor Green
Write-Host "  多 AI 代理协作应用平台" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python
Write-Host "[1/4] 检查 Python 环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ 未找到 Python，请先安装 Python 3.10+" -ForegroundColor Red
    exit 1
}

# 检查依赖
Write-Host ""
Write-Host "[2/4] 检查依赖..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  ✅ 虚拟环境已存在" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  虚拟环境不存在，创建中..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "  ✅ 虚拟环境创建完成" -ForegroundColor Green
}

# 激活虚拟环境
Write-Host ""
Write-Host "[3/4] 激活虚拟环境..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# 安装依赖
if (Test-Path "requirements.txt") {
    Write-Host "  安装依赖中..." -ForegroundColor Yellow
    pip install -r requirements.txt -q
    Write-Host "  ✅ 依赖安装完成" -ForegroundColor Green
}

# 启动服务
Write-Host ""
Write-Host "[4/4] 启动服务..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  服务启动信息:" -ForegroundColor White
Write-Host "  - API 文档：http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "  - Web UI:   http://localhost:3000" -ForegroundColor Cyan
Write-Host "  - WebSocket: ws://localhost:8000/ws" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

# 启动 API 服务
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
