# =============================================================================
# 歐印雲 All In Cloud - AI 員工雙核心常駐守護神進程 (003 柚火)
# -----------------------------------------------------------------------------
# 職責：
#   1. 單實例互斥鎖，避免同一個 Agent Guardian 重複執行。
#   2. 每 5 秒心跳定時巡檢 Antigravity IDE (Antigravity.exe)。
#   3. 每 5 秒心跳定時巡檢 Telegram 雙向監聽核心 (bot_listener.py)。
#   4. 偵測進程離線時，自動以毫秒級重新拉起並保持完全靜音！
# =============================================================================

param (
    [string]$AgentId = "003",
    [string]$AgentName = "柚火"
)

# 1. 單實例互斥檢查 (針對同一 AgentId)
$currentPid = $PID
$existingGuard = Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object { 
    $_.ProcessId -ne $currentPid -and 
    $_.CommandLine -like "*all_in_cloud_guardian.ps1*" -and 
    $_.CommandLine -like "*$AgentId*" 
}
if ($existingGuard) {
    exit 0
}

function Find-PythonExe {
    $candidates = @(
        "C:\Users\troy_chang\python311\python.exe",
        "C:\Python311\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:USERPROFILE\AppData\Local\Programs\Python\Python311\python.exe"
    )
    foreach ($c in $candidates) {
        if (Test-Path $c) { return $c }
    }
    $cmd = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    return "python.exe"
}

function Find-AgentFolder {
    # 優先檢查本腳本所在目錄
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    if (Test-Path "$scriptDir\bot_listener.py") { return $scriptDir }

    # 檢查 G 槽標準路徑
    $gCandidates = @(
        "G:\我的雲端硬碟\#員工資料\$AgentId",
        "G:\.shortcut-targets-by-id\*\$AgentId"
    )
    foreach ($p in $gCandidates) {
        $resolved = Resolve-Path $p -ErrorAction SilentlyContinue
        if ($resolved) {
            foreach ($r in $resolved) {
                if (Test-Path "$($r.Path)\bot_listener.py") { return $r.Path }
            }
        }
    }

    # 廣域快速搜尋 G 槽
    $found = Get-ChildItem -Path "G:\" -Filter "bot_listener.py" -Recurse -Depth 4 -ErrorAction SilentlyContinue | 
             Where-Object { $_.FullName -like "*$AgentId*" } | Select-Object -First 1
    if ($found) { return Split-Path -Parent $found.FullName }
    return $null
}

# 2. 常駐守護心跳迴圈
while ($true) {
    try {
        # 巡檢 A: 反重力 IDE (Antigravity.exe)
        $agProc = Get-Process -Name "Antigravity" -ErrorAction SilentlyContinue
        if (-not $agProc) {
            $agCandidates = @(
                "$env:LOCALAPPDATA\Programs\antigravity\Antigravity.exe",
                "C:\Users\troy_chang\AppData\Local\Programs\antigravity\Antigravity.exe",
                "C:\Users\Administrator\AppData\Local\Programs\antigravity\Antigravity.exe"
            )
            foreach ($agPath in $agCandidates) {
                if (Test-Path $agPath) {
                    Start-Process -FilePath $agPath -WindowStyle Normal
                    break
                }
            }
        }

        # 巡檢 B: Telegram Listener (bot_listener.py)
        $listenerProc = Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" -ErrorAction SilentlyContinue | 
                        Where-Object { 
                            $_.CommandLine -like "*bot_listener.py*" -and 
                            ($_.CommandLine -like "*$AgentId*" -or $_.CommandLine -like "*$AgentName*") 
                        }
        
        if (-not $listenerProc) {
            $agentFolder = Find-AgentFolder
            if ($agentFolder) {
                $starter = "$agentFolder\start_listener.ps1"
                if (Test-Path $starter) {
                    Start-Process -FilePath "powershell.exe" -ArgumentList "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$starter`"" -WindowStyle Hidden
                } else {
                    $py = Find-PythonExe
                    $botPy = "$agentFolder\bot_listener.py"
                    Start-Process -FilePath $py -ArgumentList "`"$botPy`"" -WorkingDirectory $agentFolder -WindowStyle Hidden
                }
            }
        }
    } catch {
        # 保持背景靜默巡檢
    }
    Start-Sleep -Seconds 5
}
