from fastapi import logger
import numpy as np
import pandas as pd
try:
    import pandas_ta as ta
except ImportError:
    print("Error importing pandas_ta. Using alternative technical indicators.")
    ta = None
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from sklearn.ensemble import RandomForestClassifier
import yfinance as yf
from scipy import stats

# Add fallback technical indicators if pandas_ta fails
def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate technical indicators using pure pandas if pandas_ta is not available"""
    if ta is not None:
        return df.ta

    # Create a copy of the dataframe to avoid the SettingWithCopyWarning
    df_copy = df.copy()

    def rsi(close, periods=14):
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def atr(high, low, close, periods=14):
        tr = pd.DataFrame()
        tr['h-l'] = high - low
        tr['h-pc'] = abs(high - close.shift(1))
        tr['l-pc'] = abs(low - close.shift(1))
        tr = tr.max(axis=1)
        return tr.rolling(periods).mean()

    # Use loc for assignment
    df_copy.loc[:, 'RSI'] = rsi(df_copy['Close'])
    df_copy.loc[:, 'ATR'] = atr(df_copy['High'], df_copy['Low'], df_copy['Close'])
    
    return df_copy

from config import SECTORAL_INDICES

@dataclass
class StockSignal:
    symbol: str
    sector: str
    confidence: float
    entry_price: float
    target_price: float
    stop_loss: float
    trade_type: str  # 'LONG' or 'SHORT'
    timeframe: str
    signal_strength: float
    risk_reward: float

class StockSelector:
    def __init__(self):
        self.features = [
            # Price Action Features
            'trend_strength',
            'price_momentum',
            'volume_momentum',
            
            # Technical Indicators
            'rsi',
            'macd',
            'adx',
            'bb_position',
            'sup_res_distance',
            
            # Volatility Features
            'atr_ratio',
            'volatility_rank',
            
            # Market Context
            'sector_momentum',
            'nifty_correlation',
            'market_breadth',
            
            # Volume Analysis
            'volume_profile',
            'delivery_percentage',
            
            # Additional Factors
            'fii_dii_activity',
            'option_chain_pcr',
            'open_interest_change'
        ]
        
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_leaf=10,
            random_state=42
        )
        
        # Add training parameters
        self.training_window = 60  # Days of historical data for training
        self.prediction_threshold = 0.7  # Minimum confidence for signals
        self.volatility = None  # Will be set during training

    def calculate_features(self, df: pd.DataFrame, market_data: Dict) -> pd.DataFrame:
        """Calculate technical and market features for analysis"""
        try:
            features = pd.DataFrame()
            
            # Basic price features
            features['returns'] = df['Close'].pct_change()
            features['volume_change'] = df['Volume'].pct_change()
            
            # Technical indicators using pandas_ta if available
            if ta is not None:
                try:
                    # RSI
                    features['rsi'] = df.ta.rsi()
                    
                    # MACD
                    macd = df.ta.macd()
                    features['macd'] = macd[macd.columns[0]] - macd[macd.columns[1]]
                    
                    # ADX
                    adx = df.ta.adx()
                    features['adx'] = adx['ADX_14']
                    
                except Exception as ta_error:
                    logger.warning(f"Error calculating ta indicators: {str(ta_error)}")
                    # Fallback to basic calculations
                    features = self._calculate_basic_indicators(df, features)
            else:
                # Use basic calculations if pandas_ta not available
                features = self._calculate_basic_indicators(df, features)
            
            # Add market context features
            features['market_breadth'] = market_data['market_breadth'][-len(features):]
            features['sector_momentum'] = market_data['sector_momentum'][-len(features):]
            
            return features.fillna(0)  # Fill any NaN values
            
        except Exception as e:
            logger.error(f"Error calculating features: {str(e)}")
            return pd.DataFrame()  # Return empty DataFrame on error

    def _calculate_basic_indicators(self, df: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
        """Calculate basic technical indicators without pandas_ta"""
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        features['rsi'] = 100 - (100 / (1 + rs))
        
        # Simple MACD
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        features['macd'] = exp1 - exp2
        
        # Basic momentum
        features['momentum'] = df['Close'].pct_change(periods=10)
        
        return features

    def _calculate_trend_strength(self, df: pd.DataFrame) -> pd.Series:
        """Calculate trend strength using multiple timeframes"""
        ema20 = df.ta.ema(length=20)
        ema50 = df.ta.ema(length=50)
        ema200 = df.ta.ema(length=200)
        
        trend_score = (
            (df['Close'] > ema20).astype(int) +
            (df['Close'] > ema50).astype(int) +
            (df['Close'] > ema200).astype(int) +
            (ema20 > ema50).astype(int) +
            (ema50 > ema200).astype(int)
        )
        return trend_score / 5  # Normalize to 0-1

    def analyze_stock(self, 
                     symbol: str, 
                     sector: str,
                     data: pd.DataFrame, 
                       market_data: Dict) -> Optional[StockSignal]:
        """Analyze stock and generate trading signal with enhanced metrics"""
        try:
            features = self.calculate_features(data, market_data)
            prediction = self.model.predict_proba(features.iloc[-1:])
            confidence = prediction[0][1]
            
            if confidence < 0.7:
                return None
                
            entry_price = data['Close'].iloc[-1]
            atr = data.ta.atr()[-1]
            
            # Calculate target and stop loss using ATR
            if confidence > 0.8:
                target_price = entry_price + (3 * atr)
                stop_loss = entry_price - (1.5 * atr)
                trade_type = 'LONG'
                
                # Get enhanced risk metrics
                risk_metrics = self.calculate_risk_reward(
                    entry_price,
                    target_price,
                    stop_loss
                )
                
                # Get IV percentile
                current_iv = self._get_historical_iv(symbol)
                iv_rank = self._calculate_iv_percentile(symbol, current_iv)
                
                # Calculate win probability
                win_prob = self._calculate_probability_of_profit(
                    entry_price,
                    target_price,
                    current_iv
                )
                
                if win_prob < 0.6 or iv_rank > 80:
                    return None
                    
                return StockSignal(
                    symbol=symbol,
                    sector=sector,
                    confidence=confidence * win_prob,  # Adjust confidence with win probability
                    entry_price=entry_price,
                    target_price=target_price,
                    stop_loss=stop_loss,
                    trade_type=trade_type,
                    timeframe='1D',
                    signal_strength=self._calculate_signal_strength(features.iloc[-1]),
                    risk_reward=risk_metrics['risk_reward_ratio']
                )
                
        except Exception as e:
            print(f"Error analyzing {symbol}: {str(e)}")
            return None

    def _calculate_signal_strength(self, features: pd.Series) -> float:
        """Calculate overall signal strength"""
        weights = {
            'trend_strength': 0.2,
            'rsi': 0.15,
            'macd': 0.15,
            'volume_profile': 0.1,
            'sector_momentum': 0.15,
            'market_breadth': 0.1,
            'option_chain_pcr': 0.15
        }
        
        signal_strength = sum(features[k] * v for k, v in weights.items())
        return min(max(signal_strength, 0), 1)  # Normalize to 0-1

    def _calculate_iv_percentile(self, symbol: str, current_iv: float) -> float:
        """
        Calculate IV percentile based on historical volatility data
        """
        try:
            # Get historical volatility data for past year
            hist_data = pd.DataFrame()
            hist_data['iv'] = self._get_historical_iv(symbol)
            
            # Calculate percentile rank of current IV
            iv_percentile = len(hist_data[hist_data['iv'] <= current_iv]) / len(hist_data) * 100
            return iv_percentile
            
        except Exception as e:
            print(f"Error calculating IV percentile for {symbol}: {str(e)}")
            return 50.0  # Return neutral value on error

    def _calculate_probability_of_profit(self, 
                                      current_price: float,
                                      target_price: float,
                                      volatility: float,
                                      days_to_target: int = 10) -> float:
        """
        Calculate probability of reaching target price using options-based approach
        """
        try:
            # Convert annual volatility to daily
            daily_vol = volatility / np.sqrt(252)
            
            # Calculate z-score for target price
            z_score = (np.log(target_price/current_price)) / (daily_vol * np.sqrt(days_to_target))
            
            # Calculate probability using normal distribution
            if target_price > current_price:
                prob = 1 - stats.norm.cdf(z_score)
            else:
                prob = stats.norm.cdf(z_score)
                
            return prob
            
        except Exception as e:
            print(f"Error calculating probability: {str(e)}")
            return 0.5

    def calculate_risk_reward(self, 
                             entry: float,
                             target: float,
                             stop_loss: float,
                             position_size: float = 100000) -> Dict:
        """
        Calculate comprehensive risk-reward metrics
        """
        try:
            # Basic R:R ratio
            risk = abs(entry - stop_loss)
            reward = abs(target - entry)
            rr_ratio = reward / risk if risk > 0 else 0
            
            # Position sizing and money metrics
            max_loss = position_size * (risk / entry)
            potential_profit = position_size * (reward / entry)
            
            # Kelly criterion for optimal position size
            win_prob = self._calculate_probability_of_profit(entry, target, self.volatility)
            kelly_pct = win_prob - ((1 - win_prob) / rr_ratio)
            kelly_pct = max(min(kelly_pct, 0.25), 0)  # Cap at 25%
            
            return {
                'risk_reward_ratio': rr_ratio,
                'max_loss': max_loss,
                'potential_profit': potential_profit,
                'win_probability': win_prob,
                'kelly_percentage': kelly_pct,
                'suggested_position': position_size * kelly_pct
            }
            
        except Exception as e:
            print(f"Error calculating risk-reward metrics: {str(e)}")
            return {
                'risk_reward_ratio': 0,
                'max_loss': 0,
                'potential_profit': 0,
                'win_probability': 0,
                'kelly_percentage': 0,
                'suggested_position': 0
            }

    def _get_historical_iv(self, symbol: str) -> pd.Series:
        """
        Get historical implied volatility data
        """
        try:
            # Use yfinance or your data provider to get options data
            ticker = yf.Ticker(symbol)
            
            # Get nearest expiry options
            expiry = ticker.options[0]
            chain = ticker.option_chain(expiry)
            
            # Calculate historical IV using ATM options
            spot_price = ticker.history(period='1d')['Close'].iloc[-1]
            atm_calls = chain.calls[chain.calls['strike'].between(spot_price*0.95, spot_price*1.05)]
            
            if not atm_calls.empty:
                return atm_calls['impliedVolatility'].mean()
            return 0.3  # Default to 30% if no data
            
        except Exception as e:
            print(f"Error getting historical IV for {symbol}: {str(e)}")
            return 0.3

    def train_model(self, symbols: List[str]) -> None:
        """Train the model using historical data from multiple stocks"""
        all_features = []
        all_targets = []

        for symbol in symbols:
            try:
                # Get training data
                data = yf.download(
                    symbol,
                    period="2y",  # 2 years of data
                    interval="1d"
                )
                
                if data.empty:
                    continue

                # Calculate future returns for target labels
                data['Future_Return'] = data['Close'].shift(-5) / data['Close'] - 1  # 5-day forward returns
                data['Target'] = (data['Future_Return'] > 0).astype(int)  # 1 for up, 0 for down
                
                # Get market context for features
                market_data = self._get_market_context(data.index)
                
                # Calculate features for each day in the window
                for i in range(self.training_window, len(data)-5):
                    window_data = data.iloc[i-self.training_window:i]
                    features = self.calculate_features(window_data, market_data)
                    
                    if not features.empty:
                        all_features.append(features.iloc[-1])
                        all_targets.append(data['Target'].iloc[i])

            except Exception as e:
                print(f"Error processing {symbol}: {str(e)}")
                continue

        # Check if we have training samples
        if len(all_features) == 0:
            print("No training samples available. Skipping training.")
            return

        # Convert to numpy arrays
        X = np.vstack(all_features)
        y = np.array(all_targets)

        # Train the model
        print(f"Training model with {len(X)} samples...")
        self.model.fit(X, y)
        
        # Calculate overall volatility for probability calculations
        self.volatility = np.std(np.diff(np.log(data['Close']))) * np.sqrt(252)

    def _get_market_context(self, dates) -> Dict:
        """Get market context data including indices and breadth"""
        try:
            # Get Nifty data
            nifty = yf.download('^NSEI', period="1y", interval="1d")
            dates_len = len(dates)
            
            # Generate market context data
            context = {
                'nifty_data': nifty,
                'sector_momentum': self._calculate_sector_momentum(nifty),
                'market_breadth': np.random.uniform(0.3, 0.7, size=dates_len),
                'pcr': np.random.uniform(0.8, 1.2, size=dates_len),
                'oi_change': np.random.uniform(-0.1, 0.1, size=dates_len),
                'fii_dii_net': np.random.uniform(-1000, 1000, size=dates_len)
            }
            
            return context

        except Exception as e:
            logger.error(f"Error getting market context: {str(e)}")
            # Return default values if error occurs
            return {
                'nifty_data': pd.DataFrame(),
                'sector_momentum': 0,
                'market_breadth': np.zeros(len(dates)),
                'pcr': np.ones(len(dates)),
                'oi_change': np.zeros(len(dates)),
                'fii_dii_net': np.zeros(len(dates))
            }

    def _calculate_sector_momentum(self, nifty_data: pd.DataFrame) -> float:
        """Calculate sector momentum using Nifty data"""
        returns = nifty_data['Close'].pct_change()
        momentum = returns.rolling(window=20).mean() / returns.rolling(window=20).std()
        return momentum.fillna(0)

    def analyze_stocks(self, symbols: List[str], sector: str) -> Union[List[StockSignal], None]:
        """Analyze multiple stocks and rank them by signal strength"""
        signals = []
        market_data = self._get_market_context(pd.date_range(end=pd.Timestamp.now(), periods=60))

        for symbol in symbols:
            try:
                # Get recent data
                data = yf.download(symbol, period="3mo", interval="1d")
                if data.empty:
                    continue

                # Get latest features
                features = self.calculate_features(data.tail(60), market_data)
                if features.empty:
                    continue

                # Make prediction
                prediction = self.model.predict_proba(features.iloc[-1:])
                confidence = prediction[0][1]  # Probability of upward movement

                if confidence > self.prediction_threshold:
                    signal = self._generate_trading_signal(
                        symbol, sector, confidence, data, market_data
                    )
                    if signal:
                        signals.append(signal)

            except Exception as e:
                print(f"Error analyzing {symbol}: {str(e)}")
                continue

        # Sort signals by confidence and strength
        return sorted(signals, key=lambda x: (x.confidence, x.signal_strength), reverse=True)

    def _generate_trading_signal(self, 
                               symbol: str, 
                               sector: str, 
                               confidence: float, 
                               data: pd.DataFrame,
                               market_data: Dict) -> Optional[StockSignal]:
        """Generate detailed trading signal with entry, target, and stop loss"""
        try:
            current_price = data['Close'].iloc[-1]
            atr = data.ta.atr().iloc[-1]

            # Calculate support and resistance
            support = data['Low'].rolling(20).min().iloc[-1]
            resistance = data['High'].rolling(20).max().iloc[-1]

            # Determine trade direction based on prediction and technical setup
            if confidence > 0.8 and current_price > support:
                trade_type = 'LONG'
                stop_loss = max(support, current_price - 2 * atr)
                target_price = current_price + (current_price - stop_loss) * 2  # 2:1 reward-risk
            else:
                return None

            # Calculate additional metrics
            risk_metrics = self.calculate_risk_reward(
                current_price, target_price, stop_loss
            )

            return StockSignal(
                symbol=symbol,
                sector=sector,
                confidence=confidence,
                entry_price=current_price,
                target_price=target_price,
                stop_loss=stop_loss,
                trade_type=trade_type,
                timeframe='1D',
                signal_strength=self._calculate_signal_strength(
                    self.calculate_features(data.tail(60), market_data).iloc[-1]
                ),
                risk_reward=risk_metrics['risk_reward_ratio']
            )

        except Exception as e:
            print(f"Error generating signal for {symbol}: {str(e)}")
            return None

# Example usage
selector = StockSelector()

# Train the model
selector.train_model(SECTORAL_INDICES['NIFTY IT'])

# Analyze stocks
signals = selector.analyze_stocks(SECTORAL_INDICES['NIFTY IT'], 'NIFTY IT')

# Print recommendations
for signal in signals:
    print(f"Symbol: {signal.symbol}")
    print(f"Action: {signal.trade_type}")
    print(f"Entry: {signal.entry_price:.2f}")
    print(f"Target: {signal.target_price:.2f}")
    print(f"Stop Loss: {signal.stop_loss:.2f}")
    print(f"Confidence: {signal.confidence:.2%}")
    print("---")