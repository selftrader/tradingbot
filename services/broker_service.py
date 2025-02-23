from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from database.connection import get_db
from datetime import datetime
import logging
from abc import ABC, abstractmethod
from typing import Dict, List
import aiohttp
import pandas as pd

from database.models import BrokerConfig

logger = logging.getLogger(__name__)

class BaseBroker(ABC):
    @abstractmethod
    async def get_tradeable_symbols(self) -> List[Dict]:
        """Get list of tradeable symbols"""
        pass

    @abstractmethod
    async def get_market_data(self, symbol: str) -> Dict:
        """Get market data for a symbol"""
        pass

class BrokerAPI(BaseBroker):
    @abstractmethod
    async def place_order(self, symbol: str, quantity: int, side: str, order_type: str) -> Dict:
        pass
    
    @abstractmethod
    async def get_positions(self) -> List[Dict]:
        pass

    @abstractmethod
    async def get_historical_data(self, symbol: str) -> pd.DataFrame:
        pass
    
    @abstractmethod
    async def close(self):
        pass

class BrokerInterface(ABC):
    @abstractmethod
    async def get_market_data(self, symbol: str):
        """Fetch market data for a symbol"""
        pass

    @abstractmethod
    async def place_order(self, symbol: str, side: str, quantity: int, price: float = None):
        """Place an order"""
        pass

class UpstoxBroker(BrokerAPI):
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = None
        
    async def _ensure_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def get_market_data(self, symbol: str) -> Dict:
        # Implement Upstox-specific market data fetching
        pass
        
    async def place_order(self, symbol: str, quantity: int, side: str, order_type: str) -> Dict:
        # Implement Upstox-specific order placement
        pass
        
    async def get_positions(self) -> List[Dict]:
        # Implement Upstox-specific position fetching
        pass

    async def get_historical_data(self, symbol: str) -> pd.DataFrame:
        """Get historical market data for training"""
        await self._ensure_session()
        try:
            # Implement actual API call to Upstox
            # This is a placeholder implementation
            async with self.session.get(
                f"https://api.upstox.com/v2/historical/{symbol}",
                headers={"X-API-KEY": self.api_key}
            ) as response:
                data = await response.json()
                return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"Error fetching historical data: {e}")
            raise
    
    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()
            self.session = None

class BrokerService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    async def save_broker_configuration(self, config_data: dict):
        """Save or update broker configuration using PostgreSQL upsert"""
        try:
            # Prepare the upsert statement
            stmt = insert(BrokerConfig).values(
                broker_name=config_data['broker_name'],
                api_key=config_data.get('api_key'),
                api_secret=config_data.get('api_secret'),
                access_token=config_data.get('access_token'),
                user_id=config_data.get('user_id'),
                config_data=config_data.get('config_data', {}),
                updated_at=datetime.utcnow()
            )

            # Add PostgreSQL ON CONFLICT clause
            stmt = stmt.on_conflict_do_update(
                constraint='broker_configs_broker_name_key',
                set_={
                    'api_key': stmt.excluded.api_key,
                    'api_secret': stmt.excluded.api_secret,
                    'access_token': stmt.excluded.access_token,
                    'user_id': stmt.excluded.user_id,
                    'config_data': stmt.excluded.config_data,
                    'updated_at': stmt.excluded.updated_at
                }
            )

            result = self.db.execute(stmt)
            self.db.commit()

            # Get the updated/inserted config
            return self.get_broker_config(config_data['broker_name'])

        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to save broker configuration: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save broker configuration: {str(e)}"
            )

    async def get_broker_config(self, broker_name: str):
        """Retrieve broker configuration with PostgreSQL-specific query"""
        try:
            config = self.db.query(BrokerConfig).filter(
                BrokerConfig.broker_name == broker_name,
                BrokerConfig.is_active.is_(True)
            ).first()

            if not config:
                raise HTTPException(
                    status_code=404,
                    detail=f"No configuration found for broker: {broker_name}"
                )

            return config

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to retrieve broker configuration"
            )

    async def connect_broker(self, broker_data: dict):
        try:
            broker = BrokerConfig(
                broker_name=broker_data['broker_name'],
                api_key=broker_data['api_key'],
                api_secret=broker_data['api_secret'],
                user_id=broker_data['user_id']
            )
            self.db.add(broker)
            self.db.commit()
            self.db.refresh(broker)
            return broker
        except Exception as e:
            logger.error(f"Failed to connect broker: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))