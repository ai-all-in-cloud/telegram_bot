# 🤖 Telegram Bot 建立標準作業程序 (SOP)

> **所屬企業**：歐印雲 (All In Cloud)  
> **制定版本**：v1.0  
> **維護單位**：數位營運與技術決策中樞  
> **適用對象**：所有新建 AI 員工代理人、技術主管與部署人員

---

## 📌 建立步驟（五分鐘快速通關）

### 步驟 1：召喚 Telegram 官方機器人之父
1. 打開 Telegram，在搜尋列搜尋 **`@BotFather`**（請認明官方藍色驗證勾勾）。
2. 點擊進入對話，輸入或點選 `/start`。

---

### 步驟 2：申請新機器人 (`/newbot`)
1. 在對話框輸入：
   ```text
   /newbot
   ```
2. **輸入顯示名稱 (Display Name)**：
   * 範例：`柚木`、`柚水`、`柚火`、`柚土`。
3. **輸入唯一使用者帳號 (Username)**：
   * 規則：必須以 `bot` 或 `_bot` 結尾，且全球唯一不可重複。
   * 命名建議：`wood_001_bot`、`water_002_bot`、`fire_003_bot`、`earth_004_bot`。

---

### 步驟 3：獲取並安全保存 API Token
BotFather 建立成功後會回傳 HTTP API Token，格式如下：
```text
8746962767:AAGX6lQaRFD4mVfjnYVMsOQMcIiTIM9zxkc
```
⚠️ **安全規範**：
* 請妥善保管此 Token，不可洩漏至公開討論區。
* 請填入該 AI 員工專屬的 `bot_listener.py` 與 `send_telegram.py` 中。

---

### 步驟 4：【最關鍵核心】關閉群組隱私保護 (Disable Privacy) ⭐️⭐️⭐️⭐️⭐️

> 💡 **核心原理解析**：  
> Telegram 所有剛建立的新 Bot，預設皆為 **`Group Privacy: ENABLED (開啟隱私保護)`**。在此模式下，若 Bot 只是群組普通成員（非管理員），**Telegram 伺服器底層會全面攔截一般文字訊息與群聊 @ 指令，導致 Bot 根本收不到任何訊息！**  
> 因此，必須手動關閉群組隱私保護。

1. 在 `@BotFather` 對話中輸入：
   ```text
   /setprivacy
   ```
2. 點選下方出現的按鈕清單中你要設定的 Bot（例如 `@wood_001_bot`）。
3. 點選 **`Disable`** 按鈕。
4. 當 BotFather 回覆：
   ```text
   SUCCESS: Group privacy mode for [你的Bot名稱] has been disabled.
   ```
   即表示設定成功！從此該 Bot 在群組中具備 100% 訊息感知能力。

*備註：若設定前 Bot 已在群組中，Telegram 伺服器快取可能需要 1~2 分鐘更新，或將 Bot 移出群組重新加入即可瞬間生效。*

---

### 步驟 5：將 Bot 邀請進入工作群組
1. 前往公司工作群組（例如：「企業雲平臺 - AI 決策指揮部」）。
2. 點選群組資訊 ➔「新增成員 (Add Members)」➔ 搜尋剛建好的 Bot Username ➔ 拉入群組。
3. 新員工機器人即可在群組中接收指令與公開回覆！
