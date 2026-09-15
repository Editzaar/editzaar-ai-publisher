import os
import sys
import threading
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import telegram_bot
import web_cms

def start_telegram_bot():
    time.sleep(2)
    print("[Main] Starting Telegram Bot listener loop...", flush=True)
    try:
        telegram_bot.run_telegram_bot()
    except Exception as e:
        print(f"[Main Bot Loop Error]: {e}", flush=True)

if __name__ == "__main__":
    print("[Main] Starting background Telegram thread...", flush=True)
    t = threading.Thread(target=start_telegram_bot, daemon=True)
    t.start()
    
    port = int(os.environ.get("PORT", 3000))
    print(f"[Main] Starting Web CMS server on 0.0.0.0:{port}...", flush=True)
    web_cms.run_server(port=port)
