#!/bin/bash
set -e

echo "[entrypoint] Waiting for MySQL at ${DB_HOST}:${DB_PORT} ..."

# PythonワンライナーでTCP接続待機（最小依存・確実）
python - <<'PY'
import os, socket, time
host = os.environ.get("DB_HOST", "db")
port = int(os.environ.get("DB_PORT", "3306"))
deadline = time.time() + 300  # 最大5分待つ
while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            print(f"[wait] Connected to {host}:{port}")
            break
    except OSError:
        if time.time() > deadline:
            raise SystemExit(f"[wait] Timeout waiting for {host}:{port}")
        print("[wait] still waiting...")
        time.sleep(2)
PY

echo "[entrypoint] Running makemigrations & migrate ..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "[entrypoint] Creating superuser if not exists ..."
python - <<'PY'
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get("SUPERUSER_NAME","admin")
email = os.environ.get("SUPERUSER_EMAIL","admin@example.com")
password = os.environ.get("SUPERUSER_PASSWORD","admin")
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"[superuser] Created: {username}/{password}")
else:
    print(f"[superuser] Exists: {username}")
PY

echo "[entrypoint] Starting Django dev server on 0.0.0.0:8000 ..."
exec python manage.py runserver 0.0.0.0:8000