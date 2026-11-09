import json
import urllib.error

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from . import youtube_utils
from .forms import ContactForm
from .models import (
    BibleStudyContent,
    BibleStudyGuide,
    ClubFusion,
    ClubFusionResource,
    EGroup,
    Event,
    GalleryAlbum,
    GivePage,
    HomeAbout,
    HomeHero,
    Membership,
    Mens,
    OurServices,
    Pastorate,
    Plugin,
    Quest,
    Volunteer,
    Womens,
)


def index(request):
    now = timezone.now()
    home_upcoming_events = Event.objects.filter(is_published=True, start_at__gte=now).order_by(
        "start_at", "sort_order", "id"
    )[:4]
    home_hero = (
        HomeHero.objects.filter(is_published=True)
        .prefetch_related("slides")
        .order_by("id")
        .first()
    )
    home_hero_slides = list(home_hero.slides.all()) if home_hero else []
    home_about = HomeAbout.objects.filter(is_published=True).order_by("id").first()
    home_services = OurServices.objects.filter(is_published=True).order_by("id").first()
    return render(
        request,
        "index.html",
        {
            "home_upcoming_events": home_upcoming_events,
            "home_hero": home_hero,
            "home_hero_slides": home_hero_slides,
            "home_about": home_about,
            "home_services": home_services,
        },
    )


def pastorate(request):
    pastorate_members = Pastorate.objects.filter(is_published=True)
    return render(
        request,
        "pastorate.html",
        {"pastorate_members": pastorate_members},
    )


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        wants_json = request.headers.get("x-requested-with") == "XMLHttpRequest"

        if form.is_valid():
            recipient = getattr(settings, "CONTACT_EMAIL_RECIPIENT", "ncngonghills@gmail.com")
            subject_line = f"[NCN Contact] {form.cleaned_data['subject']}"
            body = (
                f"Name: {form.cleaned_data['name']}\n"
                f"Email: {form.cleaned_data['email']}\n"
                f"Phone: {form.cleaned_data['phone']}\n\n"
                f"{form.cleaned_data['message']}"
            )
            if not getattr(settings, "EMAIL_HOST_PASSWORD", ""):
                if wants_json:
                    return JsonResponse(
                        {"ok": False, "error": "email_not_configured"},
                        status=503,
                    )
                form.add_error(None, "Email is not configured on the server.")
            else:
                try:
                    send_mail(
                        subject_line,
                        body,
                        settings.DEFAULT_FROM_EMAIL,
                        [recipient],
                        fail_silently=False,
                    )
                    if wants_json:
                        return JsonResponse({"ok": True})
                    return redirect("contact")
                except Exception:
                    if wants_json:
                        return JsonResponse({"ok": False, "error": "send_failed"}, status=500)
                    form.add_error(
                        None,
                        "Sorry, we could not send your message. Please try again later or email us directly.",
                    )
        elif wants_json:
            return JsonResponse({"ok": False, "errors": form.errors}, status=400)
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})


def egroups(request):
    qs = EGroup.objects.filter(is_published=True)
    egroup_intros = list(qs.filter(kind=EGroup.Kind.INTRO).order_by("sort_order", "id"))
    egroup_lede = qs.filter(kind=EGroup.Kind.LEDE).order_by("sort_order", "id").first()
    egroup_pillars = qs.filter(kind=EGroup.Kind.PILLAR).order_by("sort_order", "id")
    return render(
        request,
        "egroups.html",
        {
            "egroup_intros": egroup_intros,
            "egroup_lede": egroup_lede,
            "egroup_pillars": egroup_pillars,
        },
    )


def plugin(request):
    qs = Plugin.objects.filter(is_published=True)
    plugin_lead = qs.filter(kind=Plugin.Kind.LEAD).order_by("sort_order", "id").first()
    plugin_about = qs.filter(kind=Plugin.Kind.ABOUT).order_by("sort_order", "id").first()
    plugin_obj_title = (
        qs.filter(kind=Plugin.Kind.OBJECTIVES_TITLE).order_by("sort_order", "id").first()
    )
    plugin_objectives = qs.filter(kind=Plugin.Kind.OBJECTIVE).order_by("sort_order", "id")
    plugin_how = qs.filter(kind=Plugin.Kind.HOW).order_by("sort_order", "id").first()
    return render(
        request,
        "plugin.html",
        {
            "plugin_lead": plugin_lead,
            "plugin_about": plugin_about,
            "plugin_obj_title": plugin_obj_title,
            "plugin_objectives": plugin_objectives,
            "plugin_how": plugin_how,
        },
    )


def club_fusion(request):
    club_fusion_sections = ClubFusion.objects.filter(is_published=True)
    club_fusion_resources = ClubFusionResource.objects.filter(is_published=True).order_by(
        "-resource_date", "-created_at", "sort_order", "id"
    )
    return render(
        request,
        "club_fusion.html",
        {
            "club_fusion_sections": club_fusion_sections,
            "club_fusion_resources": club_fusion_resources,
        },
    )


def quest(request):
    quest_sections = Quest.objects.filter(is_published=True)
    for section in quest_sections:
        points = []
        if section.bullet_points:
            points = [line.strip() for line in section.bullet_points.splitlines() if line.strip()]
        section.points = points
    return render(request, "quest.html", {"quest_sections": quest_sections})


def mens_ministry(request):
    mens_sections = Mens.objects.filter(is_published=True)
    return render(request, "mens_ministry.html", {"mens_sections": mens_sections})


def womens_ministry(request):
    womens_sections = Womens.objects.filter(is_published=True)
    return render(request, "womens_ministry.html", {"womens_sections": womens_sections})


def sermon(request):
    live_videos: list = []
    videos: list = []
    error_msg = None
    api_key = (getattr(settings, "YOUTUBE_API_KEY", "") or "").strip()
    handle = getattr(settings, "YOUTUBE_CHANNEL_HANDLE", "ncngonghills")

    if not api_key:
        error_msg = "YouTube API key is not configured."
    else:
        try:
            channel_id, playlist_id = youtube_utils.resolve_channel(api_key, handle)
            if not channel_id or not playlist_id:
                error_msg = "Could not find this YouTube channel."
            else:
                live_videos = youtube_utils.get_live_videos(api_key, channel_id)
                exclude = {v["video_id"] for v in live_videos}
                videos = youtube_utils.get_recent_uploads_excluding(
                    api_key, playlist_id, exclude, max_results=30
                )
        except urllib.error.HTTPError as e:
            try:
                body = json.loads(e.read().decode())
                err = body.get("error") or {}
                error_msg = err.get("message") or f"YouTube API error ({e.code})."
            except Exception:
                error_msg = f"YouTube API error ({e.code})."
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
            error_msg = f"Could not load videos: {e}"

    return render(
        request,
        "sermon.html",
        {
            "live_videos": live_videos,
            "videos": videos,
            "error_msg": error_msg,
        },
    )


def bible_study(request):
    bible_study_content = (
        BibleStudyContent.objects.filter(is_published=True).order_by("sort_order", "id").first()
    )
    bible_study_guides = BibleStudyGuide.objects.filter(is_published=True).order_by(
        "-created_at", "-study_date", "sort_order", "id"
    )
    return render(
        request,
        "bible_study.html",
        {
            "bible_study_content": bible_study_content,
            "bible_study_guides": bible_study_guides,
        },
    )


def membership(request):
    membership = Membership.objects.filter(is_published=True).order_by("id").first()
    return render(request, "membership.html", {"membership": membership})


def volunteer(request):
    volunteer = Volunteer.objects.filter(is_published=True).order_by("id").first()
    return render(request, "volunteer.html", {"volunteer": volunteer})


def events(request):
    now = timezone.now()
    upcoming_events = Event.objects.filter(is_published=True, start_at__gte=now).order_by(
        "start_at", "sort_order", "id"
    )
    past_events = Event.objects.filter(is_published=True, start_at__lt=now).order_by(
        "-start_at", "sort_order", "id"
    )
    return render(
        request,
        "events.html",
        {
            "upcoming_events": upcoming_events,
            "past_events": past_events,
        },
    )


def give(request):
    give_page = GivePage.objects.filter(is_published=True).order_by("id").first()
    return render(request, "give.html", {"give_page": give_page})


def gallery_list(request):
    gallery_albums = (
        GalleryAlbum.objects.filter(is_published=True)
        .prefetch_related("images")
        .order_by("-created_at", "-event_date", "id")
    )
    return render(request, "gallery_list.html", {"gallery_albums": gallery_albums})


def gallery_detail(request, slug):
    album = get_object_or_404(
        GalleryAlbum.objects.prefetch_related("images"),
        slug=slug,
        is_published=True,
    )
    gallery_images = album.images.order_by("-id")
    return render(
        request,
        "gallery_detail.html",
        {
            "album": album,
            "gallery_images": gallery_images,
        },
    )


def page_not_found(request, exception):
    return render(request, "404.html", status=404)
