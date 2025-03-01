from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ✅ User Table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    accounts = relationship("Account", back_populates="user")
    broker_configs = relationship("BrokerConfig", back_populates="user")
    trading_sessions = relationship("TradingSession", back_populates="user")
    trades = relationship("Trade", back_populates="user")
    orders = relationship("Order", back_populates="user")
    ai_models = relationship("AIModel", back_populates="user")
    strategies = relationship("Strategy", back_populates="user")

    def set_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


# ✅ Demat Account Table
class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    broker_name = Column(String, nullable=False)
    account_number = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User", back_populates="accounts")
    trades = relationship("Trade", back_populates="account")
    orders = relationship("Order", back_populates="account")


# ✅ AI Model Table
class AIModel(Base):
    __tablename__ = "ai_models"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    model_name = Column(String, nullable=False)
    model_version = Column(String, nullable=False)
    parameters = Column(JSON)
    accuracy = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User", back_populates="ai_models")
    predictions = relationship("AIPredictionLog", back_populates="ai_model")
    strategies = relationship("Strategy", back_populates="ai_model")


# ✅ AI Prediction Logs Table
class AIPredictionLog(Base):
    __tablename__ = "ai_prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("ai_models.id"))
    symbol = Column(String, nullable=False)
    predicted_price = Column(Float, nullable=False)
    actual_price = Column(Float, nullable=True)
    prediction_time = Column(DateTime, default=func.now())
    accuracy = Column(Float, nullable=True)

    # Relationships
    ai_model = relationship("AIModel", back_populates="predictions")


# ✅ Trading Session Table
class TradingSession(Base):
    __tablename__ = "trading_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ai_model_id = Column(Integer, ForeignKey("ai_models.id"))
    start_time = Column(DateTime, default=func.now())
    end_time = Column(DateTime, nullable=True)
    total_pnl = Column(Float, default=0.0)

    # Relationships
    trades = relationship("Trade", back_populates="session")
    user = relationship("User", back_populates="trading_sessions")
    ai_model = relationship("AIModel")


# ✅ Trade Table
class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_id = Column(Integer, ForeignKey("trading_sessions.id"))
    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    account_id = Column(Integer, ForeignKey("accounts.id"))
    symbol = Column(String, nullable=False)
    trade_type = Column(String)  # BUY/SELL
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=False)
    status = Column(String)  # OPEN/CLOSED
    profit_loss = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User", back_populates="trades")
    session = relationship("TradingSession", back_populates="trades")
    account = relationship("Account", back_populates="trades")
    strategy = relationship("Strategy", back_populates="trades") 


# ✅ Order Table
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    account_id = Column(Integer, ForeignKey("accounts.id"))
    symbol = Column(String, nullable=False)
    order_type = Column(String)  # LIMIT, MARKET, STOP-LOSS
    price = Column(Float)
    quantity = Column(Integer)
    status = Column(String, default="PENDING")
    created_at = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User", back_populates="orders")
    account = relationship("Account", back_populates="orders")


# ✅ Backtesting Table
class Backtest(Base):
    __tablename__ = "backtests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ai_model_id = Column(Integer, ForeignKey("ai_models.id"))
    symbol = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    total_pnl = Column(Float, nullable=False)
    accuracy = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User")
    ai_model = relationship("AIModel")


# ✅ Paper Trading Table
class PaperTrade(Base):
    __tablename__ = "paper_trades"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ai_model_id = Column(Integer, ForeignKey("ai_models.id"))
    symbol = Column(String, nullable=False)
    trade_type = Column(String)  # BUY/SELL
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=False)
    status = Column(String)  # OPEN/CLOSED
    profit_loss = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User")
    ai_model = relationship("AIModel")


# ✅ AI Performance Monitoring Table
class AIPerformance(Base):
    __tablename__ = "ai_performance"

    id = Column(Integer, primary_key=True, index=True)
    ai_model_id = Column(Integer, ForeignKey("ai_models.id"))
    total_trades = Column(Integer, nullable=False)
    successful_trades = Column(Integer, nullable=False)
    accuracy = Column(Float, nullable=False)
    total_profit = Column(Float, nullable=False)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    ai_model = relationship("AIModel")


class BrokerConfig(Base):
    __tablename__ = "broker_configs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    broker_name = Column(String, index=True)
    is_active = Column(Boolean, default=False)
    config = Column(JSON)
    created_at = Column(DateTime, default=func.now())

    # Relationship
    user = relationship("User", back_populates="broker_configs")
  

class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, unique=True, nullable=False)  # Strategy Name
    description = Column(String, nullable=True)  # Short description
    ai_model_id = Column(Integer, ForeignKey("ai_models.id"))  # Link to AI model
    parameters = Column(JSON, nullable=True)  # Store strategy parameters as JSON
    created_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)  # Active or not

    # Relationships
    user = relationship("User", back_populates="strategies")
    ai_model = relationship("AIModel", back_populates="strategies")
    trades = relationship("Trade", back_populates="strategy")  # ✅ ADD THIS