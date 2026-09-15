import os
import sys
import threading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import telegram_bot
import web_cms

def start_telegram_bot():
    try:
        print([Main] Launching Telegram Bot thread..., flush=True)
        telegram_bot.run_telegram_bot()
    except Exception as e:
        print(f[Main Bot Error]: {e}, flush=True)

if __name__ == __main__:
    bot_thread = threading.Thread(target=start_telegram_bot, daemon=True)
    bot_thread.start()
    
    port = int(os.environ.get(PORT, 3000))
    print(f[Main] Launching Web CMS on port {port}..., flush=True)
    web_cms.run_server(port=port)
