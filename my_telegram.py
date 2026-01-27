import requests
from config import API_KEY, API_SECRET

bot_token = "8569256667:AAF4JgGZV2p-BG_F70MP9n1lq2hy4jjqVdg"
chat_id = "1719792436"

def send_telegram(message):
    url = f"https://api.telegram.org/bot8569256667:AAF4JgGZV2p-BG_F70MP9n1lq2hy4jjqVdg/sendMessage"
    payload = {
        "chat_id": 1719792436,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        print("Telegram status code:", response.status_code)
        print("Telegram response:", response.text)
    except Exception as e:
        print("Telegram error:", e)
    