import asyncio
from datetime import datetime
import numpy as np
from typing import Dict, List
import logging

import torch
from models.lstm_price_predictor import LSTMPricePredictor

logger = logging.getLogger(__name__)

class TradeMonitor:
    def __init__(self, broker_api, risk_manager):
        self.broker_api = broker_api
        self.risk_manager = risk_manager
        self.predictor = LSTMPricePredictor()
        self.active_trades = {}
        self.price_history = {}
        self.window_size = 30  # 30-minute window

    async def start_monitoring(self, symbol: str, trade_id: str, position: Dict):
        """Start monitoring a trade"""
        try:
            self.active_trades[trade_id] = position
            self.price_history[symbol] = []

            while trade_id in self.active_trades:
                # Get real-time market data
                market_data = await self._get_market_data(symbol)
                self.price_history[symbol].append(market_data)

                # Keep only recent history
                if len(self.price_history[symbol]) > self.window_size:
                    self.price_history[symbol].pop(0)

                # Generate prediction if enough data
                if len(self.price_history[symbol]) >= self.window_size:
                    prediction = await self._predict_price_movement(symbol)
                    await self._update_trade_strategy(trade_id, prediction)

                # Check trade status
                await self._check_trade_status(trade_id)
                
                await asyncio.sleep(60)  # Check every minute

        except Exception as e:
            logger.error(f"Error monitoring trade {trade_id}: {e}")
            await self._emergency_exit(trade_id)

    async def _predict_price_movement(self, symbol: str) -> Dict:
        """Generate price movement prediction"""
        try:
            # Prepare data
            data = np.array(self.price_history[symbol])
            features = self._prepare_features(data)
            
            # Get prediction
            with torch.no_grad():
                direction, confidence = self.predictor(features)
                
            return {
                "direction": int(direction.item()),
                "confidence": float(confidence.item()),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Prediction error for {symbol}: {e}")
            return {"direction": 0, "confidence": 0}

    async def _update_trade_strategy(self, trade_id: str, prediction: Dict):
        """Update trade strategy based on prediction"""
        position = self.active_trades[trade_id]
        
        # Calculate current P&L
        current_pnl = await self._calculate_pnl(trade_id)
        
        # Update stop loss based on prediction
        if prediction['confidence'] > 0.8:
            if prediction['direction'] != position['direction']:
                # Strong reversal predicted
                await self._exit_trade(trade_id, "Strong reversal signal")
            else:
                # Strong continuation predicted
                await self._update_trailing_sl(trade_id, current_pnl)

    async def _calculate_pnl(self, trade_id: str) -> float:
        """Calculate current P&L for a trade"""
        position = self.active_trades[trade_id]
        current_price = await self.broker_api.get_ltp(position['symbol'])
        
        entry_price = position['entry_price']
        quantity = position['quantity']
        
        if position['direction'] == 1:  # Long position
            return (current_price - entry_price) * quantity
        else:  # Short position
            return (entry_price - current_price) * quantity

    async def _check_trade_status(self, trade_id: str):
        """Check and update trade status"""
        position = self.active_trades[trade_id]
        current_pnl = await self._calculate_pnl(trade_id)
        
        # Check stop loss
        if current_pnl <= -position['max_loss']:
            await self._exit_trade(trade_id, "Stop loss hit")
            return
            
        # Check target
        if current_pnl >= position['target']:
            await self._exit_trade(trade_id, "Target achieved")
            return

    async def _exit_trade(self, trade_id: str, reason: str):
        """Exit a trade"""
        try:
            position = self.active_trades[trade_id]
            await self.broker_api.place_order(
                symbol=position['symbol'],
                quantity=position['quantity'],
                order_type='MARKET',
                transaction_type='SELL' if position['direction'] == 1 else 'BUY'
            )
            
            logger.info(f"Exited trade {trade_id}: {reason}")
            del self.active_trades[trade_id]
            
        except Exception as e:
            logger.error(f"Error exiting trade {trade_id}: {e}")