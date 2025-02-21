class StrategyEngine:
    def __init__(self, market_data, options_data=None):
        self.market_data = market_data
        self.options_data = options_data

    def mean_reversion(self):
        """Mean Reversion Strategy: Buy if RSI < 30, Sell if RSI > 70"""
        if self.market_data["RSI"] < 30:
            return "BUY"
        elif self.market_data["RSI"] > 70:
            return "SELL"
        return "HOLD"

    def breakout_trading(self):
        """Breakout Strategy: Buy if price crosses above SMA, Sell if below"""
        if self.market_data["Close"] > self.market_data["SMA_50"]:
            return "BUY"
        elif self.market_data["Close"] < self.market_data["SMA_50"]:
            return "SELL"
        return "HOLD"

    def options_greeks_strategy(self):
        """Options Trading Strategy: Based on OI, IV, Delta"""
        if self.options_data:
            if self.options_data["Call_OI"] > self.options_data["Put_OI"] and self.options_data["IV"] > 20:
                return "BUY CALL"
            elif self.options_data["Put_OI"] > self.options_data["Call_OI"] and self.options_data["IV"] > 20:
                return "BUY PUT"
        return "HOLD"
