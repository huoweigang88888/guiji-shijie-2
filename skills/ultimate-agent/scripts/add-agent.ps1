# 添加新代理脚本
# 用法：.\add-agent.ps1 -AgentId "agent-legal" -AgentName "法务顾问代理" -Role "Legal Advisor"

param(
    [Parameter(Mandatory=$true)]
    [string]$AgentId,
    
    [Parameter(Mandatory=$true)]
    [string]$AgentName,
    
    [Parameter(Mandatory=$true)]
    [string]$Role,
    
    [Parameter(Mandatory=$false)]
    [string]$Description = "",
    
    [Parameter(Mandatory=$false)]
    [string[]]$Capabilities = @(),
    
    [Parameter(Mandatory=$false)]
    [string]$Model = "bailian/qwen3.5-plus",
    
    [Parameter(Mandatory=$false)]
    [string[]]$Triggers = @()
)

$workspaceRoot = "C:\Users\97RPZ8T\.openclaw\workspace\skills\ultimate-agent"
$configPath = Join-Path $workspaceRoot "configs\company-agents.json"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "           添加新代理 - Add New Agent" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# 1. 读取现有配置
Write-Host "[1/4] 读取配置文件..." -ForegroundColor Yellow
if (-not (Test-Path $configPath)) {
    Write-Host "  ✗ 配置文件不存在：$configPath" -ForegroundColor Red
    exit 1
}

$config = Get-Content $configPath -Raw | ConvertFrom-Json
Write-Host "  ✓ 配置文件加载成功" -ForegroundColor Green
Write-Host "  当前代理数：$($config.agents.Count)" -ForegroundColor Gray
Write-Host ""

# 2. 检查 ID 是否重复
Write-Host "[2/4] 检查代理 ID..." -ForegroundColor Yellow
$existingIds = $config.agents | ForEach-Object { $_.id }
if ($existingIds -contains $AgentId) {
    Write-Host "  ✗ 代理 ID 已存在：$AgentId" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ 代理 ID 可用" -ForegroundColor Green
Write-Host ""

# 3. 创建代理配置
Write-Host "[3/4] 创建代理配置..." -ForegroundColor Yellow

if (-not $Description) {
    $Description = "$Role 代理，负责相关业务"
}

if ($Capabilities.Count -eq 0) {
    $Capabilities = @("通用能力 1", "通用能力 2", "通用能力 3")
}

if ($Triggers.Count -eq 0) {
    $Triggers = @($AgentName, $Role)
}

$newAgent = [PSCustomObject]@{
    id = $AgentId
    name = $AgentName
    role = $Role
    description = $Description
    capabilities = $Capabilities
    model = $Model
    workspace = "workspaces/$($AgentId -replace 'agent-', '')"
    triggers = $Triggers
}

$config.agents += $newAgent
Write-Host "  ✓ 代理配置创建成功" -ForegroundColor Green
Write-Host "  代理 ID: $AgentId" -ForegroundColor Gray
Write-Host "  代理名称：$AgentName" -ForegroundColor Gray
Write-Host "  角色：$Role" -ForegroundColor Gray
Write-Host ""

# 4. 保存配置
Write-Host "[4/4] 保存配置文件..." -ForegroundColor Yellow
$config | ConvertTo-Json -Depth 10 | Out-File -FilePath $configPath -Encoding UTF8
Write-Host "  ✓ 配置已保存" -ForegroundColor Green
Write-Host ""

# 5. 创建工作空间
Write-Host "[5/5] 创建工作空间..." -ForegroundColor Yellow
$workspaceName = $AgentId -replace 'agent-', ''
$workspacePath = Join-Path $workspaceRoot "workspaces\$workspaceName"

if (-not (Test-Path $workspacePath)) {
    New-Item -ItemType Directory -Force -Path $workspacePath | Out-Null
    Write-Host "  ✓ 创建目录：$workspacePath" -ForegroundColor Green
    
    # 创建 SESSION-STATE.md
    $stateContent = @"
# $AgentName - Session State

**Agent ID**: $AgentId  
**Role**: $Role  
**Status**: 🟢 Active  
**Initialized**: $(Get-Date -Format 'yyyy-MM-dd')

---

## Current Tasks
- [ ] 等待任务分配

## WAL Log (Write-Ahead Log)
*所有操作先写入 WAL，防止上下文丢失*

---

## Memory
*待记录*
"@
    
    $statePath = Join-Path $workspacePath "SESSION-STATE.md"
    $stateContent | Out-File -FilePath $statePath -Encoding UTF8
    Write-Host "  ✓ 创建状态文件：$statePath" -ForegroundColor Green
} else {
    Write-Host "  ℹ️  工作空间已存在：$workspacePath" -ForegroundColor Gray
}
Write-Host ""

# 完成
Write-Host "============================================================" -ForegroundColor Green
Write-Host "                    代理添加完成！" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "下一步操作:" -ForegroundColor Yellow
Write-Host "  1. 重启 Web UI 以查看新代理" -ForegroundColor Gray
Write-Host "     Stop-Process -Name python -Force" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. 编辑代理详细配置" -ForegroundColor Gray
Write-Host "     $configPath" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. 测试 CEO 协调器" -ForegroundColor Gray
Write-Host "     cd $workspaceRoot" -ForegroundColor Gray
Write-Host "     python agents\ceo_coordinator.py" -ForegroundColor Gray
Write-Host ""
