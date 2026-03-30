#!/usr/bin/env bash
# Render (or any Linux CI) build: install deps, collect static, migrate.
set -o errexit
set -o pipefail

pip install -r requirements.txt
# django-cloudinary-storage overrides collectstatic: copy to STATIC_ROOT for WhiteNoise
# (required when staticfiles backend is local, not StaticCloudinaryStorage).
python manage.py collectstatic --noinput --upload-unhashed-files
python manage.py migrate
