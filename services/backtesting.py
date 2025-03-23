import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from database.models import HistoricalData, TradeSignal
import pandas as pd

def backtest_ai_trades(user_id: int, symbol: str, db: Session):
    """Backtest AI trade signals against real market data."""

    # Fetch historical data
    historical_data = db.query(HistoricalData).filter(HistoricalData.symbol == symbol).all()
    trade_signals = db.query(TradeSignal).filter(TradeSignal.symbol == symbol).all()

    df = pd.DataFrame([{
        "date": entry.date, 
        "close": entry.close
    } for entry in historical_data])

    df.set_index("date", inplace=True)

    results = []
    for signal in trade_signals:
        signal_date = signal.signal_time.date()
        actual_close = df.loc[str(signal_date)]["close"]
        trade_success = "WIN" if (signal.trade_type == "BUY" and actual_close > signal.confidence) else "LOSS"

        results.append({
            "symbol": symbol,
            "trade_type": signal.trade_type,
            "ai_confidence": signal.confidence,
            "actual_close": actual_close,
            "result": trade_success
        })

    return results




def evaluate_ai_performance(user_id: int, symbol: str, db: Session):
    """Backtest AI trade signals against real market data."""

    # Fetch historical data
    historical_data = db.query(HistoricalData).filter(HistoricalData.symbol == symbol).all()
    trade_signals = db.query(TradeSignal).filter(TradeSignal.symbol == symbol).all()

    df = pd.DataFrame([{
        "date": entry.date, 
        "close": entry.close
    } for entry in historical_data])

    df.set_index("date", inplace=True)

    total_trades = len(trade_signals)
    profitable_trades = 0
    losses = 0

    results = []
    for signal in trade_signals:
        signal_date = signal.signal_time.date()
        
        if str(signal_date) in df.index:
            actual_close = df.loc[str(signal_date)]["close"]
            trade_success = "WIN" if (signal.trade_type == "BUY" and actual_close > signal.confidence) else "LOSS"

            if trade_success == "WIN":
                profitable_trades += 1
            else:
                losses += 1

            results.append({
                "symbol": symbol,
                "trade_type": signal.trade_type,
                "ai_confidence": signal.confidence,
                "actual_close": actual_close,
                "result": trade_success
            })

    accuracy = (profitable_trades / total_trades) * 100 if total_trades > 0 else 0
    return {"total_trades": total_trades, "win_rate": accuracy, "results": results}
