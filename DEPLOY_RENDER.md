# Deploying **ncn** (Django) on Render (Free plan)

This project uses **`rose_project`** as the Django package name. The WSGI module is `rose_project.wsgi`.

## Commands Render should use

| Step | Command |
|------|---------|
| **Build Command** | `bash build.sh` |
| **Start Command** | `bash start.sh` |

`build.sh` installs dependencies, runs **`migrate`** (so tables like `main_founderpurposeblock` exist), and **`collectstatic`**.

`start.sh` runs **`migrate` again** at container boot (covers cases where the runtime database differs from build), then starts **Gunicorn** bound to **`$PORT`**.

The **`Procfile`** is `web: bash start.sh` for platforms that read it.

## Environment variables (minimum for a working site)

Set these in the Render dashboard (**Environment** tab):

- **`SECRET_KEY`** — long random string (never commit it). Render can generate one.
- **`DEBUG`** — `False` for production.
- **`ALLOWED_HOSTS`** — `*` is fine to start; later set to your exact hostname, e.g. `your-app.onrender.com`.
- **`DATABASE_URL`** — **strongly recommended.** Create a **PostgreSQL** instance on Render and paste its **Internal Database URL**. Without this, the app falls back to SQLite; on ephemeral disks that can cause “missing table” errors after deploys.
- **`CSRF_TRUSTED_ORIGINS`** — `https://your-app.onrender.com` (comma-separated if you have several).

Optional (media via Cloudinary): `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`. If these are set, `build.sh` uses `collectstatic --upload-unhashed-files` as required by `django-cloudinary-storage`.

## Push code and deploy

1. Commit and push to GitHub (or GitLab/Bitbucket):

   ```bash
   git add .
   git commit -m "Configure Render build and start"
   git push origin main
   ```

2. In [Render Dashboard](https://dashboard.render.com): **New** → **Web Service** → connect the repo.

3. Choose the **Free** instance type if offered.

4. Set **Build Command** to `bash build.sh` and **Start Command** to `bash start.sh`.

5. Add the environment variables above (especially **`DATABASE_URL`** after creating Postgres).

6. Deploy. After the first successful deploy, you can run one-off commands in **Shell**, e.g. `python manage.py createsuperuser` or `python manage.py seed_cms` if your project defines it.

## Free plan notes

- Services may **spin down** after idle time; the first request after that can be slow (cold start).
- Prefer **PostgreSQL** linked via **`DATABASE_URL`** so migrations and data survive across deploys and match the running app.

## Troubleshooting `OperationalError: no such table: ...`

- Ensure **`DATABASE_URL`** points to the database you intend to use and that deploys run **`bash build.sh`** and **`bash start.sh`** so **`migrate`** runs.
- If you change models, commit migrations under `main/migrations/` and redeploy.
