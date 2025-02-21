import os
import pandas as pd

DATA_DIR = "data/sectoral"
PROCESSED_DIR = "data/processed"

def fix_missing_values(file_path, save_path):
    """Handles missing values in CSV files"""
    df = pd.read_csv(file_path)

    if df.isnull().sum().sum() > 0:
        print(f"⚠️ Missing data detected in {file_path}. Fixing...")
        df.fillna(method="ffill", inplace=True)  # Forward fill
        df.fillna(method="bfill", inplace=True)  # Backward fill

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)
    print(f"✅ Fixed & Saved: {save_path}")

# Process all CSVs
for sector in os.listdir(DATA_DIR):
    sector_path = os.path.join(DATA_DIR, sector)
    if os.path.isdir(sector_path):
        for file in os.listdir(sector_path):
            if file.endswith(".csv"):
                file_path = os.path.join(sector_path, file)
                save_path = os.path.join(PROCESSED_DIR, sector, file)
                fix_missing_values(file_path, save_path)

print("✅ Missing Data Fix Complete!")
