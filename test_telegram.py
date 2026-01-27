import requests
from my_telegram import send_telegram

bot_token = "8569256667:AAF4JgGZV2p-BG_F70MP9n1lq2hy4jjqVdg"
chat_id = "1719792436"

def send_telegram(message):
    url = f"https://api.telegram.org/bot8569256667:AAF4JgGZV2p-BG_F70MP9n1lq2hy4jjqVdg/sendMessage"
    payload = {
        "chat_id": 1719792436,
        "text": message
    }
    response = requests.post(url, data=payload)
   
# 🔹 print("Sending test message...")
send_telegram("✅ Telegram connection test successful")
print("Done")