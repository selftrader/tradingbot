@echo off
echo Running Alembic Migrations...
alembic upgrade head

echo Starting FastAPI Server...
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
