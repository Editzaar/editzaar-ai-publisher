import os
import sys
import time
import json
import socket
import urllib.request
import urllib.parse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from gemini_engine import generate_deep_article_with_gemini, post_article_with_deduplication, EXISTING_LABELS

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

TELEGRAM_BOT_TOKEN = "8747123023:AAHvZb_kgwq-i1HqGgtCkXSElC8GJG10Ngo"
BASE_TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# Single Instance Lock on localhost:59876 to guarantee no duplicate bots run
_lock_socket = None
def ensure_single_instance():
    global _lock_socket
    try:
        _lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _lock_socket.bind(('127.0.0.1', 59876))
    except Exception as e:
        print(f"[Single Instance Notice] Socket bind: {e}", flush=True)

def send_telegram_message(chat_id, text, parse_mode="HTML"):
    try:
        url = f"{BASE_TELEGRAM_URL}/sendMessage"
        data = urllib.parse.urlencode({
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": False
        }).encode('utf-8')
        req = urllib.request.Request(url, data=data)
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Error sending Telegram message: {e}", flush=True)

def send_telegram_photo_bytes(chat_id, photo_bytes, caption=""):
    try:
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        body = []
        body.append(f'--{boundary}\r\n'.encode('utf-8'))
        body.append(f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{chat_id}\r\n'.encode('utf-8'))
        
        if caption:
            body.append(f'--{boundary}\r\n'.encode('utf-8'))
            body.append(f'Content-Disposition: form-data; name="caption"\r\n\r\n{caption[:900]}\r\n'.encode('utf-8'))
            body.append(f'--{boundary}\r\n'.encode('utf-8'))
            body.append('Content-Disposition: form-data; name="parse_mode"\r\n\r\nHTML\r\n'.encode('utf-8'))

        body.append(f'--{boundary}\r\n'.encode('utf-8'))
        body.append('Content-Disposition: form-data; name="photo"; filename="thumbnail.jpg"\r\n'.encode('utf-8'))
        body.append('Content-Type: image/jpeg\r\n\r\n'.encode('utf-8'))
        body.append(photo_bytes)
        body.append(f'\r\n--{boundary}--\r\n'.encode('utf-8'))

        data = b''.join(body)
        url = f"{BASE_TELEGRAM_URL}/sendPhoto"
        req = urllib.request.Request(url, data=data, headers={'Content-Type': f'multipart/form-data; boundary={boundary}'})
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Error sending direct photo to Telegram: {e}", flush=True)

def get_updates(offset=None):
    try:
        url = f"{BASE_TELEGRAM_URL}/getUpdates?timeout=30"
        if offset:
            url += f"&offset={offset}"
        req = urllib.request.urlopen(url)
        res = json.loads(req.read().decode('utf-8'))
        return res.get("result", [])
    except Exception as e:
        time.sleep(2)
        return []

def run_telegram_bot():
    ensure_single_instance()
    print("==================================================", flush=True)
    print("EDITZAAR TELEGRAM BOT IS LIVE (POWERED BY GEMINI AI)!", flush=True)
    print("Username: @EditzaarPublisherBot", flush=True)
    print("==================================================", flush=True)

    last_update_id = None
    processed_updates = set()

    while True:
        updates = get_updates(last_update_id)
        for update in updates:
            uid = update["update_id"]
            last_update_id = uid + 1
            
            if uid in processed_updates:
                continue
            processed_updates.add(uid)

            message = update.get("message", {})
            text = message.get("text", "").strip()
            chat_id = message.get("chat", {}).get("id")

            if not text or not chat_id:
                continue

            # Greetings & Commands
            if text.lower() in ["/start", "hi", "hello", "hey"]:
                welcome_msg = (
                    "👋 <b>Welcome to Editzaar Deep Research AI Bot!</b>\n\n"
                    "Send me ANY topic, TV show review, film breakdown, editing technique, or software question.\n\n"
                    "⚡ <b>What happens:</b>\n"
                    "• 🌐 Live multi-query web grounding\n"
                    "• 🧠 Google Gemini 3.7/3.6/3.5 Flash deep reasoning & writing\n"
                    "• 🎨 Custom 3D typography thumbnail generated for the topic\n"
                    "• 📝 Full masterclass article drafted directly to Blogger with SEO tags!\n\n"
                    "<i>Try sending:</i> <code>Bigg Boss 18 Editing & Pacing Review</code> or <code>Top 10 Video Editing Hacks</code>"
                )
                send_telegram_message(chat_id, welcome_msg)
                continue

            topic = text.replace("/write", "").strip()
            if not topic:
                send_telegram_message(chat_id, "⚠️ Please type a topic! Example:\n<code>Top 5 Video Editing Hacks</code>")
                continue

            print(f"[Telegram Bot] Processing user topic: '{topic}' from Chat ID: {chat_id}", flush=True)
            send_telegram_message(chat_id, f"🔍 <b>Starting Deep Internet Research & Gemini AI Synthesis...</b>\n\nScraping live 2026 facts, breakdown formulas & rendering 3D thumbnail for:\n📝 <i>{topic}</i>")

            try:
                # 1. Live Gemini AI Deep Research & Content Compilation
                article_data = generate_deep_article_with_gemini(topic)
                
                # 2. Smart Post with In-Place Deduplication
                edit_url, post_id = post_article_with_deduplication(article_data)

                # 3. Send custom photo banner directly to Telegram
                send_telegram_photo_bytes(chat_id, article_data['img_bytes'], caption=f"📸 <b>{article_data['title']}</b>")

                # 4. Send detailed message with Blogger link
                response_text = (
                    f"🎉 <b>Deep-Researched Article Drafted on Blogger!</b>\n\n"
                    f"📌 <b>Title:</b> {article_data['title']}\n"
                    f"🏷️ <b>Tag:</b> <code>{article_data['label']}</code>\n"
                    f"🌍 <b>Location:</b> India\n\n"
                    f"📋 <b>Search Description (0/150 for Blogger sidebar):</b>\n"
                    f"<code>{article_data['search_desc']}</code>\n\n"
                    f"👉 <a href='{edit_url}'><b>Open & Preview in Blogger Dashboard ↗</b></a>"
                )
                send_telegram_message(chat_id, response_text)
                print(f"[Telegram Bot] Successfully delivered: {topic} (ID: {post_id})", flush=True)
            except Exception as e:
                send_telegram_message(chat_id, f"❌ <b>Error:</b> {str(e)}")
                print(f"[Telegram Bot] Error: {e}", flush=True)

        time.sleep(1)

if __name__ == "__main__":
    run_telegram_bot()
