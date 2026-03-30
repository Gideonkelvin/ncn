"""Bible study page: text left / one image right (match other ministry pages)."""

from django.db import migrations

GROUP_IMG = (
    "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774088922/"
    "group-four-gorgeous-african-american-womans-wear-summer-hat-holding-hands-praying-green-grass-park_ncwcwr.jpg"
)


def sync_bible_study(apps, schema_editor):
    DynamicPage = apps.get_model("main", "DynamicPage")
    row = DynamicPage.objects.filter(slug="bible-study").first()
    if not row:
        return
    DynamicPage.objects.filter(pk=row.pk).update(
        content_2="",
        image_url=GROUP_IMG,
        alt_text="Bible study and fellowship",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0018_membership_volunteer_pastoral_layout_images"),
    ]

    operations = [
        migrations.RunPython(sync_bible_study, migrations.RunPython.noop),
    ]
