#!/usr/bin/env bash
# Render build script (runs once per deploy).
# - Installs Python dependencies from requirements.txt
# - Applies database migrations (creates tables such as main_founderpurposeblock)
# - Collects static files for WhiteNoise
#
# Compatible with Render: uses bash features available on Linux builders; no chmod needed.
set -euo pipefail

cd "$(dirname "$0")"

python -m pip install -r requirements.txt

python manage.py migrate --noinput

# When CLOUDINARY_* env vars are set, django-cloudinary-storage is active and collectstatic
# expects this flag for local STATIC_ROOT + WhiteNoise. Otherwise use plain collectstatic.
if [ -n "${CLOUDINARY_CLOUD_NAME:-}" ]; then
  python manage.py collectstatic --noinput --upload-unhashed-files
else
  python manage.py collectstatic --noinput
fi
