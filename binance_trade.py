from binance.client import Client
from config import BINANCE_API_KEY, BINANCE_API_SECRET
def get_client():
    client = Client(API_KEY, API_SECRET)
    if USE_TESTNET:
        client.API_URL = "https://testnet.binance.vision/api"
    return client

def market_buy(symbol, quantity):
    client = get_client()
    order = client.order_market_buy(symbol=symbol, quantity=quantity)
    return order

def market_sell(symbol, quantity):
    client = get_client()
    order = client.order_market_sell(symbol=symbol, quantity=quantity)
    return order