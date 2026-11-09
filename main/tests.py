from datetime import date
from io import StringIO
from pathlib import Path
from unittest import skipUnless

from django.core.management import call_command
from django.test import TestCase, Client, override_settings
from django.urls import reverse

from main.models import (
    DynamicPage,
    GalleryAlbum,
    GalleryImage,
    HeroSlide,
    PageCopy,
    Service,
)


BACKUP_DB = Path(__file__).resolve().parents[1] / "ncn_backup" / "db.sqlite3"


@skipUnless(BACKUP_DB.is_file(), "ncn_backup/db.sqlite3 is required for restore tests")
class RestoreLegacyCmsTests(TestCase):
    def test_restore_creates_content_and_is_idempotent(self):
        out = StringIO()
        call_command("restore_legacy_cms", stdout=out)
        first = out.getvalue()
        self.assertIn("created:", first)

        hero_count = HeroSlide.objects.count()
        album_count = GalleryAlbum.objects.count()
        image_count = GalleryImage.objects.count()
        give = PageCopy.objects.filter(page_slug="give").first()
        egroups = DynamicPage.objects.filter(slug="egroups").first()

        self.assertGreaterEqual(hero_count, 1)
        self.assertGreaterEqual(album_count, 1)
        self.assertGreaterEqual(image_count, 1)
        self.assertIsNotNone(give)
        self.assertTrue(give.body)
        self.assertIsNotNone(egroups)
        self.assertIn("Accountability", egroups.content)

        out2 = StringIO()
        call_command("restore_legacy_cms", stdout=out2)
        self.assertEqual(HeroSlide.objects.count(), hero_count)
        self.assertEqual(GalleryAlbum.objects.count(), album_count)
        self.assertEqual(GalleryImage.objects.count(), image_count)

    def test_dry_run_does_not_write(self):
        before_heroes = HeroSlide.objects.count()
        before_albums = GalleryAlbum.objects.count()
        call_command("restore_legacy_cms", dry_run=True, stdout=StringIO())
        self.assertEqual(HeroSlide.objects.count(), before_heroes)
        self.assertEqual(GalleryAlbum.objects.count(), before_albums)

    def test_preserves_existing_meaningful_service(self):
        Service.objects.create(
            title="Children's Service",
            description="Keep me",
            day_time="11:30 am - 1:00 pm",
            location="Nairobi Chapel Ngong Hills",
            image_url="https://example.com/keep.jpg",
            order=0,
        )
        call_command("restore_legacy_cms", stdout=StringIO())
        svc = Service.objects.get(title="Children's Service")
        self.assertEqual(svc.description, "Keep me")
        self.assertEqual(svc.image_url, "https://example.com/keep.jpg")


class GalleryPagesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.album = GalleryAlbum.objects.create(
            title="Sunday Service 2026",
            event_date=date(2026, 5, 18),
            slug="sunday-service-2026",
            is_published=True,
        )
        GalleryImage.objects.create(
            album=self.album,
            image_url="https://res.cloudinary.com/demo/image/upload/sample.jpg",
            caption="Worship",
            order=0,
        )

    def test_gallery_list_and_detail_resolve(self):
        list_resp = self.client.get(reverse("gallery"))
        self.assertEqual(list_resp.status_code, 200)
        self.assertContains(list_resp, "Sunday Service 2026")

        detail_resp = self.client.get(reverse("gallery_detail", args=[self.album.slug]))
        self.assertEqual(detail_resp.status_code, 200)
        self.assertContains(detail_resp, "sample.jpg")
        self.assertContains(detail_resp, "Worship")
