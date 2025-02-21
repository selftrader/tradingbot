from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import enum

Base = declarative_base()

class OrderType(enum.Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    SL = "SL"
    SL_M = "SL-M"

class TradeType(str, enum.Enum):
    BUY = "BUY"
    SELL = "SELL"

class ProductType(str, enum.Enum):
    INTRADAY = "INTRADAY"
    DELIVERY = "DELIVERY"
    OPTIONS = "OPTIONS"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    trades = relationship("Trade", back_populates="user")
    auth_tokens = relationship("AuthToken", back_populates="user")

class AuthToken(Base):
    __tablename__ = "auth_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    broker = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
    expiry = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    config_data = Column(JSONB, nullable=True)

    user = relationship("User", back_populates="auth_tokens")

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    symbol = Column(String, index=True)
    order_type = Column(Enum(OrderType))
    trade_type = Column(String)
    product_type = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
    trigger_price = Column(Float, nullable=True)
    status = Column(String)
    order_id = Column(String, unique=True)
    exchange_order_id = Column(String, nullable=True)
    placed_at = Column(DateTime, default=datetime.utcnow)
    executed_at = Column(DateTime, nullable=True)
    stop_loss = Column(Float, nullable=True)
    target = Column(Float, nullable=True)
    trade_data = Column(JSONB, nullable=True)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="trades")

class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    symbol = Column(String, index=True)
    quantity = Column(Integer)
    average_price = Column(Float)
    current_price = Column(Float)
    pnl = Column(Float)
    product_type = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow)
    entry_price = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class TradingStrategy(Base):
    __tablename__ = "trading_strategies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    parameters = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class OptionsChain(Base):
    __tablename__ = "options_chain"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    expiry = Column(DateTime, index=True)
    strike = Column(Float)
    option_type = Column(String)  # CE or PE
    last_price = Column(Float)
    volume = Column(Integer)
    oi = Column(Integer)
    iv = Column(Float)
    delta = Column(Float)
    theta = Column(Float)
    updated_at = Column(DateTime, default=datetime.utcnow)

class BrokerConfig(Base):
    __tablename__ = "broker_configs"

    id = Column(Integer, primary_key=True, index=True)
    broker_name = Column(String, nullable=False, unique=True)
    api_key = Column(String, nullable=True)
    api_secret = Column(String, nullable=True)
    access_token = Column(String, nullable=True)
    user_id = Column(String, nullable=True)
    is_active = Column(Boolean, server_default='true')
    created_at = Column(DateTime, server_default='now()')
    updated_at = Column(DateTime, server_default='now()')
    config_data = Column(JSONB, nullable=True)