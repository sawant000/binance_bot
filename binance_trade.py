from binance.client import Client
from config import API_KEY, API_SECRET, USE_TESTNET

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