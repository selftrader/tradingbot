import asyncio
import threading
import time
import os
from typing import List
import joblib
import pandas as pd
import uvicorn
import socketio
import logging
import yfinance as yf
from dotenv import load_dotenv

from fastapi import FastAPI, WebSocket, HTTPException, Request, Depends, WebSocketDisconnect, logger
from fastapi.responses import RedirectResponse, HTMLResponse  # Add this import
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.connection import get_db, init_db
from models.ai_trading_model import AutonomousTrader
from models.database_models import Trade, Position, User
from datetime import datetime
from contextlib import asynccontextmanager

# Import custom modules and functions
from models.train_ai_model import train_model  # if needed elsewhere
from models.predict_trade import predict_trade

# Import routers
from router import  broker_config_router, upstox_router, dhan_router
from router.sector_router import router as sector_router
from router.analysis_router import router as analysis_router
from router import trading_router, broker_router, strategy_router, monitor_router
from router import config_router

# Import services
from services.technical_analysis import TechnicalAnalysis
from services.trading_service import TradingService
from services.live_trading_service import LiveTradingService
from services.options_trading_service import OptionsTradingService
from controllers.trading_controller import TradingController

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events"""
    # Startup
    logger.info("----------------")
    logger.info("Starting Trading Application")
    logger.info("----------------")
    
    try:
        # Initialize basic components without starting analysis
        logger.info("Initializing core components...")
        
        # Store configuration in app state
        app.state.config = {
            "auto_start": False,  # Prevent auto-start of analysis
            "broker_name": os.getenv("BROKER_NAME", "upstox")
        }
        
        # Initialize database connection only
        logger.info("Initializing database connection...")
        db = next(get_db())
        
        # Initialize trading controller without auto-start
        logger.info("Initializing trading controller...")
        trading_controller = TradingController()
        app.state.trading_controller = trading_controller
        
        logger.info("Basic initialization complete")
        logger.info("----------------")
        
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    if hasattr(app.state, "trading_controller"):
        await app.state.trading_controller.disconnect()

# Initialize FastAPI and Socket.IO
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = FastAPI(
    title="Trading Application",
    description="Automated trading system with options support",
    version="1.0.0",
    lifespan=lifespan
)
sio_app = socketio.ASGIApp(sio, other_asgi_app=app)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set appropriate origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    """Handle client connection"""
    logger.info(f"Client connected: {sid}")
    await sio.emit('status', {'message': 'Connected successfully'}, room=sid)

@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {sid}")

@sio.event
async def start_trading(sid, data):
    """Handle trading start request from client"""
    try:
        symbols = data.get("symbols", [])
        if not symbols:
            await sio.emit('error', {'message': 'No symbols selected'}, room=sid)
            return

        # Start trading through API endpoint
        db = next(get_db())
        result = await start_bot(symbols, db)
        
        await sio.emit('trading_started', {
            'message': 'Trading started successfully',
            'session_id': result['session_id'],
            'symbols': symbols
        }, room=sid)
        
    except Exception as e:
        await sio.emit('error', {'message': str(e)}, room=sid)

@sio.event
async def stop_trading(sid):
    """Handle trading stop request from client"""
    try:
        db = next(get_db())
        await stop_bot(db)
        await sio.emit('trading_stopped', {'message': 'Trading stopped'}, room=sid)
    except Exception as e:
        await sio.emit('error', {'message': str(e)}, room=sid)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"message": "Connected to WS endpoint"})

@app.websocket("/ws/trades/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    trader = app.state.trader
    await trader.register_client(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            # Handle client messages if needed
    except WebSocketDisconnect:
        await trader.unregister_client(websocket)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint to check application status"""
    return {
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "broker": app.state.trading_controller.config["BROKER_NAME"],
        "services": {
            "trading": bool(app.state.trading_service),
            "options": bool(app.state.options_service)
        }
    }

@app.get("/api")
async def api_root():
    """Root endpoint for API"""
    return {
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "broker": app.state.trading_controller.config["BROKER_NAME"],
        "services": {
            "trading": bool(app.state.trading_service),
            "options": bool(app.state.options_service)
        }
    }

# Create an endpoint to return available stocks
@app.get("/api/stocks/available")
async def available_stocks():
    # Sample data. Replace with your actual stock data provider.
    return [
        {"symbol": "AAPL", "name": "Apple Inc."},
        {"symbol": "GOOG", "name": "Alphabet Inc."},
        {"symbol": "MSFT", "name": "Microsoft Corporation"},
        {"symbol": "AMZN", "name": "Amazon.com Inc."}
    ]

# Update the start_bot endpoint
@app.post("/start_bot")
async def start_bot(symbols: List[str], db: Session = Depends(get_db)):
    """Start autonomous trading for selected symbols"""
    try:
        if not symbols:
            raise HTTPException(status_code=400, detail="No symbols selected")

        # Verify broker configuration
        if not hasattr(app.state, "trading_controller"):
            raise HTTPException(status_code=400, detail="Trading controller not initialized")

        # Check broker connection
        broker_status = await app.state.trading_controller.check_broker_connection()
        if not broker_status:
            raise HTTPException(status_code=400, detail="Broker not connected")

        # Create trading session record
        trading_session = Trade(
            status="STARTED",
            metadata={
                "start_time": datetime.utcnow().isoformat(),
                "symbols": symbols,
                "broker": app.state.trading_controller.config["BROKER_NAME"]
            }
        )
        db.add(trading_session)
        db.commit()

        # Set trading state
        app.state.trading_active = True
        app.state.trading_symbols = symbols

        # Start trading in background only if not running
        if not hasattr(app.state, "trading_task") or app.state.trading_task.done():
            app.state.trading_task = asyncio.create_task(
                run_trading_bot(symbols, trading_session.id)
            )

        return {
            "message": "Trading Bot Started",
            "session_id": trading_session.id,
            "symbols": symbols
        }

    except Exception as e:
        db.rollback()
        logger.error(f"Error starting bot: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/start_bot")
async def start_bot(symbols: List[str], db: Session = Depends(get_db)):
    """Start autonomous trading for selected symbols"""
    try:
        if not symbols:
            raise HTTPException(status_code=400, detail="No symbols selected")
        if not hasattr(app.state, "trading_controller"):
            raise HTTPException(status_code=400, detail="Trading controller not initialized")
        broker_status = await app.state.trading_controller.check_broker_connection()
        if not broker_status:
            raise HTTPException(status_code=400, detail="Broker not connected")
        trading_session = Trade(
            status="STARTED",
            metadata={
                "start_time": datetime.utcnow().isoformat(),
                "symbols": symbols,
                "broker": app.state.trading_controller.config["BROKER_NAME"]
            }
        )
        db.add(trading_session)
        db.commit()
        app.state.trading_active = True
        app.state.trading_symbols = symbols
        if not hasattr(app.state, "trading_task") or app.state.trading_task.done():
            app.state.trading_task = asyncio.create_task(
                run_trading_bot(symbols, trading_session.id)
            )
        return {
            "message": "Trading Bot Started",
            "session_id": trading_session.id,
            "symbols": symbols
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error starting bot: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stop_bot")
async def stop_bot(db: Session = Depends(get_db)):
    """Stop the trading bot"""
    try:
        app.state.trading_active = False
        
        # Cancel running task if exists
        if hasattr(app.state, "trading_task"):
            app.state.trading_task.cancel()
            
        # Update session status
        active_sessions = db.query(Trade).filter(
            Trade.status == "STARTED"
        ).all()
        
        for session in active_sessions:
            session.status = "STOPPED"
            session.metadata["stop_time"] = datetime.utcnow().isoformat()
            
        db.commit()
        
        return {"message": "Trading Bot Stopped"}
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error stopping bot: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stop_bot")
async def stop_bot(db: Session = Depends(get_db)):
    """Stop the trading bot"""
    try:
        app.state.trading_active = False
        if hasattr(app.state, "trading_task"):
            app.state.trading_task.cancel()
        active_sessions = db.query(Trade).filter(Trade.status == "STARTED").all()
        for session in active_sessions:
            session.status = "STOPPED"
            session.metadata["stop_time"] = datetime.utcnow().isoformat()
        db.commit()
        return {"message": "Trading Bot Stopped"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error stopping bot: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Replace the old trading loop with an async version
async def run_trading_bot(symbols: List[str], session_id: int):
    """Async trading bot execution with AI"""
    db = next(get_db())
    trader = AutonomousTrader(app.state.trading_controller.broker)
    
    try:
        while app.state.trading_active:
            for symbol in symbols:
                if not app.state.trading_active:
                    break
                    
                try:
                    # Get AI analysis
                    analysis = await trader.analyze_market(symbol)
                    
                    # Execute trade if confidence is high
                    if analysis['confidence'] >= 0.7:
                        trade_result = await trader.execute_trade(symbol, analysis)
                        
                        # Record trade
                        if trade_result['status'] == 'EXECUTED':
                            trade = Trade(
                                symbol=symbol,
                                trade_type=analysis['action'],
                                status="EXECUTED",
                                quantity=trade_result['quantity'],
                                metadata={
                                    "session_id": session_id,
                                    "confidence": analysis['confidence'],
                                    "analysis": analysis
                                }
                            )
                            db.add(trade)
                            db.commit()
                            
                            # Emit trade update
                            await sio.emit('trade_update', trade_result)
                        
                except Exception as e:
                    logger.error(f"Error trading {symbol}: {str(e)}")
                    continue
                    
            await asyncio.sleep(300)  # 5-minute interval
            
    except asyncio.CancelledError:
        logger.info("Trading bot task cancelled")
    except Exception as e:
        logger.error(f"Trading bot error: {str(e)}")
    finally:
        db.close()

# API endpoint to get active trades
@app.get("/get_trades")
def get_trades(db: Session = Depends(get_db)):
    try:
        trades = db.query(Trade).filter(
            Trade.status.in_(["PENDING", "EXECUTED"])
        ).all()
        
        return {
            "trades": [
                {
                    "id": trade.id,
                    "symbol": trade.symbol,
                    "type": trade.trade_type,
                    "status": trade.status,
                    "quantity": trade.quantity,
                    "price": trade.price,
                    "executed_at": trade.executed_at,
                    "metadata": trade.metadata
                }
                for trade in trades
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(analysis_router)
app.include_router(broker_config_router)
app.include_router(upstox_router)  # Now using the router approach
app.include_router(dhan_router)
app.include_router(sector_router)
app.include_router(trading_router.router)
app.include_router(broker_router.router)
app.include_router(strategy_router.router)
app.include_router(monitor_router.router)
app.include_router(config_router.router)
app.include_router(sector_router)

# Remove the automatic broadcast task
# Instead, implement on-demand updates
@app.get("/api/updates")
async def get_updates(db: Session = Depends(get_db)):
    """Get current trading updates on demand"""
    try:
        trades = db.query(Trade).filter(
            Trade.status.in_(["PENDING", "EXECUTED"])
        ).all()
        return {"trades": [trade.__dict__ for trade in trades]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Trading loop function – runs autonomously in a background thread
def start_trading():
    """Starts AI-Powered Trading with database integration"""
    db = next(get_db())
    stocks_to_trade = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS"]
    
    try:
        while True:
            for stock_symbol in stocks_to_trade:
                # Only predict when trading is active
                if hasattr(app.state, "trading_active") and app.state.trading_active:
                    action = predict_trade(stock_symbol)
                    if action:
                        trade_id = place_order(
                            stock_symbol, 
                            action, 
                            variety="regular",
                            db=db
                        )
                        logger.info(f"Placed trade {trade_id} for {stock_symbol}")
            time.sleep(300)
    except Exception as e:
        logger.error(f"Trading error: {str(e)}")
    finally:
        db.close()

def place_order(symbol: str, action: str, variety: str, db: Session):
    try:
        # Save trade to database
        trade = Trade(
            symbol=symbol,
            trade_type=action,
            product_type="INTRADAY",
            status="PENDING",
            quantity=1,  # Update with actual quantity
            price=0.0,  # Will be updated on execution
            metadata={
                "variety": variety,
                "placement_time": datetime.utcnow().isoformat()
            }
        )
        db.add(trade)
        db.commit()
        
        # Update positions
        position = db.query(Position).filter(
            Position.symbol == symbol
        ).first()
        
        if not position:
            position = Position(
                symbol=symbol,
                quantity=1 if action == "BUY" else -1,
                product_type="INTRADAY",
                average_price=0.0  # Will be updated on execution
            )
            db.add(position)
        else:
            position.quantity += 1 if action == "BUY" else -1
            
        db.commit()
        return trade.id
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Initialize live trading
live_trading = LiveTradingService()

@app.post("/start_live_trading")
async def start_live_trading(symbols: List[str]):
    """Start live trading for given symbols"""
    try:
        # Start trading in background task
        asyncio.create_task(live_trading.execute_live_trading(symbols))
        return {"message": "Live trading started", "symbols": symbols}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Error handling
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global error: {str(exc)}")
    return {"error": str(exc)}, 500

if __name__ == "__main__":
    print("🚀 Starting FastAPI Trading Bot Server...")
    uvicorn.run(
        "app:sio_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
