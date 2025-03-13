import sys
import os
import pandas as pd
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.connection import SessionLocal
from database.models import Stock
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get NSE & BSE file paths from `.env`
NSE_FILE_PATH = os.getenv("NSE_FILE_PATH", "data/EQUITY_L.csv")
BSE_FILE_PATH = os.getenv("BSE_FILE_PATH", "data/Equity.csv")

# Feature Flag to Control Stock Updates
SHOULD_UPDATE_STOCKS = os.getenv("SHOULD_UPDATE_STOCKS", "false").lower() == "true"

def store_stock_data(exchange: str, file_path: str):
    """Reads stock data from CSV and stores it in PostgreSQL, avoiding duplicates."""
    if not SHOULD_UPDATE_STOCKS:
        logging.info(f"Skipping stock update for {exchange} (Flag disabled)")
        return

    if not os.path.exists(file_path):
        logging.warning(f"File not found: {file_path}")
        return

    db = SessionLocal()
    try:
        df = pd.read_csv(file_path)

        # Standardizing column names for NSE
        if exchange == "NSE":
            df.rename(columns={
                "SYMBOL": "symbol",
                "NAME OF COMPANY": "name",
                " ISIN NUMBER": "isin",
                " DATE OF LISTING": "date_of_listing"
            }, inplace=True)

        # Standardizing column names for BSE
        elif exchange == "BSE":
            df.rename(columns={
                "Security Id": "symbol",
                "Issuer Name": "name",
                "ISIN No": "isin",
                "Industry": "industry",
                "Sector Name": "sector"
            }, inplace=True)

        for _, row in df.iterrows():
            existing_stock = db.query(Stock).filter(Stock.symbol == row["symbol"]).first()
            if existing_stock:
                # If the stock is already present, update the exchange field
                if exchange not in existing_stock.exchange.split(", "):
                    existing_stock.exchange += f", {exchange}"
                existing_stock.name = row["name"]
                existing_stock.industry = row.get("industry")
                existing_stock.sector = row.get("sector")
                existing_stock.date_of_listing = row.get("date_of_listing")
            else:
                # Insert new stock data
                new_stock = Stock(
                    symbol=row["symbol"],
                    name=row["name"],
                    exchange=exchange,
                    isin=row["isin"],
                    industry=row.get("industry"),
                    sector=row.get("sector"),
                    date_of_listing=row.get("date_of_listing"),
                )
                db.add(new_stock)
        
        db.commit()
        logging.info(f"{exchange} Stock Data Stored Successfully!")

    except IntegrityError as e:
        db.rollback()
        logging.error(f"Integrity Error storing {exchange} stock data: {str(e)}")
    except Exception as e:
        db.rollback()
        logging.error(f"Error storing {exchange} stock data: {str(e)}")
    finally:
        db.close()

# Run based on argument passed
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python stock_data_service.py <NSE|BSE>")
    else:
        exchange = sys.argv[1]
        if exchange == "NSE":
            store_stock_data("NSE", NSE_FILE_PATH)
        elif exchange == "BSE":
            store_stock_data("BSE", BSE_FILE_PATH)
        else:
            print("Invalid exchange! Use NSE or BSE.")
