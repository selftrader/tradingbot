from typing import Dict, Optional
import logging
from datetime import datetime, timedelta
from models.database_models import Trade, Position
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class OptionsTradingService:
    def __init__(self, broker, config: Dict):
        self.broker = broker
        self.config = config
        self.lot_size = config['LOT_SIZE']
        self.max_lots = config['MAX_LOTS']

    async def get_options_symbol(self, index_price: float) -> str:
        """Generate options symbol based on current market price"""
        try:
            # Calculate ATM strike
            strike = round(index_price / 50) * 50  # For NIFTY
            if self.config['INDEX'] == 'BANKNIFTY':
                strike = round(index_price / 100) * 100

            # Apply strike offset
            strike += self.config['STRIKE_OFFSET']

            # Get next expiry
            expiry = await self._get_next_expiry()

            # Format symbol
            symbol = (f"{self.config['INDEX']}{expiry}"
                     f"{strike}{self.config['OPTION_TYPE']}")
            
            return symbol

        except Exception as e:
            logger.error(f"Error generating options symbol: {e}")
            raise

    async def execute_options_trade(self, signal: Dict, db: Session) -> Dict:
        """Execute options trade based on signal"""
        try:
            # Get index price
            index_price = await self.broker.get_live_quote(self.config['INDEX'])
            
            # Generate options symbol
            options_symbol = await self.get_options_symbol(index_price['price'])
            
            # Get options quote
            quote = await self.broker.get_live_quote(options_symbol)
            
            if signal['action'] == 'BUY' and signal['confidence'] > 0.7:
                return await self._place_options_trade(
                    options_symbol, 
                    'BUY',
                    quote['price'],
                    db
                )
                
            elif signal['action'] == 'SELL' and signal['confidence'] > 0.7:
                return await self._place_options_trade(
                    options_symbol,
                    'SELL',
                    quote['price'],
                    db
                )

        except Exception as e:
            logger.error(f"Options trade execution error: {e}")
            raise

    async def _place_options_trade(self, symbol: str, action: str, 
                                 price: float, db: Session) -> Dict:
        """Place options trade"""
        try:
            quantity = self.lot_size * self.max_lots
            
            # Place order
            order = await self.broker.place_order(
                symbol=symbol,
                quantity=quantity,
                order_type=action,
                price=price
            )

            # Record trade
            trade = Trade(
                symbol=symbol,
                quantity=quantity,
                trade_type=action,
                entry_price=price,
                status='OPEN',
                product_type='OPTIONS',
                metadata={
                    'lot_size': self.lot_size,
                    'lots': self.max_lots,
                    'expiry': await self._get_next_expiry(),
                    'strike': self._extract_strike(symbol),
                    'option_type': self.config['OPTION_TYPE']
                }
            )
            
            db.add(trade)
            db.commit()

            return {
                "status": "SUCCESS",
                "order_id": order['order_id'],
                "trade_id": trade.id,
                "symbol": symbol,
                "action": action,
                "quantity": quantity,
                "price": price
            }

        except Exception as e:
            db.rollback()
            logger.error(f"Error placing options trade: {e}")
            raise

    async def _get_next_expiry(self) -> str:
        """Get next expiry date based on configuration"""
        today = datetime.now()
        
        if self.config['EXPIRY_SELECTION'] == 'WEEKLY':
            # Find next Thursday
            days_ahead = 3 - today.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            next_expiry = today + timedelta(days=days_ahead)
        else:
            # Monthly expiry - last Thursday
            next_month = today.replace(day=28) + timedelta(days=4)
            last_day = next_month - timedelta(days=next_month.day)
            days_ahead = 3 - last_day.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            next_expiry = last_day + timedelta(days=days_ahead)

        return next_expiry.strftime('%d%b%Y').upper()