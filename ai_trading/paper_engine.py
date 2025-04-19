class TradeLogger:
    def __init__(self):
        self.trades = []
        self.pnl = 0

    def log(self, trade):
        self.trades.append(trade)
        if trade["action"] == "SELL":
            self.pnl += trade.get("pnl", 0)

    def get_total_pnl(self):
        return self.pnl


class PaperTradingEngine:
    def __init__(self):
        self.logger = TradeLogger()
        self.position = None

    def trade(self, signal):
        if signal["signal"] == "FIB_AI_BUY" and not self.position:
            self.position = {
                "entry_price": signal["price"],
                "quantity": 1,
                "entry_time": signal["timestamp"],
            }
            self.logger.log(
                {
                    "timestamp": signal["timestamp"],
                    "action": "BUY",
                    "type": signal["type"],
                    "price": signal["price"],
                    "quantity": 1,
                }
            )
        elif self.position:
            pnl = signal["price"] - self.position["entry_price"]
            self.logger.log(
                {
                    "timestamp": signal["timestamp"],
                    "action": "SELL",
                    "type": signal["type"],
                    "price": signal["price"],
                    "quantity": 1,
                    "pnl": pnl,
                }
            )
            self.position = None
