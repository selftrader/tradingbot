import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# ✅ Ensure DATABASE_URL is set
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("ERROR: DATABASE_URL is missing in .env file!")

# ✅ Create PostgreSQL Engine with Connection Pooling
try:
    engine = create_engine(
        DATABASE_URL,
        pool_size=20,
        max_overflow=10,
        echo=False,  # Set True for debugging SQL queries
        pool_pre_ping=True
    )
    print("Database connected successfully.")
except Exception as e:
    raise RuntimeError(f"Database connection failed: {e}")

# ✅ Session Management
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ Dependency to get database session
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
