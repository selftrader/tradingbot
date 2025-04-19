# services/ai_trading_engine.py


from services import ai_model


def analyze_and_trade(live_data):
    trades = []
    for symbol, ltp in live_data.items():
        # Your AI model logic here
        signal = ai_model.predict(symbol, ltp)
        if signal == "BUY":
            trades.append({"symbol": symbol, "action": "BUY", "ltp": ltp})
        elif signal == "SELL":
            trades.append({"symbol": symbol, "action": "SELL", "ltp": ltp})
    return trades
