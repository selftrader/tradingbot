import pandas as pd
import os

DATA_DIR = "data/processed"
TRAINING_DATA_PATH = "data/training_data.csv"

def load_training_data():
    """Combine all processed CSV files into one dataset."""
    all_data = []
    
    for sector in os.listdir(DATA_DIR):
        sector_path = os.path.join(DATA_DIR, sector)

        if os.path.isdir(sector_path):  # Ensure it's a folder
            for file in os.listdir(sector_path):
                file_path = os.path.join(sector_path, file)
                if file.endswith(".csv"):
                    df = pd.read_csv(file_path)
                    df["Sector"] = sector  # Add sector name

                    # Ensure required columns exist
                    required_cols = ["SMA_50", "EMA_50", "RSI", "MACD", "Close"]
                    missing_cols = [col for col in required_cols if col not in df.columns]
                    if missing_cols:
                        print(f"❌ Missing columns in {file}: {missing_cols}")
                        continue  # Skip this file if missing columns

                    df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)  # Buy (1) or Sell (0)
                    all_data.append(df)

    if not all_data:
        print("❌ No valid data found for training.")
        return None

    df_final = pd.concat(all_data, ignore_index=True)
    df_final.to_csv(TRAINING_DATA_PATH, index=False)
    print(f"✅ Training Data Saved: {TRAINING_DATA_PATH}")

if __name__ == "__main__":
    load_training_data()
