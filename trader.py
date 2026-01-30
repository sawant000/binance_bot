from config import TRAILING_STOP_PERCENT

# Stores trailing stop per symbol
trailing_stops = {}

def update_trailing_stop(symbol, current_price, last_buy_price):
    """
    Updates trailing stop for a symbol
    """
    global trailing_stops
    stop_price = last_buy_price * (1 - TRAILING_STOP_PERCENT / 100)

    # Only raise stop if price moves up
    if symbol not in trailing_stops or current_price > trailing_stops[symbol]:
        trailing_stops[symbol] = max(stop_price, trailing_stops.get(symbol, 0))

    return trailing_stops[symbol]

def check_sell(symbol, current_price):
    """
    Returns True if price hits trailing stop
    """
    global trailing_stops
    stop_price = trailing_stops.get(symbol, 0)
    if stop_price and current_price <= stop_price:
        trailing_stops[symbol] = 0  # reset
        return True
    return False