#!/usr/bin/env bash
set -euo pipefail

pip install -r requirements.txt

python manage.py migrate --noinput

# django-cloudinary-storage needs this flag when using local STATIC_ROOT + WhiteNoise
python manage.py collectstatic --noinput --upload-unhashed-files
