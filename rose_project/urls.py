"""
URL configuration for rose_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from django.views.generic import RedirectView


def admin_dynamicpage_compat(request, subpath=""):
    """
    DynamicPage was split into per-page proxies + Other site pages.
    Old bookmarks to /admin/main/dynamicpage/ → Other site pages (same table, same PKs).
    """
    url = "/admin/main/othersitepage/"
    if subpath:
        url += subpath
    qs = request.META.get("QUERY_STRING", "")
    if qs:
        url += "?" + qs
    return redirect(url, permanent=True)


urlpatterns = [
    # No trailing slash must resolve before main.urls catch-all (<slug>) steals "admin", "ckeditor", etc.
    path("admin", RedirectView.as_view(url="/admin/", permanent=True)),
    # Legacy admin URLs (before proxy models) — must be before admin.site.urls
    path("admin/main/dynamicpage/", admin_dynamicpage_compat),
    path("admin/main/dynamicpage/<path:subpath>", admin_dynamicpage_compat),
    path("admin/", admin.site.urls),
    path("ckeditor", RedirectView.as_view(url="/ckeditor/", permanent=True)),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("", include("main.urls")),
]

# Local media uploads (when Cloudinary is not configured). Required on cPanel so /media/
# works with DEBUG=False; when using Cloudinary, uploads are served from the CDN.
if not getattr(settings, "MEDIA_CLOUDINARY_ENABLED", False):
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {"document_root": settings.MEDIA_ROOT},
        ),
    ]

handler404 = "main.views.page_not_found_view"