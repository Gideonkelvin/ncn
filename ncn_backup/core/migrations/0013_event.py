from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0012_biblestudyguide_created_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(help_text="Event title.", max_length=200)),
                ("organizer", models.CharField(blank=True, help_text="Organizer name (optional).", max_length=200)),
                ("venue", models.CharField(blank=True, help_text="Venue/location text (optional).", max_length=200)),
                ("start_at", models.DateTimeField(help_text="Event start date and time.")),
                ("image", models.ImageField(blank=True, help_text="Event card image (optional).", null=True, upload_to="events/")),
                ("button_text", models.CharField(default="Watch Online", help_text="Button text shown on the event card.", max_length=80)),
                ("button_url", models.URLField(blank=True, help_text="Optional button link. Leave empty if not needed.")),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                ("is_published", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Event",
                "verbose_name_plural": "Events",
                "ordering": ["start_at", "sort_order", "id"],
            },
        ),
    ]

