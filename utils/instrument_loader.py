import json
import pandas as pd


def load_instruments_df():
    with open("data/upstox_instruments.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # Convert expiry from Unix timestamp if it's numeric
    if df["expiry"].dtype in ["int64", "float64"]:
        df["expiry"] = pd.to_datetime(df["expiry"], unit="ms", errors="coerce")
    else:
        df["expiry"] = pd.to_datetime(df["expiry"], errors="coerce")

    # Clean up invalid values for JSON compatibility
    df = df.replace([float("inf"), float("-inf")], pd.NA)
    df = df.fillna(value={"strike_price": 0})  # Prevent NaN in key fields

    return df
