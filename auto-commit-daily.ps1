# Silicon World 2 - Daily Auto-Commit Script
# Scheduled to run at 2:00 AM daily

param(
    [switch]$RunNow,
    [switch]$Setup,
    [switch]$Remove,
    [switch]$Status
)

$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$taskName = "SiliconWorld2-DailyCommit"
$taskTime = "02:00"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] [$Level] $Message"
}

function Do-Commit {
    Set-Location $projectPath
    
    Write-Log "Checking Git status..."
    
    $status = git status --porcelain
    if ([string]::IsNullOrWhiteSpace($status)) {
        Write-Log "No changes to commit" "INFO"
        return $true
    }
    
    Write-Log "Found uncommitted changes:"
    git status --short
    
    Write-Log "Adding all changes..."
    git add -A
    if ($LASTEXITCODE -ne 0) {
        Write-Log "git add failed" "ERROR"
        return $false
    }
    
    $commitMsg = "Auto-commit - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    Write-Log "Committing: $commitMsg"
    git commit -m $commitMsg
    if ($LASTEXITCODE -ne 0) {
        Write-Log "git commit failed" "ERROR"
        return $false
    }
    
    Write-Log "Pushing to GitHub..."
    git push origin main
    if ($LASTEXITCODE -ne 0) {
        Write-Log "git push failed, but local commit completed" "WARN"
        return $true
    }
    
    Write-Log "Auto-commit completed!" "SUCCESS"
    return $true
}

function Setup-ScheduledTask {
    Write-Log "Setting up daily commit scheduled task..."
    
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
    
    Write-Log "Scheduled task created: Daily at $taskTime" "SUCCESS"
    Write-Log "Task name: $taskName"
}

function Remove-ScheduledTask {
    Write-Log "Removing scheduled task..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Log "Scheduled task removed" "SUCCESS"
}

function Get-TaskStatus {
    Write-Log "Checking scheduled task status..."
    $task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($task) {
        $info = Get-ScheduledTaskInfo -TaskName $taskName
        Write-Host "Task: $taskName"
        Write-Host "State: $($task.State)"
        Write-Host "Last Run: $($info.LastRunTime)"
        Write-Host "Next Run: $($info.NextRunTime)"
        Write-Host "Result: $($info.LastTaskResult)"
    } else {
        Write-Log "Scheduled task not found" "WARN"
    }
}

if ($Setup) {
    Setup-ScheduledTask
} elseif ($Remove) {
    Remove-ScheduledTask
} elseif ($Status) {
    Get-TaskStatus
} elseif ($RunNow) {
    Do-Commit
} else {
    Write-Host "Silicon World 2 - Daily Auto-Commit Tool"
    Write-Host "Usage:"
    Write-Host "  .\auto-commit-daily.ps1 -Setup    Setup daily auto-commit"
    Write-Host "  .\auto-commit-daily.ps1 -RunNow   Run commit now"
    Write-Host "  .\auto-commit-daily.ps1 -Status   Check task status"
    Write-Host "  .\auto-commit-daily.ps1 -Remove   Remove scheduled task"
}
