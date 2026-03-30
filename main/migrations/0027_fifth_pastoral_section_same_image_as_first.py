# Fifth pastoral block (order=4): use same profile image as first block (Lead Pastor).

from django.db import migrations

FIRST_SECTION_IMG = (
    "https://res.cloudinary.com/dogxiekul/image/upload/v1774715728/"
    "WhatsApp_Image_2026-03-28_at_15.35.32_1_lauxoj.jpg"
)


def set_fifth_image_like_first(apps, schema_editor):
    PastoralTeamSection = apps.get_model("main", "PastoralTeamSection")
    PastoralTeamSection.objects.filter(order=4).update(image_url=FIRST_SECTION_IMG)


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0026_second_pastoral_section_erick"),
    ]

    operations = [
        migrations.RunPython(set_fifth_image_like_first, migrations.RunPython.noop),
    ]
