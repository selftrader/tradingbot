#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Ensure the PORT variable is set (Render provides this automatically)
PORT=${PORT:-8000}

echo "Running Alembic database migrations..."
alembic upgrade head

echo "Starting FastAPI server on port $PORT..."
exec uvicorn app:app --host 0.0.0.0 --port $PORT --workers 4
