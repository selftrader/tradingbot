import logging

logging.basicConfig(filename="logs/bot.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def log_trade(symbol, trade_type, price):
    logging.info(f"Executed {trade_type} order for {symbol} at {price}")
