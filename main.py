from binance_price import get_btc_price
from my_telegram import send_telegram_message
import time

# List of multiple targets
BUY_TARGETS = [90000, 95000, 100000]
SELL_TARGETS = [88000, 85000, 80000]

# Keep track of which targets have been alerted
buy_alerted = set()
sell_alerted = set()

print("🚀 Binance BTC Multi-Target Alert Bot Started")

while True:
    try:
        price = get_btc_price()
        print(f"📊 Current BTC price: {price}")

        # Check BUY targets
        for target in BUY_TARGETS:
            if price > target and target not in buy_alerted:
                message = (
                    f"🟢 BUY ALERT\n\n"
                    f"BTC crossed ABOVE {target}\n"
                    f"Current Price: {price}"
                )
                send_telegram_message(message)
                buy_alerted.add(target)
                print(f"✅ Buy alert sent for {target}")

        # Check SELL targets
        for target in SELL_TARGETS:
            if price < target and target not in sell_alerted:
                message = (
                    f"🔴 SELL ALERT\n\n"
                    f"BTC dropped BELOW {target}\n"
                    f"Current Price: {price}"
                )
                send_telegram_message(message)
                sell_alerted.add(target)
                print(f"✅ Sell alert sent for {target}")

    except Exception as e:
        print("❌ Error:", e)

    time.sleep(60)