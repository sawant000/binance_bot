import requests
def get_closes(symbol, limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit={limit}"
    data = requests.get(url).json()
    closes = [float(x[4]) for x in data]  # closing price
    return closes