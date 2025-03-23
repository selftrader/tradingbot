import numpy as np
from requests import Session
from services.dhan_client import get_dhan_client
from services.market_data_service import fetch_live_stock_price
from services.telegram_alerts import send_telegram_message
from services.notifications import send_trade_email, send_trade_sms
from services.ai_model import train_lstm_model, predict_future_prices
from services.trade_size import calculate_trade_size


def execute_ai_trade(user_id: int, symbol: str, db: Session):
    """Execute AI-driven trades and send Telegram alerts."""
    
    # Train AI Model
    model, scaler = train_lstm_model(user_id, symbol, db)
    
    # Predict price movement
    recent_data = np.array([fetch_live_stock_price(user_id, symbol, db)["livePrice"]])
    predicted_price = predict_future_prices(model, scaler, recent_data)
    
    # Decide Trade Action
    live_price = recent_data[0]
    trade_type = "BUY" if predicted_price > live_price else "SELL"

    client = get_dhan_client(user_id, db)
    order_response = client.place_order(
        symbol=symbol,
        exchange="NSE",
        transactionType=trade_type,
        quantity=1,
        orderType="MARKET",
        productType="INTRADAY"
    )

    # Send Telegram Alert
    message = f"Trade Executed: {trade_type} {symbol} at ₹{live_price}"
    send_telegram_message(message)

    return {"status": f"{trade_type} order placed", "order_id": order_response["orderId"]}




def execute_trade_with_alerts(user_id: int, symbol: str, trade_type: str, db: Session):
    """Execute a trade and send alerts via Email & SMS."""
    
    # Execute trade
    trade_details = execute_ai_trade(user_id, symbol, db)
    
    # Send Alerts
    message = f"Trade Executed: {trade_type} {symbol}"
    send_trade_email("Trade Alert", message, "user@example.com")
    send_trade_sms(message, "+919876543210")

    return trade_details



def execute_trade_with_sizing(user_id: int, symbol: str, trade_type: str, db: Session):
    """Execute a trade with AI-calculated position size."""
    
    trade_size_data = calculate_trade_size(user_id, symbol, db)
    trade_size = trade_size_data["trade_size"]

    client = get_dhan_client(user_id, db)
    order_response = client.place_order(
        symbol=symbol,
        exchange="NSE",
        transactionType=trade_type,
        quantity=trade_size,
        orderType="MARKET",
        productType="INTRADAY"
    )

    return {"status": f"{trade_type} order placed with {trade_size} quantity", "order_id": order_response["orderId"]}
