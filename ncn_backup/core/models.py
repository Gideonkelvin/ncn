from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.text import slugify


def _bible_study_guide_storage():
    """PDFs on Cloudinary (raw) when USE_CLOUDINARY_MEDIA; otherwise local MEDIA_ROOT."""
    if getattr(settings, "USE_CLOUDINARY_MEDIA", False):
        from cloudinary_storage.storage import RawMediaCloudinaryStorage

        return RawMediaCloudinaryStorage()
    return FileSystemStorage()


class EGroup(models.Model):
    """One block of copy for the E-Groups ministry page (intro, highlight, or pillar)."""

    class Kind(models.TextChoices):
        INTRO = "intro", "Intro paragraph"
        LEDE = "lede", "ABCDE highlight (single highlighted box)"
        PILLAR = "pillar", "Pillar card"

    kind = models.CharField(
        max_length=20,
        choices=Kind.choices,
        db_index=True,
        help_text="Intro = opening paragraphs (add several rows). Lede = one highlighted line. Pillar = titled cards.",
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        help_text="Required for pillars (e.g. Accountability). Leave empty for intro/lede.",
    )
    body = models.TextField(
        help_text="Main text. Blank lines create new paragraphs where line breaks are enabled.",
    )
    sort_order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Order within the same kind (lower first).",
    )
    is_published = models.BooleanField(
        default=True,
        help_text="Untick to hide this block on the site.",
    )

    class Meta:
        ordering = ["kind", "sort_order", "id"]
        verbose_name = "eGroup"
        verbose_name_plural = "eGroups"

    def __str__(self):
        if self.title:
            return f"{self.get_kind_display()}: {self.title}"
        return f"{self.get_kind_display()} #{self.sort_order}"


class Plugin(models.Model):
    """One content block for the Plug-In ministry page."""

    class Kind(models.TextChoices):
        LEAD = "lead", "Opening highlight (top band)"
        ABOUT = "about", "About section"
        OBJECTIVES_TITLE = "objectives_title", "Objectives heading (above cards)"
        OBJECTIVE = "objective", "Objective card"
        HOW = "how", "How it works section"

    kind = models.CharField(
        max_length=30,
        choices=Kind.choices,
        db_index=True,
        help_text="Use one Lead, one About, one Objectives heading, several Objective cards, one How section.",
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        help_text="Section heading (About, How, Objectives) or objective card title. Leave blank for Lead.",
    )
    body = models.TextField(
        blank=True,
        help_text="Main text. Blank lines become paragraphs. Objectives heading can leave this empty.",
    )
    sort_order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Order for objective cards (lower first). Other kinds typically use 0.",
    )
    is_published = models.BooleanField(
        default=True,
        help_text="Untick to hide this block on the site.",
    )

    class Meta:
        ordering = ["kind", "sort_order", "id"]
        verbose_name = "Plugin"
        verbose_name_plural = "Plug-In page"

    def __str__(self):
        if self.title:
            return f"{self.get_kind_display()}: {self.title}"
        return f"{self.get_kind_display()} #{self.sort_order}"


class ClubFusion(models.Model):
    """One section block for the Club Fusion page."""

    title = models.CharField(max_length=200)
    kicker = models.CharField(
        max_length=120,
        blank=True,
        help_text="Small label above the section title (optional).",
    )
    body = models.TextField(help_text="Section body text. You can use line breaks.")
    image = models.ImageField(
        upload_to="club_fusion/",
        blank=True,
        null=True,
        help_text="Optional section image. If empty, text uses full width.",
    )
    image_on_left = models.BooleanField(
        default=False,
        help_text="Tick to place image on left for this section (desktop).",
    )
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Club Fusion"
        verbose_name_plural = "Club Fusion"

    def __str__(self):
        return self.title


class ClubFusionResource(models.Model):
    """One downloadable resource row on the Club Fusion page."""

    resource_date = models.DateField(help_text="Date shown in the resources table.")
    note = models.CharField(max_length=255, help_text="Short note for this row.")
    resource_file = models.FileField(
        upload_to="club_fusion/resources/",
        storage=_bible_study_guide_storage(),
        blank=True,
        null=True,
        help_text="Upload a file to view or download.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-resource_date", "-created_at", "sort_order", "id"]
        verbose_name = "Club fusion resource"
        verbose_name_plural = "Club fusion resources"

    def __str__(self):
        return f"{self.resource_date} - {self.note}"


class Quest(models.Model):
    """One content section for the Quest page."""

    heading = models.CharField(max_length=200)
    body = models.TextField(
        blank=True,
        help_text="Main paragraph text. Use line breaks to separate paragraphs.",
    )
    bullet_points = models.TextField(
        blank=True,
        help_text="Optional bullet points. Add one item per line.",
    )
    image = models.ImageField(
        upload_to="quest/",
        blank=True,
        null=True,
        help_text="Optional image for this section.",
    )
    image_on_right = models.BooleanField(
        default=True,
        help_text="If image is set, show it on the right on large screens.",
    )
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Quest"
        verbose_name_plural = "Quest"

    def __str__(self):
        return self.heading


class Mens(models.Model):
    """One content section for the Men's Ministry page."""

    heading = models.CharField(max_length=200)
    body = models.TextField(
        blank=True,
        help_text="Main paragraph text. Use line breaks to separate paragraphs.",
    )
    image = models.ImageField(
        upload_to="mens/",
        blank=True,
        null=True,
        help_text="Optional image for this section.",
    )
    image_secondary = models.ImageField(
        upload_to="mens/",
        blank=True,
        null=True,
        help_text="Optional second image for collage layout.",
    )
    image_on_right = models.BooleanField(
        default=True,
        help_text="If image is set, show it on the right on large screens.",
    )
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Men's"
        verbose_name_plural = "Men's"

    def __str__(self):
        return self.heading


class Womens(models.Model):
    """One content section for the Women's Ministry page."""

    heading = models.CharField(max_length=200)
    body = models.TextField(
        blank=True,
        help_text="Main paragraph text. Use line breaks to separate paragraphs.",
    )
    image = models.ImageField(
        upload_to="womens/",
        blank=True,
        null=True,
        help_text="Optional image for this section.",
    )
    image_secondary = models.ImageField(
        upload_to="womens/",
        blank=True,
        null=True,
        help_text="Optional second image for collage layout.",
    )
    image_on_right = models.BooleanField(
        default=True,
        help_text="If image is set, show it on the right on large screens.",
    )
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Women's"
        verbose_name_plural = "Women's"

    def __str__(self):
        return self.heading


class BibleStudyContent(models.Model):
    """Main heading and body text for the Bible Study page."""

    heading = models.CharField(max_length=200, default="Bible Study")
    body = models.TextField(
        help_text="Main page text. Use line breaks to separate paragraphs.",
    )
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Bible Study content"
        verbose_name_plural = "Bible Study content"

    def __str__(self):
        return self.heading


class BibleStudyGuide(models.Model):
    """One row in the Bible Study table (date, notes, guide file)."""

    study_date = models.DateField(help_text="Select the posting/study date.")
    notes = models.CharField(max_length=255, help_text="Short notes text for this row.")
    guide_file = models.FileField(
        upload_to="bible_study/guides/",
        storage=_bible_study_guide_storage(),
        blank=True,
        null=True,
        help_text="Upload the Bible study guide file.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at", "-study_date", "sort_order", "id"]
        verbose_name = "Bible Study guide row"
        verbose_name_plural = "Bible Study guide rows"

    def __str__(self):
        return f"{self.study_date} - {self.notes}"


class Event(models.Model):
    """Event card used on the Events page and Home page."""

    title = models.CharField(max_length=200, help_text="Event title.")
    organizer = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional line shown under the title, exactly as you type it.",
    )
    venue = models.CharField(
        max_length=200,
        blank=True,
        help_text="Venue/location text (optional).",
    )
    start_at = models.DateTimeField(help_text="Event start date and time.")
    image = models.ImageField(
        upload_to="events/",
        blank=True,
        null=True,
        help_text="Event card image (optional).",
    )
    button_text = models.CharField(
        max_length=80,
        default="Watch Online",
        help_text="Button text shown on the event card.",
    )
    button_url = models.URLField(
        blank=True,
        help_text="Optional button link. Leave empty if not needed.",
    )
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["start_at", "sort_order", "id"]
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.title


class Membership(models.Model):
    """Content for the Membership page (single record in admin)."""

    heading = models.CharField(max_length=200, default="Membership")
    subtitle = models.CharField(max_length=300, blank=True)
    body = models.TextField(help_text="Main paragraph shown in the hero.")
    hero_image = models.ImageField(
        upload_to="membership/",
        blank=True,
        null=True,
        help_text="Hero background image. If empty, the default theme image is used.",
    )
    button_text = models.CharField(max_length=80, default="Karibu")
    button_url = models.URLField(
        blank=True,
        help_text="Optional button link. Leave empty to use the Contact page.",
    )
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Membership"
        verbose_name_plural = "Membership"

    def __str__(self):
        return self.heading


class Volunteer(models.Model):
    """Content for the Volunteer page (single record in admin)."""

    heading = models.CharField(max_length=200, default="Volunteer")
    subtitle = models.CharField(max_length=300, blank=True)
    body = models.TextField(help_text="Main paragraph shown in the hero.")
    hero_image = models.ImageField(
        upload_to="volunteer/",
        blank=True,
        null=True,
        help_text="Hero background image. If empty, the default theme image is used.",
    )
    button_text = models.CharField(max_length=80, default="Volunteer")
    button_url = models.URLField(
        blank=True,
        help_text="Optional button link. Leave empty to use the Contact page.",
    )
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Volunteer"
        verbose_name_plural = "Volunteer"

    def __str__(self):
        return self.heading


class GivePage(models.Model):
    """Editable Give page content (use a single published row in admin)."""

    lead_title = models.CharField(max_length=300, default="Together, We Can Make a Change")
    lead_text = models.TextField(
        help_text="Intro below the headline. Line breaks are preserved.",
        default=(
            "Your generous giving helps us spread the love of Christ and make a difference in our community. "
            "Join us in supporting Nairobi Chapel Ngong Hills as we continue to serve those in need and share the Gospel."
        ),
    )
    mpesa_title = models.CharField(max_length=120, default="M-Pesa Paybill")
    mpesa_body = models.TextField(
        help_text='HTML allowed for emphasis, e.g. <strong class="give-highlight--mpesa">867509</strong>.',
        default=(
            "Giving is easy with Lipa na M-Pesa. Simply use PayBill number "
            '<strong class="give-highlight--mpesa">867509</strong> '
            "and enter the appropriate account number—e.g. "
            '<strong class="give-highlight--mpesa">Tithe</strong>, '
            '<strong class="give-highlight--mpesa">Offering</strong>, '
            '<strong class="give-highlight--mpesa">Quest</strong>, '
            '<strong class="give-highlight--mpesa">Development</strong>, '
            "or other designations as needed."
        ),
    )
    cheque_title = models.CharField(max_length=120, default="Cheque")
    cheque_body = models.TextField(
        help_text='HTML allowed for emphasis, e.g. <strong class="give-highlight--cheque">Ngong Hills</strong>.',
        default=(
            "Write a cheque to "
            '<strong class="give-highlight--cheque">Nairobi Chapel</strong>. '
            "On the back, please indicate "
            '<strong class="give-highlight--cheque">Ngong Hills</strong>.'
        ),
    )
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Give page"
        verbose_name_plural = "Give page"

    def __str__(self):
        return "Give page"


class HomeHero(models.Model):
    """Editable hero section for the Home page."""

    title = models.CharField(max_length=300, default="Welcome to Nairobi Chapel Ngong Hills")
    body = models.TextField(
        default="A Christ-centered community growing in faith, love, and service.",
        help_text="Hero description text.",
    )
    button_text = models.CharField(max_length=80, default="Learn More")
    button_url = models.URLField(blank=True, help_text="Optional button link. Leave empty to use Contact page.")
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Home Hero"
        verbose_name_plural = "Home Hero"

    def __str__(self):
        return "Home Hero"


class HomeHeroSlide(models.Model):
    """One hero carousel image for the home page."""

    hero = models.ForeignKey(
        HomeHero,
        related_name="slides",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to="home/hero/")
    sort_order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Lower numbers appear first in the carousel.",
    )

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Hero slide"
        verbose_name_plural = "Hero slides"

    def __str__(self):
        return f"Hero slide #{self.sort_order}"


class HomeAbout(models.Model):
    """Editable 'Why Choose Us' section on Home page."""

    section_title = models.CharField(max_length=120, default="Why Choose Us!")
    heading = models.CharField(
        max_length=300,
        default="Why You Should Trust Us? Learn More About Us!",
    )
    body = models.TextField(
        default=(
            "We are committed to biblical teaching, loving community, and practical support for every stage "
            "of life."
        ),
        help_text="Main paragraph below the heading.",
    )
    point_1_title = models.CharField(max_length=120, default="Design Approach")
    point_1_body = models.TextField(default="We prayerfully plan every program to serve people with excellence.")
    point_1_icon = models.ImageField(
        upload_to="home/about/icons/",
        blank=True,
        null=True,
        help_text="Icon for point 1 (e.g. Mission).",
    )
    point_2_title = models.CharField(max_length=120, default="Innovative Solutions")
    point_2_body = models.TextField(default="We use relevant and creative methods to share Christ effectively.")
    point_2_icon = models.ImageField(
        upload_to="home/about/icons/",
        blank=True,
        null=True,
        help_text="Icon for point 2 (e.g. Vision).",
    )
    image_1 = models.ImageField(upload_to="home/about/", blank=True, null=True)
    image_2 = models.ImageField(upload_to="home/about/", blank=True, null=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Home About"
        verbose_name_plural = "Home About"

    def __str__(self):
        return "Home About"


class OurServices(models.Model):
    """Editable 'Our Services' section on Home page."""

    section_title = models.CharField(max_length=120, default="Our Services")
    heading = models.CharField(max_length=300, default="Programs for children, teens, and adults")
    card_1_title = models.CharField(max_length=120, default="Children Service")
    card_1_body = models.TextField(default="Programs that help children know God, grow in faith, and build friendships.")
    card_1_bg_image = models.ImageField(upload_to="home/services/", blank=True, null=True)
    card_1_icon = models.ImageField(upload_to="home/services/icons/", blank=True, null=True)
    card_1_button_text = models.CharField(max_length=80, default="Read More")
    card_1_button_url = models.URLField(blank=True)
    card_2_title = models.CharField(max_length=120, default="Teens Service")
    card_2_body = models.TextField(default="A space for teens to discover purpose, build character, and follow Christ.")
    card_2_bg_image = models.ImageField(upload_to="home/services/", blank=True, null=True)
    card_2_icon = models.ImageField(upload_to="home/services/icons/", blank=True, null=True)
    card_2_button_text = models.CharField(max_length=80, default="Read More")
    card_2_button_url = models.URLField(blank=True)
    card_3_title = models.CharField(max_length=120, default="Adults Service")
    card_3_body = models.TextField(default="Discipleship and fellowship opportunities for adults in every life stage.")
    card_3_bg_image = models.ImageField(upload_to="home/services/", blank=True, null=True)
    card_3_icon = models.ImageField(upload_to="home/services/icons/", blank=True, null=True)
    card_3_button_text = models.CharField(max_length=80, default="Read More")
    card_3_button_url = models.URLField(blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Our Services"
        verbose_name_plural = "Our Services"

    def __str__(self):
        return "Our Services"


class Pastorate(models.Model):
    """A pastoral team member shown on the Pastorate page."""

    name = models.CharField(max_length=200)
    role = models.CharField(
        max_length=300,
        help_text="Title or short description (e.g. Lead Pastor, Elders).",
    )
    bio = models.TextField(
        blank=True,
        help_text="Longer biography; shown below the role (justified on the site).",
    )
    photo = models.ImageField(
        upload_to="pastorate/",
        help_text="Portrait photo; shown in the team grid.",
    )
    sort_order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Lower numbers appear first.",
    )
    is_published = models.BooleanField(
        default=True,
        help_text="Untick to hide from the website without deleting.",
    )

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "Pastorate member"
        verbose_name_plural = "Pastorate members"

    def __str__(self):
        return self.name


class GalleryAlbum(models.Model):
    """A dated photo album shown on the Gallery page."""

    title = models.CharField(max_length=200)
    event_date = models.DateField(help_text="Date shown on the gallery listing and detail page.")
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    is_published = models.BooleanField(
        default=True,
        help_text="Untick to hide this album on the website.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-event_date", "id"]
        verbose_name = "Gallery album"
        verbose_name_plural = "Gallery albums"

    def __str__(self):
        return f"{self.title} ({self.event_date})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.title}-{self.event_date}")
            slug = base or "gallery"
            counter = 1
            while GalleryAlbum.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def cover_image(self):
        return self.images.order_by("-id").first()


class GalleryImage(models.Model):
    """One image inside a gallery album."""

    album = models.ForeignKey(
        GalleryAlbum,
        related_name="images",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to="gallery/")
    caption = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional alt text / caption for this image.",
    )
    sort_order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Lower numbers appear first in the album.",
    )

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Gallery image"
        verbose_name_plural = "Gallery images"

    def __str__(self):
        return self.caption or f"Image #{self.pk or 'new'}"

    @property
    def alt_text(self):
        return self.caption or self.album.title
