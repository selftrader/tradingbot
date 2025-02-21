import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List, Tuple
import pandas as pd
from datetime import datetime
import logging
from fastapi import WebSocket
import asyncio

logger = logging.getLogger(__name__)

class AITradingModel(nn.Module):
    def __init__(self):
        super(AITradingModel, self).__init__()
        
        # Price prediction LSTM
        self.lstm = nn.LSTM(
            input_size=10,  # Technical indicators + price data
            hidden_size=64,
            num_layers=2,
            batch_first=True,
            dropout=0.2
        )
        
        # Market state encoder
        self.market_encoder = nn.Sequential(
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.2)
        )
        
        # Decision maker (Actor network)
        self.actor = nn.Sequential(
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 3)  # BUY, SELL, HOLD
        )
        
        # Value predictor (Critic network)
        self.critic = nn.Sequential(
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )

    def forward(self, market_data: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        # Process market data through LSTM
        lstm_out, _ = self.lstm(market_data)
        last_hidden = lstm_out[:, -1, :]
        
        # Encode market state
        market_state = self.market_encoder(last_hidden)
        
        # Get action probabilities and value
        action_probs = torch.softmax(self.actor(market_state), dim=1)
        value = self.critic(market_state)
        
        return action_probs, value

class AutonomousTrader:
    def __init__(self, broker_api):
        self.model = AITradingModel()
        self.broker_api = broker_api
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        self.active_trades = {}
        self.websocket_clients = set()
        
        # Load pre-trained model if available
        self._load_model()

    def _load_model(self):
        try:
            model_path = 'models/saved/ai_trader.pth'
            self.model.load_state_dict(torch.load(model_path))
            logger.info("Loaded pre-trained AI model")
        except:
            logger.warning("No pre-trained model found. Starting fresh.")

    async def analyze_market(self, symbol: str) -> Dict:
        """Real-time market analysis"""
        try:
            # Get market data
            market_data = await self._get_market_features(symbol)
            
            # Convert to tensor
            market_tensor = torch.FloatTensor(market_data).unsqueeze(0).to(self.device)
            
            # Get model predictions
            with torch.no_grad():
                action_probs, value = self.model(market_tensor)
            
            # Get action with highest probability
            action_idx = torch.argmax(action_probs).item()
            confidence = action_probs[0][action_idx].item()
            
            actions = ['BUY', 'SELL', 'HOLD']
            return {
                'action': actions[action_idx],
                'confidence': confidence,
                'value': value.item(),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Market analysis error: {e}")
            raise

    async def execute_trade(self, symbol: str, analysis: Dict) -> Dict:
        """Execute trade based on AI analysis"""
        try:
            if analysis['confidence'] < 0.7:  # Minimum confidence threshold
                return {'status': 'SKIPPED', 'reason': 'Low confidence'}

            if analysis['action'] == 'HOLD':
                return {'status': 'HOLD'}

            # Calculate position size
            quantity = self._calculate_position_size(symbol, analysis)

            # Execute order
            order = await self.broker_api.place_order(
                symbol=symbol,
                quantity=quantity,
                side=analysis['action'],
                order_type='MARKET'
            )

            return {
                'status': 'EXECUTED',
                'order_id': order['order_id'],
                'action': analysis['action'],
                'quantity': quantity,
                'confidence': analysis['confidence']
            }

        except Exception as e:
            logger.error(f"Trade execution error: {e}")
            raise

    async def _get_market_features(self, symbol: str) -> np.ndarray:
        """Get real-time market features"""
        try:
            # Get market data from broker
            ohlcv = await self.broker_api.get_market_data(symbol)
            df = pd.DataFrame(ohlcv)

            # Calculate technical indicators
            features = []
            
            # Price features
            features.append(df['close'].pct_change().values)
            features.append(df['volume'].pct_change().values)
            
            # Technical indicators
            features.append(self._calculate_rsi(df['close']))
            features.append(self._calculate_macd(df['close']))
            features.append(self._calculate_bollinger_bands(df['close']))
            
            # Market depth features
            depth = await self.broker_api.get_market_depth(symbol)
            features.append(self._process_market_depth(depth))
            
            # Options chain features (if available)
            try:
                options = await self.broker_api.get_option_chain(symbol)
                features.append(self._process_options_data(options))
            except:
                features.append(np.zeros(10))  # Placeholder if no options data

            return np.column_stack(features)[-100:]  # Last 100 data points

        except Exception as e:
            logger.error(f"Error getting market features: {e}")
            raise

    def _calculate_position_size(self, symbol: str, analysis: Dict) -> int:
        """Calculate position size based on confidence and risk"""
        base_quantity = 1
        if analysis['confidence'] > 0.9:
            return base_quantity * 2
        return base_quantity

    # Add technical indicator calculations here
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> np.ndarray:
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs)).values

    def _calculate_macd(self, prices: pd.Series) -> np.ndarray:
        """Calculate MACD indicator"""
        exp1 = prices.ewm(span=12, adjust=False).mean()
        exp2 = prices.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        return (macd - signal).values

    async def start_trading(self, symbol: str):
        """Start autonomous trading for a symbol"""
        try:
            while True:
                # Get real-time market data
                market_data = await self.broker_api.get_market_data(symbol)
                
                # Generate prediction
                prediction = await self.analyze_market(symbol)
                
                if prediction['confidence'] > 0.7:
                    # Execute trade
                    trade = await self.execute_trade(symbol, prediction)
                    
                    # Broadcast update to all connected clients
                    await self._broadcast_update({
                        'type': 'trade_executed',
                        'symbol': symbol,
                        'trade': trade
                    })
                
                # Monitor existing positions
                await self._monitor_positions()
                
                await asyncio.sleep(1)  # Check every second
                
        except Exception as e:
            logger.error(f"Trading error: {e}")
            await self._broadcast_update({
                'type': 'error',
                'message': str(e)
            })

    async def register_client(self, websocket: WebSocket):
        """Register a new WebSocket client"""
        await websocket.accept()
        self.websocket_clients.add(websocket)

    async def unregister_client(self, websocket: WebSocket):
        """Unregister a WebSocket client"""
        self.websocket_clients.remove(websocket)

    async def _broadcast_update(self, data: dict):
        """Broadcast update to all connected clients"""
        dead_clients = set()
        for client in self.websocket_clients:
            try:
                await client.send_json(data)
            except:
                dead_clients.add(client)
        
        # Remove dead clients
        self.websocket_clients -= dead_clients 