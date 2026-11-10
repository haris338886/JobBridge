#!/bin/sh
# ============================================================
# JobBridge — Docker entrypoint
# ============================================================
set -e

# Wait for database if a DB_HOST is set
if [ -n "$DB_HOST" ]; then
    echo "Waiting for database at $DB_HOST:${DB_PORT:-5432}..."
    until python -c "import socket; s=socket.socket(); s.settimeout(1); s.connect(('${DB_HOST}', ${DB_PORT:-5432}))" 2>/dev/null; do
        sleep 1
    done
    echo "Database is up."
fi

# Migrate
python manage.py migrate --noinput

# Collect static
python manage.py collectstatic --noinput --clear

# Hand off to CMD (gunicorn / uvicorn / etc.)
exec "$@"