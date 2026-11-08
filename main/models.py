"""
CMS models for Nairobi Chapel Ngong Hills.
All content is editable from the admin dashboard.
Uploaded files use default storage (Cloudinary when configured).
"""
from django.db import models


# =============================================================================
# SITE SETTINGS (Singleton)
# =============================================================================

class SiteSettings(models.Model):
    """Singleton: global site config (footer, contact, social)."""
    site_name = models.CharField(max_length=200, default="Nairobi Chapel Ngong Hills")
    tagline = models.CharField(max_length=300, blank=True)
    contact_email = models.EmailField(default="info@ncngonghills.org")
    contact_location = models.CharField(max_length=200, default="Ngong Hills, Kenya")
    contact_phone = models.CharField(max_length=50, default="+254 797 559118", blank=True)
    footer_copyright = models.CharField(max_length=200, default="© 2026 Nairobi Chapel Ngong Hills. All rights reserved.")
    credits_url = models.URLField(blank=True, help_text="e.g. Website by BKG Consulting")
    credits_text = models.CharField(max_length=200, default="Website by BKG Consulting")
    newsletter_heading = models.CharField(max_length=200, default="Stay Connected")
    newsletter_description = models.TextField(blank=True, default="Get updates on our services, events, and community life.")
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True, help_text="YouTube channel URL (footer & social links)")
    linkedin_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    whatsapp_url = models.URLField(blank=True)
    map_embed_url = models.URLField(blank=True, help_text="Google Maps embed src URL")
    logo_url = models.URLField(blank=True, help_text="Navbar logo (Cloudinary URL)")
    favicon_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class HeroSlide(models.Model):
    """Homepage carousel slides."""
    title = models.CharField(max_length=200)
    subtitle = models.TextField()
    cta_text = models.CharField(max_length=100)
    cta_url = models.CharField(max_length=255, default="/about")
    image_url = models.URLField(help_text="Cloudinary image URL")
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "Hero"

    def __str__(self):
        return self.title[:50]


# =============================================================================
# HOMEPAGE SECTIONS
# =============================================================================

class Service(models.Model):
    """Homepage service cards (Children's Service, Teens Service, Adult Service, etc.)"""
    title = models.CharField(max_length=200, help_text="Service name (e.g., Children's Service)")
    description = models.TextField(blank=True, help_text="Brief description of the service")
    day_time = models.CharField(max_length=100, help_text="When the service occurs (e.g., Sundays 11:30 am - 1:00 pm)")
    location = models.CharField(max_length=200, default="Nairobi Chapel Ngong Hills", help_text="Where the service is held")
    place = models.CharField(max_length=200, blank=True, help_text="Specific venue (e.g., Quest Classrooms)")
    image_url = models.URLField(blank=True, help_text="Service image URL (Cloudinary)")
    learn_more_url = models.CharField(max_length=255, blank=True, help_text="Link to more information about this service")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title


class WhatWeDoItem(models.Model):
    """Home page: What We Do (3 blocks)."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon_url = models.URLField(blank=True, help_text="Icon image Cloudinary URL")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "What We Do item"
        verbose_name_plural = "What We Do items"

    def __str__(self):
        return self.title


class AboutPreview(models.Model):
    """Home: About preview section (images + copy + CTA)."""
    heading = models.CharField(max_length=200, default="About Us")
    subheading = models.CharField(max_length=300, default="A Nonprofit Dedicated to Visual Health and Inclusion")
    body_paragraph_1 = models.TextField(blank=True)
    body_paragraph_2 = models.TextField(blank=True)
    stat_number = models.CharField(max_length=20, default="100")
    stat_label_line1 = models.CharField(max_length=100, default="Percent")
    stat_label_line2 = models.CharField(max_length=100, default="Mission")
    stat_label_line3 = models.CharField(max_length=100, default="Driven")
    cta_text = models.CharField(max_length=100, default="Read More")
    cta_url = models.CharField(max_length=255, default="/about")
    image_1_url = models.URLField(blank=True)
    image_2_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk and AboutPreview.objects.exists():
            return
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class FounderPurposeBlock(models.Model):
    """Home: About Founder and Purpose section (copy + 3 bullets + 2 images)."""
    section_title = models.CharField(max_length=200, default="About Founder and Purpose")
    subheading = models.CharField(max_length=300, default="The Story Behind Rose Coloured Lens")
    intro_paragraph_1 = models.TextField(blank=True)
    intro_paragraph_2 = models.TextField(blank=True)
    bullet_1_title = models.CharField(max_length=200, blank=True)
    bullet_1_text = models.TextField(blank=True)
    bullet_2_title = models.CharField(max_length=200, blank=True)
    bullet_2_text = models.TextField(blank=True)
    bullet_3_title = models.CharField(max_length=200, blank=True)
    bullet_3_text = models.TextField(blank=True)
    image_1_url = models.URLField(blank=True)
    image_2_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk and FounderPurposeBlock.objects.exists():
            return
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class CallToActionBlock(models.Model):
    """Home: Get Involved CTA section."""
    heading = models.CharField(max_length=200, default="Get Involved")
    subheading = models.CharField(max_length=300, default="Support Visual Health and Visual Inclusion")
    body = models.TextField(blank=True)
    primary_button_text = models.CharField(max_length=100, default="Donate")
    primary_button_url = models.CharField(max_length=255, default="/give")
    secondary_button_text = models.CharField(max_length=100, default="Contact Us")
    secondary_button_url = models.CharField(max_length=255, default="/contact")
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk and CallToActionBlock.objects.exists():
            return
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# =============================================================================
# BLOG & EVENTS
# =============================================================================

class BlogCategory(models.Model):
    """Blog filter categories."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "Blog categories"

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """Blog listing and detail."""
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField(help_text="Short summary for cards")
    body = models.TextField(blank=True, help_text="Full content (rich text)")
    featured_image = models.ImageField(
        upload_to="rose-coloured-lens/blog",
        blank=True,
        null=True,
        help_text="Uploaded via default storage (Cloudinary when CLOUDINARY_* env vars are set).",
    )
    featured_image_url = models.URLField(blank=True, help_text="Cloudinary URL (auto-filled when image is uploaded)")
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    published_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "order", "-created_at"]

    def __str__(self):
        return self.title[:80]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Keep featured_image_url in sync with storage URL (Cloudinary or local)
        if self.featured_image:
            try:
                url = self.featured_image.url
            except ValueError:
                url = ""
            if url and self.featured_image_url != url:
                BlogPost.objects.filter(pk=self.pk).update(featured_image_url=url)
        elif self.featured_image_url:
            BlogPost.objects.filter(pk=self.pk).update(featured_image_url="")


# =============================================================================
# SHOP
# =============================================================================

class Product(models.Model):
    """Shop products."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, help_text="Cloudinary URL")
    badge = models.CharField(max_length=50, blank=True, help_text="e.g. Bestseller, New")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


# =============================================================================
# CONTACT & PAGE COPY
# =============================================================================

class PageCopy(models.Model):
    """Editable copy for give, 404, contact intro, shop intro, etc."""
    page_slug = models.SlugField(unique=True, help_text="e.g. give, 404, contact, shop")
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    heading = models.CharField(max_length=200, blank=True)
    subheading = models.CharField(max_length=300, blank=True)
    body = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Page copies"

    def __str__(self):
        return self.page_slug


class ContactPageCopy(PageCopy):
    """Proxy: the public /contact page copy."""

    class Meta:
        proxy = True
        verbose_name_plural = "Contact"


class GivePageCopy(PageCopy):
    """Proxy: the public /give page copy."""

    class Meta:
        proxy = True
        verbose_name_plural = "Give"


class ContactSubmission(models.Model):
    """Contact form submissions."""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.subject} from {self.email}"


class Event(models.Model):
    """Events for homepage and events page."""
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField(help_text="Short summary for cards")
    description = models.TextField(blank=True, help_text="Full event description")
    event_date = models.DateTimeField(help_text="Date and time of the event")
    location = models.CharField(max_length=200, blank=True, help_text="Event location")
    image_url = models.URLField(blank=True, help_text="Event image URL (Cloudinary)")
    watch_online_url = models.URLField(
        blank=True,
        help_text='YouTube live, premiere, or channel URL (shows "Watch online" on the home page)',
    )
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["event_date", "order"]
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.title


class PastoralTeamSection(models.Model):
    """Up to six profile blocks on /pastoral/, alternating text/image columns."""

    order = models.PositiveSmallIntegerField(default=0, db_index=True)
    eyebrow = models.CharField(
        max_length=120,
        blank=True,
        help_text='Small label above the name (e.g. "Lead Pastor")',
    )
    name_heading = models.CharField(
        max_length=200,
        help_text="Primary name line (e.g. Rev. Collins Ouma)",
    )
    subheading = models.CharField(
        max_length=200,
        blank=True,
        help_text="Secondary line (e.g. Daniel Aswa)",
    )
    body = models.TextField(blank=True, help_text="Biography (HTML allowed)")
    image_url = models.URLField(blank=True, help_text="Cloudinary or other image URL")
    alt_text = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Pastoral page · team section"
        verbose_name_plural = "Pastoral page · team sections"

    def __str__(self):
        return f"{self.order}: {self.name_heading}"


class BibleStudyResource(models.Model):
    """Rows for the Resources table on /bible-study/."""

    session_date = models.DateField()
    description = models.CharField(max_length=500, help_text="Summary or topic (Resources table)")
    document_url = models.URLField(
        blank=True,
        help_text="PDF or outline URL for View / Download (optional)",
    )
    order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-session_date", "order", "id"]
        verbose_name = "Bible study · resource row"
        verbose_name_plural = "Bible study · resource rows"

    def __str__(self):
        return f"{self.session_date}: {self.description[:50]}"


# =============================================================================
# DYNAMIC PAGES
# =============================================================================

class DynamicPage(models.Model):
    """Dynamic pages that can be managed from admin panel."""
    TEMPLATE_CHOICES = [
        ("default", "Default - Image Left, Content Right"),
        ("full_width", "Full Width - Hero Image with Overlay"),
        ("content_only", "Content Only - No Image"),
        ("split", "Split - Two Column Layout"),
        ("centered", "Centered - Text Centered with Image Below"),
    ]
    
    MENU_PLACEMENT_CHOICES = [
        ("none", "None - Not in Menu"),
        ("about", "About Dropdown"),
        ("ministries", "Ministries Dropdown"),
        ("resources", "Resources Dropdown"),
        ("engage", "Engage Dropdown"),
    ]
    
    slug = models.SlugField(unique=True, help_text="URL slug (e.g., 'egroups', 'pastoral')")
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True, help_text="SEO title (leave empty to use page title)")
    meta_description = models.TextField(blank=True, help_text="SEO meta description")
    
    # Template and layout
    template = models.CharField(max_length=50, choices=TEMPLATE_CHOICES, default="default")
    
    # Header section
    header_text = models.TextField(blank=True, help_text="Text displayed in the page header")
    image_url = models.URLField(blank=True, help_text="Main image URL (Cloudinary)")
    alt_text = models.CharField(max_length=200, blank=True, help_text="Image alt text for accessibility")
    
    # Main content
    content = models.TextField(blank=True, help_text="Main content text (supports HTML)")
    content_2 = models.TextField(blank=True, help_text="Secondary content (for split template)")
    
    # Call to Action
    cta_text = models.CharField(max_length=100, blank=True, help_text="Button text")
    cta_url = models.CharField(max_length=255, blank=True, help_text="Button link")
    cta_text_2 = models.CharField(max_length=100, blank=True, help_text="Secondary button text")
    cta_url_2 = models.CharField(max_length=255, blank=True, help_text="Secondary button link")
    
    # Menu settings
    menu_placement = models.CharField(max_length=50, choices=MENU_PLACEMENT_CHOICES, default="none", help_text="Which dropdown menu to appear in")
    menu_order = models.PositiveIntegerField(default=0, help_text="Order within the menu")
    show_in_menu = models.BooleanField(default=True, help_text="Show in navigation menu")
    
    # Status
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Dynamic Page"
        verbose_name_plural = "Dynamic Pages"

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f"/{self.slug}"
    
    def get_meta_title(self):
        return self.meta_title or self.title
    
    def get_menu_display_name(self):
        return self.title


# Slugs that have their own admin entry (proxy models below). Not listed under “Other pages”.
INDIVIDUAL_PAGE_SLUGS = frozenset(
    {
        "about",
        "pastoral",
        "mens-ministry",
        "womens-ministry",
        "egroups",
        "prayer",
        "club-fusion",
        "quest",
        "sermon",
        "bible-study",
        "membership",
        "volunteer",
    }
)


class AboutPage(DynamicPage):
    class Meta:
        proxy = True
        verbose_name = "Page · About"
        verbose_name_plural = "Our Story"


class PastoralCarePage(DynamicPage):
    class Meta:
        proxy = True
        verbose_name = "Page · Pastorate"
        verbose_name_plural = "Pastorate"


class EgroupsPage(DynamicPage):
    class Meta:
        proxy = True
        verbose_name = "Page · E-Groups"
        verbose_name_plural = "eGroups"


class PrayerPage(DynamicPage):
    class Meta:
        proxy = True
        verbose_name = "Page · Plug-In (/prayer)"
        verbose_name_plural = "Plug-in"


class ClubFusionPage(DynamicPage):
    class Meta:
        proxy = True
        verbose_name = "Page · Club Fusion (teens)"
        verbose_name_plural = "Club Fusion"


class QuestPage(DynamicPage):
    class Meta:
        proxy = True
        verbose_name = "Page · Quest"
        verbose_name_plural = "Quest"


class MensMinistryPage(DynamicPage):
    """Proxy: the /mens-ministry page content."""

    class Meta:
        proxy = True
        verbose_name = "Page · Men’s Ministry"
        verbose_name_plural = "Men's Ministry"


class WomensMinistryPage(DynamicPage):
    """Proxy: the /womens-ministry page content."""

    class Meta:
        proxy = True
        verbose_name = "Page · Women’s Ministry"
        verbose_name_plural = "Women's Ministry"


class SermonPage(DynamicPage):
    class Meta:
        proxy = True
        verbose_name = "Page · Sermon"
        verbose_name_plural = "Page · Sermon"


class BibleStudyPage(DynamicPage):
    class Meta:
        proxy = True
        verbose_name = "Page · Bible study"
        verbose_name_plural = "Bible Study"


class MembershipPage(DynamicPage):
    class Meta:
        proxy = True
        verbose_name = "Page · Membership"
        verbose_name_plural = "Membership"


class VolunteerPage(DynamicPage):
    class Meta:
        proxy = True
        verbose_name = "Page · Volunteer"
        verbose_name_plural = "Volunteer"


class PluginPage(DynamicPage):
    class Meta:
        proxy = True
        verbose_name = "Page · Plug-In"
        verbose_name_plural = "Page · Plug-In"


class OtherSitePage(DynamicPage):
    """Any DynamicPage whose slug is not one of the individual route pages above."""

    class Meta:
        proxy = True
        verbose_name = "Other site pages"
        verbose_name_plural = "Other site pages"
