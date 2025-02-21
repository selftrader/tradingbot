from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    trade_type = Column(String)  # BUY/SELL
    entry_price = Column(Float)
    exit_price = Column(Float, nullable=True)
    quantity = Column(Integer)
    status = Column(String)  # OPEN/CLOSED
    profit_loss = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now())
    closed_at = Column(DateTime, nullable=True)
    strategy = Column(String)
    confidence = Column(Float)
    session_id = Column(Integer, ForeignKey('trading_sessions.id'))
    stop_loss = Column(Float, nullable=True)
    take_profit = Column(Float, nullable=True)
    
    # Relationship
    session = relationship("TradingSession", back_populates="trades")

class TradingSession(Base):
    __tablename__ = "trading_sessions"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    started_at = Column(DateTime, default=func.now())
    ended_at = Column(DateTime, nullable=True)
    config = Column(JSON)
    total_pnl = Column(Float, default=0.0)
    broker_name = Column(String)
    
    # Relationship
    trades = relationship("Trade", back_populates="session")

class BrokerConfig(Base):
    __tablename__ = "broker_configs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    broker_name = Column(String, index=True)
    is_active = Column(Boolean, default=False)
    config = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    status = Column(String, default="disconnected")  
    last_error = Column(String, nullable=True)
    metadata = Column(JSON, nullable=True)  # For broker-specific data

    # Relationship to User
    user = relationship("User", back_populates="broker_configs")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

    # Relationship: one-to-many with broker_configs
    broker_configs = relationship("BrokerConfig", back_populates="user")
