"""Sync CMS fields for pastoral / membership / volunteer split-style layout."""

from django.db import migrations

GROUP_IMG = (
    "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774088922/"
    "group-four-gorgeous-african-american-womans-wear-summer-hat-holding-hands-praying-green-grass-park_ncwcwr.jpg"
)


def sync_page_images(apps, schema_editor):
    DynamicPage = apps.get_model("main", "DynamicPage")
    for slug, alt in (
        ("pastoral", "Pastoral care and prayer"),
        ("membership", "Church membership and community"),
        ("volunteer", "Volunteers serving together"),
    ):
        row = DynamicPage.objects.filter(slug=slug).first()
        if not row:
            continue
        DynamicPage.objects.filter(pk=row.pk).update(
            content_2="",
            image_url=GROUP_IMG,
            alt_text=alt,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0017_remove_services_page"),
    ]

    operations = [
        migrations.RunPython(sync_page_images, migrations.RunPython.noop),
    ]
