from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =======================
# User & Authentication
# =======================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="trader")  # Options: Admin, Trader, Analyst
    isVerified = Column(Boolean, default=False)
    country_code = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    failed_login_attempts = Column(Integer, default=0)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    accounts = relationship("Account", back_populates="user", cascade="all, delete")
    broker_configs = relationship("BrokerConfig", back_populates="user", cascade="all, delete")
    trading_sessions = relationship("TradingSession", back_populates="user", cascade="all, delete")
    trades = relationship("Trade", back_populates="user", cascade="all, delete")
    orders = relationship("Order", back_populates="user", cascade="all, delete")
    ai_models = relationship("AIModel", back_populates="user", cascade="all, delete")
    strategies = relationship("Strategy", back_populates="user", cascade="all, delete")
    trading_performance = relationship("TradingPerformance", back_populates="user", cascade="all, delete")
    trading_reports = relationship("TradingReport", back_populates="user", cascade="all, delete")

    # Password Management
    def set_password(self, password):
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


# =======================
# Broker & Configuration
# =======================
class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    broker_name = Column(String, nullable=False)
    account_number = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="accounts")
    trades = relationship("Trade", back_populates="account", cascade="all, delete")
    orders = relationship("Order", back_populates="account", cascade="all, delete")


class BrokerConfig(Base):
    __tablename__ = "broker_configs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    broker_name = Column(String, index=True)
    api_key = Column(String, nullable=False)
    api_secret = Column(String, nullable=False)
    additional_params = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=False)
    config = Column(JSON)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User", back_populates="broker_configs")


# =======================
# AI Model & Prediction Logs
# =======================
class AIModel(Base):
    __tablename__ = "ai_models"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    model_name = Column(String, nullable=False)
    model_version = Column(String, nullable=False)
    model_type = Column(String, nullable=True)  # e.g., Regression, Classification, RL
    parameters = Column(JSON)
    accuracy = Column(Float, nullable=True)
    training_data_size = Column(Integer, nullable=True)
    last_trained_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User", back_populates="ai_models")
    predictions = relationship("AIPredictionLog", back_populates="ai_model", cascade="all, delete")
    strategies = relationship("Strategy", back_populates="ai_model")


class AIPredictionLog(Base):
    __tablename__ = "ai_prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("ai_models.id", ondelete="CASCADE"), index=True)
    symbol = Column(String, nullable=False)
    predicted_price = Column(Float, nullable=False)
    actual_price = Column(Float, nullable=True)
    prediction_time = Column(DateTime, default=func.now())
    accuracy = Column(Float, nullable=True)

    # Relationships
    ai_model = relationship("AIModel", back_populates="predictions")


# =======================
# Strategies
# =======================
class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    ai_model_id = Column(Integer, ForeignKey("ai_models.id", ondelete="SET NULL"), index=True)
    parameters = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User", back_populates="strategies")
    ai_model = relationship("AIModel", back_populates="strategies")
    trades = relationship("Trade", back_populates="strategy", cascade="all, delete")
    backtests = relationship("Backtest", back_populates="strategy", cascade="all, delete")
    paper_trades = relationship("PaperTrade", back_populates="strategy", cascade="all, delete")


# =======================
# Trading Sessions
# =======================
class TradingSession(Base):
    __tablename__ = "trading_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    ai_model_id = Column(Integer, ForeignKey("ai_models.id", ondelete="SET NULL"), index=True)
    start_time = Column(DateTime, default=func.now())
    end_time = Column(DateTime, nullable=True)
    total_pnl = Column(Float, default=0.0)

    # Relationships
    user = relationship("User", back_populates="trading_sessions")
    ai_model = relationship("AIModel")
    trades = relationship("Trade", back_populates="session", cascade="all, delete")
    trading_performance = relationship("TradingPerformance", back_populates="session", cascade="all, delete")
    trading_reports = relationship("TradingReport", back_populates="session", cascade="all, delete")


# =======================
# Trades
# =======================
class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    session_id = Column(Integer, ForeignKey("trading_sessions.id", ondelete="CASCADE"), index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id", ondelete="CASCADE"), index=True)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), index=True)
    symbol = Column(String, nullable=False)
    trade_type = Column(String, nullable=False)  # BUY/SELL
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=False)
    stop_loss = Column(Float, nullable=True)
    take_profit = Column(Float, nullable=True)
    status = Column(String, default="OPEN", nullable=False)  # OPEN, FILLED, CANCELED
    profit_loss = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User", back_populates="trades")
    session = relationship("TradingSession", back_populates="trades")
    account = relationship("Account", back_populates="trades")
    strategy = relationship("Strategy", back_populates="trades")


# =======================
# Orders
# =======================
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), index=True)
    symbol = Column(String, nullable=False)
    order_type = Column(String, nullable=False)  # LIMIT, MARKET, STOP-LOSS
    price = Column(Float)
    quantity = Column(Integer)
    status = Column(String, default="PENDING")  # PENDING, FILLED, CANCELED
    created_at = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User", back_populates="orders")
    account = relationship("Account", back_populates="orders")


# =======================
# Backtesting
# =======================
class Backtest(Base):
    __tablename__ = "backtests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id", ondelete="CASCADE"), index=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    total_pnl = Column(Float, nullable=False)
    accuracy = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User")
    strategy = relationship("Strategy", back_populates="backtests")


# =======================
# Paper Trading
# =======================
class PaperTrade(Base):
    __tablename__ = "paper_trades"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id", ondelete="CASCADE"), index=True)
    symbol = Column(String, nullable=False)
    trade_type = Column(String, nullable=False)  # BUY/SELL
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=False)
    status = Column(String, default="OPEN", nullable=False)
    profit_loss = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User")
    strategy = relationship("Strategy", back_populates="paper_trades")


# =======================
# Trading Performance
# =======================
class TradingPerformance(Base):
    __tablename__ = "trading_performance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    session_id = Column(Integer, ForeignKey("trading_sessions.id", ondelete="CASCADE"), index=True)
    total_trades = Column(Integer, nullable=False)
    win_rate = Column(Float, nullable=False)
    total_profit_loss = Column(Float, nullable=False)
    max_drawdown = Column(Float, nullable=True)
    risk_reward_ratio = Column(Float, nullable=True)
    profit_factor = Column(Float, nullable=True)
    sharpe_ratio = Column(Float, nullable=True)
    performance_type = Column(String, nullable=False)  # LIVE, PAPER, BACKTEST
    generated_at = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User", back_populates="trading_performance")
    session = relationship("TradingSession")


# =======================
# Trading Reports
# =======================
class TradingReport(Base):
    __tablename__ = "trading_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    session_id = Column(Integer, ForeignKey("trading_sessions.id", ondelete="CASCADE"), index=True)
    total_trades = Column(Integer, nullable=False)
    total_profit = Column(Float, nullable=False)
    win_rate = Column(Float, nullable=False)
    report_type = Column(String, nullable=False)  # LIVE, PAPER, BACKTEST
    generated_at = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User", back_populates="trading_reports")
    session = relationship("TradingSession")


# =======================
# Stocks
# =======================
class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), unique=True, nullable=False)  # Symbol used for all instruments
    name = Column(String(100), nullable=False)
    exchange = Column(String(10), nullable=False, default="NSE")  # Default to NSE

    # Relationships (if needed)
    stock_trades = relationship("StockTrade", back_populates="stock")



# =======================
# Stock Trading History
# =======================
class StockTrade(Base):
    __tablename__ = "stock_trades"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete="CASCADE"), index=True)
    trade_id = Column(Integer, ForeignKey("trades.id", ondelete="CASCADE"), index=True, nullable=True)
    symbol = Column(String, nullable=False)
    exchange = Column(String, nullable=False)
    trade_date = Column(DateTime, default=func.now())
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=False)
    profit_loss = Column(Float, nullable=True)
    status = Column(String, default="OPEN")

    # Relationships
    user = relationship("User")
    stock = relationship("Stock", back_populates="stock_trades")


class OTP(Base):
    __tablename__ = "otp_codes"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, nullable=False)
    otp_code = Column(String, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False, default=func.now())  # ✅ Ensure timezone-aware datetime
