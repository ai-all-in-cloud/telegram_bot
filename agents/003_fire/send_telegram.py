#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
歐印雲 All In Cloud - 003 柚火專屬 Telegram 回傳工具 (send_telegram.py)
-----------------------------------------------------------------------------
供 003 反重力 (Antigravity) IDE 處理完指令後，主動將思考結果回傳至 Telegram。
=============================================================================
"""

import os
import sys
import argparse
import requests
from datetime import datetime

# 確保 UTF-8 輸出
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BOT_TOKEN = "8856411250:AAGSgNOF-2FwkCRZ3XFKHYKFFxstLhobP-s"
BOT_NAME = "003 柚火 (You-Huo) 🔥"
LOG_DIR = os.path.join(os.path.dirname(__file__), "員工日誌")
os.makedirs(LOG_DIR, exist_ok=True)

def append_to_daily_log(chat_id: str | int, text: str):
    """將發送的回覆自動寫入 003 員工日誌"""
    try:
        today_str = datetime.now().strftime("%Y-%m-%d")
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = os.path.join(LOG_DIR, f"{today_str}_log.md")
        quoted_text = text.replace("\n", "\n> ")
        entry = (
            f"#### 📤 [{now_str}] 003 成果回傳 (ChatID: `{chat_id}`)\n"
            f"> {quoted_text}\n\n"
            f"---\n"
        )
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        print(f"⚠️ 寫入日誌失敗: {e}")

def send_message(chat_id: str | int, text: str, reply_to_id: int | None = None) -> bool:
    """發送訊息至 Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    }
    if reply_to_id:
        payload["reply_to_message_id"] = reply_to_id

    try:
        res = requests.post(url, json=payload, timeout=10)
        data = res.json()
        if data.get("ok"):
            print("✅ 003 訊息已成功回傳至 Telegram")
            append_to_daily_log(chat_id, text)
            return True
        else:
            print(f"❌ Telegram API 拒絕: {data.get('description')}")
            if "can't parse entities" in str(data.get("description", "")).lower():
                payload.pop("parse_mode", None)
                res = requests.post(url, json=payload, timeout=10)
                if res.json().get("ok"):
                    print("✅ 降級純文字後發送成功！")
                    append_to_daily_log(chat_id, text)
                    return True
            return False
    except Exception as e:
        print(f"❌ 連線失敗: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="003 Telegram 回傳腳本")
    parser.add_argument("--chat-id", "--chat_id", dest="chat_id", required=True, help="目標 Chat ID")
    parser.add_argument("--text", "--message", "-m", dest="text", required=True, help="回傳之 Markdown 文字")
    parser.add_argument("--reply-to", "--reply_to", dest="reply_to", type=int, default=None, help="回覆的 Message ID")
    args = parser.parse_args()

    send_message(args.chat_id, args.text, args.reply_to)
