import re

from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.db import models
from django.db.models import Max
from django.utils.html import format_html, format_html_join

from .forms import GalleryAlbumAdminForm, HomeHeroAdminForm

from .models import (
    BibleStudyContent,
    BibleStudyGuide,
    ClubFusion,
    ClubFusionResource,
    EGroup,
    Event,
    GalleryAlbum,
    GalleryImage,
    GivePage,
    HomeAbout,
    HomeHero,
    HomeHeroSlide,
    Membership,
    Mens,
    OurServices,
    Pastorate,
    Plugin,
    Quest,
    Volunteer,
    Womens,
)

admin.site.site_header = "Nairobi Chapel Ngong Hills"
admin.site.site_title = "Nairobi Chapel Ngong Hills"
admin.site.index_title = "Nairobi Chapel Ngong Hills"


def _plain_preview(text, max_len=60):
    if not text:
        return "—"
    s = re.sub(r"<[^>]+>", " ", str(text))
    s = " ".join(s.split())
    if len(s) > max_len:
        return s[:max_len] + "…"
    return s


class CKEditorAdminMixin:
    """
    Use CKEditor for all TextField inputs. Exclude Quest.bullet_points (one item per line).
    """

    ckeditor_exclude_text_fields = frozenset({"bullet_points"})

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if isinstance(db_field, models.TextField) and db_field.name not in self.ckeditor_exclude_text_fields:
            kwargs["widget"] = CKEditorWidget(config_name="default")
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(Plugin)
class PluginAdmin(CKEditorAdminMixin, admin.ModelAdmin):
    list_display = ("kind", "title", "sort_order", "is_published", "body_preview")
    list_editable = ("sort_order", "is_published")
    list_filter = ("kind", "is_published")
    search_fields = ("title", "body")
    ordering = ("kind", "sort_order", "id")

    @admin.display(description="Body preview")
    def body_preview(self, obj):
        return _plain_preview(obj.body)


@admin.register(EGroup)
class EGroupAdmin(CKEditorAdminMixin, admin.ModelAdmin):
    list_display = ("kind", "title", "sort_order", "is_published", "body_preview")
    list_editable = ("sort_order", "is_published")
    list_filter = ("kind", "is_published")
    search_fields = ("title", "body")
    ordering = ("kind", "sort_order", "id")

    @admin.display(description="Body preview")
    def body_preview(self, obj):
        return _plain_preview(obj.body)


@admin.register(Pastorate)
class PastorateAdmin(CKEditorAdminMixin, admin.ModelAdmin):
    list_display = ("name", "role", "sort_order", "is_published", "photo_preview")
    list_editable = ("sort_order", "is_published")
    list_filter = ("is_published",)
    search_fields = ("name", "role", "bio")
    ordering = ("sort_order", "name")

    @admin.display(description="Photo")
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height:48px;max-width:48px;object-fit:cover;" alt="" />',
                obj.photo.url,
            )
        return "—"


@admin.register(ClubFusion)
class ClubFusionAdmin(CKEditorAdminMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "kicker",
        "sort_order",
        "is_published",
        "image_on_left",
        "image_preview",
    )
    list_editable = ("sort_order", "is_published", "image_on_left")
    list_filter = ("is_published", "image_on_left")
    search_fields = ("title", "kicker", "body")
    ordering = ("sort_order", "id")

    @admin.display(description="Image")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:48px;max-width:48px;object-fit:cover;" alt="" />',
                obj.image.url,
            )
        return "—"


@admin.register(ClubFusionResource)
class ClubFusionResourceAdmin(admin.ModelAdmin):
    list_display = ("resource_date", "note", "sort_order", "is_published", "resource_link")
    list_editable = ("sort_order", "is_published")
    list_filter = ("is_published", "resource_date")
    search_fields = ("note",)
    ordering = ("-resource_date", "-created_at", "sort_order", "id")
    date_hierarchy = "resource_date"

    @admin.display(description="View / Download")
    def resource_link(self, obj):
        if obj.resource_file:
            return format_html(
                '<a href="{}" target="_blank" rel="noopener">View</a> &nbsp;|&nbsp; '
                '<a href="{}" download>Download</a>',
                obj.resource_file.url,
                obj.resource_file.url,
            )
        return "—"


@admin.register(Quest)
class QuestAdmin(CKEditorAdminMixin, admin.ModelAdmin):
    list_display = (
        "heading",
        "sort_order",
        "is_published",
        "image_on_right",
        "image_preview",
    )
    list_editable = ("sort_order", "is_published", "image_on_right")
    list_filter = ("is_published", "image_on_right")
    search_fields = ("heading", "body", "bullet_points")
    ordering = ("sort_order", "id")

    @admin.display(description="Image")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:48px;max-width:48px;object-fit:cover;" alt="" />',
                obj.image.url,
            )
        return "—"


@admin.register(Mens)
class MensAdmin(CKEditorAdminMixin, admin.ModelAdmin):
    list_display = (
        "heading",
        "sort_order",
        "is_published",
        "image_on_right",
        "image_preview",
        "image_secondary_preview",
    )
    list_editable = ("sort_order", "is_published", "image_on_right")
    list_filter = ("is_published", "image_on_right")
    search_fields = ("heading", "body")
    ordering = ("sort_order", "id")

    @admin.display(description="Image")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:48px;max-width:48px;object-fit:cover;" alt="" />',
                obj.image.url,
            )
        return "—"

    @admin.display(description="Image 2")
    def image_secondary_preview(self, obj):
        if obj.image_secondary:
            return format_html(
                '<img src="{}" style="max-height:48px;max-width:48px;object-fit:cover;" alt="" />',
                obj.image_secondary.url,
            )
        return "—"


@admin.register(Womens)
class WomensAdmin(CKEditorAdminMixin, admin.ModelAdmin):
    list_display = (
        "heading",
        "sort_order",
        "is_published",
        "image_on_right",
        "image_preview",
        "image_secondary_preview",
    )
    list_editable = ("sort_order", "is_published", "image_on_right")
    list_filter = ("is_published", "image_on_right")
    search_fields = ("heading", "body")
    ordering = ("sort_order", "id")

    @admin.display(description="Image")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:48px;max-width:48px;object-fit:cover;" alt="" />',
                obj.image.url,
            )
        return "—"

    @admin.display(description="Image 2")
    def image_secondary_preview(self, obj):
        if obj.image_secondary:
            return format_html(
                '<img src="{}" style="max-height:48px;max-width:48px;object-fit:cover;" alt="" />',
                obj.image_secondary.url,
            )
        return "—"


@admin.register(BibleStudyContent)
class BibleStudyContentAdmin(CKEditorAdminMixin, admin.ModelAdmin):
    list_display = ("heading", "sort_order", "is_published")
    list_editable = ("sort_order", "is_published")
    list_filter = ("is_published",)
    search_fields = ("heading", "body")
    ordering = ("sort_order", "id")


@admin.register(BibleStudyGuide)
class BibleStudyGuideAdmin(CKEditorAdminMixin, admin.ModelAdmin):
    list_display = ("study_date", "notes", "created_at", "sort_order", "is_published", "guide_download")
    list_editable = ("sort_order", "is_published")
    list_filter = ("is_published", "study_date")
    search_fields = ("notes",)
    ordering = ("-created_at", "-study_date", "sort_order", "id")
    date_hierarchy = "study_date"

    @admin.display(description="Guide")
    def guide_download(self, obj):
        if obj.guide_file:
            return format_html('<a href="{}" target="_blank" rel="noopener">Download</a>', obj.guide_file.url)
        return "—"


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    form = GalleryAlbumAdminForm
    list_display = ("title", "event_date", "slug", "is_published", "image_count", "cover_preview")
    list_editable = ("is_published",)
    list_filter = ("is_published", "event_date")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "event_date"
    ordering = ("-created_at", "-event_date", "id")
    readonly_fields = ("existing_images_preview",)

    def get_fieldsets(self, request, obj=None):
        photo_fields = ["upload_images"]
        if obj:
            photo_fields.append("existing_images_preview")
        return (
            (None, {"fields": ("title", "event_date", "slug", "is_published")}),
            (
                "Photos",
                {
                    "fields": tuple(photo_fields),
                    "description": "Use the file input below to select multiple photos at once.",
                },
            ),
        )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        uploads = form.cleaned_data.get("upload_images") or request.FILES.getlist("upload_images")
        if not uploads:
            return
        max_order = obj.images.aggregate(Max("sort_order"))["sort_order__max"]
        next_order = 0 if max_order is None else max_order + 1
        for offset, uploaded in enumerate(uploads):
            GalleryImage.objects.create(
                album=obj,
                image=uploaded,
                sort_order=next_order + offset,
            )

    @admin.display(description="Images")
    def image_count(self, obj):
        return obj.images.count()

    @admin.display(description="Cover")
    def cover_preview(self, obj):
        cover = obj.cover_image
        if cover and cover.image:
            return format_html(
                '<img src="{}" style="max-height:48px;max-width:64px;object-fit:cover;" alt="" />',
                cover.image.url,
            )
        return "—"

    @admin.display(description="Current photos")
    def existing_images_preview(self, obj):
        if not obj or not obj.pk:
            return "Save the album first, then upload photos below."
        images = obj.images.order_by("-id")
        if not images:
            return "No photos yet."
        thumbs = []
        for image in images:
            if image.image:
                thumbs.append(
                    format_html(
                        '<img src="{}" style="height:56px;width:56px;object-fit:cover;margin:0 6px 6px 0;border-radius:4px;" alt="" />',
                        image.image.url,
                    )
                )
        return format_html(
            '<div style="display:flex;flex-wrap:wrap;">{}</div>',
            format_html_join("", "{}", ((thumb,) for thumb in thumbs)),
        )


@admin.register(Event)
class EventAdmin(CKEditorAdminMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "start_at",
        "sort_order",
        "is_published",
        "button_text",
        "is_upcoming",
        "image_preview",
    )
    list_editable = ("sort_order", "is_published", "button_text")
    list_filter = ("is_published",)
    search_fields = ("title", "organizer", "venue", "button_text")
    ordering = ("start_at", "sort_order", "id")
    date_hierarchy = "start_at"

    @admin.display(boolean=True, description="Upcoming")
    def is_upcoming(self, obj):
        from django.utils import timezone

        return obj.start_at >= timezone.now()

    @admin.display(description="Image")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:48px;max-width:48px;object-fit:cover;" alt="" />',
                obj.image.url,
            )
        return "—"


@admin.register(GivePage)
class GivePageAdmin(CKEditorAdminMixin, admin.ModelAdmin):
    list_display = ("lead_title", "is_published")
    list_editable = ("is_published",)
    list_filter = ("is_published",)
    search_fields = ("lead_title", "lead_text", "mpesa_title", "mpesa_body", "cheque_title", "cheque_body")
    fieldsets = (
        (
            "Intro",
            {"fields": ("lead_title", "lead_text")},
        ),
        (
            "M-Pesa card",
            {"fields": ("mpesa_title", "mpesa_body")},
        ),
        (
            "Cheque card",
            {"fields": ("cheque_title", "cheque_body")},
        ),
        (None, {"fields": ("is_published",)}),
    )

    def has_add_permission(self, request):
        return GivePage.objects.count() < 1


@admin.register(Membership)
class MembershipAdmin(CKEditorAdminMixin, admin.ModelAdmin):
    list_display = ("heading", "is_published", "hero_preview")
    list_editable = ("is_published",)
    list_filter = ("is_published",)
    search_fields = ("heading", "subtitle", "body")
    fieldsets = (
        (None, {"fields": ("heading", "subtitle", "body", "hero_image", "button_text", "button_url", "is_published")}),
    )

    @admin.display(description="Hero image")
    def hero_preview(self, obj):
        if obj.hero_image:
            return format_html(
                '<img src="{}" style="max-height:48px;max-width:80px;object-fit:cover;" alt="" />',
                obj.hero_image.url,
            )
        return "—"


@admin.register(Volunteer)
class VolunteerAdmin(CKEditorAdminMixin, admin.ModelAdmin):
    list_display = ("heading", "is_published", "hero_preview")
    list_editable = ("is_published",)
    list_filter = ("is_published",)
    search_fields = ("heading", "subtitle", "body")
    fieldsets = (
        (None, {"fields": ("heading", "subtitle", "body", "hero_image", "button_text", "button_url", "is_published")}),
    )

    @admin.display(description="Hero image")
    def hero_preview(self, obj):
        if obj.hero_image:
            return format_html(
                '<img src="{}" style="max-height:48px;max-width:80px;object-fit:cover;" alt="" />',
                obj.hero_image.url,
            )
        return "—"


class HomeHeroSlideInline(admin.TabularInline):
    model = HomeHeroSlide
    extra = 1
    fields = ("image", "sort_order")
    ordering = ("sort_order", "id")


@admin.register(HomeHero)
class HomeHeroAdmin(CKEditorAdminMixin, admin.ModelAdmin):
    form = HomeHeroAdminForm
    list_display = ("title", "slide_count", "is_published")
    list_editable = ("is_published",)
    list_filter = ("is_published",)
    inlines = (HomeHeroSlideInline,)
    fieldsets = (
        ("Content", {"fields": ("title", "body", "button_text", "button_url", "is_published")}),
        (
            "Hero images",
            {
                "fields": ("upload_slides",),
                "description": "Upload any number of images, or manage individual slides below.",
            },
        ),
    )

    def has_add_permission(self, request):
        return HomeHero.objects.count() < 1

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        uploads = form.cleaned_data.get("upload_slides") or request.FILES.getlist("upload_slides")
        if not uploads:
            return
        max_order = obj.slides.aggregate(Max("sort_order"))["sort_order__max"]
        next_order = 0 if max_order is None else max_order + 1
        for offset, uploaded in enumerate(uploads):
            HomeHeroSlide.objects.create(
                hero=obj,
                image=uploaded,
                sort_order=next_order + offset,
            )

    @admin.display(description="Slides")
    def slide_count(self, obj):
        return obj.slides.count()


@admin.register(HomeAbout)
class HomeAboutAdmin(CKEditorAdminMixin, admin.ModelAdmin):
    list_display = ("section_title", "heading", "is_published")
    list_editable = ("is_published",)
    list_filter = ("is_published",)
    fieldsets = (
        ("Headings", {"fields": ("section_title", "heading", "body", "is_published")}),
        (
            "Points",
            {
                "fields": (
                    "point_1_title",
                    "point_1_body",
                    "point_1_icon",
                    "point_2_title",
                    "point_2_body",
                    "point_2_icon",
                )
            },
        ),
        ("Images", {"fields": ("image_1", "image_2")}),
    )

    def has_add_permission(self, request):
        return HomeAbout.objects.count() < 1


@admin.register(OurServices)
class OurServicesAdmin(CKEditorAdminMixin, admin.ModelAdmin):
    list_display = ("section_title", "heading", "is_published")
    list_editable = ("is_published",)
    list_filter = ("is_published",)
    fieldsets = (
        ("Section headings", {"fields": ("section_title", "heading", "is_published")}),
        (
            "Card 1",
            {"fields": ("card_1_title", "card_1_body", "card_1_bg_image", "card_1_icon", "card_1_button_text", "card_1_button_url")},
        ),
        (
            "Card 2",
            {"fields": ("card_2_title", "card_2_body", "card_2_bg_image", "card_2_icon", "card_2_button_text", "card_2_button_url")},
        ),
        (
            "Card 3",
            {"fields": ("card_3_title", "card_3_body", "card_3_bg_image", "card_3_icon", "card_3_button_text", "card_3_button_url")},
        ),
    )

    def has_add_permission(self, request):
        return OurServices.objects.count() < 1
