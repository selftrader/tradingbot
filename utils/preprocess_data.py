import pandas as pd
import os
import ta

DATA_DIR = "data/sectoral"
PROCESSED_DIR = "data/processed"

def preprocess_csv(file_path, save_path):
    """Handles missing data & adds technical indicators."""
    df = pd.read_csv(file_path)

    # Ensure 'Close' column is numeric
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    # Drop rows where Close price is missing
    df.dropna(subset=["Close"], inplace=True)

    # Fill missing values
    df.ffill(inplace=True)  # Fixed deprecated fillna()

    # ✅ Add Exponential Moving Average (EMA)
    df["SMA_50"] = ta.trend.sma_indicator(df["Close"], window=50)
    df["EMA_50"] = ta.trend.ema_indicator(df["Close"], window=50)  # ✅ Fixed EMA calculation
    df["RSI"] = ta.momentum.rsi(df["Close"], window=14)
    df["MACD"] = ta.trend.macd(df["Close"])

    # Save processed data
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)
    print(f"✅ Processed & Saved: {save_path}")

# Process all sectoral data
for item in os.listdir(DATA_DIR):
    item_path = os.path.join(DATA_DIR, item)

    if os.path.isdir(item_path):  # Only process directories
        for file in os.listdir(item_path):
            file_path = os.path.join(item_path, file)
            save_path = os.path.join(PROCESSED_DIR, item, file)

            if os.path.isfile(file_path):  # Ensure it's a CSV file
                preprocess_csv(file_path, save_path)

print("✅ Data Preprocessing Complete!")
