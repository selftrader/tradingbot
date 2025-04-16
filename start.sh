#!/bin/bash

set -e

PORT=${PORT:-10000}

echo "Running Alembic database migrations..."
alembic upgrade head

echo "Starting FastAPI server with SocketIO on port $PORT..."
exec uvicorn app:sio_app --host 0.0.0.0 --port $PORT --workers 1
