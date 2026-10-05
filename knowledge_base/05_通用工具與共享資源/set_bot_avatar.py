#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
歐印雲 All In Cloud - 代理共同知識庫共用工具
腳本名稱: set_bot_avatar.py
用途: 一鍵更換 Telegram Bot 頭像 (支援本地檔案路徑與網路圖片 URL)
維護人: 002 柚水 💧
=============================================================================
使用方式:
  python set_bot_avatar.py --token "<BOT_TOKEN>" --image "avatar.png"
  python set_bot_avatar.py --token "<BOT_TOKEN>" --image "https://example.com/avatar.png"
=============================================================================
"""

import os
import sys
import json
import argparse
import requests

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def change_avatar(token: str, image_source: str) -> bool:
    url = f"https://api.telegram.org/bot{token}/setMyProfilePhoto"
    temp_file = None

    try:
        # 下載網路圖檔
        if image_source.startswith("http://") or image_source.startswith("https://"):
            print(f"🌐 正在下載圖片: {image_source}")
            r = requests.get(image_source, timeout=15)
            r.raise_for_status()
            temp_file = "temp_downloaded_avatar.png"
            with open(temp_file, "wb") as f:
                f.write(r.content)
            img_path = temp_file
        else:
            img_path = image_source

        if not os.path.exists(img_path):
            print(f"❌ 找不到圖片檔案: {img_path}")
            return False

        # InputProfilePhotoStatic 協定封裝
        photo_meta = {"type": "static", "photo": "attach://avatar_file"}
        with open(img_path, "rb") as f:
            files = {"avatar_file": (os.path.basename(img_path), f, "image/png")}
            data = {"photo": json.dumps(photo_meta)}
            res = requests.post(url, data=data, files=files, timeout=20)
            res_json = res.json()

        if res.status_code == 200 and res_json.get("ok"):
            print("✅ Telegram 機器人頭像已成功更新！")
            return True
        else:
            print(f"❌ 更新失敗: [{res.status_code}] {res_json.get('description')}")
            return False

    except Exception as e:
        print(f"❌ 發生例外: {e}")
        return False
    finally:
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Telegram Bot 一鍵更換頭像工具")
    parser.add_argument("--token", "-t", required=True, help="Telegram Bot API Token")
    parser.add_argument("--image", "-i", required=True, help="本地圖片路徑或網路圖片網址")
    args = parser.parse_args()

    success = change_avatar(args.token, args.image)
    sys.exit(0 if success else 1)
