from datetime import datetime
from trade_log import read_trades


def calculate_daily_pnl():
    today = datetime.now().date()
    pnl = 0.0

    trades = read_trades()

    positions = {}

    for t in trades:
        trade_date = datetime.strptime(
            t["time"], "%Y-%m-%d %H:%M:%S"
        ).date()

        if trade_date != today:
            continue

        symbol = t["symbol"]
        side = t["side"]
        price = float(t["price"])
        amount = float(t["amount"])

        if side == "BUY":
            positions[symbol] = positions.get(symbol, 0) - price * amount
        elif side == "SELL":
            positions[symbol] = positions.get(symbol, 0) + price * amount

    pnl = sum(positions.values())
    return round(pnl, 2)