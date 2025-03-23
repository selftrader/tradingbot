import numpy as np
import pandas as pd
from sqlalchemy.orm import Session
from database.models import HistoricalData, TradeSignal
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def detect_trade_signal(user_id: int, symbol: str, db: Session):
    """AI-based pattern detection for optimal trade entry points."""
    
    # Fetch last 100 price points
    historical_data = db.query(HistoricalData).filter(
        HistoricalData.symbol == symbol
    ).order_by(HistoricalData.date.desc()).limit(100).all()

    if len(historical_data) < 60:  # Minimum required data
        return {"error": "Not enough historical data for AI analysis."}

    df = pd.DataFrame([{
        "date": entry.date, 
        "close": entry.close,
        "open": entry.open,
        "high": entry.high,
        "low": entry.low
    } for entry in historical_data])

    df.set_index("date", inplace=True)

    # Normalize the data
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(df["close"].values.reshape(-1,1))

    X_test = np.array([scaled_data[-60:]])  # Last 60 price points
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    # Load pre-trained LSTM model for pattern recognition
    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=(60, 1)),
        LSTM(units=50),
        Dense(units=1, activation="sigmoid")
    ])
    model.load_weights("models/trade_entry_model.h5")

    prediction = model.predict(X_test)[0][0]
    trade_type = "BUY" if prediction > 0.5 else "SELL"
    confidence = round(prediction * 100, 2)

    # Store AI signal in the database
    trade_signal = TradeSignal(
        user_id=user_id,
        symbol=symbol,
        trade_type=trade_type,
        confidence=confidence
    )
    db.add(trade_signal)
    db.commit()

    return {"symbol": symbol, "trade_type": trade_type, "confidence": confidence, "status": "PENDING"}
