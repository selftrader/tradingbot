import pandas as pd
from requests import Session
from database.models import HistoricalData
from services.backtesting import evaluate_ai_performance


def compare_ai_vs_market(user_id: int, symbol: str, db: Session):
    """Compare AI trading returns vs. NIFTY index performance."""

    ai_trades = evaluate_ai_performance(user_id, symbol, db)
    market_performance = db.query(HistoricalData).filter(HistoricalData.symbol == "NIFTY 50").all()

    market_df = pd.DataFrame([{
        "date": entry.date, 
        "close": entry.close
    } for entry in market_performance])

    market_df.set_index("date", inplace=True)

    # Calculate AI returns
    ai_wins = sum(1 for trade in ai_trades["results"] if trade["result"] == "WIN")
    ai_losses = sum(1 for trade in ai_trades["results"] if trade["result"] == "LOSS")
    ai_return = ai_wins - ai_losses  # Simple P&L calculation

    # Calculate Market returns
    first_price = market_df.iloc[0]["close"]
    last_price = market_df.iloc[-1]["close"]
    market_return = ((last_price - first_price) / first_price) * 100

    return {"AI_Returns": ai_return, "Market_Returns": market_return}
