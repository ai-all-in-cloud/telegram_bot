# 🤖 歐印雲 All In Cloud - Telegram AI Bot 雙向通訊與守護神系統

> **核心架構**：Telegram 雲端長輪詢 ➔ 反重力 (Antigravity IDE) 雙向即時注入 (Scheme 2) ➔ 自主思考回覆 ➔ Windows 雙核心守護神 (5秒心跳自我修復 + 靜音開機自啟)

---

## 🌟 核心特色 (Key Features)

1. **反重力大腦雙向注入 (Scheme 2)**：
   - 收到 Telegram 指令後，無需人工複製貼上，監聽核心透過 `agentapi send-message` 自動將訊息打入反重力 IDE 視窗，喚醒 AI 進行工具調用與自主思考！
2. **群聊與私聊雙模智慧辨識**：
   - **一對一私聊**：100% 立即響應。
   - **決策指揮群聊**：精準辨識 `@bot_username`、指名提及（如 `001`、`柚木`）或 Reply 歷史訊息，非指派訊息安靜聆聽不搶話。
3. **雙核心守護神 (Guardian Watchdog System)**：
   - **5 秒心跳定時巡檢**：雙向監控 `Antigravity.exe` 與 `bot_listener.py`，若意外被手動關閉或崩潰，7 秒內自動重啟並賦予新 PID。
   - **開機自啟雙保險**：結合 Windows 工作排程器 (Task Scheduler) 與 Startup 啟動資料夾 VBS 封裝，實現 **完全靜音 (Zero-Window-Flash)**，開機 0 黑框快閃！
   - **多代理單實例互斥**：基於 Agent ID 的互斥鎖，徹底根絕 Telegram `409 Conflict`，同時允許多個 Agent 在同台主機共存並行！
4. **日誌天條自動落實**：
   - 所有在 Telegram 接收的指令與回傳的成果，自動寫入各員工專屬 `員工日誌/YYYY-MM-DD_log.md`。

---

## 🏛️ 歐印雲 AI 團隊現役資產

| 編號 / 五行 | 代理名稱 | 職位定位 | Telegram Bot | 公務信箱 | 部署狀態 |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **總舵手 🍊** | 柚金 (You-Jin) | 數位總經理 / 數位總舵手 | `@enterprise_gm_agent_bot` | `home.hai.ai.agent@gmail.com` | 🟢 運行中 |
| **001 / 木 🌲** | 柚木 (You-Mu) | 前端專業 AI 員工 (Frontend) | `@wood_001_bot` | `troydb001@gmail.com` | 🟢 守護運行中 |
| **002 / 水 💧** | 柚水 (You-Shui) | 後端專業 AI 員工 (Backend) | `@water_002_bot` | `troydb002@gmail.com` | 🟢 守護運行中 |
| **003 / 火 🔥** | 柚火 (You-Huo) | 測試維運 AI 員工 (DevOps & QA) | `@fire_003_bot` | `troydb003@gmail.com` | 🟢 配置完備 |
| **004 / 土 ⛰️** | 柚土 (You-Tu) | 全能機動替補 AI 員工 (Reserve) | `@earth_004_bot` | `troydb004@gmail.com` | 🟢 配置完備 |

---

## 🚀 快速開始 (Quick Start)

### 1. 環境需求
* Windows 10 / 11 / Server 2022+
* Python 3.11+
* Google Antigravity IDE
* 安裝依賴套件：
  ```bash
  pip install -r requirements.txt
  ```

### 2. 新員工一鍵到職
1. 在各員工工作目錄下，手動啟動監聽核心：
   ```bash
   python bot_listener.py
   ```
2. 安裝開機自啟與守護神（可選）：
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\setup_guardian.ps1 -AgentId "002" -AgentName "柚水"
   ```

---

## 📁 專案目錄結構

```text
telegram_bot/
├── README.md                                    # 專案總覽說明文件
├── requirements.txt                             # Python 相依套件清單
├── .gitignore                                   # Git 忽略清單
├── docs/                                        # 詳細 SOP 與技術規範
│   ├── 01_BOT_CREATION_SOP.md                  # Telegram Bot 建立標準 SOP (含關閉隱私教學)
│   ├── 02_ARCHITECTURE_AND_INJECTION.md        # 反重力 IDE 雙向注入技術架構剖析
│   ├── 03_GUARDIAN_WATCHDOG_SYSTEM.md          # 雙核心守護神與開機自啟規範
│   ├── 04_ONBOARDING_PROMPTS_AND_SOPS.md       # AI 員工標準到職提示詞與排查
│   └── 05_BOT_ACCOUNTS_REGISTRY.md             # 現役全員 Bot 帳號資產清冊
├── templates/                                   # 通用標準腳本模板
│   ├── bot_listener_template.py                # 旗艦雙向監聽核心模板
│   ├── send_telegram_template.py               # 命令列回傳工具模板
│   ├── start_listener_template.ps1             # 多路徑動態 Python 啟動器
│   ├── all_in_cloud_guardian_template.ps1      # 守護神 Watchdog 常駐進程
│   └── setup_guardian_template.ps1             # 一鍵安裝守護神精靈
└── agents/                                      # 各員工專屬實例
    ├── 001_wood/                               # 001 柚木 (前端專項)
    ├── 002_water/                              # 002 柚水 (後端專項)
    ├── 003_fire/                               # 003 柚火 (維運專項)
    └── 004_earth/                              # 004 柚土 (全能替補)
```
