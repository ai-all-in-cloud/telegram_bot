# =============================================================================
# 歐印雲 All In Cloud - AI 員工萬無一失守護配置安裝腳本 (通用模板)
# setup_guardian_template.ps1
# =============================================================================

param (
    [string]$AgentId = "00X",
    [string]$AgentName = "柚X"
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🛡️ 歐印雲 All In Cloud - AI 員工守護神部署精靈" -ForegroundColor Green
Write-Host "   目標員工: $AgentId $AgentName" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan

$userProfile = $env:USERPROFILE
$guardianPs1 = "$userProfile\all_in_cloud_guardian.ps1"
$startupDir = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$startupVbs = "$startupDir\Start-AllInCloudGuardian_${AgentId}.vbs"
$taskName = "歐印雲_${AgentId}${AgentName}_Guardian"

# 0. 確保核心守護腳本到位
$localGuardian = Join-Path $PSScriptRoot "all_in_cloud_guardian.ps1"
if (Test-Path $localGuardian) {
    Copy-Item $localGuardian $guardianPs1 -Force
    Write-Host "[0/4] ✅ 核心守護腳本已同步至: $guardianPs1" -ForegroundColor Green
} elseif (-not (Test-Path $guardianPs1)) {
    Write-Host "[0/4] ⚠️ 警告: 未在本地或 UserProfile 找到 all_in_cloud_guardian.ps1" -ForegroundColor Red
}

# 1. 確保 execution policy
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force

# 2. 部署啟動資料夾 VBS (完全靜音背景執行，防止任何 CMD/黑框快閃)
$vbsContent = @"
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File ""$guardianPs1"" -AgentId ""$AgentId"" -AgentName ""$AgentName""", 0, False
"@
[System.IO.File]::WriteAllText($startupVbs, $vbsContent, [System.Text.Encoding]::ASCII)
Write-Host "[1/4] ✅ Windows 啟動資料夾已植入靜音自啟腳本: $startupVbs" -ForegroundColor Green

# 3. 註冊 Windows 工作排程器 (Task Scheduler: 登入自啟 + 崩潰自動重啟)
$taskXml = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>歐印雲 $AgentId $AgentName - 反重力大腦與 Telegram 雙向監聽守護進程</Description>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
      <UserId>$env:USERDOMAIN\$env:USERNAME</UserId>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>$env:USERDOMAIN\$env:USERNAME</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <RestartOnFailure>
      <Interval>PT1M</Interval>
      <Count>999</Count>
    </RestartOnFailure>
    <Enabled>true</Enabled>
  </Settings>
  <Actions>
    <Exec>
      <Command>wscript.exe</Command>
      <Arguments>"$startupVbs"</Arguments>
    </Exec>
  </Actions>
</Task>
"@
$tmpXml = "$env:TEMP\guardian_task_${AgentId}.xml"
$taskXml | Out-File -FilePath $tmpXml -Encoding unicode
schtasks /Create /TN "$taskName" /XML $tmpXml /F | Out-Null
Remove-Item $tmpXml -Force
Write-Host "[2/4] ✅ Windows 工作排程器已成功登錄: $taskName" -ForegroundColor Green

# 4. 清理過期舊版任務排程
@("歐印雲_${AgentId}${AgentName}_Listener", "歐印雲_${AgentId}${AgentName}_Watchdog") | ForEach-Object {
    schtasks /Delete /TN $_ /F 2>$null
}
Write-Host "[3/4] ✅ 舊版任務清理完成" -ForegroundColor Green

# 5. 立即啟動守護神進程
schtasks /Run /TN "$taskName" | Out-Null
Start-Sleep -Seconds 3
Write-Host "[4/4] ✅ 守護神進程已即時上線！" -ForegroundColor Green

# 6. 狀態檢驗
$guardProc = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like "*all_in_cloud_guardian*.ps1*" -and $_.CommandLine -like "*$AgentId*" }
$agProc = Get-Process -Name "Antigravity" -ErrorAction SilentlyContinue
$listProc = Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*bot_listener.py*" -and ($_.CommandLine -like "*$AgentId*" -or $_.CommandLine -like "*$AgentName*") }

Write-Host "`n------------------------------------------------------------" -ForegroundColor Cyan
Write-Host "📊 系統即時健檢報告:" -ForegroundColor Yellow
Write-Host "   • 守護進程 (Guardian) : $(if($guardProc){"🟢 正常運行 (PID: $($guardProc.ProcessId))"}else{"🔴 尚未啟動"})"
Write-Host "   • 反重力大腦 (IDE)    : $(if($agProc){"🟢 正常運行"}else{"🟡 守護中 (待自動拉起)"})"
Write-Host "   • 監聽核心 (Listener) : $(if($listProc){"🟢 正常運行 (PID: $($listProc.ProcessId))"}else{"🟡 守護中 (待自動拉起)"})"
Write-Host "------------------------------------------------------------" -ForegroundColor Cyan
Write-Host "🎉 恭喜！$AgentId $AgentName 守護系統部署完成，已具備開機自啟與防關閉自我修復能力！" -ForegroundColor Green
