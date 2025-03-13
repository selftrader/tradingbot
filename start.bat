@echo off
setlocal enabledelayedexpansion

echo Running Alembic Migrations...
alembic upgrade head || (
    echo Migration failed. Exiting...
    exit /b 1
)

echo Starting FastAPI Server on port 8000...
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
