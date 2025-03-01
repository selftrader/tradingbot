from database.connection import engine, Base
from database.models import User, Account, AIModel

# ✅ Create all tables
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("✅ Database initialized successfully!")
