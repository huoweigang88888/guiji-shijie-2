# 公司多智能体系统启动脚本
# Company Multi-Agent System Launcher

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "           公司多智能体系统 - Company Multi-Agent System" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$workspaceRoot = "C:\Users\97RPZ8T\.openclaw\workspace\skills\ultimate-agent"

# 检查配置
Write-Host "[1/4] 检查配置文件..." -ForegroundColor Yellow
$configPath = Join-Path $workspaceRoot "configs\company-agents.json"
if (Test-Path $configPath) {
    $config = Get-Content $configPath -Raw | ConvertFrom-Json
    Write-Host "  ✓ 配置文件加载成功" -ForegroundColor Green
    Write-Host "  系统名称：$($config.name)" -ForegroundColor Gray
    Write-Host "  代理数量：$($config.agents.Count)" -ForegroundColor Gray
    Write-Host "  工作流数量：$($config.workflows.Count)" -ForegroundColor Gray
} else {
    Write-Host "  ✗ 配置文件不存在：$configPath" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 检查工作空间
Write-Host "[2/4] 初始化工作空间..." -ForegroundColor Yellow
$workspaces = @('product-manager', 'architect', 'senior-dev', 'ui-designer', 'qa', 'devops', 'data', 'hr', 'finance', 'marketing')
foreach ($ws in $workspaces) {
    $wsPath = Join-Path $workspaceRoot "workspaces\$ws"
    if (-not (Test-Path $wsPath)) {
        New-Item -ItemType Directory -Force -Path $wsPath | Out-Null
        Write-Host "  ✓ 创建：$ws" -ForegroundColor Green
    } else {
        Write-Host "  ✓ 已存在：$ws" -ForegroundColor Gray
    }
}
Write-Host ""

# 检查代理状态
Write-Host "[3/4] 检查代理状态..." -ForegroundColor Yellow
$activeAgents = 0
foreach ($ws in $workspaces) {
    $stateFile = Join-Path $workspaceRoot "workspaces\$ws\SESSION-STATE.md"
    if (Test-Path $stateFile) {
        $activeAgents++
    }
}
Write-Host "  活跃代理：$activeAgents / $($workspaces.Count)" -ForegroundColor Green
Write-Host ""

# 启动 CEO 协调器
Write-Host "[4/4] 启动 CEO 协调器..." -ForegroundColor Yellow
$ceoScript = Join-Path $workspaceRoot "agents\ceo_coordinator.py"
if (Test-Path $ceoScript) {
    Write-Host "  OK CEO 协调器就绪" -ForegroundColor Green
    Write-Host "  脚本位置：$ceoScript" -ForegroundColor Gray
} else {
    Write-Host "  X CEO 协调器脚本不存在" -ForegroundColor Red
}
Write-Host ""

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "                    系统启动完成！" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "可用命令:" -ForegroundColor Yellow
Write-Host "  python agents\ceo_coordinator.py  - 测试 CEO 协调器" -ForegroundColor Gray
Write-Host "  通过 webchat/Discord/Telegram 发送任务指令" -ForegroundColor Gray
Write-Host ""
Write-Host "配置文件：configs\company-agents.json" -ForegroundColor Gray
Write-Host "系统文档：docs\公司多智能体系统.md" -ForegroundColor Gray
Write-Host ""
