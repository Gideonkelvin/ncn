"""
Restore legacy CMS content from existing MySQL core_* tables into main models.

Usage:
  python manage.py restore_legacy_cms
  python manage.py restore_legacy_cms --dry-run
  python manage.py restore_legacy_cms --skip-media-copy
  python manage.py restore_legacy_cms --backup-dir /home/xaygcaxz/ncn_backup
"""
from __future__ import annotations

import os
import re
import shutil
from datetime import datetime
from html import escape
from pathlib import Path
from urllib.parse import urlparse

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.text import slugify

from main.models import (
    BibleStudyResource,
    ClubFusionResource,
    DynamicPage,
    Event,
    FounderPurposeBlock,
    GalleryAlbum,
    GalleryImage,
    HeroSlide,
    PageCopy,
    PastoralTeamSection,
    Service,
    SiteSettings,
)


def _truthy(value) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _is_blank(value) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    return False


def _looks_placeholder(value: str) -> bool:
    if _is_blank(value):
        return True
    lowered = value.strip().lower()
    placeholders = {
        "event",
        "untitled",
        "placeholder",
        "test",
        "lorem ipsum",
        "coming soon",
    }
    return lowered in placeholders


class Command(BaseCommand):
    help = (
        "Idempotently restore legacy CMS content from existing MySQL core_* tables "
        "into main models. Never deletes records; only creates missing rows and "
        "fills blank fields."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview creates/updates without writing to the database.",
        )
        parser.add_argument(
            "--backup-dir",
            default="",
            help=(
                "Optional path containing a media/ folder to copy "
                "(default: /home/xaygcaxz/ncn_backup, then <BASE_DIR>/ncn_backup)."
            ),
        )
        parser.add_argument(
            "--skip-media-copy",
            action="store_true",
            help="Do not copy files from backup media/ into project media/.",
        )

    def handle(self, *args, **options):
        self.dry_run = bool(options["dry_run"])
        self.stats = {
            "created": 0,
            "updated": 0,
            "skipped": 0,
            "unresolved": [],
            "media_copied": 0,
        }
        base = Path(settings.BASE_DIR)
        if options["backup_dir"]:
            backup_dir = Path(options["backup_dir"]).expanduser().resolve()
        else:
            cpanel_backup = Path("/home/xaygcaxz/ncn_backup")
            local_backup = base / "ncn_backup"
            backup_dir = cpanel_backup if cpanel_backup.is_dir() else local_backup

        self.backup_dir = backup_dir
        self.backup_media = backup_dir / "media"
        self.project_media = base / "media"
        self.assets_dir = base.parent / "ASSETS"
        self.cloud_name = self._resolve_cloud_name()

        if not options["skip_media_copy"]:
            self._copy_media_tree()

        # Legacy CMS tables (core_*) already live in the configured MySQL database.
        legacy = connection
        with transaction.atomic():
            self._restore_site_settings(legacy)
            self._restore_hero(legacy)
            self._restore_founder_from_home_about(legacy)
            self._restore_services(legacy)
            self._restore_events(legacy)
            self._restore_pastoral(legacy)
            self._restore_give(legacy)
            self._restore_membership(legacy)
            self._restore_volunteer(legacy)
            self._restore_egroups(legacy)
            self._restore_plugin(legacy)
            self._restore_quest(legacy)
            self._restore_club_fusion(legacy)
            self._restore_club_fusion_resources(legacy)
            self._restore_mens(legacy)
            self._restore_womens(legacy)
            self._restore_bible_study(legacy)
            self._restore_gallery(legacy)
            self._ensure_gallery_nav_page()
            if self.dry_run:
                transaction.set_rollback(True)

        self._print_summary()

    # ------------------------------------------------------------------ helpers

    def _resolve_cloud_name(self) -> str:
        name = (getattr(settings, "CLOUDINARY_CLOUD_NAME", "") or "").strip()
        if name:
            return name
        url = os.environ.get("CLOUDINARY_URL", "").strip()
        if url.startswith("cloudinary://"):
            parsed = urlparse(url)
            return (parsed.hostname or "").strip()
        return ""

    def _table_rows(self, con, table: str) -> list[dict]:
        available_tables = set(con.introspection.table_names())

        if table not in available_tables:
            self.stats["unresolved"].append(
                f"Missing legacy MySQL table: {table}"
            )
            return []

        quoted_table = con.ops.quote_name(table)

        with con.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {quoted_table}")
            columns = [column[0] for column in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

    def _copy_media_tree(self):
        if not self.backup_media.is_dir():
            self.stats["unresolved"].append(
                f"No backup media directory at {self.backup_media} "
                "(continuing with MySQL content restore only)"
            )
            return
        for src in self.backup_media.rglob("*"):
            if not src.is_file():
                continue
            rel = src.relative_to(self.backup_media)
            dest = self.project_media / rel
            if dest.exists():
                continue
            if self.dry_run:
                self.stats["media_copied"] += 1
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            self.stats["media_copied"] += 1

    def _media_url(self, stored: str | None) -> str:
        """Map a legacy ImageField/FileField value to a usable URL."""
        if _is_blank(stored):
            return ""
        value = str(stored).strip().replace("\\", "/")
        if value.startswith(("http://", "https://", "/media/")):
            return value

        rel = value[6:] if value.startswith("media/") else value.lstrip("/")

        # Local file already in project or backup media
        for root in (self.project_media, self.backup_media):
            candidate = root / rel
            if candidate.is_file():
                return f"/media/{rel}"

        # Cloudinary-style public id without extension: try ASSETS stem match
        stem = Path(rel).name
        # e.g. HOME1_vcl3i8 -> HOME1
        base_stem = stem.split("_")[0] if "_" in stem else Path(stem).stem
        for ext in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
            asset = self.assets_dir / f"{base_stem}{ext}"
            if asset.is_file():
                dest_rel = Path("home/hero") / f"{base_stem}{ext}" if "hero" in rel else Path(rel).with_name(f"{base_stem}{ext}")
                dest = self.project_media / dest_rel
                if not dest.exists() and not self.dry_run:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(asset, dest)
                    self.stats["media_copied"] += 1
                if dest.exists() or self.dry_run:
                    return f"/media/{dest_rel.as_posix()}"

            local = self.project_media / Path(rel).with_name(f"{base_stem}{ext}")
            if local.is_file():
                return f"/media/{local.relative_to(self.project_media).as_posix()}"

        # Cloudinary delivery URL from public id
        if self.cloud_name:
            public_id = value if value.startswith("media/") else f"media/{rel}" if not rel.startswith("media/") else rel
            # Prefer original stored public id shape
            public_id = value if "/" in value else f"media/{value}"
            return f"https://res.cloudinary.com/{self.cloud_name}/image/upload/{public_id}"

        return f"/media/{rel}"

    def _file_url(self, stored: str | None) -> str:
        url = self._media_url(stored)
        if not url or not self.cloud_name:
            return url
        # Raw docs on Cloudinary often need /raw/upload/
        if url.endswith((".pdf", ".docx", ".doc", ".xlsx", ".ppt", ".pptx")) and "/image/upload/" in url:
            return url.replace("/image/upload/", "/raw/upload/")
        return url

    def _log(self, action: str, message: str):
        style = {
            "created": self.style.SUCCESS,
            "updated": self.style.WARNING,
            "skipped": self.style.HTTP_INFO,
            "unresolved": self.style.NOTICE,
        }.get(action, self.style.NOTICE)
        self.stdout.write(style(f"[{action}] {message}"))

    def _create(self, model, defaults: dict, **lookup):
        existing = model.objects.filter(**lookup).first()
        if existing:
            self.stats["skipped"] += 1
            self._log("skipped", f"{model.__name__} exists ({lookup})")
            return existing, False
        if self.dry_run:
            self.stats["created"] += 1
            self._log("created", f"{model.__name__} {lookup} (dry-run)")
            return None, True
        obj = model.objects.create(**lookup, **defaults)
        self.stats["created"] += 1
        self._log("created", f"{model.__name__} pk={obj.pk} {lookup}")
        return obj, True

    def _fill_blank_fields(self, obj, mapping: dict, label: str) -> bool:
        """Update only blank/placeholder fields on an existing object."""
        if obj is None:
            return False
        updates = {}
        for field, new_value in mapping.items():
            if _is_blank(new_value):
                continue
            current = getattr(obj, field, None)
            if _is_blank(current) or (_looks_placeholder(str(current)) and not _looks_placeholder(str(new_value))):
                updates[field] = new_value
        if not updates:
            self.stats["skipped"] += 1
            self._log("skipped", f"{label}: nothing to fill")
            return False
        if self.dry_run:
            self.stats["updated"] += 1
            self._log("updated", f"{label}: would set {sorted(updates.keys())} (dry-run)")
            return True
        for field, value in updates.items():
            setattr(obj, field, value)
        obj.save(update_fields=list(updates.keys()) + (["updated_at"] if hasattr(obj, "updated_at") else []))
        self.stats["updated"] += 1
        self._log("updated", f"{label}: set {sorted(updates.keys())}")
        return True

    def _upsert_dynamic_page(self, slug: str, defaults: dict):
        page = DynamicPage.objects.filter(slug=slug).first()
        if page:
            self._fill_blank_fields(page, defaults, f"DynamicPage:{slug}")
            return page
        payload = {"slug": slug, **defaults}
        if self.dry_run:
            self.stats["created"] += 1
            self._log("created", f"DynamicPage slug={slug} (dry-run)")
            return None
        page = DynamicPage.objects.create(**payload)
        self.stats["created"] += 1
        self._log("created", f"DynamicPage slug={slug}")
        return page

    def _paras(self, text: str) -> str:
        text = (text or "").strip()
        if not text:
            return ""
        if "<" in text and ">" in text:
            return text
        chunks = [c.strip() for c in re.split(r"\n\s*\n", text) if c.strip()]
        if not chunks:
            chunks = [text]
        return "".join(f"<p>{escape(c).replace(chr(10), '<br>')}</p>" for c in chunks)

    def _bullets_html(self, text: str) -> str:
        lines = [ln.strip(" -\t") for ln in (text or "").splitlines() if ln.strip()]
        if not lines:
            return ""
        items = "".join(f"<li>{escape(ln)}</li>" for ln in lines)
        return f"<ul>{items}</ul>"

    # ------------------------------------------------------------------ restores

    def _restore_site_settings(self, con):
        settings_obj = SiteSettings.get() if not self.dry_run else SiteSettings.objects.filter(pk=1).first()
        if settings_obj is None and self.dry_run:
            self.stats["created"] += 1
            self._log("created", "SiteSettings pk=1 (dry-run)")
            return
        self._fill_blank_fields(
            settings_obj,
            {
                "site_name": "Nairobi Chapel Ngong Hills",
                "tagline": "A Community of Faith, Love & Purpose",
                "contact_email": "ncngonghills@gmail.com",
                "contact_phone": "+254 797 559118",
                "contact_location": "Link Road, Off Ngong-Suswa Road",
            },
            "SiteSettings",
        )

    def _restore_hero(self, con):
        heroes = self._table_rows(con, "core_homehero")
        slides = sorted(self._table_rows(con, "core_homeheroslide"), key=lambda r: (r.get("sort_order") or 0, r["id"]))
        hero = heroes[0] if heroes else {}
        title = (hero.get("title") or "Welcome to Nairobi Chapel Ngong Hills").strip()
        subtitle = strip_tags(hero.get("body") or "").strip() or (
            "A Christ-centered community growing in faith, love, and service."
        )
        cta_text = (hero.get("button_text") or "Learn More").strip()
        cta_url = (hero.get("button_url") or "/about").strip() or "/about"

        if not slides:
            self.stats["unresolved"].append("No legacy HomeHeroSlide rows")
            return

        for index, slide in enumerate(slides):
            image_url = self._media_url(slide.get("image"))
            order = int(slide.get("sort_order") or index)
            existing = HeroSlide.objects.filter(order=order).first()
            defaults = {
                "title": title if index == 0 else title,
                "subtitle": subtitle,
                "cta_text": cta_text,
                "cta_url": cta_url,
                "image_url": image_url,
                "alt_text": title,
                "is_active": True,
            }
            if existing:
                self._fill_blank_fields(existing, defaults, f"HeroSlide order={order}")
            else:
                self._create(HeroSlide, defaults, order=order)

    def _restore_founder_from_home_about(self, con):
        rows = self._table_rows(con, "core_homeabout")
        if not rows:
            self.stats["unresolved"].append("Legacy HomeAbout empty — FounderPurposeBlock left unchanged")
            return
        row = rows[0]
        obj = FounderPurposeBlock.get() if not self.dry_run else FounderPurposeBlock.objects.filter(pk=1).first()
        if obj is None and self.dry_run:
            self.stats["created"] += 1
            self._log("created", "FounderPurposeBlock (dry-run)")
            return
        self._fill_blank_fields(
            obj,
            {
                "section_title": row.get("section_title") or "",
                "subheading": row.get("heading") or "",
                "intro_paragraph_1": row.get("body") or "",
                "bullet_1_title": row.get("point_1_title") or "",
                "bullet_1_text": row.get("point_1_body") or "",
                "bullet_2_title": row.get("point_2_title") or "",
                "bullet_2_text": row.get("point_2_body") or "",
                "image_1_url": self._media_url(row.get("image_1")),
                "image_2_url": self._media_url(row.get("image_2")),
            },
            "FounderPurposeBlock",
        )

    def _restore_services(self, con):
        rows = self._table_rows(con, "core_ourservices")
        if not rows:
            self.stats["unresolved"].append("Legacy OurServices empty — existing Service records preserved")
            return
        row = rows[0]
        for n in (1, 2, 3):
            title = (row.get(f"card_{n}_title") or "").strip()
            if not title:
                continue
            defaults = {
                "description": row.get(f"card_{n}_body") or "",
                "day_time": "",
                "location": "Nairobi Chapel Ngong Hills",
                "place": "",
                "image_url": self._media_url(row.get(f"card_{n}_bg_image")),
                "learn_more_url": row.get(f"card_{n}_button_url") or "",
                "is_active": True,
                "order": n - 1,
            }
            existing = Service.objects.filter(title=title).first()
            if existing:
                self._fill_blank_fields(existing, defaults, f"Service:{title}")
            else:
                self._create(Service, defaults, title=title)

    def _restore_events(self, con):
        for row in self._table_rows(con, "core_event"):
            if not row.get("is_published", 1):
                continue
            title = (row.get("title") or "").strip() or "Untitled event"
            slug = slugify(title)[:200] or f"event-{row['id']}"
            start_raw = row.get("start_at")
            try:
                event_date = datetime.fromisoformat(str(start_raw).replace("Z", "+00:00"))
            except Exception:
                event_date = timezone.now()
            if timezone.is_naive(event_date):
                event_date = timezone.make_aware(event_date, timezone.get_current_timezone())
            image_url = self._media_url(row.get("image"))
            watch_url = (row.get("button_url") or "").strip()
            defaults = {
                "title": title,
                "excerpt": title if _looks_placeholder(title) else f"{title} at Nairobi Chapel Ngong Hills",
                "description": "",
                "event_date": event_date,
                "location": row.get("venue") or row.get("organizer") or "",
                "image_url": image_url,
                "watch_online_url": watch_url if watch_url.startswith("http") else "",
                "is_published": True,
                "order": int(row.get("sort_order") or 0),
            }
            existing = Event.objects.filter(slug=slug).first() or Event.objects.filter(title=title).first()
            if existing:
                # Never replace a meaningful production title/image with weak legacy placeholders
                safe = {
                    "excerpt": defaults["excerpt"],
                    "location": defaults["location"],
                    "image_url": defaults["image_url"],
                    "watch_online_url": defaults["watch_online_url"],
                }
                if not _looks_placeholder(title):
                    safe["title"] = title
                self._fill_blank_fields(existing, safe, f"Event:{existing.slug}")
            else:
                if self.dry_run:
                    self.stats["created"] += 1
                    self._log("created", f"Event slug={slug} (dry-run)")
                else:
                    Event.objects.create(slug=slug, **defaults)
                    self.stats["created"] += 1
                    self._log("created", f"Event slug={slug}")

    def _restore_pastoral(self, con):
        rows = [r for r in self._table_rows(con, "core_pastorate") if r.get("is_published", 1)]
        if not rows:
            self.stats["unresolved"].append(
                "Legacy Pastorate empty — existing PastoralTeamSection records preserved"
            )
            return
        for row in sorted(rows, key=lambda r: (r.get("sort_order") or 0, r["id"])):
            name = (row.get("name") or "").strip()
            if not name:
                continue
            order = int(row.get("sort_order") or 0)
            defaults = {
                "eyebrow": (row.get("role") or "").strip(),
                "subheading": "",
                "body": row.get("bio") or "",
                "image_url": self._media_url(row.get("photo")),
                "alt_text": name,
                "is_active": True,
                "order": order,
            }
            existing = (
                PastoralTeamSection.objects.filter(name_heading__iexact=name).first()
                or PastoralTeamSection.objects.filter(order=order, name_heading__icontains=name.split()[0]).first()
            )
            if existing:
                self._fill_blank_fields(existing, defaults, f"PastoralTeamSection:{name}")
            else:
                self._create(PastoralTeamSection, {**defaults, "name_heading": name}, name_heading=name)

    def _restore_give(self, con):
        rows = self._table_rows(con, "core_givepage")
        if not rows:
            self.stats["unresolved"].append("Legacy GivePage empty")
            return
        row = rows[0]
        body = (
            f"<p>{escape(row.get('lead_text') or '')}</p>"
            f"<h3>{escape(row.get('mpesa_title') or 'M-Pesa Paybill')}</h3>"
            f"<div class='give-mpesa'>{row.get('mpesa_body') or ''}</div>"
            f"<h3>{escape(row.get('cheque_title') or 'Cheque')}</h3>"
            f"<div class='give-cheque'>{row.get('cheque_body') or ''}</div>"
        )
        defaults = {
            "heading": row.get("lead_title") or "Together, We Can Make a Change",
            "subheading": "Partner with Nairobi Chapel Ngong Hills",
            "body": body,
            "meta_title": "Give | Nairobi Chapel Ngong Hills",
            "meta_description": strip_tags(row.get("lead_text") or "")[:300],
        }
        existing = PageCopy.objects.filter(page_slug="give").first()
        if existing:
            self._fill_blank_fields(existing, defaults, "PageCopy:give")
        else:
            self._create(PageCopy, defaults, page_slug="give")

    def _restore_membership(self, con):
        rows = self._table_rows(con, "core_membership")
        if not rows:
            self.stats["unresolved"].append("Legacy Membership empty")
            return
        row = rows[0]
        self._upsert_dynamic_page(
            "membership",
            {
                "title": row.get("heading") or "Membership",
                "subtitle": row.get("subtitle") or "",
                "content": self._paras(row.get("body") or ""),
                "cta_text": row.get("button_text") or "Karibu",
                "cta_url": row.get("button_url") or "/contact",
                "image_url": self._media_url(row.get("hero_image")),
                "template": "split",
                "menu_placement": "engage",
                "show_in_menu": True,
                "is_active": True,
            },
        )

    def _restore_volunteer(self, con):
        rows = self._table_rows(con, "core_volunteer")
        if not rows:
            self.stats["unresolved"].append("Legacy Volunteer empty")
            return
        row = rows[0]
        body = row.get("body") or ""
        # Correct known legacy campus name for Ngong Hills site
        body = body.replace("Nairobi Chapel Waiyaki Way", "Nairobi Chapel Ngong Hills")
        self._upsert_dynamic_page(
            "volunteer",
            {
                "title": row.get("heading") or "Volunteer",
                "subtitle": row.get("subtitle") or "",
                "header_text": row.get("subtitle") or "",
                "content": body if "<" in body else self._paras(body),
                "cta_text": row.get("button_text") or "Volunteer",
                "cta_url": row.get("button_url") or "/contact",
                "image_url": self._media_url(row.get("hero_image")),
                "template": "split",
                "menu_placement": "engage",
                "show_in_menu": True,
                "is_active": True,
            },
        )

    def _restore_egroups(self, con):
        rows = [r for r in self._table_rows(con, "core_egroup") if r.get("is_published", 1)]
        if not rows:
            self.stats["unresolved"].append("Legacy EGroup empty")
            return
        intros = [r for r in rows if r["kind"] == "intro"]
        ledes = [r for r in rows if r["kind"] == "lede"]
        pillars = sorted([r for r in rows if r["kind"] == "pillar"], key=lambda r: r.get("sort_order") or 0)
        parts = []
        for r in sorted(intros, key=lambda x: x.get("sort_order") or 0):
            parts.append(self._paras(r.get("body") or ""))
        for r in ledes:
            parts.append(self._paras(r.get("body") or ""))
        if pillars:
            parts.append("<div class='egroups-pillars'>")
            for r in pillars:
                parts.append(
                    f"<section><h3>{escape(r.get('title') or '')}</h3>{self._paras(r.get('body') or '')}</section>"
                )
            parts.append("</div>")
        self._upsert_dynamic_page(
            "egroups",
            {
                "title": "eGroups",
                "subtitle": "Small Groups",
                "content": "".join(parts),
                "template": "content_only",
                "menu_placement": "ministries",
                "show_in_menu": True,
                "is_active": True,
            },
        )

    def _restore_plugin(self, con):
        rows = [r for r in self._table_rows(con, "core_plugin") if r.get("is_published", 1)]
        if not rows:
            self.stats["unresolved"].append("Legacy Plugin empty")
            return
        by_kind = {}
        for r in rows:
            by_kind.setdefault(r["kind"], []).append(r)
        parts = []
        for r in by_kind.get("lead", []):
            parts.append(self._paras(r.get("body") or ""))
        for r in by_kind.get("about", []):
            parts.append(f"<h2>{escape(r.get('title') or 'About Plug-In')}</h2>")
            parts.append(self._paras(r.get("body") or ""))
        for r in by_kind.get("objectives_title", []):
            parts.append(f"<h2>{escape(r.get('title') or 'Objectives')}</h2>")
        for r in sorted(by_kind.get("objective", []), key=lambda x: x.get("sort_order") or 0):
            parts.append(f"<h3>{escape(r.get('title') or '')}</h3>{self._paras(r.get('body') or '')}")
        for r in by_kind.get("how", []):
            parts.append(f"<h2>{escape(r.get('title') or 'How does Plug-In work?')}</h2>")
            parts.append(self._paras(r.get("body") or ""))
        self._upsert_dynamic_page(
            "prayer",
            {
                "title": "Plug-In",
                "subtitle": "10 week discipleship experience",
                "content": "".join(parts),
                "template": "content_only",
                "menu_placement": "ministries",
                "show_in_menu": True,
                "is_active": True,
            },
        )

    def _restore_quest(self, con):
        rows = [r for r in self._table_rows(con, "core_quest") if r.get("is_published", 1)]
        if not rows:
            self.stats["unresolved"].append("Legacy Quest empty")
            return
        parts = []
        image_url = ""
        for r in sorted(rows, key=lambda x: x.get("sort_order") or 0):
            parts.append(f"<h2>{escape(r.get('heading') or '')}</h2>")
            parts.append(self._paras(r.get("body") or ""))
            parts.append(self._bullets_html(r.get("bullet_points") or ""))
            if not image_url:
                image_url = self._media_url(r.get("image"))
        self._upsert_dynamic_page(
            "quest",
            {
                "title": "QUEST",
                "subtitle": "Children's Ministry",
                "content": "".join(parts),
                "image_url": image_url,
                "template": "content_only",
                "menu_placement": "ministries",
                "show_in_menu": True,
                "is_active": True,
                "cta_text": "Contact us about Quest",
                "cta_url": "/contact",
            },
        )

    def _restore_club_fusion(self, con):
        rows = [r for r in self._table_rows(con, "core_clubfusion") if r.get("is_published", 1)]
        if not rows:
            self.stats["unresolved"].append("Legacy ClubFusion empty")
            return
        parts = []
        image_url = ""
        for r in sorted(rows, key=lambda x: x.get("sort_order") or 0):
            kicker = escape(r.get("kicker") or "")
            title = escape(r.get("title") or "")
            if kicker:
                parts.append(f"<p class='text-uppercase small fw-semibold'>{kicker}</p>")
            parts.append(f"<h2>{title}</h2>")
            parts.append(self._paras(r.get("body") or ""))
            if not image_url:
                image_url = self._media_url(r.get("image"))
        self._upsert_dynamic_page(
            "club-fusion",
            {
                "title": "Club Fusion",
                "subtitle": "Teens' Church",
                "content": "".join(parts),
                "image_url": image_url,
                "template": "content_only",
                "menu_placement": "ministries",
                "show_in_menu": True,
                "is_active": True,
            },
        )

    def _restore_club_fusion_resources(self, con):
        for row in self._table_rows(con, "core_clubfusionresource"):
            if not row.get("is_published", 1):
                continue
            note = (row.get("note") or "").strip()
            date = row.get("resource_date")
            existing = ClubFusionResource.objects.filter(resource_date=date, note=note).first()
            defaults = {
                "document_url": self._file_url(row.get("resource_file")),
                "order": int(row.get("sort_order") or 0),
                "is_active": True,
            }
            if existing:
                self._fill_blank_fields(existing, defaults, f"ClubFusionResource:{note}")
            else:
                if self.dry_run:
                    self.stats["created"] += 1
                    self._log("created", f"ClubFusionResource {note} (dry-run)")
                else:
                    ClubFusionResource.objects.create(
                        resource_date=date,
                        note=note or "Resource",
                        **defaults,
                    )
                    self.stats["created"] += 1
                    self._log("created", f"ClubFusionResource {note}")

    def _restore_mens(self, con):
        rows = [r for r in self._table_rows(con, "core_mens") if r.get("is_published", 1)]
        if not rows:
            self.stats["unresolved"].append(
                "Legacy Mens empty — existing mens-ministry DynamicPage preserved"
            )
            return
        parts = []
        image_url = ""
        image2 = ""
        for r in sorted(rows, key=lambda x: x.get("sort_order") or 0):
            parts.append(f"<h2>{escape(r.get('heading') or '')}</h2>")
            parts.append(self._paras(r.get("body") or ""))
            if not image_url:
                image_url = self._media_url(r.get("image"))
            if not image2:
                image2 = self._media_url(r.get("image_secondary"))
        self._upsert_dynamic_page(
            "mens-ministry",
            {
                "title": "Men's Ministry",
                "content": "".join(parts),
                "image_url": image_url,
                "content_2": f'<p><img src="{escape(image2)}" alt=""></p>' if image2 else "",
                "template": "content_only",
                "menu_placement": "ministries",
                "show_in_menu": True,
                "is_active": True,
            },
        )

    def _restore_womens(self, con):
        rows = [r for r in self._table_rows(con, "core_womens") if r.get("is_published", 1)]
        if not rows:
            self.stats["unresolved"].append(
                "Legacy Womens empty — existing womens-ministry DynamicPage preserved"
            )
            return
        parts = []
        image_url = ""
        for r in sorted(rows, key=lambda x: x.get("sort_order") or 0):
            parts.append(f"<h2>{escape(r.get('heading') or '')}</h2>")
            parts.append(self._paras(r.get("body") or ""))
            if not image_url:
                image_url = self._media_url(r.get("image"))
        self._upsert_dynamic_page(
            "womens-ministry",
            {
                "title": "Women's Ministry",
                "content": "".join(parts),
                "image_url": image_url,
                "template": "content_only",
                "menu_placement": "ministries",
                "show_in_menu": True,
                "is_active": True,
            },
        )

    def _restore_bible_study(self, con):
        contents = [r for r in self._table_rows(con, "core_biblestudycontent") if r.get("is_published", 1)]
        guides = [r for r in self._table_rows(con, "core_biblestudyguide") if r.get("is_published", 1)]
        if contents:
            parts = []
            for r in sorted(contents, key=lambda x: x.get("sort_order") or 0):
                parts.append(f"<h2>{escape(r.get('heading') or 'Bible Study')}</h2>")
                parts.append(self._paras(r.get("body") or ""))
            self._upsert_dynamic_page(
                "bible-study",
                {
                    "title": "Bible Study",
                    "content": "".join(parts),
                    "template": "split",
                    "menu_placement": "resources",
                    "show_in_menu": True,
                    "is_active": True,
                },
            )
        else:
            self.stats["unresolved"].append("Legacy BibleStudyContent empty")

        if not guides:
            self.stats["unresolved"].append(
                "Legacy BibleStudyGuide empty — existing BibleStudyResource rows preserved"
            )
            return
        for row in guides:
            desc = (row.get("notes") or "").strip() or "Bible study guide"
            date = row.get("study_date")
            existing = BibleStudyResource.objects.filter(session_date=date, description=desc).first()
            defaults = {
                "document_url": self._file_url(row.get("guide_file")),
                "order": int(row.get("sort_order") or 0),
                "is_active": True,
            }
            if existing:
                self._fill_blank_fields(existing, defaults, f"BibleStudyResource:{desc}")
            else:
                if self.dry_run:
                    self.stats["created"] += 1
                    self._log("created", f"BibleStudyResource {desc} (dry-run)")
                else:
                    BibleStudyResource.objects.create(session_date=date, description=desc, **defaults)
                    self.stats["created"] += 1
                    self._log("created", f"BibleStudyResource {desc}")

    def _restore_gallery(self, con):
        albums = self._table_rows(con, "core_galleryalbum")
        images = self._table_rows(con, "core_galleryimage")
        if not albums:
            self.stats["unresolved"].append("Legacy GalleryAlbum empty")
            return
        images_by_album: dict[int, list] = {}
        for img in images:
            images_by_album.setdefault(img["album_id"], []).append(img)

        for album in albums:
            if not album.get("is_published", 1):
                continue
            slug = (album.get("slug") or slugify(album.get("title") or "")).strip()
            title = (album.get("title") or slug).strip()
            existing = GalleryAlbum.objects.filter(slug=slug).first()
            defaults = {
                "title": title,
                "event_date": album.get("event_date"),
                "is_published": True,
            }
            if existing:
                self._fill_blank_fields(existing, defaults, f"GalleryAlbum:{slug}")
                album_obj = existing
            else:
                if self.dry_run:
                    self.stats["created"] += 1
                    self._log("created", f"GalleryAlbum {slug} (dry-run)")
                    album_obj = None
                else:
                    album_obj = GalleryAlbum.objects.create(slug=slug, **defaults)
                    self.stats["created"] += 1
                    self._log("created", f"GalleryAlbum {slug}")

            for img in sorted(images_by_album.get(album["id"], []), key=lambda x: (x.get("sort_order") or 0, x["id"])):
                image_url = self._media_url(img.get("image"))
                if not image_url:
                    self.stats["unresolved"].append(f"Gallery image unresolved: {img.get('image')}")
                    continue
                caption = img.get("caption") or ""
                order = int(img.get("sort_order") or 0)
                if album_obj is None:
                    # dry-run without album instance
                    self.stats["created"] += 1
                    self._log("created", f"GalleryImage {image_url} (dry-run)")
                    continue
                existing_img = GalleryImage.objects.filter(album=album_obj, image_url=image_url).first()
                if existing_img:
                    self._fill_blank_fields(
                        existing_img,
                        {"caption": caption, "order": order},
                        f"GalleryImage:{album_obj.slug}:{order}",
                    )
                else:
                    if self.dry_run:
                        self.stats["created"] += 1
                        self._log("created", f"GalleryImage for {album_obj.slug} (dry-run)")
                    else:
                        GalleryImage.objects.create(
                            album=album_obj,
                            image_url=image_url,
                            caption=caption,
                            order=order,
                        )
                        self.stats["created"] += 1
                        self._log("created", f"GalleryImage for {album_obj.slug}")

    def _ensure_gallery_nav_page(self):
        self._upsert_dynamic_page(
            "gallery",
            {
                "title": "Gallery",
                "subtitle": "Photos from our church events and gatherings",
                "content": "<p>Browse photos from our church events and gatherings.</p>",
                "template": "content_only",
                "menu_placement": "engage",
                "menu_order": 5,
                "show_in_menu": True,
                "is_active": True,
            },
        )

    def _print_summary(self):
        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING("Legacy CMS restore summary"))
        self.stdout.write(f"  created:      {self.stats['created']}")
        self.stdout.write(f"  updated:      {self.stats['updated']}")
        self.stdout.write(f"  skipped:      {self.stats['skipped']}")
        self.stdout.write(f"  media copied: {self.stats['media_copied']}")
        if self.stats["unresolved"]:
            self.stdout.write(self.style.NOTICE("  unresolved / notes:"))
            for item in self.stats["unresolved"]:
                self.stdout.write(f"    - {item}")
        if self.dry_run:
            self.stdout.write(self.style.WARNING("Dry-run complete — no database writes committed."))
