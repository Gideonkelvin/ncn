# Moving this project to cPanel without losing data

Git and `.gitignore` **do not** include several things that hold your real site content. Copy them explicitly or you will “lose” uploads, the database, and secrets.

## What Git does **not** track (copy these separately)

| Item | Why it matters |
|------|----------------|
| **`.env`** | `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, Cloudinary keys, email, YouTube API, etc. Without it, the app misbehaves or won’t connect to services. |
| **`db.sqlite3`** | Your SQLite database (all CMS pages, users, media URLs, etc.). **Not in Git.** |
| **`media/`** | Local file uploads if you are **not** using Cloudinary for everything. **Not in Git.** |
| **`staticfiles/`** | Built by `collectstatic` — can be recreated on the server; optional to copy if you prefer to regenerate. |
| **`venv/`** | Virtual environment — recreate on cPanel with `pip install -r requirements.txt`. |

## Before you leave your current machine

1. **Back up the database**  
   - Copy `db.sqlite3`, **or** if you switch to MySQL on cPanel, run `python manage.py dumpdata` (with venv active) and restore with `loaddata` after configuring MySQL.

2. **Back up environment**  
   - Copy `.env` to a **secure** place (password manager, encrypted archive). Never commit it to Git.

3. **Back up uploads**  
   - Zip the whole `media/` folder if you store files locally.

4. **Zip the project** (or use Git clone + the backups above)  
   - Include: all code, `db.sqlite3`, `media/`, and `.env` (keep `.env` out of public downloads).

## On cPanel (typical steps)

1. **Python version** — Use the same major version as locally (check with `python --version`), or match what your host supports.

2. **Virtual environment** — Create a venv in your app directory, then:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment file** — Upload your `.env` next to `manage.py` (or set variables in cPanel’s “Environment” UI if your host provides it). Set at least:
   - `SECRET_KEY` (strong, unique)
   - `DEBUG=False`
   - `ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com`
   - **`CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com`** (required for forms/admin over HTTPS)
   - Cloudinary / email / API keys as on your old server

4. **Database** — Either:
   - Upload **`db.sqlite3`** into the project folder (same path as locally), **or**
   - Create a MySQL database in cPanel and set **`DATABASE_URL`** in `.env` (see `.env.example`). The project reads this automatically (`dj-database-url` + `mysqlclient`). Then run **`migrate`**.

5. **Static files (CSS, JS, theme)** — Templates use Django’s `{% static %}` so assets are served at **`/static/...`** (WhiteNoise). You **must** run **`collectstatic`** on the server or pages will load with no styling. From the folder that contains `manage.py`:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
   If you use Cloudinary + `django-cloudinary-storage`, use:
   ```bash
   python manage.py collectstatic --noinput --upload-unhashed-files
   ```

6. **Local media** — If Cloudinary is **not** configured, uploaded files under **`media/`** are served by Django in production (so `/media/` works with `DEBUG=False`). Copy the **`media/`** folder when migrating, or keep using Cloudinary so files stay on the CDN.

7. **Permissions** — Ensure the web user can read the app and write to `media/` (and `db.sqlite3` if you use SQLite).

8. **WSGI** — Point the Python app to **`passenger_wsgi.py`** in this repo (see file header). Adjust paths if your host puts the project in a subfolder.

9. **HTTPS** — With `DEBUG=False`, the project enables secure cookies and HSTS. Use HTTPS on your domain; set **`CSRF_TRUSTED_ORIGINS`** as above. If you must test over plain HTTP temporarily, set `SECURE_SSL_REDIRECT=False` in `.env` (not recommended long-term).

## Quick “nothing lost” checklist

- [ ] Code (Git clone or zip)
- [ ] `.env` recreated on the server with the same keys
- [ ] `db.sqlite3` copied **or** DB exported/imported
- [ ] `media/` copied if you use local uploads
- [ ] `pip install -r requirements.txt`
- [ ] `migrate` + **`collectstatic`** (open the site and confirm CSS/JS load)
- [ ] `ALLOWED_HOSTS`, **`CSRF_TRUSTED_ORIGINS`**, and `DEBUG=False` for production
- [ ] Test admin login and a page with uploads

Keeping this checklist avoids losing CMS content, users, or uploaded files when moving to cPanel.
