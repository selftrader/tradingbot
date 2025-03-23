import random
import time
import logging
from sqlalchemy.orm import Session
from database.models import TradePerformance
from services.ai_strategy import detect_trend_reversal
from services.trade_execution import exit_trade

class TradeMonitorService:
    """Simulates real-time trade updates"""

    def __init__(self):
        self.trade_counter = 1

    def get_latest_trade(self):
        """Simulate a random trade update"""
        time.sleep(2)  # Simulate market delay
        trade_update = {
            "order_id": self.trade_counter,
            "status": random.choice(["Executed", "Pending", "Failed"]),
            "message": random.choice(["Buy Order Executed", "Sell Order Pending", "Trade Canceled"]),
        }
        self.trade_counter += 1
        logging.info(f"📡 New Trade Update: {trade_update}")
        return trade_update





def monitor_trades(user_id: int, db: Session):
    """Monitor open trades and exit on AI trend reversal detection."""
    
    open_trades = db.query(TradePerformance).filter(
        TradePerformance.user_id == user_id, TradePerformance.status == "OPEN"
    ).all()

    for trade in open_trades:
        trend_analysis = detect_trend_reversal(user_id, trade.symbol, db)

        if trend_analysis["status"] == "Trend Reversal Detected - EXIT TRADE":
            exit_trade(user_id, trade.symbol, db)
