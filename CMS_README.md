# Rose Coloured Lens – CMS & Admin

The site is now **dynamic**: all content is stored in the database and editable from the admin.

## Quick start

1. **Environment**
   - Copy `.env.example` to `.env`
   - Set `SECRET_KEY` (Django) and Cloudinary credentials:
     - `CLOUDINARY_CLOUD_NAME=dcngzaxlv`
     - `CLOUDINARY_API_KEY=714791931259849`
     - `CLOUDINARY_API_SECRET=<your-secret>`

2. **Database & seed**
   ```bash
   python manage.py migrate
   python manage.py seed_cms
   ```

3. **Admin user** (for dashboard and Django admin)
   ```bash
   python manage.py createsuperuser
   ```

4. **Run server**
   ```bash
   python manage.py runserver
   ```

- **Site:** http://127.0.0.1:8000/
- **Dashboard:** http://127.0.0.1:8000/dashboard/ (login required)
- **Django Admin:** http://127.0.0.1:8000/admin/ (login required)

## What’s dynamic

- **Home:** Hero carousel, What We Do, About preview, Founder & Purpose, CTA (all from DB).
- **About:** Founder & Vision, Mission, Speaking sections and bullets.
- **Blog:** Categories and posts (listing; detail page can be added).
- **Shop:** Products and colour swatches.
- **Contact:** Location/email from Site Settings; form saves to ContactSubmission.
- **Donate / 404:** Page copy from PageCopy.
- **Footer:** Site settings (contact, social, newsletter text, credits).

## Images & Cloudinary

- **Current:** Seed data uses paths like `/img/carousel-1.jpg` (served from your `img/` folder).
- **Cloudinary:** Set `CLOUDINARY_*` in `.env`. Upload images to Cloudinary and store the returned image URL in the relevant model field (e.g. HeroSlide `image_url`, Product `image_url`). The frontend uses whatever URL is stored (static path or Cloudinary CDN).
- **Upload API:** `POST /dashboard/upload-image/` (login required) with form field `file`. Returns `{"url": "<cloudinary-url>"}`. Use this to upload an image, then paste the returned URL into any image URL field in Django Admin.

## Dashboard

- **Theme:** Nguni-Zulu inspired (Red, Orange, Yellow, Pink, Purple, Green, Teal, Black).
- **Login:** `/dashboard/login/`
- **Home:** Overview cards and links to Django Admin for each content type.
- **Editing:** Use Django Admin (or the linked “Edit” buttons) to change content; rich text and image URL fields are available.

## Seed again

To reset and re-load default content:

```bash
python manage.py seed_cms --clear
```

## Code layout

- **Models:** `main/models.py` (SiteSettings, HeroSlide, WhatWeDoItem, AboutPreview, FounderPurposeBlock, CallToActionBlock, AboutSection, BlogCategory, BlogPost, Product, PageCopy, ContactSubmission, NewsletterSubscriber).
- **Views:** `main/views.py` (frontend); `main/dashboard_views.py` (dashboard).
- **Templates:** `main/templates/main/` (base, home, about, blog, shop, contact, donate, 404) and `main/templates/main/dashboard/`.
- **Seed:** `main/management/commands/seed_cms.py`.
