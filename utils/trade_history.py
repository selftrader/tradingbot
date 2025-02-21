# utils/trade_history.py

import logging

class TradeHistory:
    def __init__(self):
        self.trades = []

    def record_trade(self, trade):
        """
        Record a new trade.
        :param trade: Dictionary containing trade details.
        """
        self.trades.append(trade)
        logging.info(f"Recorded trade: {trade}")

    def update_last_trade_result(self, profit):
        """
        Update the result of the last trade.
        :param profit: Profit (positive) or loss (negative).
        """
        if not self.trades:
            logging.warning("No trades to update.")
            return
        self.trades[-1]['result'] = profit
        # Optionally, store the features used during the trade (for learning).
        self.trades[-1]['features'] = [1000, 500]  # Replace with actual feature values.

    def get_all_trades(self):
        return self.trades
