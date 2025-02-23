import asyncio
import logging
import os
from datetime import datetime
from contextlib import asynccontextmanager

import uvicorn
import socketio
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import database and models
from database.connection import get_db
from database.init_db import init_db

# Import routers
from router.auth_router import auth_router
from router.broker_router import broker_router
from router.analysis_router import router as analysis_router
from router.sector_router import router as sector_router

# Import services
from services.trading_service import TradingService
from controllers.trading_controller import TradingController

# Load environment variables
load_dotenv()

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles application startup and shutdown events."""
    logger.info("🚀 Starting Trading Application...")

    try:
        # Initialize core components
        app.state.config = {
            "auto_start": False,
            "broker_name": os.getenv("BROKER_NAME", "upstox")
        }

        # Initialize database connection
        db = next(get_db())

        # Initialize Trading Controller
        trading_controller = TradingController()
        app.state.trading_controller = trading_controller

        logger.info("✅ Trading bot initialized successfully.")

    except Exception as e:
        logger.error(f"❌ Startup error: {str(e)}")
        raise

    yield

    logger.info("⚠️ Shutting down application...")
    if hasattr(app.state, "trading_controller"):
        await app.state.trading_controller.disconnect()

# Initialize FastAPI app
app = FastAPI(
    title="Trading Bot API",
    description="AI-powered automated trading system",
    version="1.0.0",
    lifespan=lifespan
)

# Initialize SocketIO
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
sio_app = socketio.ASGIApp(sio, other_asgi_app=app)

# Add Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(broker_router, prefix="/broker", tags=["Broker API"])
app.include_router(analysis_router, prefix="/analysis", tags=["Market Analysis"])
app.include_router(sector_router, prefix="/sector", tags=["Sector Analysis"])

# Root API Endpoint
@app.get("/")
async def root():
    return {
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "broker": app.state.trading_controller.config.get("BROKER_NAME", "unknown"),
        "services": {
            "trading": bool(getattr(app.state, "trading_service", None)),
            "options": bool(getattr(app.state, "options_service", None))
        }
    }

# API Health Check
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "broker": app.state.trading_controller.config.get("BROKER_NAME", "unknown")
    }

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"🔥 Global error: {str(exc)}")
    return JSONResponse(status_code=500, content={"error": str(exc)})

# Start FastAPI Server
if __name__ == "__main__":
    print("🚀 Starting FastAPI Trading Bot Server...")
    uvicorn.run(
        "app:sio_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug"
    )
