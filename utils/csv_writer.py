import csv
from datetime import datetime
import os

def save_backtest_to_csv(symbol, trades, report):
    filename = f"{symbol}_backtest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    file_path = f"./backtest_results/{filename}"
    os.makedirs("./backtest_results", exist_ok=True)

    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Type", "Price", "Timestamp", "PnL"])
        for trade in trades:
            writer.writerow([
                trade["type"], trade["price"], trade["timestamp"], trade.get("pnl", "")
            ])
        writer.writerow([])
        writer.writerow(["Total PnL", report["total_pnl"]])
        writer.writerow(["Total Trades", report["total_trades"]])
    return file_path
