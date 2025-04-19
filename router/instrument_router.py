from fastapi import APIRouter, Query
import pandas as pd
from utils.instrument_loader import load_instruments_df
from datetime import datetime

router = APIRouter()
df = load_instruments_df()


@router.get("/api/instruments/search")
def search_instruments(q: str = Query(...), exchange: str = Query("ALL")):
    results = df[df["trading_symbol"].str.contains(q.upper(), na=False)]
    if exchange != "ALL":
        results = results[results["exchange"] == exchange]

    columns_to_return = [
        "trading_symbol",
        "name",
        "instrument_key",
        "exchange",
        "segment",
        "instrument_type",
        "underlying_symbol",
        "expiry",
        "strike_price",
    ]

    # Ensure only available columns are selected
    results = results[[col for col in columns_to_return if col in results.columns]]

    # Drop rows with invalid float (NaN, inf)
    results = results.replace([float("inf"), float("-inf")], pd.NA).dropna()

    return results.head(30).to_dict(orient="records")


@router.get("/api/instruments/chain")
def get_option_chain(symbol: str, range: int = 20):
    options = df[
        (df["symbol"].str.upper() == symbol.upper())
        & (df["instrument_type"].str.startswith("OPT"))
    ].copy()

    if options.empty:
        return {"chain": []}

    options["expiry"] = pd.to_datetime(options["expiry"], errors="coerce")
    future_expiry = options[options["expiry"] > datetime.now()]
    nearest_expiry = future_expiry["expiry"].min()
    current = options[options["expiry"] == nearest_expiry]

    atm = current["strike_price"].median()
    min_strike = atm - range
    max_strike = atm + range

    strikes = current[current["strike_price"].between(min_strike, max_strike)]

    chain = []
    for strike in sorted(strikes["strike_price"].unique()):
        row = {"strike_price": strike, "ce": None, "pe": None}
        ce = strikes[
            (strikes["strike_price"] == strike) & (strikes["option_type"] == "CE")
        ]
        pe = strikes[
            (strikes["strike_price"] == strike) & (strikes["option_type"] == "PE")
        ]
        if not ce.empty:
            row["ce"] = ce.iloc[0].to_dict()
        if not pe.empty:
            row["pe"] = pe.iloc[0].to_dict()
        chain.append(row)

    return {
        "symbol": symbol.upper(),
        "atm": atm,
        "expiry": str(nearest_expiry.date()),
        "chain": chain,
    }
