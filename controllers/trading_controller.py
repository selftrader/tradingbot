# controllers/trading_controller.py

import logging
from upstox_api.api import OHLCInterval
from config import get_config, get_options_config
from services.trading_service import TradingService
from services.options_trading_service import OptionsTradingService
from brokers.base_broker import BaseBroker
from brokers.upstox_broker import UpstoxBroker
from brokers.zerodha_broker import ZerodhaBroker
from typing import Dict
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class TradingController:
    """
    Orchestrates the trading workflow.
    """
    def __init__(self):
        self.config = get_config()
        self.broker = self._initialize_broker()

    async def _initialize_broker(self):
        """Initialize and authenticate broker"""
        try:
            broker = UpstoxBroker(
                api_key=self.config["UPSTOX_API_KEY"],
                api_secret=self.config["UPSTOX_API_SECRET"],
                redirect_uri=self.config["UPSTOX_REDIRECT_URI"]
            )

            if not broker.is_authenticated:
                auth_result = await broker.authenticate()
                if not auth_result:
                    raise Exception("Broker authentication failed")
                
            return broker
            
        except Exception as e:
            logger.error(f"Broker initialization error: {e}")
            raise

    async def connect_broker(self) -> bool:
        """Connect to the configured broker"""
        try:
            success = await self.broker.connect()
            if success:
                logger.info(f"Successfully connected to {self.config['BROKER_NAME']}")
            return success
        except Exception as e:
            logger.error(f"Broker connection error: {e}")
            return False

    async def execute(self):
        """Execute trading operations"""
        if not await self.connect_broker():
            raise ConnectionError("Failed to connect to broker")

        symbol = self.config["SYMBOL"]
        try:
            quote = await self.broker.get_live_quote(symbol)
            result = await self.service.execute_strategy(symbol, quote)
            logger.info(f"Trading operation executed: {result}")
            return result
        except Exception as e:
            logger.error(f"Trading execution error: {e}")
            raise

    async def execute_options_trade(self, db: Session):
        """Execute options trading strategy"""
        try:
            # Connect to broker
            if not await self.connect_broker():
                raise ConnectionError("Failed to connect to broker")

            # Get market analysis
            analysis = await self.strategy_service.analyze_index(
                self.options_config['INDEX']
            )

            # Execute options trade
            if analysis['signal']:
                result = await self.options_service.execute_options_trade(
                    analysis,
                    db
                )
                logger.info(f"Options trade executed: {result}")
                return result

        except Exception as e:
            logger.error(f"Options trading error: {e}")
            raise

    async def execute_trade(self, symbol: str, action: str):
        """Execute trade with token validation"""
        try:
            if not await self.broker.validate_token():
                await self.broker.authenticate()
            
            # Continue with trade execution
            # ...existing code...
            
        except Exception as e:
            logger.error(f"Trade execution error: {e}")
            raise
