#!/usr/bin/env bash
# Render / production: apply migrations on every deploy, then start Gunicorn.
# (Build-time migrate can miss or use a different filesystem than runtime.)
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONUNBUFFERED=1
python manage.py migrate --noinput
exec gunicorn rose_project.wsgi:application --bind "0.0.0.0:${PORT:-8000}"
