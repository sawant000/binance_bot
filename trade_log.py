import csv
import os
from datetime import datetime


TRADE_LOG_FILE = "trade_log.csv"


def log_trade(symbol, side, price, amount):
    file_exists = False
    try:
        with open(TRADE_LOG_FILE, "r"):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(TRADE_LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["time", "symbol", "side", "price", "amount"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            symbol,
            side,
            price,
            amount
        ])


def read_trades():
    trades = []

    try:
        with open(TRADE_LOG_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                trades.append(row)
    except FileNotFoundError:
        pass

    return trades
