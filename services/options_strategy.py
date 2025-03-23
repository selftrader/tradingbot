from services.options_chain import get_options_chain

def recommend_options_trade(symbol: str):
    """AI suggests best options trade based on IV and OI levels."""
    
    options_data = get_options_chain(symbol)
    if "error" in options_data:
        return options_data

    best_call = max(options_data, key=lambda x: x["CE"]["openInterest"])
    best_put = max(options_data, key=lambda x: x["PE"]["openInterest"])

    return {
        "best_call_strike": best_call["strikePrice"],
        "best_call_IV": best_call["CE"]["impliedVolatility"],
        "best_call_OI": best_call["CE"]["openInterest"],
        "best_put_strike": best_put["strikePrice"],
        "best_put_IV": best_put["PE"]["impliedVolatility"],
        "best_put_OI": best_put["PE"]["openInterest"]
    }
