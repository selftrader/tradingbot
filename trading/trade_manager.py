import time
import logging

class TradeManager:
    def __init__(self, broker_api, predictor):
        self.broker_api = broker_api
        self.predictor = predictor
        self.active_trades = {}  # Stores Open Trades
        self.trading_active = False

    def execute_trade(self, symbol, trade_type, entry_price):
        """Executes trade & adds it to the active trades list"""
        order_id = self.broker_api.place_order(trade_type, entry_price, symbol)
        if order_id:
            self.active_trades[symbol] = {
                "trade_type": trade_type,
                "entry_price": entry_price,
                "stop_loss": entry_price * 0.98,  # Initial Stop-Loss (2% Down)
                "take_profit": entry_price * 1.05,  # Initial Take-Profit (5% Up)
                "status": "open"
            }
            logging.info(f"Trade Executed: {trade_type} {symbol} @ {entry_price}")

    def monitor_trades(self):
        """Continuously monitors open trades & adjusts positions"""
        while self.trading_active:
            for symbol, trade in list(self.active_trades.items()):
                live_price = self.broker_api.get_live_price(symbol)
                prediction = self.predictor.predict_live_trade(self.broker_api.get_live_market_data(symbol))

                # If AI predicted a change in trend → Exit Trade
                if trade["trade_type"] == "BUY" and prediction == "SELL":
                    self.close_trade(symbol, live_price, reason="Trend Reversal")
                elif trade["trade_type"] == "SELL" and prediction == "BUY":
                    self.close_trade(symbol, live_price, reason="Trend Reversal")

                # If Take-Profit or Stop-Loss Hits → Exit Trade
                if live_price >= trade["take_profit"]:
                    self.close_trade(symbol, live_price, reason="Take-Profit Hit")
                elif live_price <= trade["stop_loss"]:
                    self.close_trade(symbol, live_price, reason="Stop-Loss Hit")

            time.sleep(5)  # Check every 5 seconds

    def close_trade(self, symbol, exit_price, reason):
        """Closes trade when conditions are met"""
        trade = self.active_trades[symbol]
        profit_loss = exit_price - trade["entry_price"] if trade["trade_type"] == "BUY" else trade["entry_price"] - exit_price
        order_id = self.broker_api.place_order("SELL" if trade["trade_type"] == "BUY" else "BUY", exit_price, symbol)

        if order_id:
            logging.info(f"Trade Closed: {symbol} @ {exit_price} | P/L: {profit_loss:.2f} | Reason: {reason}")
            del self.active_trades[symbol]  # Remove from active trades
