import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram(message):
    url = f"https://api.telegram.org/bot8569256667:AAF4JgGZV2p-BG_F70MP9n1lq2hy4jjqVdg/sendMessage"
    payload = {
        "chat_id":1719792436,
        "text": message
    }
    requests.post(url, json=payload)