"""
Custom staff dashboard (login required).
"""
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .models import (
    HeroSlide,
    Service,
    WhatWeDoItem,
    DynamicPage,
    OtherSitePage,
    ContactSubmission,
    PageCopy,
    Event,
)


@require_http_methods(["GET", "POST"])
def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next")
            if next_url and next_url.startswith("/"):
                return redirect(next_url)
            return redirect("dashboard_home")
        return render(request, "main/dashboard/login.html", {"error": "Invalid username or password."})
    return render(request, "main/dashboard/login.html")


@require_http_methods(["GET"])
def dashboard_logout(request):
    logout(request)
    return redirect("dashboard_login")


@login_required(login_url="/dashboard/login/")
def dashboard_home(request):
    return render(
        request,
        "main/dashboard/home.html",
        {
            "hero_count": HeroSlide.objects.count(),
            "services_count": Service.objects.count(),
            "what_we_do_count": WhatWeDoItem.objects.count(),
            "site_pages_total": DynamicPage.objects.filter(is_active=True).count(),
            "other_site_pages_count": OtherSitePage.objects.filter(is_active=True).count(),
            "page_copies_count": PageCopy.objects.count(),
            "events_count": Event.objects.filter(is_published=True).count(),
            "contact_submissions_count": ContactSubmission.objects.filter(read=False).count(),
        },
    )


@login_required(login_url="/dashboard/login/")
@require_http_methods(["POST"])
def dashboard_upload_image(request):
    """Upload image to Cloudinary; return JSON with url. Requires login."""
    if not getattr(request, "FILES") or "file" not in request.FILES:
        return JsonResponse({"error": "No file provided"}, status=400)
    if not all([
        getattr(settings, "CLOUDINARY_CLOUD_NAME", None),
        getattr(settings, "CLOUDINARY_API_KEY", None),
        getattr(settings, "CLOUDINARY_API_SECRET", None),
    ]):
        return JsonResponse({"error": "Cloudinary not configured"}, status=503)
    try:
        import cloudinary.uploader
        result = cloudinary.uploader.upload(
            request.FILES["file"],
            use_filename=True,
            unique_filename=True,
            overwrite=False,
        )
        url = result.get("secure_url") or result.get("url")
        if not url:
            return JsonResponse({"error": "No URL in response"}, status=500)
        return JsonResponse({"url": url})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
