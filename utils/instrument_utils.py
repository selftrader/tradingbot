import json
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger("instrument_utils")


def get_default_instrument_keys():
    top_stocks_path = Path("data/top_stocks.json")
    instrument_path = Path("data/upstox_instruments.json")

    if not top_stocks_path.exists() or not instrument_path.exists():
        logger.error("❌ Missing required JSON files for instrument keys.")
        return []

    try:
        with open(top_stocks_path, "r", encoding="utf-8") as f:
            top_stocks = json.load(f).get("securities", [])

        with open(instrument_path, "r", encoding="utf-8") as f:
            all_instruments = json.load(f)
    except Exception as e:
        logger.error(f"❌ Failed to load or parse files: {e}")
        return []

    instrument_keys = []

    for stock in top_stocks:
        symbol = stock.get("symbol")
        exchange = stock.get("exchange")

        if not symbol or not exchange:
            continue

        # Match using trading_symbol, asset_symbol, or underlying_symbol
        matches = [
            instr
            for instr in all_instruments
            if instr.get("exchange") == exchange
            and (
                instr.get("trading_symbol") == symbol
                or instr.get("asset_symbol") == symbol
                or instr.get("underlying_symbol") == symbol
            )
        ]

        # Pick instrument with nearest expiry (if available)
        def parse_expiry(instr):
            expiry = instr.get("expiry")
            try:
                return datetime.fromtimestamp(expiry / 1000) if expiry else datetime.max
            except:
                return datetime.max

        matches.sort(key=parse_expiry)

        if matches:
            instrument_key = matches[0].get("instrument_key")
            if instrument_key:
                instrument_keys.append(instrument_key)

    return instrument_keys
