# Rose – Django Project Setup

This document describes how the **rose** folder was converted into a Django project and how to run it locally.

---

## Terminal commands used

Run these from the project root (`c:\Users\servi\Music\rose` or `.\rose`).

### 1. Create virtual environment

```powershell
python -m venv venv
```

### 2. Activate virtual environment (PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Django

```powershell
pip install django
```

Or install from `requirements.txt`:

```powershell
pip install -r requirements.txt
```

### 4. Initialize Django project (already done)

```powershell
django-admin startproject rose_project .
```

### 5. Create the main app (already done)

```powershell
python manage.py startapp main
```

### 6. Run migrations

```powershell
python manage.py migrate
```

### 7. Start the development server

```powershell
python manage.py runserver 8000
```

Then open **http://localhost:8000/** or **http://127.0.0.1:8000/** in your browser.

### Optional: create a superuser (for admin)

```powershell
python manage.py createsuperuser
```

Admin site: **http://localhost:8000/admin/**

---

## Project structure after setup

```
rose/
├── manage.py                 # Django CLI entry point
├── requirements.txt         # Python dependencies
├── db.sqlite3               # SQLite database (created after migrate)
├── venv/                    # Virtual environment (activate before running commands)
├── static/                  # Project-wide static files (CSS, JS, images)
├── staticfiles/             # Collected static files (after collectstatic, for production)
├── templates/               # Project-level templates (optional)
├── rose_project/            # Project configuration package
│   ├── __init__.py
│   ├── settings.py          # ALLOWED_HOSTS, TEMPLATES, STATIC, INSTALLED_APPS
│   ├── urls.py              # Root URLconf (includes main app)
│   ├── asgi.py
│   └── wsgi.py
├── main/                    # Main application
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py             # home view
│   ├── urls.py              # App URL routes
│   ├── templates/
│   │   └── main/
│   │       └── home.html    # Home page template
│   └── migrations/
│       └── __init__.py
├── index.html               # (existing template assets)
├── css/, js/, lib/, scss/   # (existing template assets)
└── DJANGO_SETUP.md          # This file
```

- **rose_project**: Holds settings, root URLs, and WSGI/ASGI config.
- **main**: Main app; home page is at `/` and rendered from `main/templates/main/home.html`.
- **static**: Put project-wide static files here; they are served under `/static/` in development.
- **STATIC_ROOT** (`staticfiles/`): Used for `collectstatic` in production.

---

## Configuration summary

- **ALLOWED_HOSTS**: `['localhost', '127.0.0.1']` for local development.
- **TEMPLATES**: `DIRS` includes `templates/`; app templates are in `main/templates/`.
- **STATIC**: `STATIC_URL = 'static/'`, `STATICFILES_DIRS = [BASE_DIR / 'static']`, `STATIC_ROOT = staticfiles`.
- **INSTALLED_APPS**: Includes `main.apps.MainConfig` and all default Django apps.
- **Database**: SQLite (`db.sqlite3`) by default.

The development server runs at **http://localhost:8000/** with no errors after migrations.
