"""
cPanel / Phusion Passenger entry point.

In cPanel → Setup Python App, set the application root to this folder (where
manage.py lives) and the startup file to this module if your host expects
"passenger_wsgi.py". Some hosts auto-detect it.

If imports fail, add your virtualenv site-packages to PYTHONPATH in the panel
or uncomment/adjust sys.path below.
"""
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rose_project.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
