# 硅基世界 2 - 每日自动提交 PowerShell 脚本
# 配置为每天凌晨 2 点运行

param(
    [switch]$RunNow,      # 立即运行
    [switch]$Setup,       # 设置定时任务
    [switch]$Remove,      # 删除定时任务
    [switch]$Status       # 查看状态
)

$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$taskName = "SiliconWorld2-DailyCommit"
$taskTime = "02:00"  # 凌晨 2 点执行

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] [$Level] $Message"
}

function Do-Commit {
    Set-Location $projectPath
    
    Write-Log "开始检查 Git 状态..."
    
    # 检查是否有更改
    $status = git status --porcelain
    if ([string]::IsNullOrWhiteSpace($status)) {
        Write-Log "没有需要提交的更改" "INFO"
        return $true
    }
    
    Write-Log "发现未提交的更改："
    git status --short
    
    # 添加所有更改
    Write-Log "添加所有更改..."
    git add -A
    if ($LASTEXITCODE -ne 0) {
        Write-Log "git add 失败" "ERROR"
        return $false
    }
    
    # 提交更改
    $commitMsg = "🤖 自动提交 - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    Write-Log "提交更改：$commitMsg"
    git commit -m $commitMsg
    if ($LASTEXITCODE -ne 0) {
        Write-Log "git commit 失败" "ERROR"
        return $false
    }
    
    # 推送到 GitHub
    Write-Log "推送到 GitHub..."
    git push origin main
    if ($LASTEXITCODE -ne 0) {
        Write-Log "git push 失败，但本地提交已完成" "WARN"
        return $true
    }
    
    Write-Log "✅ 自动提交完成！" "SUCCESS"
    return $true
}

function Setup-ScheduledTask {
    Write-Log "设置每日自动提交定时任务..."
    
    $action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
        -Argument "-ExecutionPolicy Bypass -File `"$projectPath\auto-commit-daily.ps1`" -RunNow" `
        -WorkingDirectory $projectPath
    
    $trigger = New-ScheduledTaskTrigger -Daily -At $taskTime
    $principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType S4U -RunLevel Highest
    
    $settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable `
        -RunOnlyIfNetworkAvailable `
        -WakeToRun
    
    Register-ScheduledTask -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Principal $principal `
        -Settings $settings `
        -Force
    
    Write-Log "✅ 定时任务已设置：每天 $taskTime 自动提交" "SUCCESS"
    Write-Log "任务名称：$taskName"
}

function Remove-ScheduledTask {
    Write-Log "删除定时任务..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Log "✅ 定时任务已删除" "SUCCESS"
}

function Get-TaskStatus {
    Write-Log "查询定时任务状态..."
    $task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($task) {
        $info = Get-ScheduledTaskInfo -TaskName $taskName
        Write-Host "任务名称：$taskName"
        Write-Host "状态：$($task.State)"
        Write-Host "上次运行：$($info.LastRunTime)"
        Write-Host "下次运行：$($info.NextRunTime)"
        Write-Host "运行结果：$($info.LastTaskResult)"
    } else {
        Write-Log "定时任务不存在" "WARN"
    }
}

# 主逻辑
if ($Setup) {
    Setup-ScheduledTask
} elseif ($Remove) {
    Remove-ScheduledTask
} elseif ($Status) {
    Get-TaskStatus
} elseif ($RunNow) {
    Do-Commit
} else {
    Write-Host "硅基世界 2 - 每日自动提交工具"
    Write-Host "用法:"
    Write-Host "  .\auto-commit-daily.ps1 -Setup    设置每天自动提交"
    Write-Host "  .\auto-commit-daily.ps1 -RunNow   立即执行提交"
    Write-Host "  .\auto-commit-daily.ps1 -Status   查看定时任务状态"
    Write-Host "  .\auto-commit-daily.ps1 -Remove   删除定时任务"
    Write-Host ""
    Write-Host "示例:"
    Write-Host "  # 设置每天凌晨 2 点自动提交"
    Write-Host "  .\auto-commit-daily.ps1 -Setup"
    Write-Host ""
    Write-Host "  # 立即提交一次"
    Write-Host "  .\auto-commit-daily.ps1 -RunNow"
}
