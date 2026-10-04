# ============================================================
# All In Cloud 002 You-Shui - Bot Listener Starter
# start_listener.ps1
# ============================================================

# 1. Prevent duplicate instances for 002 specifically
$existing = Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" -ErrorAction SilentlyContinue | Where-Object { 
    $_.CommandLine -like "*bot_listener.py*" -and ($_.CommandLine -like "*002*" -or $_.CommandLine -like "*柚水*") 
}
if ($existing) {
    Write-Host "[002 You-Shui] Listener already running (PID: $($existing.ProcessId))."
    exit 0
}

# 2. Python environment detection
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
    Write-Host "[002 You-Shui] Error: python.exe not found."
    exit 1
}

# 3. Locate script
$scriptPath = $null
$localScript = Join-Path $PSScriptRoot "bot_listener.py"
if (Test-Path $localScript) {
    $scriptPath = $localScript
} else {
    $gCandidates = @(
        'G:\.shortcut-targets-by-id\*\002\bot_listener.py',
        'G:\我的雲端硬碟\#員工資料\002\bot_listener.py'
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
        $found = Get-ChildItem -Path 'G:\' -Filter 'bot_listener.py' -Recurse -Depth 4 -ErrorAction SilentlyContinue | Where-Object { $_.FullName -like '*002*' } | Select-Object -First 1
        if ($found) { $scriptPath = $found.FullName }
    }
}

if (-not $scriptPath -or -not (Test-Path $scriptPath)) {
    Write-Host "[002 You-Shui] Error: bot_listener.py not found."
    exit 1
}

Write-Host "[002 You-Shui] Found script: $scriptPath"
Write-Host "[002 You-Shui] Starting bot listener..."

$workDir = Split-Path -Parent $scriptPath
Set-Location $workDir

& $pythonExe $scriptPath
