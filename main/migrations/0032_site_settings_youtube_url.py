# SiteSettings.youtube_url for footer social links.

from django.db import migrations, models


def backfill_youtube_url(apps, schema_editor):
    SiteSettings = apps.get_model("main", "SiteSettings")
    row = SiteSettings.objects.filter(pk=1).first()
    if row and not (row.youtube_url or "").strip():
        row.youtube_url = "https://www.youtube.com/@ncngonghills"
        row.save(update_fields=["youtube_url"])


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0031_womens_ministry_numbered_list"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="youtube_url",
            field=models.URLField(
                blank=True,
                help_text="YouTube channel URL (footer & social links)",
            ),
        ),
        migrations.RunPython(backfill_youtube_url, migrations.RunPython.noop),
    ]
