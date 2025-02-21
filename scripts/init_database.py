import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import logging
from sqlalchemy import create_engine, inspect

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Now we can import from models
from models.database_models import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database():
    """Create PostgreSQL database if it doesn't exist"""
    load_dotenv()
    
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not found in environment variables")
    
    parts = db_url.split("/")
    dbname = parts[-1]
    credentials = parts[2].split("@")[0].split(":")
    user = credentials[0]
    password = credentials[1]
    host = parts[2].split("@")[1].split(":")[0]
    
    try:
        conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            database="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}'")
        exists = cur.fetchone()
        
        if not exists:
            cur.execute(f'CREATE DATABASE {dbname}')
            logger.info(f"Database {dbname} created successfully")
        else:
            logger.info(f"Database {dbname} already exists")
            
    except Exception as e:
        logger.error(f"Database creation failed: {str(e)}")
        raise
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

def init_tables():
    """Initialize database tables using SQLAlchemy models"""
    try:
        engine = create_engine(os.getenv("DATABASE_URL"))
        inspector = inspect(engine)
        
        # Get existing tables
        existing_tables = inspector.get_table_names()
        logger.info(f"Existing tables: {existing_tables}")
        
        # Create missing tables
        Base.metadata.create_all(engine)
        logger.info("Database tables initialized successfully")
        
        return True
    except Exception as e:
        logger.error(f"Table initialization failed: {str(e)}")
        return False

def main():
    """Main initialization function"""
    try:
        # Create database if needed
        create_database()
        
        # Initialize tables
        if init_tables():
            logger.info("Database initialization completed successfully")
        else:
            logger.error("Failed to initialize database tables")
            
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()