from sqlalchemy import text
from database.connection import get_db
import logging

logger = logging.getLogger(__name__)

def test_database_connection():
    """Test the PostgreSQL database connection"""
    try:
        db = next(get_db())
        # Use text() to create executable SQL
        result = db.execute(text("SELECT 1")).scalar()
        assert result == 1
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_database_connection()