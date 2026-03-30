"""Update first pastoral section: reuse third image and set short bio."""

from django.db import migrations


def update_first_section_image_and_bio(apps, schema_editor):
    PastoralTeamSection = apps.get_model("main", "PastoralTeamSection")

    # Use the image from the third visible block (order=2) if available.
    third = PastoralTeamSection.objects.filter(order=2).first()
    image_url = getattr(third, "image_url", "") or ""

    updates = {"body": "<p>Bio coming soon.</p>"}
    if image_url:
        updates["image_url"] = image_url

    if updates:
        PastoralTeamSection.objects.filter(order=0).update(**updates)


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0034_mens_ministry_split_content_for_mobile_collage"),
    ]

    operations = [
        migrations.RunPython(update_first_section_image_and_bio, migrations.RunPython.noop),
    ]

