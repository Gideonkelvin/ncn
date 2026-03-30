"""First pastoral team section: hero profile image."""

from django.db import migrations

FIRST_IMG = (
    "https://res.cloudinary.com/dogxiekul/image/upload/v1774715728/"
    "WhatsApp_Image_2026-03-28_at_15.35.32_1_lauxoj.jpg"
)


def set_first_section_image(apps, schema_editor):
    PastoralTeamSection = apps.get_model("main", "PastoralTeamSection")
    PastoralTeamSection.objects.filter(order=0).update(image_url=FIRST_IMG)


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0024_fifth_pastoral_section_daniel"),
    ]

    operations = [
        migrations.RunPython(set_first_section_image, migrations.RunPython.noop),
    ]
