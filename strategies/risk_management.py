class RiskManagement:
    def __init__(self, risk_percent=1.5, reward_percent=2):
        self.risk_percent = risk_percent
        self.reward_percent = reward_percent

    def apply_risk_rules(self, entry_price):
        stop_loss = entry_price * (1 - (self.risk_percent / 100))
        take_profit = entry_price * (1 + (self.reward_percent / 100))
        return stop_loss, take_profit
