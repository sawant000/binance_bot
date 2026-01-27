from binance_price import get_closes
from my_telegram import send_telegram
import time
from datetime import datetime, timedelta
from binance_trade import market_buy,market_sell,get_client
from config import USE_TESTNET,API_KEY,API_SECRET
import csv
import os
# =====================
# CONFIG
# =====================
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]  # Multiple coins
MA_PERIOD = 20
RSI_PERIOD = 14
INTERVAL_SECONDS = 60
STOP_LOSS_PERCENT = 0.02
TRAILING_STOP_PERCENT = 0.015  # 1.5% trailing SL
TAKE_PROFIT_PERCENT = 0.03
TRADE_QUANTITY = 0.001  # small default for testing
LOG_FILE = "trade_log.csv"

# Track positions per symbol
positions = {symbol: {"status": None, "entry_price": 0, "highest_price": 0} for symbol in SYMBOLS}

# Track daily P/L
daily_trades = []
last_summary_date = datetime.now().date()

print("🚀 Multi-Coin Trading Bot Started (FINAL UPGRADED)")

# =====================
# LOG FUNCTION
# =====================
def log_trade(symbol, action, price, quantity):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Time", "Symbol", "Action", "Price", "Quantity"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            symbol,
            action,
            f"{price:.2f}",
            f"{quantity:.5f}"
        ])
    # Track for daily P/L
    if action in ["BUY", "SELL", "TAKE_PROFIT", "STOP_LOSS"]:
        daily_trades.append({"symbol": symbol, "action": action, "price": price, "quantity": quantity})

# =====================
# INDICATORS
# =====================
def calculate_ma(closes, period):
    return sum(closes[-period:]) / period

def calculate_rsi(closes, period):
    gains, losses = [], []
    for i in range(1, period + 1):
        diff = closes[-i] - closes[-i - 1]
        if diff > 0:
            gains.append(diff)
        else:
            losses.append(abs(diff))
    avg_gain = sum(gains) / period if gains else 0
    avg_loss = sum(losses) / period if losses else 0
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# =====================
# MAIN LOOP
# =====================
while True:
    try:
        now = datetime.now()
        client = get_client()
        balance_info = client.get_asset_balance(asset='USDT')
        balance = float(balance_info['free']) if balance_info else 0

        for symbol in SYMBOLS:
            closes = get_closes(symbol, limit=100)
            price = closes[-1]

            ma = calculate_ma(closes, MA_PERIOD)
            rsi = calculate_rsi(closes, RSI_PERIOD)

            pos = positions[symbol]
            safe_quantity = min(TRADE_QUANTITY, balance * 0.05 / price)

            # ---------------------
            # BUY LOGIC
            # ---------------------
            if pos["status"] is None and rsi < 30 and price > ma and safe_quantity > 0:
                market_buy(symbol, safe_quantity)
                pos["status"] = "LONG"
                pos["entry_price"] = price
                pos["highest_price"] = price

                send_telegram(
                    f"🟢 {'TESTNET ' if USE_TESTNET else ''}BUY EXECUTED\n"
                    f"{symbol}\nQty: {safe_quantity:.5f}\nPrice: {price:.2f}"
                )
                log_trade(symbol, "BUY", price, safe_quantity)

            # ---------------------
            # MANAGE POSITION WITH TRAILING SL
            # ---------------------
            elif pos["status"] == "LONG":
                # Update highest price since entry
                if price > pos["highest_price"]:
                    pos["highest_price"] = price

                # Trailing stop-loss calculation
                trailing_sl = max(pos["highest_price"] * (1 - TRAILING_STOP_PERCENT),
                                  pos["entry_price"] * (1 - STOP_LOSS_PERCENT))
                tp_price = pos["entry_price"] * (1 + TAKE_PROFIT_PERCENT)

                # TAKE PROFIT
                if price >= tp_price:
                    market_sell(symbol, safe_quantity)
                    send_telegram(
                        f"🎯 {'TESTNET ' if USE_TESTNET else ''}TAKE-PROFIT HIT\n"
                        f"{symbol}\nQty: {safe_quantity:.5f}\nExit: {price:.2f}"
                    )
                    log_trade(symbol, "TAKE_PROFIT", price, safe_quantity)
                    pos["status"] = None
                    pos["entry_price"] = 0
                    pos["highest_price"] = 0

                # TRAILING / STOP LOSS
                elif price <= trailing_sl:
                    market_sell(symbol, safe_quantity)
                    send_telegram(
                        f"🛑 {'TESTNET ' if USE_TESTNET else ''}STOP-LOSS HIT\n"
                        f"{symbol}\nQty: {safe_quantity:.5f}\nExit: {price:.2f}"
                    )
                    log_trade(symbol, "STOP_LOSS", price, safe_quantity)
                    pos["status"] = None
                    pos["entry_price"] = 0
                    pos["highest_price"] = 0

            # ---------------------
            # STATUS LOG
            # ---------------------
            status = pos["status"] if pos["status"] else "NO POSITION"
            print(
                f"{now.strftime('%Y-%m-%d %H:%M:%S')} | {symbol} | Price: {price:.2f} | "
                f"MA: {ma:.2f} | RSI: {rsi:.2f} | Status: {status} | Safe Qty: {safe_quantity:.5f}"
            )

        # ---------------------
        # DAILY PROFIT / LOSS SUMMARY
        # ---------------------
        if now.date() != last_summary_date:
            # Calculate daily P/L
            daily_pl_message = "📊 Daily P/L Summary:\n"
            for trade in daily_trades:
                action = trade['action']
                if action in ["TAKE_PROFIT", "STOP_LOSS"]:
                    daily_pl_message += f"{trade['symbol']} | {action} | {trade['price']:.2f} | Qty: {trade['quantity']:.5f}\n"
            send_telegram(daily_pl_message)
            daily_trades.clear()
            last_summary_date = now.date()

        time.sleep(INTERVAL_SECONDS)

    except Exception as e:
        print("Error:", e)
        send_telegram(f"❌ Bot error:\n{e}")
        time.sleep(60)