#!/usr/bin/env sh
set -eu

if [ "${WAIT_FOR_DATABASE:-1}" = "1" ]; then
  python - <<'PY'
import os
import time

import psycopg

url = os.environ.get("DATABASE_URL", "")
if not url.startswith(("postgres://", "postgresql://")):
    raise SystemExit(0)

last_error = None
for _ in range(int(os.environ.get("DATABASE_WAIT_ATTEMPTS", "30"))):
    try:
        with psycopg.connect(url, connect_timeout=3):
            raise SystemExit(0)
    except Exception as exc:
        last_error = exc
        time.sleep(1)
raise SystemExit(f"Database did not become ready: {last_error}")
PY
fi

if [ "${RUN_MIGRATIONS:-1}" = "1" ]; then
  python manage.py migrate --noinput
fi

if [ "${COLLECT_STATIC:-1}" = "1" ]; then
  python manage.py collectstatic --noinput
fi

exec "$@"
