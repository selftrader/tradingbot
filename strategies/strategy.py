import pandas as pd

def run_ema_strategy(df: pd.DataFrame, short_period=9, long_period=21):
    df["EMA_Short"] = df["close"].ewm(span=short_period).mean()
    df["EMA_Long"] = df["close"].ewm(span=long_period).mean()

    position = 0
    trades = []
    for i in range(1, len(df)):
        if df["EMA_Short"][i] > df["EMA_Long"][i] and df["EMA_Short"][i-1] <= df["EMA_Long"][i-1]:
            # Buy Signal
            trades.append({"type": "BUY", "price": df["close"][i], "timestamp": df["timestamp"][i]})
            position = df["close"][i]
        elif df["EMA_Short"][i] < df["EMA_Long"][i] and df["EMA_Short"][i-1] >= df["EMA_Long"][i-1] and position:
            # Sell Signal
            pnl = df["close"][i] - position
            trades.append({
                "type": "SELL",
                "price": df["close"][i],
                "timestamp": df["timestamp"][i],
                "pnl": pnl
            })
            position = 0

    total_pnl = sum([t.get("pnl", 0) for t in trades if t["type"] == "SELL"])
    return trades, {"total_pnl": total_pnl, "total_trades": len(trades)}
