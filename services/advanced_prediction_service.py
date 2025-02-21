import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
from datetime import datetime, timedelta
import yfinance as yf
from sqlalchemy.orm import Session
import aiohttp
import asyncio
import logging
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)
    
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        predictions = self.fc(lstm_out[:, -1, :])
        return predictions

class AdvancedStockPredictor:
    def __init__(self, broker_api):
        self.sectors = {
            'NIFTY50': '^NSEI',
            'BANKNIFTY': '^NSEBANK',
            'FINNIFTY': 'FINNIFTY.NS',
            'IT': ['TCS.NS', 'INFY.NS', 'WIPRO.NS'],
            'BANK': ['HDFCBANK.NS', 'SBIN.NS', 'ICICIBANK.NS'],
            'PHARMA': ['SUNPHARMA.NS', 'DRREDDY.NS', 'CIPLA.NS']
        }
        self.models = self._initialize_models()
        self.scaler = StandardScaler()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.broker_api = broker_api
        self.trade_monitor = TradeMonitor(broker_api)
        self.min_confidence = 0.75
        
    def _initialize_models(self) -> Dict:
        """Initialize different models for different aspects of prediction"""
        return {
            'trend': GradientBoostingRegressor(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=5
            ),
            'volatility': RandomForestClassifier(
                n_estimators=150,
                max_depth=7
            ),
            'option_chain': LSTMModel(
                input_size=10,  # Number of features
                hidden_size=64,
                num_layers=2
            ).to(self.device)
        }

    def _prepare_data_for_lstm(self, data: pd.DataFrame) -> torch.Tensor:
        """Prepare data for LSTM model"""
        features = self._calculate_technical_indicators(data)
        feature_matrix = np.array([list(features[k]) for k in features.keys()]).T
        scaled_features = self.scaler.fit_transform(feature_matrix)
        return torch.FloatTensor(scaled_features).unsqueeze(0).to(self.device)

    async def predict_trades(self, db: Session) -> Dict:
        """Generate trading predictions with comprehensive analysis"""
        try:
            # Get market data
            market_data = await self._gather_market_data()
            
            # Get economic indicators
            economic_data = await self._get_economic_indicators()
            
            # Get news sentiment
            news_sentiment = await self._analyze_market_news()
            
            # Prepare data for LSTM
            predictions = {}
            for sector, data in market_data.items():
                if isinstance(self.sectors[sector], str):
                    lstm_input = self._prepare_data_for_lstm(data['price_data'])
                    with torch.no_grad():
                        lstm_pred = self.models['option_chain'](lstm_input)
                    predictions[sector] = lstm_pred.cpu().numpy()[0][0]
            
            # Generate final predictions
            analysis = await self._combine_analysis(market_data, economic_data, news_sentiment)
            final_predictions = await self._generate_predictions(analysis, predictions)
            
            return {
                "timestamp": datetime.now().isoformat(),
                "market_condition": await self._get_market_condition(analysis),
                "sector_predictions": final_predictions['sectors'],
                "stock_recommendations": final_predictions['stocks'],
                "option_trades": final_predictions['options'],
                "risk_factors": final_predictions['risks']
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise

    async def _gather_market_data(self) -> Dict:
        """Gather comprehensive market data"""
        try:
            market_data = {}
            
            # Get index data
            for index_name, symbol in self.sectors.items():
                if isinstance(symbol, str):
                    data = yf.download(symbol, period="1y", interval="1d")
                    market_data[index_name] = {
                        'price_data': data,
                        'technical_indicators': self._calculate_technical_indicators(data),
                        'volatility': self._calculate_volatility(data),
                        'trend_strength': self._calculate_trend_strength(data)
                    }
            
            # Add options data
            market_data['options_data'] = await self._fetch_options_chain()
            
            return market_data
            
        except Exception as e:
            logger.error(f"Error gathering market data: {e}")
            raise

    def _calculate_technical_indicators(self, data: pd.DataFrame) -> Dict:
        """Calculate comprehensive technical indicators"""
        indicators = {}
        
        # Moving averages
        indicators['SMA_20'] = data['Close'].rolling(window=20).mean()
        indicators['SMA_50'] = data['Close'].rolling(window=50).mean()
        indicators['EMA_13'] = data['Close'].ewm(span=13).mean()
        
        # Momentum indicators
        indicators['RSI'] = self._calculate_rsi(data['Close'])
        indicators['MACD'] = self._calculate_macd(data['Close'])
        
        # Volatility indicators
        indicators['ATR'] = self._calculate_atr(data)
        indicators['BB_upper'], indicators['BB_lower'] = self._calculate_bollinger_bands(data['Close'])
        
        # Volume analysis
        indicators['OBV'] = self._calculate_obv(data)
        indicators['Volume_MA'] = data['Volume'].rolling(window=20).mean()
        
        return indicators

    async def _get_economic_indicators(self) -> Dict:
        """Get economic indicators affecting market"""
        return {
            'interest_rates': await self._fetch_interest_rates(),
            'fx_rates': await self._fetch_fx_rates(),
            'vix': await self._fetch_india_vix(),
            'bond_yields': await self._fetch_bond_yields(),
            'fii_dii_data': await self._fetch_fii_dii_data()
        }

    def _generate_predictions(self, analysis: Dict, lstm_predictions: Dict) -> Dict:
        """Generate comprehensive trading predictions"""
        predictions = {
            'sectors': {},
            'stocks': [],
            'options': [],
            'risks': []
        }
        
        # Analyze each sector
        for sector, data in analysis['market_data'].items():
            if isinstance(self.sectors[sector], str):  # Index
                sector_pred = self._predict_sector_movement(data, analysis)
                predictions['sectors'][sector] = sector_pred
                
                # Generate options trades if conditions are favorable
                if sector_pred['confidence'] > 0.8:
                    options = self._generate_options_strategy(
                        sector,
                        sector_pred['direction'],
                        analysis
                    )
                    predictions['options'].extend(options)
        
        return predictions

    def _generate_options_strategy(self, 
                                 index: str, 
                                 direction: str, 
                                 analysis: Dict) -> List[Dict]:
        """Generate options trading strategies"""
        strategies = []
        current_price = analysis['market_data'][index]['price_data']['Close'][-1]
        
        # Calculate strikes
        atm_strike = round(current_price / 50) * 50
        
        if direction == 'BULLISH':
            strategies.append({
                'index': index,
                'strategy': 'BULL_CALL_SPREAD',
                'buy_strike': atm_strike,
                'sell_strike': atm_strike + 100,
                'expiry': self._get_next_expiry(),
                'confidence': analysis['sectors'][index]['confidence'],
                'risk_reward': self._calculate_risk_reward_ratio(
                    'BULL_CALL_SPREAD',
                    atm_strike,
                    atm_strike + 100,
                    analysis
                )
            })
        else:
            strategies.append({
                'index': index,
                'strategy': 'BEAR_PUT_SPREAD',
                'buy_strike': atm_strike,
                'sell_strike': atm_strike - 100,
                'expiry': self._get_next_expiry(),
                'confidence': analysis['sectors'][index]['confidence'],
                'risk_reward': self._calculate_risk_reward_ratio(
                    'BEAR_PUT_SPREAD',
                    atm_strike,
                    atm_strike - 100,
                    analysis
                )
            })
        
        return strategies

    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def _calculate_macd(self, prices: pd.Series) -> pd.Series:
        """Calculate MACD indicator"""
        exp1 = prices.ewm(span=12, adjust=False).mean()
        exp2 = prices.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        return macd - signal

    def _calculate_atr(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(period).mean()

    def _calculate_bollinger_bands(self, prices: pd.Series, 
                                 period: int = 20, 
                                 std_dev: int = 2) -> Tuple[pd.Series, pd.Series]:
        """Calculate Bollinger Bands"""
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        return upper_band, lower_band

    def _calculate_obv(self, data: pd.DataFrame) -> pd.Series:
        """Calculate On-Balance Volume"""
        obv = pd.Series(index=data.index, dtype='float64')
        obv.iloc[0] = 0
        
        for i in range(1, len(data.index)):
            if data['Close'].iloc[i] > data['Close'].iloc[i-1]:
                obv.iloc[i] = obv.iloc[i-1] + data['Volume'].iloc[i]
            elif data['Close'].iloc[i] < data['Close'].iloc[i-1]:
                obv.iloc[i] = obv.iloc[i-1] - data['Volume'].iloc[i]
            else:
                obv.iloc[i] = obv.iloc[i-1]
        
        return obv

    def _get_next_expiry(self) -> str:
        """Get next expiry date"""
        today = datetime.now()
        days_to_thursday = (3 - today.weekday()) % 7
        next_thursday = today + timedelta(days=days_to_thursday)
        return next_thursday.strftime('%Y-%m-%d')

    async def start_autonomous_trading(self, symbol: str):
        """Start autonomous trading for a symbol"""
        try:
            while True:
                # Get real-time market data
                market_data = await self._get_realtime_data(symbol)
                
                # Generate prediction
                prediction = await self._generate_realtime_prediction(market_data)
                
                if prediction['confidence'] >= self.min_confidence:
                    # Execute trade based on prediction
                    trade_id = await self._execute_options_trade(symbol, prediction)
                    
                    if trade_id:
                        # Start monitoring the trade
                        position = await self.broker_api.get_position(trade_id)
                        asyncio.create_task(
                            self.trade_monitor.monitor_trade(trade_id, position)
                        )
                
                await asyncio.sleep(5)  # Wait before next analysis
                
        except Exception as e:
            logger.error(f"Error in autonomous trading: {e}")
            raise

    async def _generate_realtime_prediction(self, market_data: Dict) -> Dict:
        """Generate real-time trading prediction"""
        try:
            # Prepare features
            features = self._prepare_data_for_lstm(market_data['price_data'])
            
            # Get LSTM prediction
            with torch.no_grad():
                lstm_pred = self.models['option_chain'](features)
            
            # Get technical signals
            technical_signals = self._analyze_technical_indicators(
                market_data['technical']
            )
            
            # Combine signals
            direction = "CALL" if lstm_pred > 0 else "PUT"
            confidence = float(abs(lstm_pred))
            
            return {
                "direction": direction,
                "confidence": confidence,
                "technical_signals": technical_signals,
                "suggested_strike": self._calculate_strike_price(
                    market_data['ltp'],
                    direction
                )
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise

    async def _execute_options_trade(self, symbol: str, prediction: Dict) -> str:
        """Execute options trade based on prediction"""
        try:
            expiry = self._get_next_expiry()
            strike = prediction['suggested_strike']
            option_type = 'CE' if prediction['direction'] == 'CALL' else 'PE'
            
            # Calculate position size based on risk management
            quantity = self._calculate_position_size(
                symbol,
                strike,
                option_type
            )
            
            # Place order
            order = await self.broker_api.place_order(
                symbol=symbol,
                strike=strike,
                option_type=option_type,
                quantity=quantity,
                expiry=expiry,
                order_type='MARKET'
            )
            
            logger.info(f"Executed trade: {order}")
            return order['trade_id']
            
        except Exception as e:
            logger.error(f"Trade execution error: {e}")
            return None

class TradeMonitor:
    def __init__(self, broker_api):
        self.broker_api = broker_api
        self.active_trades = {}
        self.stop_loss_percent = 0.15  # 15% stop loss
        self.target_profit_percent = 0.30  # 30% target profit
        self.trailing_sl_percent = 0.10  # 10% trailing stop loss

    async def monitor_trade(self, trade_id: str, position: Dict):
        """Monitor individual trade"""
        entry_price = position['entry_price']
        quantity = position['quantity']
        trade_type = position['trade_type']  # 'CE' or 'PE'
        
        while True:
            try:
                # Get real-time LTP (Last Traded Price)
                ltp = await self.broker_api.get_ltp(position['symbol'])
                
                # Calculate P&L
                if trade_type == 'CE':
                    pnl = (ltp - entry_price) * quantity
                else:
                    pnl = (entry_price - ltp) * quantity
                
                # Calculate P&L percentage
                pnl_percent = (pnl / (entry_price * quantity)) * 100
                
                # Check stop loss
                if pnl_percent <= -self.stop_loss_percent:
                    await self._exit_trade(trade_id, position, "Stop Loss Hit")
                    break
                
                # Check target profit
                if pnl_percent >= self.target_profit_percent:
                    await self._exit_trade(trade_id, position, "Target Achieved")
                    break
                
                # Update trailing stop loss
                if pnl_percent > 0:
                    new_sl = ltp * (1 - self.trailing_sl_percent)
                    self.active_trades[trade_id]['trailing_sl'] = max(
                        new_sl,
                        self.active_trades[trade_id].get('trailing_sl', 0)
                    )
                
                await asyncio.sleep(1)  # Check every second
                
            except Exception as e:
                logger.error(f"Error monitoring trade {trade_id}: {e}")
                await asyncio.sleep(5)  # Wait before retrying