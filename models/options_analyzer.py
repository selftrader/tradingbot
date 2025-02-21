import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import yfinance as yf

class OptionsChainAnalyzer:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            random_state=42
        )
        self.scaler = StandardScaler()

    def get_options_chain(self, symbol: str) -> pd.DataFrame:
        """Fetch options chain data for a symbol"""
        stock = yf.Ticker(symbol)
        expiry_dates = stock.options

        all_options = []
        for date in expiry_dates[:2]:  # Consider nearest two expiries
            opt = stock.option_chain(date)
            calls = opt.calls.assign(optionType='call', expiryDate=date)
            puts = opt.puts.assign(optionType='put', expiryDate=date)
            all_options.extend([calls, puts])

        return pd.concat(all_options)

    def calculate_options_features(self, chain_data: pd.DataFrame, stock_price: float) -> pd.DataFrame:
        """Calculate option-specific features"""
        features = pd.DataFrame()
        
        # Basic option metrics
        features['moneyness'] = stock_price / chain_data['strike']
        features['timeToExpiry'] = (pd.to_datetime(chain_data['expiryDate']) - datetime.now()).dt.days
        features['impliedVolatility'] = chain_data['impliedVolatility']
        
        # Option Greeks
        features['delta'] = chain_data['delta']
        features['theta'] = chain_data['theta']
        features['gamma'] = chain_data['gamma']
        features['vega'] = chain_data['vega']
        
        # Volume and OI analysis
        features['volumeOIRatio'] = chain_data['volume'] / chain_data['openInterest'].where(chain_data['openInterest'] > 0, 1)
        features['putCallRatio'] = chain_data['volume'] / chain_data.groupby('strike')['volume'].transform('sum')
        
        return features

    def analyze_options(self, symbol: str) -> dict:
        """Analyze options for trading opportunities"""
        try:
            # Get stock data
            stock = yf.Ticker(symbol)
            current_price = stock.history(period='1d')['Close'].iloc[-1]
            
            # Get options chain
            chain = self.get_options_chain(symbol)
            
            # Calculate features
            features = self.calculate_options_features(chain, current_price)
            
            # Apply trading rules
            opportunities = self._identify_opportunities(chain, features, current_price)
            
            return {
                'symbol': symbol,
                'current_price': current_price,
                'opportunities': opportunities
            }
            
        except Exception as e:
            print(f"Error analyzing options for {symbol}: {str(e)}")
            return None

    def _identify_opportunities(self, chain: pd.DataFrame, features: pd.DataFrame, current_price: float) -> list:
        opportunities = []
        
        # High probability trades
        high_prob = chain[
            (features['delta'].abs() > 0.3) & 
            (features['delta'].abs() < 0.7) &
            (features['impliedVolatility'] > 0.2) &
            (features['volumeOIRatio'] > 1.5)
        ]
        
        for _, option in high_prob.iterrows():
            opportunity = {
                'strategy': 'Single Option',
                'type': option['optionType'],
                'strike': option['strike'],
                'expiry': option['expiryDate'],
                'iv': option['impliedVolatility'],
                'probability': self._calculate_probability(option, current_price),
                'risk_reward': self._calculate_risk_reward(option)
            }
            opportunities.append(opportunity)

        return opportunities

    def _calculate_probability(self, option: pd.Series, current_price: float) -> float:
        # Calculate probability of profit based on delta and IV
        if option['optionType'] == 'call':
            return abs(option['delta'])
        else:
            return 1 - abs(option['delta'])

    def _calculate_risk_reward(self, option: pd.Series) -> float:
        # Calculate risk/reward ratio
        max_loss = option['lastPrice']
        max_profit = option['strike'] - option['lastPrice'] if option['optionType'] == 'call' else option['lastPrice']
        return max_profit / max_loss if max_loss > 0 else 0