import numpy as np
import pandas as pd
from sqlalchemy.orm import Session
from database.models import HistoricalData
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

import numpy as np

def detect_trend_reversal(user_id: int, symbol: str, db: Session):
    """AI-based Trend Reversal Detection"""

    # Fetch last 100 price points
    historical_data = db.query(HistoricalData).filter(HistoricalData.symbol == symbol).order_by(HistoricalData.date.desc()).limit(100).all()
    
    if len(historical_data) < 60:  # Minimum data needed
        return {"error": "Not enough historical data for AI analysis."}

    df = pd.DataFrame([{
        "date": entry.date, 
        "close": entry.close
    } for entry in historical_data])

    df.set_index("date", inplace=True)

    # Normalize the data
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(df["close"].values.reshape(-1,1))

    X_test = np.array([scaled_data[-60:]])  # Last 60 price points
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    # Load pre-trained LSTM model
    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=(60, 1)),
        LSTM(units=50),
        Dense(units=1)
    ])
    model.load_weights("models/trend_model.h5")

    predicted_price = scaler.inverse_transform(model.predict(X_test))[0][0]
    actual_price = df["close"].iloc[-1]

    if predicted_price < actual_price * 0.98:  # 2% drop detected
        return {"status": "Trend Reversal Detected - EXIT TRADE"}

    return {"status": "No Trend Reversal"}
