"""
Django Admin — models that power the public site only.

Site pages are split: each route (About, Pastorate, Quest, …) has its own admin
entry via proxy models. Extra slugs use “Other site pages”.
"""
from django.contrib import admin
from django.contrib.auth.models import Group
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.conf import settings
import cloudinary
import cloudinary.uploader
from .models import (
    SiteSettings,
    HeroSlide,
    Service,
    WhatWeDoItem,
    AboutPreview,
    FounderPurposeBlock,
    CallToActionBlock,
    Event,
    PastoralTeamSection,
    BibleStudyResource,
    PageCopy,
    ContactPageCopy,
    GivePageCopy,
    ContactSubmission,
    DynamicPage,
    INDIVIDUAL_PAGE_SLUGS,
    AboutPage,
    PastoralCarePage,
    EgroupsPage,
    PrayerPage,
    ClubFusionPage,
    QuestPage,
    SermonPage,
    BibleStudyPage,
    MembershipPage,
    VolunteerPage,
    MensMinistryPage,
    WomensMinistryPage,
    OtherSitePage,
    BlogCategory,
    BlogPost,
    Product,
)

###############################################################################
# Cloudinary-backed admin uploads (device -> Cloudinary -> saved URL field)
#
# Your models store images as URLFields (e.g. image_url). In the admin we hide
# those URL inputs and provide file pickers instead; on save we upload the file
# to Cloudinary and store the returned secure_url back into the URL field.
###############################################################################

CLOUDINARY_UPLOAD_FOLDER = "rose-coloured-lens/admin"


def _cloudinary_upload_image(uploaded_file, *, folder: str) -> str:
    """Upload an image file to Cloudinary and return the secure URL."""
    cloud_name = getattr(settings, "CLOUDINARY_CLOUD_NAME", "")
    api_key = getattr(settings, "CLOUDINARY_API_KEY", "")
    api_secret = getattr(settings, "CLOUDINARY_API_SECRET", "")
    if not (cloud_name and api_key and api_secret):
        raise forms.ValidationError(
            "Cloudinary is not configured. Add CLOUDINARY_CLOUD_NAME / API_KEY / API_SECRET to your environment."
        )

    try:
        result = cloudinary.uploader.upload(
            uploaded_file,
            folder=folder,
            resource_type="image",
        )
    except Exception as exc:
        raise forms.ValidationError(f"Cloudinary upload failed: {exc}") from exc

    url = result.get("secure_url") or result.get("url")
    if not url:
        raise forms.ValidationError("Cloudinary upload succeeded but returned no URL.")
    return url


class SiteSettingsAdminForm(forms.ModelForm):
    logo_upload = forms.ImageField(
        required=False,
        help_text="Upload navbar logo from your device (replaces logo URL).",
    )
    favicon_upload = forms.ImageField(
        required=False,
        help_text="Upload favicon from your device (replaces favicon URL).",
    )

    # Hide URL inputs so admins upload from device only.
    logo_url = forms.CharField(required=False, widget=forms.HiddenInput())
    favicon_url = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = SiteSettings
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get("logo_upload"):
            instance.logo_url = _cloudinary_upload_image(
                self.cleaned_data["logo_upload"], folder=f"{CLOUDINARY_UPLOAD_FOLDER}/site"
            )
        if self.cleaned_data.get("favicon_upload"):
            instance.favicon_url = _cloudinary_upload_image(
                self.cleaned_data["favicon_upload"], folder=f"{CLOUDINARY_UPLOAD_FOLDER}/site"
            )
        if commit:
            instance.save()
        return instance


class HeroSlideAdminForm(forms.ModelForm):
    image_upload = forms.ImageField(required=False, help_text="Upload slide image from your device.")
    image_url = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = HeroSlide
        fields = "__all__"

    def clean(self):
        cleaned = super().clean()
        if not self.instance.pk and not cleaned.get("image_upload"):
            # Previously admins had to paste an image_url. Now we require upload.
            raise forms.ValidationError({"image_upload": "Please upload an image."})
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        upload = self.cleaned_data.get("image_upload")
        if upload:
            instance.image_url = _cloudinary_upload_image(
                upload, folder=f"{CLOUDINARY_UPLOAD_FOLDER}/hero-slides"
            )
        if commit:
            instance.save()
        return instance


class ServiceAdminForm(forms.ModelForm):
    image_upload = forms.ImageField(required=False, help_text="Upload service image from your device.")
    image_url = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Service
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)
        upload = self.cleaned_data.get("image_upload")
        if upload:
            instance.image_url = _cloudinary_upload_image(upload, folder=f"{CLOUDINARY_UPLOAD_FOLDER}/services")
        if commit:
            instance.save()
        return instance


class WhatWeDoItemAdminForm(forms.ModelForm):
    icon_upload = forms.ImageField(required=False, help_text="Upload icon image from your device.")
    icon_url = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = WhatWeDoItem
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)
        upload = self.cleaned_data.get("icon_upload")
        if upload:
            instance.icon_url = _cloudinary_upload_image(upload, folder=f"{CLOUDINARY_UPLOAD_FOLDER}/what-we-do")
        if commit:
            instance.save()
        return instance


class AboutPreviewAdminForm(forms.ModelForm):
    image_1_upload = forms.ImageField(required=False, help_text="Upload first about image from your device.")
    image_2_upload = forms.ImageField(required=False, help_text="Upload second about image from your device.")
    image_1_url = forms.CharField(required=False, widget=forms.HiddenInput())
    image_2_url = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = AboutPreview
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get("image_1_upload"):
            instance.image_1_url = _cloudinary_upload_image(
                self.cleaned_data["image_1_upload"], folder=f"{CLOUDINARY_UPLOAD_FOLDER}/about-preview"
            )
        if self.cleaned_data.get("image_2_upload"):
            instance.image_2_url = _cloudinary_upload_image(
                self.cleaned_data["image_2_upload"], folder=f"{CLOUDINARY_UPLOAD_FOLDER}/about-preview"
            )
        if commit:
            instance.save()
        return instance


class FounderPurposeBlockAdminForm(forms.ModelForm):
    image_1_upload = forms.ImageField(required=False, help_text="Upload first image from your device.")
    image_2_upload = forms.ImageField(required=False, help_text="Upload second image from your device.")
    image_1_url = forms.CharField(required=False, widget=forms.HiddenInput())
    image_2_url = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = FounderPurposeBlock
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get("image_1_upload"):
            instance.image_1_url = _cloudinary_upload_image(
                self.cleaned_data["image_1_upload"], folder=f"{CLOUDINARY_UPLOAD_FOLDER}/founder-purpose"
            )
        if self.cleaned_data.get("image_2_upload"):
            instance.image_2_url = _cloudinary_upload_image(
                self.cleaned_data["image_2_upload"], folder=f"{CLOUDINARY_UPLOAD_FOLDER}/founder-purpose"
            )
        if commit:
            instance.save()
        return instance


class EventAdminForm(forms.ModelForm):
    image_upload = forms.ImageField(required=False, help_text="Upload event image from your device.")
    image_url = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Event
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)
        upload = self.cleaned_data.get("image_upload")
        if upload:
            instance.image_url = _cloudinary_upload_image(upload, folder=f"{CLOUDINARY_UPLOAD_FOLDER}/events")
        if commit:
            instance.save()
        return instance


class ProductAdminForm(forms.ModelForm):
    image_upload = forms.ImageField(required=False, help_text="Upload product image from your device.")
    image_url = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Product
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)
        upload = self.cleaned_data.get("image_upload")
        if upload:
            instance.image_url = _cloudinary_upload_image(upload, folder=f"{CLOUDINARY_UPLOAD_FOLDER}/products")
        if commit:
            instance.save()
        return instance


# =============================================================================
# SITE SETTINGS
# =============================================================================

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Global site configuration (singleton)."""
    form = SiteSettingsAdminForm
    list_display = ("site_name", "contact_email", "updated_at")
    readonly_fields = ("updated_at",)

    def has_add_permission(self, request):
        return False if self.model.objects.exists() else True

    def has_delete_permission(self, request, obj=None):
        return False


# =============================================================================
# HOME PAGE
# =============================================================================

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    form = HeroSlideAdminForm
    list_display = ("title", "order", "is_active", "updated_at")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "subtitle")
    ordering = ("order",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    form = ServiceAdminForm
    list_display = ("title", "day_time", "location", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("title", "description", "location")
    ordering = ("order",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Service Information", {
            "fields": ("title", "description", "day_time", "location", "place")
        }),
        ("Media & Links", {
            "fields": ("image_upload", "image_url", "learn_more_url")
        }),
        ("Display Settings", {
            "fields": ("is_active", "order")
        }),
        ("Metadata", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )


@admin.register(WhatWeDoItem)
class WhatWeDoItemAdmin(admin.ModelAdmin):
    form = WhatWeDoItemAdminForm
    list_display = ("title", "order", "created_at")
    list_editable = ("order",)
    search_fields = ("title", "description")
    ordering = ("order",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(AboutPreview)
class AboutPreviewAdmin(admin.ModelAdmin):
    form = AboutPreviewAdminForm
    list_display = ("heading", "subheading", "updated_at")
    readonly_fields = ("updated_at",)

    def has_add_permission(self, request):
        return False if self.model.objects.exists() else True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(FounderPurposeBlock)
class FounderPurposeBlockAdmin(admin.ModelAdmin):
    form = FounderPurposeBlockAdminForm
    list_display = ("section_title", "subheading", "updated_at")
    readonly_fields = ("updated_at",)

    fieldsets = (
        ("Section Header", {
            "fields": ("section_title", "subheading")
        }),
        ("Introduction", {
            "fields": ("intro_paragraph_1", "intro_paragraph_2")
        }),
        ("Feature 1", {
            "fields": ("bullet_1_title", "bullet_1_text")
        }),
        ("Feature 2", {
            "fields": ("bullet_2_title", "bullet_2_text")
        }),
        ("Feature 3", {
            "fields": ("bullet_3_title", "bullet_3_text")
        }),
        ("Images", {
            "fields": ("image_1_upload", "image_1_url", "image_2_upload", "image_2_url")
        }),
    )

    def has_add_permission(self, request):
        return False if self.model.objects.exists() else True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CallToActionBlock)
class CallToActionBlockAdmin(admin.ModelAdmin):
    list_display = ("heading", "subheading", "updated_at")
    readonly_fields = ("updated_at",)

    fieldsets = (
        (None, {
            "fields": ("heading", "subheading", "body")
        }),
        ("Primary Button", {
            "fields": ("primary_button_text", "primary_button_url")
        }),
        ("Secondary Button", {
            "fields": ("secondary_button_text", "secondary_button_url")
        }),
    )

    def has_add_permission(self, request):
        return False if self.model.objects.exists() else True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Upcoming events on the home page."""
    form = EventAdminForm

    @admin.display(boolean=True, description="Watch online")
    def has_watch_online(self, obj):
        return bool(obj.watch_online_url)

    list_display = ("title", "event_date", "location", "has_watch_online", "is_published", "order")
    list_editable = ("is_published", "order")
    list_filter = ("is_published", "event_date")
    search_fields = ("title", "excerpt", "description", "location")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "event_date"

    fieldsets = (
        ("Event Information", {
            "fields": ("title", "slug", "excerpt")
        }),
        ("Details", {
            "fields": ("event_date", "location", "description", "watch_online_url")
        }),
        ("Media", {
            "fields": ("image_upload", "image_url")
        }),
        ("Publishing", {
            "fields": ("is_published", "order")
        }),
        ("Metadata", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )


class PastoralTeamSectionForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget(config_name="default"), required=False)
    image_upload = forms.ImageField(required=False, help_text="Upload profile image from your device.")
    image_url = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = PastoralTeamSection
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)
        upload = self.cleaned_data.get("image_upload")
        if upload:
            instance.image_url = _cloudinary_upload_image(
                upload, folder=f"{CLOUDINARY_UPLOAD_FOLDER}/pastoral"
            )
        if commit:
            instance.save()
        return instance


@admin.register(BibleStudyResource)
class BibleStudyResourceAdmin(admin.ModelAdmin):
    """Table rows on /bible-study/ under Resources."""
    list_display = ("session_date", "description", "document_url", "order", "is_active", "updated_at")
    list_display_links = ("session_date",)
    list_filter = ("is_active",)
    list_editable = ("order", "is_active")
    search_fields = ("description",)
    ordering = ("-session_date", "order", "id")
    readonly_fields = ("created_at", "updated_at")


@admin.register(PastoralTeamSection)
class PastoralTeamSectionAdmin(admin.ModelAdmin):
    """Six blocks on /pastoral/ (order 0–5); layout alternates by row index in the template."""
    form = PastoralTeamSectionForm
    list_display = ("name_heading", "order", "eyebrow", "is_active", "updated_at")
    list_display_links = ("name_heading",)
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name_heading", "subheading", "eyebrow")
    ordering = ("order", "id")


# =============================================================================
# CONTACT & PAGE TEXT
# =============================================================================

@admin.register(PageCopy)
class PageCopyAdmin(admin.ModelAdmin):
    """Intro/SEO text for contact, give, 404, etc. (page_slug matches URL purpose)."""
    list_display = ("page_slug", "heading", "updated_at")
    search_fields = ("page_slug", "heading", "body")
    readonly_fields = ("updated_at",)

    fieldsets = (
        (None, {
            "fields": ("page_slug",)
        }),
        ("SEO", {
            "fields": ("meta_title", "meta_description"),
            "classes": ("collapse",)
        }),
        ("Content", {
            "fields": ("heading", "subheading", "body")
        }),
    )


class FixedSlugPageCopyAdmin(admin.ModelAdmin):
    """Proxy admin: filter PageCopy by a fixed page_slug."""

    fixed_page_slug: str | None = None

    list_display = ("page_slug", "heading", "updated_at")
    search_fields = ("page_slug", "heading", "body")
    readonly_fields = ("page_slug", "updated_at")

    fieldsets = (
        (None, {
            "fields": ("page_slug",),
        }),
        ("SEO", {
            "fields": ("meta_title", "meta_description"),
            "classes": ("collapse",),
        }),
        ("Content", {
            "fields": ("heading", "subheading", "body"),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self.fixed_page_slug:
            qs = qs.filter(page_slug=self.fixed_page_slug)
        return qs

    def save_model(self, request, obj, form, change):
        if self.fixed_page_slug:
            obj.page_slug = self.fixed_page_slug
        super().save_model(request, obj, form, change)


@admin.register(ContactPageCopy)
class ContactPageCopyAdmin(FixedSlugPageCopyAdmin):
    fixed_page_slug = "contact"


@admin.register(GivePageCopy)
class GivePageCopyAdmin(FixedSlugPageCopyAdmin):
    fixed_page_slug = "give"


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "submitted_at", "read")
    list_filter = ("read", "submitted_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "submitted_at")
    date_hierarchy = "submitted_at"

    actions = ["mark_as_read", "mark_as_unread"]

    def mark_as_read(self, request, queryset):
        queryset.update(read=True)
    mark_as_read.short_description = "Mark selected as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(read=False)
    mark_as_unread.short_description = "Mark selected as unread"


# =============================================================================
# BLOG & SHOP (public /blog and /shop)
# =============================================================================

class BlogPostForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget(config_name="default"), required=False)
    featured_image_url = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = BlogPost
        fields = "__all__"


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    ordering = ("order", "name")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostForm
    list_display = ("title", "category", "published_at", "is_published", "order", "updated_at")
    list_filter = ("is_published", "category")
    list_editable = ("is_published", "order")
    search_fields = ("title", "excerpt", "slug", "body")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "published_at"
    ordering = ("-published_at", "order", "-created_at")

    fieldsets = (
        (None, {
            "fields": ("title", "slug", "excerpt", "body", "category"),
        }),
        ("Publishing", {
            "fields": ("published_at", "is_published", "order"),
        }),
        ("Featured image", {
            "fields": ("featured_image", "featured_image_url"),
            "description": "Upload an image file from your device (Cloudinary URL is synced automatically).",
        }),
        ("Metadata", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ("name", "price", "badge", "is_active", "order", "updated_at")
    list_filter = ("is_active",)
    list_editable = ("is_active", "order")
    search_fields = ("name", "description", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")
    ordering = ("order", "name")

    fieldsets = (
        (None, {
            "fields": ("name", "slug", "description", "price", "badge"),
        }),
        ("Media", {
            "fields": ("image_upload", "image_url"),
        }),
        ("Display", {
            "fields": ("is_active", "order"),
        }),
        ("Metadata", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


# =============================================================================
# SITE PAGES (one admin entry per route + “Other” for extra slugs)
# =============================================================================

def _dynamic_page_form(model_cls):
    """CKEditor on HTML fields; model is the concrete (proxy) class."""
    class _DynamicPageForm(forms.ModelForm):
        content = forms.CharField(widget=CKEditorWidget(config_name='default'), required=False)
        content_2 = forms.CharField(widget=CKEditorWidget(config_name='default'), required=False)
        header_text = forms.CharField(widget=CKEditorWidget(config_name='default'), required=False)
        image_upload = forms.ImageField(required=False, help_text="Upload header image from your device.")
        image_url = forms.CharField(required=False, widget=forms.HiddenInput())

        class Meta:
            model = model_cls
            fields = '__all__'

        def save(self, commit=True):
            instance = super().save(commit=False)
            upload = self.cleaned_data.get("image_upload")
            if upload:
                instance.image_url = _cloudinary_upload_image(
                    upload, folder=f"{CLOUDINARY_UPLOAD_FOLDER}/pages"
                )
            if commit:
                instance.save()
            return instance

    return _DynamicPageForm


_PAGE_FIELDSETS = (
    ("Basic Information", {
        "fields": ("slug", "title", "subtitle", "template", "order", "is_active"),
    }),
    ("SEO", {
        "fields": ("meta_title", "meta_description"),
        "classes": ("collapse",)
    }),
    ("Navigation Menu", {
        "fields": ("show_in_menu", "menu_placement", "menu_order"),
    }),
    ("Header Section", {
        "fields": ("header_text", "image_upload", "image_url", "alt_text"),
    }),
    ("Main Content", {
        "fields": ("content",),
    }),
    ("Secondary Content", {
        "fields": ("content_2",),
        "classes": ("collapse",)
    }),
    ("Call to Action Buttons", {
        "fields": ("cta_text", "cta_url", "cta_text_2", "cta_url_2"),
    }),
    ("Metadata", {
        "fields": ("created_at", "updated_at"),
        "classes": ("collapse",)
    }),
)


class FixedSlugPageAdmin(admin.ModelAdmin):
    """Single row per site route; slug is locked."""
    fixed_slug = None
    list_display = ("title", "is_active", "updated_at")
    list_editable = ("is_active",)
    list_display_links = ("title",)
    search_fields = ("title",)
    readonly_fields = ("slug", "created_at", "updated_at")
    fieldsets = _PAGE_FIELDSETS

    def get_queryset(self, request):
        return super().get_queryset(request).filter(slug=self.fixed_slug)

    def save_model(self, request, obj, form, change):
        obj.slug = self.fixed_slug
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        if DynamicPage.objects.filter(slug=self.fixed_slug).exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj)


_FIXED_PAGE_SPECS = (
    (AboutPage, "about"),
    (PastoralCarePage, "pastoral"),
    (MensMinistryPage, "mens-ministry"),
    (EgroupsPage, "egroups"),
    (PrayerPage, "prayer"),
    (ClubFusionPage, "club-fusion"),
    (QuestPage, "quest"),
    (SermonPage, "sermon"),
    (WomensMinistryPage, "womens-ministry"),
    (BibleStudyPage, "bible-study"),
    (MembershipPage, "membership"),
    (VolunteerPage, "volunteer"),
)

for _model_cls, _slug in _FIXED_PAGE_SPECS:
    _admin_cls = type(
        f"{_model_cls.__name__}Admin",
        (FixedSlugPageAdmin,),
        {
            "fixed_slug": _slug,
            "form": _dynamic_page_form(_model_cls),
        },
    )
    admin.site.register(_model_cls, _admin_cls)


@admin.register(OtherSitePage)
class OtherSitePageAdmin(admin.ModelAdmin):
    """Pages not covered by the fixed routes above (custom slugs / catch-all URLs)."""
    form = _dynamic_page_form(OtherSitePage)
    list_display = ("title", "slug", "template", "menu_placement", "is_active", "order", "updated_at")
    list_filter = ("is_active", "menu_placement", "template")
    list_editable = ("is_active", "order", "menu_placement", "template")
    search_fields = ("title", "slug", "content")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Basic Information", {
            "fields": ("slug", "title", "subtitle", "template", "order", "is_active"),
            "description": "Choose a unique slug for the URL (e.g. my-page → /my-page/).",
        }),
        ("SEO", {
            "fields": ("meta_title", "meta_description"),
            "classes": ("collapse",)
        }),
        ("Navigation Menu", {
            "fields": ("show_in_menu", "menu_placement", "menu_order"),
        }),
        ("Header Section", {
            "fields": ("header_text", "image_upload", "image_url", "alt_text"),
        }),
        ("Main Content", {
            "fields": ("content",),
        }),
        ("Secondary Content", {
            "fields": ("content_2",),
            "classes": ("collapse",)
        }),
        ("Call to Action Buttons", {
            "fields": ("cta_text", "cta_url", "cta_text_2", "cta_url_2"),
        }),
        ("Metadata", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(slug__in=INDIVIDUAL_PAGE_SLUGS)


if admin.site.is_registered(Group):
    admin.site.unregister(Group)
