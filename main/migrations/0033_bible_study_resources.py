# BibleStudyResource model + sample rows for /bible-study/ Resources table.

import datetime

from django.db import migrations, models


def seed_resources(apps, schema_editor):
    BibleStudyResource = apps.get_model("main", "BibleStudyResource")
    if BibleStudyResource.objects.exists():
        return
    BibleStudyResource.objects.create(
        session_date=datetime.date(2026, 3, 19),
        description="Romans 8 — Life in the Spirit (discussion & prayer)",
        document_url="",
        order=0,
        is_active=True,
    )
    BibleStudyResource.objects.create(
        session_date=datetime.date(2026, 3, 12),
        description="Romans 7 — The struggle with sin; practical application",
        document_url="",
        order=0,
        is_active=True,
    )


def trim_bible_study_subtitle(apps, schema_editor):
    DynamicPage = apps.get_model("main", "DynamicPage")
    DynamicPage.objects.filter(slug="bible-study").update(subtitle="")


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0032_site_settings_youtube_url"),
    ]

    operations = [
        migrations.CreateModel(
            name="BibleStudyResource",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("session_date", models.DateField()),
                ("description", models.CharField(help_text="Summary or topic (Resources table)", max_length=500)),
                (
                    "document_url",
                    models.URLField(
                        blank=True,
                        help_text="PDF or outline URL for View / Download (optional)",
                    ),
                ),
                ("order", models.PositiveIntegerField(db_index=True, default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Bible study · resource row",
                "verbose_name_plural": "Bible study · resource rows",
                "ordering": ["-session_date", "order", "id"],
            },
        ),
        migrations.RunPython(seed_resources, migrations.RunPython.noop),
        migrations.RunPython(trim_bible_study_subtitle, migrations.RunPython.noop),
    ]
