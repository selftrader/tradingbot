from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Fetch DATABASE_URL from .env (Ensure it's properly set)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is not set. Please configure it in the .env file.")

# ✅ Create PostgreSQL Engine with Connection Pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=20,           # ✅ Allows up to 20 connections
    max_overflow=10,        # ✅ Allows 10 extra connections if needed
    echo=False,             # ✅ Set to True to debug SQL queries
    pool_pre_ping=True,     # ✅ Ensures broken connections are detected & removed
)

# ✅ Session Management
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ Dependency to get database session
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        print(f"⚠️ Database connection error: {e}")  # ✅ Log errors
    finally:
        if db:
            db.close()
