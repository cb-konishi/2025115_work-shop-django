#!/bin/bash
set -e

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