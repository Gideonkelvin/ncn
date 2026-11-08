from django.db import migrations, models


def seed_membership_volunteer(apps, schema_editor):
    Membership = apps.get_model("core", "Membership")
    Volunteer = apps.get_model("core", "Volunteer")
    if not Membership.objects.exists():
        Membership.objects.create(
            heading="Membership",
            subtitle="Growing in Faith, Together",
            body=(
                "Become a part of our vibrant church community. Membership is a way to formally express "
                "your commitment to our church family and connect with others on a deeper level. "
                "It's a step towards deeper discipleship and service within our community."
            ),
            button_text="Karibu",
            button_url="",
            is_published=True,
        )
    if not Volunteer.objects.exists():
        Volunteer.objects.create(
            heading="Volunteer",
            subtitle="Serving God with Your Gifts",
            body=(
                "Volunteering at Nairobi Chapel Waiyaki Way provides an opportunity to use your gifts "
                "and talents to serve God and others. Whether in ministries, events, or outreach, "
                "there's a place for you to make a meaningful impact and be part of our mission to serve "
                "the community."
            ),
            button_text="Volunteer",
            button_url="",
            is_published=True,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0013_event"),
    ]

    operations = [
        migrations.CreateModel(
            name="Membership",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("heading", models.CharField(default="Membership", max_length=200)),
                ("subtitle", models.CharField(blank=True, max_length=300)),
                ("body", models.TextField(help_text="Main paragraph shown in the hero.")),
                (
                    "hero_image",
                    models.ImageField(
                        blank=True,
                        help_text="Hero background image. If empty, the default theme image is used.",
                        null=True,
                        upload_to="membership/",
                    ),
                ),
                ("button_text", models.CharField(default="Karibu", max_length=80)),
                (
                    "button_url",
                    models.URLField(
                        blank=True,
                        help_text="Optional button link. Leave empty to use the Contact page.",
                    ),
                ),
                ("is_published", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Membership",
                "verbose_name_plural": "Membership",
            },
        ),
        migrations.CreateModel(
            name="Volunteer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("heading", models.CharField(default="Volunteer", max_length=200)),
                ("subtitle", models.CharField(blank=True, max_length=300)),
                ("body", models.TextField(help_text="Main paragraph shown in the hero.")),
                (
                    "hero_image",
                    models.ImageField(
                        blank=True,
                        help_text="Hero background image. If empty, the default theme image is used.",
                        null=True,
                        upload_to="volunteer/",
                    ),
                ),
                ("button_text", models.CharField(default="Volunteer", max_length=80)),
                (
                    "button_url",
                    models.URLField(
                        blank=True,
                        help_text="Optional button link. Leave empty to use the Contact page.",
                    ),
                ),
                ("is_published", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Volunteer",
                "verbose_name_plural": "Volunteer",
            },
        ),
        migrations.RunPython(seed_membership_volunteer, migrations.RunPython.noop),
    ]
