from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys
from dotenv import load_dotenv

#Fix Import Path for `database/`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ✅ Load Environment Variables
load_dotenv()

# ✅ Ensure Base Model is Imported Correctly
from database.connection import Base  # Fix import error

# ✅ Read Alembic Config
config = context.config

# ✅ Load Logging Configuration
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Target Metadata for Auto Migrations
target_metadata = Base.metadata

# ✅ Get Database URL from `.env`
def get_url():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL is not set in .env file")
    return db_url

# ✅ Offline Migrations (SQL Script Generation)
def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# ✅ Online Migrations (Direct DB Changes)
def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# ✅ Run the Correct Migration Mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
