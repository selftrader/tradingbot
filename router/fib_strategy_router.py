from fastapi import APIRouter, Query
from utils.upstox_data import fetch_historical_candles
from ai_trading.fibonacci_strategy import detect_fib_trade_with_ai
from ai_trading.paper_engine import PaperTradingEngine

router = APIRouter()


@router.post("/fib-trade-run")
def run_fib_ai_trade(symbol: str = Query(...)):
    df = fetch_historical_candles(symbol)
    signals, levels = detect_fib_trade_with_ai(df)

    engine = PaperTradingEngine()
    for signal in signals:
        engine.trade(signal)

    return {
        "symbol": symbol,
        "fibonacci_levels": levels,
        "trades": engine.logger.trades,
        "pnl": engine.logger.get_total_pnl(),
        "signals": signals,
        "candles": df.tail(100).to_dict(orient="records"),
    }
