#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
歐印雲 All In Cloud 專業 AI 員工 - 反重力雙向即時注入監聽核心 (002 柚水)
-----------------------------------------------------------------------------
身分: 002 柚水 (Backend Specialist)
五行: 水 💧
公務信箱: troydb002@gmail.com
核心技術能力:
  1. 動態偵測本地電腦運行的 Antigravity Language Server (LS) 與 CSRF Token。
  2. 收到 Telegram 指令後，透過 agentapi 自動注入 002 的反重力 IDE 視窗！
  3. 喚醒 002 自主思考並由 002 調用 send_telegram.py 回覆！
  4. 支援群聊 @water_002_bot / 指名提及 / Reply 精準過濾與一對一私聊雙模響應。
  5. 自動將交辦與成果落實於 員工日誌/YYYY-MM-DD_log.md。
=============================================================================
"""

import os
import re
import sys
import logging
import psutil
import subprocess
from datetime import datetime
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# 確保 Windows UTF-8 輸出
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("002_YouShui_Bridge")

AGENT_ID = "002"
AGENT_NAME = "柚水 (You-Shui) 💧"
AGENT_ROLE = "後端專業 AI 員工 (Backend Specialist)"
BOT_USERNAME = "water_002_bot"
BOT_TOKEN = "8837947832:AAGAMztcy1iSbXeOt3ewDz9DEryFa-r_vQ0"

BASE_DIR = os.path.dirname(__file__)
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
PHOTOS_DIR = os.path.join(DOWNLOADS_DIR, "photos")
DOCS_DIR = os.path.join(DOWNLOADS_DIR, "documents")
LOG_DIR = os.path.join(BASE_DIR, "員工日誌")

for d in [PHOTOS_DIR, DOCS_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)

def detect_antigravity_ls() -> tuple[str, str]:
    """自動動態偵測當前電腦運行的 Antigravity Language Server 端口與 CSRF Token"""
    csrf = ""
    ports = []
    try:
        for p in psutil.process_iter(["name", "cmdline"]):
            try:
                p_name = p.info.get("name") or ""
                if "language_server" in p_name.lower():
                    cmdline = " ".join(p.info.get("cmdline") or [])
                    m = re.search(r"--csrf_token\s+([a-zA-Z0-9\-]+)", cmdline)
                    if m:
                        csrf = m.group(1)
                    for c in p.net_connections(kind="inet"):
                        if c.status == "LISTEN" and c.laddr.ip in ["127.0.0.1", "0.0.0.0"]:
                            ports.append(c.laddr.port)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        if ports:
            ports.sort()
            return f"localhost:{ports[-1]}", csrf
    except Exception as e:
        logger.error(f"偵測 LS 連線位址失敗: {e}")
    return "localhost:64560", csrf

def get_latest_conversation_id() -> str | None:
    """自動偵測本地電腦最新的 Antigravity 對話 ID"""
    candidates = [
        os.path.expandvars(r"%USERPROFILE%\.gemini\antigravity\brain"),
        r"C:\Users\Administrator\.gemini\antigravity\brain",
    ]
    for brain_dir in candidates:
        if os.path.isdir(brain_dir):
            dirs = [
                os.path.join(brain_dir, d)
                for d in os.listdir(brain_dir)
                if os.path.isdir(os.path.join(brain_dir, d)) and "-" in d and len(d) > 30
            ]
            if dirs:
                dirs.sort(key=os.path.getmtime, reverse=True)
                return os.path.basename(dirs[0])
    return None

def find_language_server_exe() -> str | None:
    """自動尋找當前電腦的 language_server.exe 路徑"""
    candidates = [
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\antigravity\resources\bin\language_server.exe"),
        r"C:\Users\Administrator\AppData\Local\Programs\antigravity\resources\bin\language_server.exe",
    ]
    for p in candidates:
        if os.path.isfile(p):
            return p
    return None

def inject_message_to_ide(content: str) -> bool:
    """透過 agentapi 將訊息直接打進 002 的反重力對話視窗，喚醒其自主思考大腦！"""
    conv_id = get_latest_conversation_id()
    exe = find_language_server_exe()
    if not conv_id or not exe:
        logger.warning(f"⚠️ 無法定位 IDE (conv_id={conv_id}, exe={exe})")
        return False

    addr, csrf = detect_antigravity_ls()
    env = os.environ.copy()
    if addr:
        env["ANTIGRAVITY_LS_ADDRESS"] = addr
    if csrf:
        env["ANTIGRAVITY_CSRF_TOKEN"] = csrf

    create_no_window = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    try:
        res = subprocess.run(
            [exe, "agentapi", "send-message", conv_id, content],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=15,
            creationflags=create_no_window,
            env=env,
        )
        if res.returncode == 0:
            logger.info(f"✅ 成功將訊息打入 002 反重力 IDE (ConvID: {conv_id})")
            return True
        else:
            logger.error(f"❌ 注入 IDE 失敗: {res.stderr}")
            return False
    except Exception as e:
        logger.error(f"❌ 執行 agentapi 發生例外: {e}")
        return False

def record_to_employee_log(user_name: str, cmd_text: str, chat_desc: str = "私聊"):
    """落實日誌天條"""
    try:
        today_str = datetime.now().strftime("%Y-%m-%d")
        now_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        weekday_names = ["一", "二", "三", "四", "五", "六", "日"]
        weekday_str = weekday_names[datetime.now().weekday()]
        log_file = os.path.join(LOG_DIR, f"{today_str}_log.md")
        
        if not os.path.exists(log_file):
            header = (
                f"# {today_str} 工作日誌\n\n"
                f"* **日期**：{today_str} ({weekday_str})\n"
                f"* **執行代理**：{AGENT_ID} {AGENT_NAME} ({AGENT_ROLE})\n\n"
                f"---\n\n"
                f"## ⚡ 本日重大任務極速摘要 (Quick Updates Summary)\n\n"
                f"| 項次 | 任務標題 | 30字極速精準摘要 | 狀態 |\n"
                f"| :---: | :--- | :--- | :---: |\n\n"
                f"---\n\n"
                f"## 📋 詳細交辦與架構執行紀錄\n\n"
            )
            with open(log_file, "w", encoding="utf-8") as f:
                f.write(header)
                
        entry = (
            f"### 📥 [{now_time_str}] Telegram 對話交辦任務 ({chat_desc})\n"
            f"* **處理代理**：{AGENT_ID} {AGENT_NAME}\n"
            f"* **接收管道**：Telegram (@{BOT_USERNAME})\n"
            f"* **接收時間**：{now_time_str}\n"
            f"* **交辦主管**：`{user_name}`\n"
            f"* **指示內容**：{cmd_text}\n"
            f"* **處理狀態**：⚙️ 已注入反重力 IDE 喚醒大腦自主處理中...\n\n"
            f"---\n\n"
        )
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        logger.error(f"寫入日誌失敗: {e}")

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理 /start 指令"""
    user_name = update.effective_user.first_name if update.effective_user else "主管"
    reply = (
        f"💧 **報告 {user_name} 主管！**\n\n"
        f"我是 **{AGENT_NAME}**\n"
        f"🏢 **所屬單位**：歐印雲 (All In Cloud)\n"
        f"📌 **職能定位**：`{AGENT_ROLE}`\n"
        f"🟢 **大腦狀態**：反重力雙向自主思考核心已就位，隨時待命！\n"
        f"📧 **公務信箱**：`troydb002@gmail.com`"
    )
    await update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """接收訊息（支援私聊與群聊 @Mention / Reply）並打入 IDE 讓 002 大腦親自回答！"""
    if not update.message or not update.message.text:
        return

    msg = update.message
    chat = update.effective_chat
    chat_id = chat.id
    chat_type = chat.type  # 'private', 'group', 'supergroup', 'channel'
    chat_title = chat.title if chat.title else "私聊對話"
    msg_id = msg.message_id
    user_name = update.effective_user.first_name if update.effective_user else "主管"
    cmd_text = msg.text.strip()

    is_private = chat_type == "private"
    is_group = chat_type in ["group", "supergroup"]

    # 判斷是否為指派給本代理之指令
    is_for_me = False
    clean_text = cmd_text

    if is_private:
        # 私聊直接全員響應
        is_for_me = True
        chat_desc = "一對一私聊"
    elif is_group:
        # 群聊判斷：1. 是否 @water_002_bot 或指名 002/柚水；2. 是否 Reply 本 Bot 的訊息
        bot_tag = f"@{BOT_USERNAME.lower()}"
        lower_text = cmd_text.lower()

        if bot_tag in lower_text or "002" in cmd_text or "柚水" in cmd_text:
            is_for_me = True
            clean_text = re.sub(rf"@{BOT_USERNAME}", "", cmd_text, flags=re.IGNORECASE).strip()
        elif msg.reply_to_message and msg.reply_to_message.from_user and msg.reply_to_message.from_user.username == BOT_USERNAME:
            is_for_me = True
            clean_text = cmd_text
            
        chat_desc = f"群組頻道: {chat_title}"

    if not is_for_me:
        # 在群聊中不是在叫 002，禮貌略過，不互相干擾
        return

    # 1. 寫入員工日誌
    record_to_employee_log(user_name, clean_text, chat_desc=chat_desc)

    # 2. 先回覆收到確認（群組中自動引用該則訊息）
    await msg.reply_text(
        f"📥 **【{AGENT_NAME} 收到指示】**\n> {clean_text}\n\n🧠 正在呼叫反重力大腦思考並處理中，請稍候...",
        parse_mode=ParseMode.MARKDOWN,
    )

    # 3. 核心大腦注入：將題目直接打入 002 反重力對話！
    prompt_for_ide = (
        f"【來自 Telegram 主管指示 ({chat_desc})】\n"
        f"發送主管：{user_name} (ChatID: {chat_id}, MsgID: {msg_id})\n"
        f"指示內容：\n{clean_text}\n\n"
        f"請以 002 柚水 (歐印雲後端專業 AI 員工) 的身分研讀手冊並思考，"
        f"完成後請立即執行以下命令將你的精確答覆回傳至該頻道：\n"
        f"python send_telegram.py --chat-id {chat_id} --reply-to {msg_id} --text \"你的詳細回答內容\""
    )
    injected = inject_message_to_ide(prompt_for_ide)
    if not injected:
        logger.warning("IDE 注入未成功，可能當前電腦未開啟反重力視窗。")

def main():
    logger.info(f"🚀 [{AGENT_NAME}] 反重力雙向即時注入監聽核心啟動中 (@{BOT_USERNAME})...")
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("status", start_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info(f"🟢 [{AGENT_NAME}] 已連線至 Telegram 長輪詢接收中...")
    app.run_polling()

if __name__ == "__main__":
    main()
