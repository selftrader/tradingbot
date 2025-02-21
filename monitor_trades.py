import yfinance as yf
import time

open_trades = {}  # Store open trade details

def monitor_and_exit_trades():
    """Monitor open trades and close positions with profit."""
    for symbol, trade in open_trades.items():
        current_price = yf.download(symbol, period="1d", interval="5m")["Close"].iloc[-1]
        entry_price = trade["entry_price"]
        target_profit = entry_price * 1.02  # 2% profit target
        stop_loss = entry_price * 0.98  # 2% stop loss

        if current_price >= target_profit:
            print(f"✅ Profit target reached for {symbol}. Closing trade.")
            close_trade(symbol, "SELL" if trade["action"] == "BUY" else "BUY")
            del open_trades[symbol]
        elif current_price <= stop_loss:
            print(f"❌ Stop-loss hit for {symbol}. Exiting trade.")
            close_trade(symbol, "SELL" if trade["action"] == "BUY" else "BUY")
            del open_trades[symbol]

def close_trade(symbol, action):
    """Simulates trade exit."""
    print(f"🔄 Closing trade for {symbol} with {action} order.")
