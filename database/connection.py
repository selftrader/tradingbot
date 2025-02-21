from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

def get_database_url():
    """Get database URL from environment"""
    return os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:root@localhost:5432/tradingapp"
    )

def create_engine_with_retry(retries=3):
    """Create database engine with retry logic"""
    url = get_database_url()
    for attempt in range(retries):
        try:
            engine = create_engine(url, pool_pre_ping=True)
            # Test connection with proper SQL execution
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connection successful")
            return engine
        except OperationalError as e:
            if attempt == retries - 1:
                logger.error(f"Failed to connect to database after {retries} attempts")
                raise
            logger.warning(f"Database connection attempt {attempt + 1} failed, retrying...")

# Create engine
engine = create_engine_with_retry()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        from models.database_models import Base, BrokerConfig
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise

def save_broker_config(broker_data: dict, db=None):
    """Save broker configuration to database"""
    if db is None:
        db = next(get_db())
    
    try:
        from models.database_models import BrokerConfig
        
        config = BrokerConfig(
            broker_name=broker_data['broker_name'],
            api_key=broker_data.get('api_key'),
            api_secret=broker_data.get('api_secret'),
            access_token=broker_data.get('access_token'),
            user_id=broker_data.get('user_id'),
            config_data=broker_data.get('config_data', {})
        )
        
        db.add(config)
        db.commit()
        db.refresh(config)
        logger.info(f"Saved config for broker: {broker_data['broker_name']}")
        return config
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save broker config: {str(e)}")
        raise
    finally:
        if db and not hasattr(db, '_is_dependency'):
            db.close()

def test_connection():
    """Test database connection"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
            assert result == 1
            logger.info("Database connection test successful")
            return True
    except Exception as e:
        logger.error(f"Database connection test failed: {str(e)}")
        return False