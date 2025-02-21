import os
import pandas as pd

DATA_DIR = "data/sectoral"

def check_csv_files(directory):
    """Check if CSV files exist and contain valid data."""
    for sector in os.listdir(directory):
        sector_path = os.path.join(directory, sector)
        if os.path.isdir(sector_path):  # Check if it's a directory
            for file in os.listdir(sector_path):
                if file.endswith(".csv"):
                    file_path = os.path.join(sector_path, file)
                    df = pd.read_csv(file_path)
                    print(f"✅ Checking {file} - Rows: {len(df)}, Columns: {df.shape[1]}")
                    if df.isnull().sum().sum() > 0:
                        print(f"⚠️ WARNING: {file} contains missing values!")

# Run Check
if __name__ == "__main__":
    check_csv_files(DATA_DIR)
