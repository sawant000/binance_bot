import requests

bot_token = "8569256667:AAF4JgGZV2p-BG_F70MP9n1lq2hy4jjqVdg"

url = f"https://api.telegram.org/bot8569256667:AAF4JgGZV2p-BG_F70MP9n1lq2hy4jjqVdg/getUpdates"
response = requests.get(url).json()

print(response)