from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False) # Unique username
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    broker_configs = relationship("BrokerConfig", back_populates="user")
    trading_sessions = relationship("TradingSession", back_populates="user")
    trades = relationship("Trade", back_populates="user")
    orders = relationship("Order", back_populates="user")

    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        """Verify password."""
        return pwd_context.verify(password, self.password_hash)

class BrokerConfig(Base):
    __tablename__ = "broker_configs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    broker_name = Column(String, index=True)
    is_active = Column(Boolean, default=False)
    config = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    status = Column(String, default="disconnected")  
    last_error = Column(String, nullable=True)
    broker_metadata = Column(JSON, nullable=True)  # For broker-specific data

    # Relationships
    user = relationship("User", back_populates="broker_configs")

class TradingSession(Base):
    __tablename__ = "trading_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    symbol = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    started_at = Column(DateTime, default=func.now())
    ended_at = Column(DateTime, nullable=True)
    config = Column(JSON)
    total_pnl = Column(Float, default=0.0)
    broker_name = Column(String)

    # Relationships
    trades = relationship("Trade", back_populates="session")
    user = relationship("User", back_populates="trading_sessions")

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    session_id = Column(Integer, ForeignKey('trading_sessions.id'))
    symbol = Column(String, index=True)
    trade_type = Column(String)  # BUY/SELL
    entry_price = Column(Float)
    exit_price = Column(Float, nullable=True)
    quantity = Column(Integer)
    status = Column(String)  # OPEN/CLOSED
    profit_loss = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now())
    closed_at = Column(DateTime, nullable=True)
    strategy_id = Column(Integer, ForeignKey('strategies.id'))
    stop_loss = Column(Float, nullable=True)
    take_profit = Column(Float, nullable=True)

    # Relationships
    session = relationship("TradingSession", back_populates="trades")
    user = relationship("User", back_populates="trades")
    strategy = relationship("Strategy", back_populates="trades")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    symbol = Column(String, index=True)
    order_type = Column(String)  # LIMIT, MARKET, STOP-LOSS
    price = Column(Float)
    quantity = Column(Integer)
    status = Column(String, default="PENDING")  # PENDING, EXECUTED, CANCELLED
    created_at = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User", back_populates="orders")

class MarketData(Base):
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    timestamp = Column(DateTime, default=func.now())
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)

class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    parameters = Column(JSON)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    trades = relationship("Trade", back_populates="strategy")

class TradeLogs(Base):
    __tablename__ = "trade_logs"

    id = Column(Integer, primary_key=True, index=True)
    trade_id = Column(Integer, ForeignKey('trades.id'))
    log_message = Column(String)
    timestamp = Column(DateTime, default=func.now())

    # Relationships
    trade = relationship("Trade")

class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Links to user
    symbol = Column(String, index=True)  # Stock symbol (e.g., NIFTY, AAPL)
    quantity = Column(Integer)  # Number of shares
    avg_price = Column(Float)  # Average entry price
    status = Column(String, default="OPEN")  # OPEN/CLOSED
    unrealized_pnl = Column(Float, default=0.0)  # Profit/loss before closing
    created_at = Column(DateTime, default=func.now())
  # Relationships
    user = relationship("User")
    def close_position(self, exit_price):
        """Close the position & calculate final P&L"""
        self.status = "CLOSED"
        self.unrealized_pnl = (exit_price - self.avg_price) * self.quantity
