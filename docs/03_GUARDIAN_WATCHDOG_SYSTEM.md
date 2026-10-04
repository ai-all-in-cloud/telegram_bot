# 🛡️ 雙核心萬無一失守護神架構 (Guardian Watchdog System)

> **設計代理**：001 柚木 🌲  
> **最佳化與多代理標準化**：數位總舵手 柚金 🍊💰  
> **核心目標**：實現 Windows 重開機 100% 自動恢復運行、意外被關閉 5 秒內自我修復，且全流程完全靜音、0 黑框快閃。

---

## 🏛️ 架構總覽

```mermaid
flowchart TD
    subgraph Windows 系統事件觸發
        E1["系統重新開機 / 使用者登入"]
        E2["守護神進程崩潰事件"]
    end

    subgraph 開機自啟雙保險 (Zero-Flash)
        T1["Windows 工作排程器 (Task Scheduler)<br/>TaskName: 歐印雲_XXX_Guardian<br/>LogonTrigger + RestartOnFailure x 999"]
        T2["Windows Startup 啟動資料夾<br/>Start-AllInCloudGuardian_XXX.vbs<br/>(wscript.exe 靜音執行)"]
    end

    subgraph 常駐守護神核心 (Guardian Daemon)
        G["all_in_cloud_guardian.ps1<br/>(單實例互斥鎖，避免同Agent重複執行)"]
    end

    subgraph 雙守護標的 (每 5 秒心跳巡檢)
        Target1["反重力大腦視窗<br/>Antigravity.exe"]
        Target2["Telegram 雙向監聽核心<br/>bot_listener.py"]
    end

    E1 --> T1
    E1 --> T2
    E2 -->|排程器自動重試| T1
    T1 --> G
    T2 --> G
    G -->|巡檢 1: 若離線自動拉起| Target1
    G -->|巡檢 2: 若斷線自動喚醒| Target2
```

---

## 🌟 四大核心技術指標

| 特性項目 | 技術細節 | 帶來的效益 |
| :--- | :--- | :--- |
| **雙層啟動保險** | 工作排程器 (系統級) + Startup 資料夾 (使用者級) | 即使群組原則限制某項，另一項亦能 100% 確保開機即上線。 |
| **極致靜音體驗** | 全鏈路採用 `wscript.exe` 封裝 VBS 呼叫 | 開機或修復時，螢幕上**絕無任何黑框快閃**，不干擾使用者操作。 |
| **自我修復巡檢** | 每 5 秒 Heartbeat 心跳檢查 | 實測強制殺死進程後，守護引擎在 **7 秒內自動重啟並賦予新 PID**。 |
| **單實例多代理相容** | 檢查 `CommandLine` 中之 `$AgentId` 互斥鎖 | 徹底杜絕同代理重複啟動引發之 `Telegram 409 Conflict`，同時允許多位不同代理在同台主機共存並行！ |

---

## 🛠️ 一鍵部署 SOP

日後任何新進員工（如 005、006...）到職，只需在 PowerShell 執行：
```powershell
.\setup_guardian.ps1 -AgentId "005" -AgentName "柚金"
```
腳本將全自動完成：
1. 同步 `all_in_cloud_guardian.ps1` 核心守護檔至使用者家目錄。
2. 佈署開機啟動資料夾靜音 VBS。
3. 註冊 Windows 工作排程器。
4. 立即拉起守護程序與監聽核心，並輸出 🟢 全綠健檢狀態報告！
