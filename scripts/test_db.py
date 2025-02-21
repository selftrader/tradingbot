import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import test_connection
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    if test_connection():
        print("Database connection successful!")
    else:
        print("Database connection failed!")
        sys.exit(1)