#!/bin/bash
echo "Running database migrations on Supabase..."
alembic upgrade head || exit 1  # ✅ Run migrations & exit on failure
echo "Starting FastAPI server..."
uvicorn app:app --host 0.0.0.0 --port 8000
