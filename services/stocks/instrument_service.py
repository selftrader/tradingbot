import json
import pandas as pd
from datetime import datetime

with open("data/top_stocks.json") as f:
    top_stocks = json.load(f)

instrument_df = pd.read_json("data/upstox_instruments.json")


def get_top_stocks_with_chain():
    results = []
    for stock in top_stocks:
        symbol = stock["symbol"]
        name = stock["name"]
        eq = instrument_df[
            (instrument_df["symbol"] == symbol)
            & (instrument_df["instrument_type"] == "EQ")
        ]
        opt = instrument_df[
            (instrument_df["symbol"] == symbol)
            & (instrument_df["instrument_type"] == "OPTSTK")
        ].copy()
        if opt.empty or eq.empty:
            continue

        opt["expiry"] = pd.to_datetime(opt["expiry"], errors="coerce")
        nearest_expiry = opt[opt["expiry"] > datetime.now()]["expiry"].min()
        current = opt[opt["expiry"] == nearest_expiry]
        atm = current["strike_price"].median()
        strikes = current[current["strike_price"].between(atm - 20, atm + 20)]

        results.append(
            {
                "symbol": symbol,
                "name": name,
                "trading_symbol": eq.iloc[0]["trading_symbol"],
                "exchange": eq.iloc[0]["exchange"],
                "instrument_key": eq.iloc[0]["instrument_key"],
                "atm": atm,
                "expiry": str(nearest_expiry.date()),
                "strike_prices": sorted(strikes["strike_price"].unique().tolist()),
            }
        )
    return results
