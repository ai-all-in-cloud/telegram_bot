# 🛠️ Windows 排程與背景常駐守護規範

> **適用對象**：003 柚火 (DevOps)、004 柚土 (QA)、全體 AI 員工

---

## 🔄 常駐進程架構原則

1. **靜默運行 (Silent Background Execution)**：
   - 避免在伺服器桌面上彈出黑窗 (cmd.exe)。
   - 使用 VBScript (`run_silent.vbs`) 啟動批次檔：
     ```vbscript
     Set WshShell = CreateObject("WScript.Shell")
     WshShell.Run chr(34) & "C:\path\to\start.bat" & chr(34), 0
     Set WshShell = Nothing
     ```
2. **工作排程器自動開機啟動 (Task Scheduler)**：
   - 任務觸發條件設為「在系統啟動時 (At startup)」。
   - 執行身分使用 `SYSTEM` 或具備權限之管理者帳號。
3. **健康檢查與自我修復迴圈 (Health-Check & Keep-Alive Loop)**：
   - 定時透過 `curl.exe` 或 `Invoke-WebRequest` 監測 Localhost 埠號。
   - 連線超時或異常時，自動終止孤兒進程並重新拉起服務。
