"""
Frontend views: serve dynamic CMS-backed pages and static assets.
"""
# Cache pages for 15 minutes for faster navigation
from pathlib import Path

from django.conf import settings
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page

from .models import (
    BibleStudyResource,
    FounderPurposeBlock,
    HeroSlide,
    PageCopy,
    Product,
    BlogPost,
    BlogCategory,
    DynamicPage,
    Event,
    PastoralTeamSection,
    Service,
    SiteSettings,
)


# Static file serving (unchanged)
STATIC_FOLDERS = ("css", "js", "lib", "img")
CONTENT_TYPES = {
    ".css": "text/css",
    ".js": "application/javascript",
    ".json": "application/json",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".ico": "image/x-icon",
    ".svg": "image/svg+xml",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
    ".ttf": "font/ttf",
    ".eot": "application/vnd.ms-fontobject",
}


def _serve_static(request, folder, path):
    if folder not in STATIC_FOLDERS:
        raise Http404
    # Normalize path so both `/static/css/style.css` and accidental
    # `path="css/style.css"` variants still resolve correctly.
    norm_path = (path or "").replace("\\", "/").lstrip("/")
    if norm_path.startswith(f"{folder}/"):
        norm_path = norm_path[len(folder) + 1 :]
    if ".." in norm_path or norm_path.startswith("/"):
        raise Http404
    filepath = settings.BASE_DIR / folder / norm_path
    if not filepath.is_file():
        raise Http404
    try:
        filepath = filepath.resolve()
        base = settings.BASE_DIR.resolve()
        if not str(filepath).startswith(str(base)):
            raise Http404
    except Exception:
        raise Http404
    content_type = CONTENT_TYPES.get((Path(norm_path).suffix or "").lower(), "application/octet-stream")
    return HttpResponse(filepath.read_bytes(), content_type=content_type)


def serve_static_css(request, path):
    return _serve_static(request, "css", path)


def serve_static_js(request, path):
    return _serve_static(request, "js", path)


def serve_static_lib(request, path):
    return _serve_static(request, "lib", path)


def serve_static_img(request, path):
    return _serve_static(request, "img", path)


# ——— Dynamic CMS pages ———

@cache_page(60 * 15)
def home_view(request):
    hero_slides = HeroSlide.objects.filter(is_active=True).order_by("order")
    services = Service.objects.filter(is_active=True).order_by("order")
    founder_purpose = FounderPurposeBlock.get()
    site = SiteSettings.get()
    # Get upcoming events (future events, published, ordered by date)
    from django.utils import timezone
    events = Event.objects.filter(
        is_published=True,
        event_date__gte=timezone.now()
    ).order_by("event_date", "order")[:9]
    meta_title = site.site_name
    if site.tagline:
        meta_title = f"{site.site_name} | {site.tagline}"
    desc = (site.tagline or "").strip() or (getattr(site, "newsletter_description", "") or "").strip()
    meta_description = desc[:320] if desc else f"Welcome to {site.site_name}."
    return render(
        request,
        "main/home.html",
        {
            "hero_slides": hero_slides,
            "services": services,
            "founder_purpose": founder_purpose,
            "events": events,
            "meta_title": meta_title,
            "meta_description": meta_description,
        },
    )


@cache_page(60 * 15)
def about_view(request):
    # Get about page content from DynamicPage model
    about_page = DynamicPage.objects.filter(slug="about", is_active=True).first()
    return render(
        request,
        "main/about.html",
        {
            "about_page": about_page,
            "meta_title": "About | Nairobi Chapel Ngong Hills",
            "meta_description": "Learn about Nairobi Chapel Ngong Hills: our history, mission, vision, and values. Join our community of faith.",
        },
    )


def blog_view(request):
    from django.http import JsonResponse
    categories = BlogCategory.objects.all().order_by("order")
    
    # Handle AJAX load more requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        page = int(request.GET.get('page', 1))
        per_page = 6
        offset = (page - 1) * per_page
        
        posts = BlogPost.objects.filter(is_published=True).order_by("-published_at", "order")[offset:offset + per_page]
        has_more = BlogPost.objects.filter(is_published=True).count() > offset + per_page
        
        posts_data = []
        for post in posts:
            posts_data.append({
                'title': post.title,
                'slug': post.slug,
                'excerpt': post.excerpt,
                'published_at': post.published_at.strftime('%B %d, %Y') if post.published_at else '',
                'featured_image_url': post.featured_image_url or '',
                'detail_url': f'/blog/{post.slug}/',
            })
        
        return JsonResponse({
            'posts': posts_data,
            'has_more': has_more,
            'next_page': page + 1 if has_more else None,
        })
    
    # Initial page load - show first 6 posts
    posts = BlogPost.objects.filter(is_published=True).order_by("-published_at", "order")[:6]
    total_posts = BlogPost.objects.filter(is_published=True).count()
    has_more = total_posts > 6
    
    return render(
        request,
        "main/blog.html",
        {
            "categories": categories,
            "posts": posts,
            "has_more": has_more,
            "next_page": 2 if has_more else None,
            "meta_title": "Blog | Nairobi Chapel Ngong Hills",
            "meta_description": "Latest news, sermons, and updates from Nairobi Chapel Ngong Hills.",
        },
    )


def blog_detail_view(request, slug):
    post = get_object_or_404(BlogPost.objects.filter(is_published=True), slug=slug)
    other_posts = BlogPost.objects.filter(is_published=True).exclude(pk=post.pk).order_by("-published_at", "order")[:6]
    return render(
        request,
        "main/blog_detail.html",
        {
            "post": post,
            "other_posts": other_posts,
            "meta_title": f"{post.title} | Nairobi Chapel Ngong Hills",
            "meta_description": post.excerpt[:160] if post.excerpt else None,
        },
    )


def shop_view(request):
    products = Product.objects.filter(is_active=True).order_by("order")
    page_copy = PageCopy.objects.filter(page_slug="shop").first()
    return render(
        request,
        "main/shop.html",
        {
            "products": products,
            "page_copy": page_copy,
            "meta_title": getattr(page_copy, "meta_title", None) or "Shop | Nairobi Chapel Ngong Hills",
            "meta_description": getattr(page_copy, "meta_description", None) or "Get Nairobi Chapel merchandise and show your church pride.",
        },
    )


def contact_view(request):
    from django.shortcuts import redirect
    from django.contrib import messages
    from django.http import JsonResponse
    from django.core.mail import send_mail
    from django.conf import settings
    from .models import ContactSubmission

    page_copy = PageCopy.objects.filter(page_slug="contact").first()
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        email = (request.POST.get("email") or "").strip()
        subject = (request.POST.get("subject") or "").strip()
        message = (request.POST.get("message") or "").strip()
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

        if name and email and subject and message:
            # Save to database
            ContactSubmission.objects.create(name=name, email=email, subject=subject, message=message)

            # Send email to info@rosecolouredlens.org
            try:
                email_body = f"""
New Contact Form Submission from Rose Coloured Lens Website

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
This message was sent from the contact form on the Rose Coloured Lens website.
"""
                send_mail(
                    subject=f"Contact Form: {subject}",
                    message=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['info@rosecolouredlens.org'],
                    fail_silently=False,
                )
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Failed to send contact email: {e}")

            # Send auto-reply to sender
            try:
                auto_reply_body = f"""
Dear {name},

Thank you for contacting Rose Coloured Lens (NPC). We have received your message and will get back to you soonest.

Your message:
Subject: {subject}
{message}

Best regards,
Rose Coloured Lens Team

---
Equal Opportunity | SustainAbility | Visually Impaired Professionals (VIP's)
"""
                send_mail(
                    subject="We've received your message - Rose Coloured Lens",
                    message=auto_reply_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Failed to send auto-reply email: {e}")

            if is_ajax:
                return JsonResponse({"success": True, "message": "Thank you. Your message has been sent and we will get back to you soon."})
            messages.success(request, "Thank you. Your message has been sent and we will get back to you soon.")
            return redirect("contact")

        if is_ajax:
            return JsonResponse({"success": False, "message": "Please fill in all fields."}, status=400)
        messages.error(request, "Please fill in all fields.")

    return render(
        request,
        "main/contact.html",
        {
            "page_copy": page_copy,
            "meta_title": getattr(page_copy, "meta_title", None) or "Contact | Nairobi Chapel Ngong Hills",
            "meta_description": getattr(page_copy, "meta_description", None) or "Get in touch with Nairobi Chapel Ngong Hills. We'd love to hear from you!",
        },
    )


@require_http_methods(["GET", "POST"])
def donate_view(request):
    page_copy = PageCopy.objects.filter(page_slug="give").first() or PageCopy.objects.filter(
        page_slug="donate"
    ).first()

    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        reason = (request.POST.get("reason") or "").strip()
        amount_raw = (request.POST.get("amount") or "").strip()
        errors = []
        if not name:
            errors.append("Please enter your name.")
        if not reason:
            errors.append("Please share a reason for giving.")
        if not amount_raw:
            errors.append("Please enter an amount.")
        else:
            try:
                amount_val = float(amount_raw.replace(",", ""))
                if amount_val <= 0:
                    errors.append("Amount must be greater than zero.")
            except ValueError:
                errors.append("Please enter a valid amount.")
        for err in errors:
            messages.error(request, err)
        if not errors:
            messages.success(
                request,
                "Thank you for your generosity. Our team will follow up with payment options to complete your gift.",
            )
            return redirect("give")

    give_form = {}
    if request.method == "POST":
        give_form = {
            "name": request.POST.get("name", ""),
            "reason": request.POST.get("reason", ""),
            "amount": request.POST.get("amount", ""),
        }

    return render(
        request,
        "main/donate.html",
        {
            "page_copy": page_copy,
            "give_form": give_form,
            "meta_title": getattr(page_copy, "meta_title", None) or "Give | Nairobi Chapel Ngong Hills",
            "meta_description": getattr(page_copy, "meta_description", None) or "Support Nairobi Chapel Ngong Hills. Your generous giving helps us continue our ministries and community work.",
        },
    )


# url_name (underscore) → DynamicPage.slug (may use hyphens)
_FIXED_ROUTE_SLUGS = {
    "club_fusion": "club-fusion",
    "bible_study": "bible-study",
}


@cache_page(60 * 15)
def generic_page_view(request, slug=None):
    """Generic view for dynamically created pages like pastoral, egroups, prayer, etc."""
    if slug is None:
        raw_name = request.resolver_match.url_name
        effective_slug = _FIXED_ROUTE_SLUGS.get(raw_name, raw_name)
        dynamic_page = DynamicPage.objects.filter(slug=effective_slug, is_active=True).first()
    else:
        effective_slug = slug
        dynamic_page = DynamicPage.objects.filter(slug=slug, is_active=True).first()

    sermon_youtube_videos = None
    youtube_feed_error = None
    youtube_channel_handle = getattr(settings, "YOUTUBE_SERMON_CHANNEL_HANDLE", "ncngonghills").strip().lstrip("@")
    youtube_channel_url = f"https://www.youtube.com/@{youtube_channel_handle}"

    if effective_slug == "sermon":
        from .youtube_api import get_channel_latest_videos

        sermon_youtube_videos, youtube_feed_error = get_channel_latest_videos(
            youtube_channel_handle, max_results=10
        )

    if dynamic_page:
        page_title = dynamic_page.title
        page_subtitle = dynamic_page.subtitle
        header_text = dynamic_page.header_text
        content = dynamic_page.content
        content_2 = dynamic_page.content_2
        image_url = dynamic_page.image_url
        alt_text = dynamic_page.alt_text
        cta_text = dynamic_page.cta_text
        cta_url = dynamic_page.cta_url
        cta_text_2 = dynamic_page.cta_text_2
        cta_url_2 = dynamic_page.cta_url_2
        template = dynamic_page.template
        breadcrumb = dynamic_page.title
        meta_title = dynamic_page.get_meta_title()
        meta_description = dynamic_page.meta_description
    else:
        raise Http404(f"Page not found: {effective_slug}")

    pastoral_sections = []
    if effective_slug == "pastoral":
        pastoral_sections = list(
            PastoralTeamSection.objects.filter(is_active=True).order_by("order", "id")[:6]
        )

    bible_study_resources = []
    if effective_slug == "bible-study":
        bible_study_resources = list(
            BibleStudyResource.objects.filter(is_active=True).order_by("-session_date", "order", "id")
        )

    return render(
        request,
        "main/generic_page.html",
        {
            "dynamic_page": dynamic_page,
            "page_title": page_title,
            "page_subtitle": page_subtitle,
            "header_text": header_text,
            "content": content,
            "content_2": content_2,
            "image_url": image_url,
            "alt_text": alt_text,
            "cta_text": cta_text,
            "cta_url": cta_url,
            "cta_text_2": cta_text_2,
            "cta_url_2": cta_url_2,
            "template": template,
            "page_name": effective_slug,
            "breadcrumb": breadcrumb,
            "meta_title": f"{meta_title} | Nairobi Chapel Ngong Hills",
            "meta_description": meta_description,
            "sermon_youtube_videos": sermon_youtube_videos,
            "youtube_feed_error": youtube_feed_error,
            "youtube_channel_handle": youtube_channel_handle,
            "youtube_channel_url": youtube_channel_url,
            "pastoral_sections": pastoral_sections,
            "bible_study_resources": bible_study_resources,
        },
    )


def dynamic_page_catchall(request, slug):
    """Catch-all view for any dynamic page by slug."""
    return generic_page_view(request, slug=slug)


def page_not_found_view(request, exception=None):
    page_copy = PageCopy.objects.filter(page_slug="404").first()
    return render(
        request,
        "main/404.html",
        {"page_copy": page_copy},
        status=404,
    )
