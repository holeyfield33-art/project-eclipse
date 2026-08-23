#!/usr/bin/env bash
set -euo pipefail

echo "=== Project Eclipse – Local Dev Setup ==="

# Start infrastructure
echo "Starting Docker services..."
docker compose up -d

echo "Waiting for Postgres..."
until docker compose exec -T postgres pg_isready -U eclipse >/dev/null 2>&1; do
  sleep 1
done

echo "Infrastructure is up."
echo ""
echo "Next steps:"
echo "  1. Backend API:  cd backend/api && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && uvicorn app.main:app --reload"
echo "  2. ML service:   cd backend/ml && pip install -r requirements.txt && python serve.py"
echo "  3. Frontend:     cd frontend && npm install && npm run dev"
echo ""
echo "API docs → http://localhost:8000/docs"
echo "Dashboard → http://localhost:5173"
