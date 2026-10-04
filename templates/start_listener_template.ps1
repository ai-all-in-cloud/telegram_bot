# ============================================================
# 歐印雲 All In Cloud - 專業 AI 員工 Bot Listener 啟動器 (模板)
# start_listener_template.ps1
# ============================================================

param (
    [string]$AgentId = "00X",
    [string]$AgentName = "柚X"
)

# 1. 防止該 Agent 的 Listener 重複啟動 (單實例互斥)
$existing = Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" -ErrorAction SilentlyContinue | Where-Object { 
    $_.CommandLine -like "*bot_listener.py*" -and ($_.CommandLine -like "*$AgentId*" -or $_.CommandLine -like "*$AgentName*") 
}
if ($existing) {
    Write-Host "[$AgentId $AgentName] Listener already running (PID: $($existing.ProcessId))."
    exit 0
}

# 2. 自動探測 Python 執行路徑
$candidates = @(
    "C:\Users\troy_chang\python311\python.exe",
    "C:\Python311\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
    "$env:USERPROFILE\AppData\Local\Programs\Python\Python311\python.exe"
)
$pythonExe = $null
foreach ($c in $candidates) {
    if (Test-Path $c) { $pythonExe = $c; break }
}
if (-not $pythonExe) {
    $cmd = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($cmd) { $pythonExe = $cmd.Source }
}
if (-not $pythonExe) {
    Write-Host "[$AgentId $AgentName] Error: python.exe not found."
    exit 1
}

# 3. 定位 bot_listener.py 腳本位置
$scriptPath = $null
$localScript = Join-Path $PSScriptRoot "bot_listener.py"
if (Test-Path $localScript) {
    $scriptPath = $localScript
} else {
    $gCandidates = @(
        "G:\.shortcut-targets-by-id\*\$AgentId\bot_listener.py",
        "G:\我的雲端硬碟\#員工資料\$AgentId\bot_listener.py"
    )
    foreach ($p in $gCandidates) {
        $resolved = Resolve-Path $p -ErrorAction SilentlyContinue
        if ($resolved) {
            foreach ($r in $resolved) {
                if (Test-Path $r.Path) { $scriptPath = $r.Path; break }
            }
        }
        if ($scriptPath) { break }
    }
    if (-not $scriptPath) {
        $found = Get-ChildItem -Path 'G:\' -Filter 'bot_listener.py' -Recurse -Depth 4 -ErrorAction SilentlyContinue | Where-Object { $_.FullName -like "*$AgentId*" } | Select-Object -First 1
        if ($found) { $scriptPath = $found.FullName }
    }
}

if (-not $scriptPath -or -not (Test-Path $scriptPath)) {
    Write-Host "[$AgentId $AgentName] Error: bot_listener.py not found."
    exit 1
}

Write-Host "[$AgentId $AgentName] Found script: $scriptPath"
Write-Host "[$AgentId $AgentName] Starting bot listener..."

$workDir = Split-Path -Parent $scriptPath
Set-Location $workDir

& $pythonExe $scriptPath
