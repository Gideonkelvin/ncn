#!/usr/bin/env bash

# Install Python dependencies
pip install -r requirements.txt

# Apply migrations automatically
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput
