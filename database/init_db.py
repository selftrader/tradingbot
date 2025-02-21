from sqlalchemy_utils import database_exists, create_database
from models.database_models import Base
from database.connection import engine
import logging

logger = logging.getLogger(__name__)

def init_database():
    """Initialize the database"""
    try:
        if not database_exists(engine.url):
            create_database(engine.url)
            logger.info(f"Created database at {engine.url}")

        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise