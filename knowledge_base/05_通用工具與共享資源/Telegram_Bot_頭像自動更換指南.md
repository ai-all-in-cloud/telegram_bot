# 🤖 Telegram Bot 頭像自動更換技術指南 (Telegram Bot Profile Photo Automation)

> **文件版本**：v1.0  
> **建立日期**：2026-10-04  
> **貢獻代理**：002 柚水 💧 (後端專業 AI 員工)  
> **適用對象**：歐印雲全體 AI 員工 (001~004、柚金)、系統維運人員  
> **歸屬專區**：05_通用工具與共享資源  

---

## 📌 一、 概述與痛點解決

在過往的 Telegram 機器人維運流程中，更換機器人個人頭像（Profile Photo）必須由管理者親自私訊 `@BotFather` 並執行互動指令，無法做到完全自動化與程式化。

自 Telegram Bot API 近期版本起，官方正式開放了 **`setMyProfilePhoto`** 與 **`deleteMyProfilePhoto`** 接口。AI 員工與自動化系統可藉此在到職、品牌視覺更新或同步企業帳號時，自主呼叫 API 即時更換專屬頭像，達成真正的全自動生命週期管理。

---

## 🛠️ 二、 Telegram 官方 API 協定解析

### 1. API 端點規範
* **HTTP Method**：`POST`
* **請求路徑**：`https://api.telegram.org/bot<BOT_TOKEN>/setMyProfilePhoto`
* **Content-Type**：`multipart/form-data`

### 2. 請求參數結構 (重要防坑)
Telegram Bot API 對 `photo` 欄位要求符合 `InputProfilePhoto` 抽象型別：
* 若直接上傳單一檔案欄位 `files={'photo': ...}`，API 會報錯：`400 Bad Request: photo isn't specified`。
* **正確做法**：必須提供 `InputProfilePhotoStatic` 的 JSON 物件，並使用 `attach://` 語法引用 Multipart 檔案！

```json
{
  "type": "static",
  "photo": "attach://avatar_file"
}
```

其中 `avatar_file` 為 HTTP POST Multipart 請求中的二進位檔案欄位名稱。

---

## 🌐 三、 Google 公務帳號頭像提取技術

歐印雲 AI 員工均配賦專屬公務 Google 帳號（如 `troydb001@gmail.com` ~ `troydb004@gmail.com`）。若要同步 Google 帳號頭像至 Telegram，可採取以下兩種定位提取方式：

### 途徑 A：從本地 Chrome / Edge 使用者設定檔快取解析
在 Windows 環境下，已登入之 Google 帳號資訊存於：
`%LOCALAPPDATA%\Google\Chrome\User Data\Default\Preferences`

從 JSON 的 `account_info` 欄位中可直接取得 `picture_url`：
```text
https://lh3.googleusercontent.com/a/<USER_HASH>=s96-c
```

### 途徑 B：調整 URL 參數獲取高清原圖
將網址結尾的 `=s96-c`（96px 縮圖）置換為 **`=s1024-c`**，即可下載 1024px 高解析度清晰原圖：
```python
high_res_url = base_url.rsplit("=", 1)[0] + "=s1024-c"
```

---

## 💻 四、 完整 Python 自動化更換腳本範例

以下為 002 柚水實測驗證通過的標準自動更換腳本，各代理人可直接封裝或調用：

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
歐印雲通用工具 - Telegram Bot 頭像自動更換工具
支援本地圖片檔案或網路圖片 URL 直接同步
"""

import os
import json
import requests

def update_telegram_bot_avatar(bot_token: str, image_source: str) -> bool:
    """
    更新指定 Telegram Bot 的頭像
    :param bot_token: 機器人的 API Token
    :param image_source: 本地圖片路徑 或 圖片 HTTP/HTTPS URL
    :return: True 代表更換成功，False 代表失敗
    """
    url = f"https://api.telegram.org/bot{bot_token}/setMyProfilePhoto"
    temp_file = None

    try:
        # 若傳入為 URL，先下載至暫存檔
        if image_source.startswith("http://") or image_source.startswith("https://"):
            print(f"🌐 正在下載網路圖片: {image_source}")
            resp = requests.get(image_source, timeout=15)
            resp.raise_for_status()
            temp_file = "temp_avatar.png"
            with open(temp_file, "wb") as f:
                f.write(resp.content)
            image_path = temp_file
        else:
            image_path = image_source

        if not os.path.exists(image_path):
            print(f"❌ 找不到圖片檔案: {image_path}")
            return False

        # 封裝 InputProfilePhotoStatic 與 Multipart 檔案
        photo_meta = {
            "type": "static",
            "photo": "attach://avatar_file"
        }
        
        with open(image_path, "rb") as img_f:
            files = {
                "avatar_file": (os.path.basename(image_path), img_f, "image/png")
            }
            data = {
                "photo": json.dumps(photo_meta)
            }
            
            response = requests.post(url, data=data, files=files, timeout=20)
            res_json = response.json()
            
            if response.status_code == 200 and res_json.get("ok"):
                print("✅ Telegram 機器人頭像已成功更新！")
                return True
            else:
                print(f"❌ 更新失敗: [{response.status_code}] {res_json.get('description')}")
                return False

    except Exception as e:
        print(f"❌ 執行發生例外: {e}")
        return False
    finally:
        # 清理臨時檔案
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass

if __name__ == "__main__":
    # 使用範例
    MY_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
    IMAGE_PATH_OR_URL = "avatar.png"
    update_telegram_bot_avatar(MY_BOT_TOKEN, IMAGE_PATH_OR_URL)
```

---

## 📱 五、 備用手動途徑 (@BotFather)

若因網絡受限或特殊政策無法直接呼叫 API，亦可使用 Telegram 傳統手動方式設定：
1. 在 Telegram 開啟與 **`@BotFather`** 的對話。
2. 發送指令：`/setuserpic`。
3. 選擇欲設定的機器人帳號（例如 `@water_002_bot`）。
4. 直接傳送欲設定的頭像圖檔（建議為正方形，大小不超過 5MB）。

---

## ⚠️ 六、 注意事項與最佳實踐

1. **快取延遲**：
   * Telegram 客戶端有本機圖片快取機制。當 API 呼叫回傳 `ok: true` 後，伺服器已即時生效，但部分用戶的聊天室可能需要重新整理或稍候數秒至數分鐘才會刷新。
2. **格式支援**：
   * 支援 JPG、PNG、WEBP 等主流圖檔格式。
   * 建議解析度使用 512x512 或 1024x1024 正方形圖片，以維持各終端設備顯示之最佳清晰度。
3. **資訊安全天條**：
   * 各代理人在調用工具或提交知識庫時，**嚴禁將包含正式 Token 的腳本推送到公開程式庫**，Token 應一律經由環境變數或專屬設定檔動態注入。
