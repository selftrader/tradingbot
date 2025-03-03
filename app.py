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
from router.auth_router import  auth_router 
from router.broker_router import broker_router

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
        # Initialize database connection
        db = next(get_db())

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


origins = [
    "https://resplendent-shortbread-e830d3.netlify.app",  # ✅ Your Netlify frontend URL
    "http://localhost:3000"  # ✅ Allow local development
]
# Add Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Change this to specific frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(broker_router, prefix="/broker", tags=["Broker API"])
# app.include_router(analysis_router, prefix="/analysis", tags=["Market Analysis"])

# Root API Endpoint
@app.get("/")
async def root():
    return {
        "status": "running",
        "timestamp": datetime.now().isoformat(),
    }

# API Health Check
@app.get("/health")
async def health_check():
    trading_controller = getattr(app.state, "trading_controller", None)
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
    }

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"🔥 Global error: {str(exc)}")
    return JSONResponse(status_code=500, content={"error": str(exc)})

# Start FastAPI Server
if __name__ == "__main__":
    logger.info("🚀 Starting FastAPI Trading Bot Server...")
    uvicorn.run(
        "app:sio_app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),  # Use Render's PORT dynamically
        log_level="info"
    )
