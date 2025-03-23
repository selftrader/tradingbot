import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from database.models import HistoricalData, TradeHistory
from services.ai_model import train_lstm_model, predict_future_prices

def backtest_ai_strategy(user_id: int, symbol: str, db: Session):
    """Run backtesting on historical data before live execution."""
    
    # Fetch historical data
    historical_data = db.query(HistoricalData).filter(HistoricalData.symbol == symbol).all()
    if not historical_data:
        return {"error": "No historical data found."}

    # Convert to DataFrame
    df = pd.DataFrame([{
        "date": entry.date, 
        "close": entry.close
    } for entry in historical_data])

    df.set_index("date", inplace=True)

    # Train AI Model
    model, scaler = train_lstm_model(user_id, symbol, db)
    
    trade_results = []
    for i in range(60, len(df)):
        recent_data = df.iloc[i-60:i]["close"].values.reshape(-1,1)
        predicted_price = predict_future_prices(model, scaler, recent_data)
        actual_price = df.iloc[i]["close"]

        trade_type = "BUY" if predicted_price > recent_data[-1][0] else "SELL"
        profit_loss = actual_price - recent_data[-1][0] if trade_type == "BUY" else recent_data[-1][0] - actual_price

        trade_results.append({
            "date": df.index[i],
            "symbol": symbol,
            "trade_type": trade_type,
            "entry_price": recent_data[-1][0],
            "exit_price": actual_price,
            "profit_loss": profit_loss
        })

        # Save in DB for analysis
        trade_entry = TradeHistory(
            user_id=user_id,
            symbol=symbol,
            trade_type=trade_type,
            quantity=1,
            entry_price=recent_data[-1][0],
            exit_price=actual_price,
            profit_loss=profit_loss,
            status="CLOSED"
        )
        db.add(trade_entry)

    db.commit()
    
    return {"message": "✅ Backtesting completed successfully", "trade_results": trade_results}
