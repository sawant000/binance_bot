import requests
from config import TELEGRAM_BOT_TOKEN, ADMIN_CHAT_ID

BASE_URL = f"https://api.telegram.org/bot8569256667:AAF4JgGZV2p-BG_F70MP9n1lq2hy4jjqVdg{TELEGRAM_BOT_TOKEN}"
last_update_id = None


def get_updates():
    global last_update_id

    params = {}
    if last_update_id:
        params["offset"] = last_update_id + 1

    response = requests.get(f"{BASE_URL}/getUpdates", params=params)
    data = response.json()

    if not data["ok"]:
        return []

    updates = data["result"]

    if updates:
        last_update_id = updates[-1]["update_id"]

    return updates


def get_commands():
    updates = get_updates()
    commands = []

    for update in updates:
        if "message" not in update:
            continue

        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "").strip()

        # 🔐 ADMIN PROTECTION
        if chat_id != ADMIN_CHAT_ID:
            continue

        if text.startswith("/"):
            commands.append(text)

    return commands