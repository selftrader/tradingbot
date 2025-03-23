import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy.orm import Session
from database.models import HistoricalData

def train_lstm_model(user_id: int, symbol: str, db: Session):
    """Train LSTM model on historical stock price movements."""
    
    # Fetch historical data from DB
    historical_data = db.query(HistoricalData).filter(HistoricalData.symbol == symbol).all()
    if not historical_data:
        return {"error": "No historical data found."}

    df = pd.DataFrame([{
        "date": entry.date, 
        "close": entry.close
    } for entry in historical_data])

    df.set_index("date", inplace=True)

    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(df["close"].values.reshape(-1,1))

    X_train, y_train = [], []
    for i in range(60, len(scaled_data)):
        X_train.append(scaled_data[i-60:i, 0])
        y_train.append(scaled_data[i, 0])

    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
        LSTM(units=50),
        Dense(units=1)
    ])

    model.compile(optimizer="adam", loss="mean_squared_error")
    model.fit(X_train, y_train, epochs=25, batch_size=32)
    
    return model, scaler

def predict_future_prices(model, scaler, recent_data):
    """Predict future stock prices using the trained LSTM model."""
    scaled_data = scaler.transform(recent_data.reshape(-1,1))
    X_test = np.array([scaled_data])
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    prediction = model.predict(X_test)
    return scaler.inverse_transform(prediction)[0][0]
