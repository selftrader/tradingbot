from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from services.trade_execution import execute_trade_with_sizing
from database.connection import SessionLocal

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("📢 Welcome to your Trading Bot! Use /buy or /sell to execute trades.")

def buy(update: Update, context: CallbackContext):
    """Handles /buy command: /buy SYMBOL"""
    symbol = context.args[0].upper()
    db = SessionLocal()
    result = execute_trade_with_sizing(1, symbol, "BUY", db)
    db.close()
    update.message.reply_text(f"✅ Trade Executed: {result}")

def sell(update: Update, context: CallbackContext):
    """Handles /sell command: /sell SYMBOL"""
    symbol = context.args[0].upper()
    db = SessionLocal()
    result = execute_trade_with_sizing(1, symbol, "SELL", db)
    db.close()
    update.message.reply_text(f"✅ Trade Executed: {result}")

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("buy", buy))
dp.add_handler(CommandHandler("sell", sell))

updater.start_polling()
updater.idle()
# Compare this snippet from services/telegram_bot.py:
# from telegram import Update   # ✅ Import Update from telegram module 
# from telegram.ext import Updater, CommandHandler, CallbackContext  # ✅ Import Updater, CommandHandler, CallbackContext   
# from services.trade_execution import execute_trade_with_sizing  # ✅ Import execute_trade_with_sizing function
# from database.connection import SessionLocal  # ✅ Import SessionLocal from database.connection
