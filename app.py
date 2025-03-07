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
from router.user_router import router as user_router 
from router.auth_router import auth_router
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

# Initialize FastAPI app
app = FastAPI(
    title="Trading Bot API",
    description="AI-powered automated trading system",
    version="1.0.0",
    lifespan=lifespan
)

# ✅ Initialize SocketIO with proper CORS handling
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
sio_app = socketio.ASGIApp(sio, other_asgi_app=app)

# ✅ CORS Configuration for FastAPI
origins = [
    "https://resplendent-shortbread-e830d3.netlify.app",  # ✅ Netlify frontend
    "http://localhost:3000",  # ✅ Local development frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ✅ Allow frontend URLs explicitly
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # ✅ Explicitly allow all necessary methods
    allow_headers=["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With"],  # ✅ Necessary headers
    expose_headers=["Content-Disposition"],  # ✅ If required for file downloads
)

# ✅ Debug Preflight Requests
@app.options("/{full_path:path}")
async def preflight_handler(full_path: str):
    return JSONResponse(content={"message": "Preflight OK"}, status_code=200)

# ✅ Include Routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(broker_router, prefix="/broker", tags=["Broker API"])
app.include_router(user_router, prefix="/user", tags=["User Profile"])

# ✅ Root API Endpoint
@app.get("/")
async def root():
    return {
        "status": "running",
        "timestamp": datetime.now().isoformat(),
    }

# ✅ API Health Check
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
    }

# ✅ Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"🔥 Global error: {str(exc)}")
    return JSONResponse(status_code=500, content={"error": str(exc)})

# ✅ Start FastAPI Server
if __name__ == "__main__":
    logger.info("🚀 Starting FastAPI Trading Bot Server...")
    uvicorn.run(
        "app:sio_app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),  # Use Render's PORT dynamically
        log_level="info"
    )
