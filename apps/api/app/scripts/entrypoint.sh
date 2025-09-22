#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="/app:${PYTHONPATH:-}"

echo "[ENTRYPOINT] Waiting for database to be ready..."
python - <<'PY'
import os, time, sys
import psycopg
url = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@db:5432/app").replace("postgresql+psycopg://", "postgresql://")
deadline = time.time() + 120
last_err = None
while time.time() < deadline:
    try:
        with psycopg.connect(url, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                print("[ENTRYPOINT] Database is ready.")
                sys.exit(0)
    except Exception as e:
        last_err = e
        time.sleep(1)
print("[ENTRYPOINT] ERROR: DB not ready after 120s:", last_err, file=sys.stderr)
sys.exit(1)
PY

echo "[ENTRYPOINT] Running Alembic migrations..."
alembic upgrade head || { echo "[ENTRYPOINT] Alembic failed"; exit 1; }

echo "[ENTRYPOINT] Starting Gunicorn..."
exec gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --log-level "${API_LOG_LEVEL:-info}"
