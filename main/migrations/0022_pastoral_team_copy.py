"""Pastoral page: Lead Pastor / Rev. Collins Ouma + Daniel Aswa bio (CMS body)."""

from django.db import migrations

DANIEL_BIO = (
    "<p>Daniel Aswa is a devoted husband to his wife, Ressy, and together they have two 11-year-old twins, "
    "Immanuel and Ariel. A lifelong servant of the Lord, Daniel gave his life to Christ in 2003 and has "
    "faithfully served in ministry from his home church in Busia to university fellowships, IVC Church in "
    "Eldoret, and now Nairobi Chapel.</p>"
    "<p>He is passionate about discipleship, mentorship, intercessory prayer, and pastoral care, especially "
    "mentoring young boys and supporting ministry teams. Professionally, Daniel is an experienced Data "
    "Scientist and public health researcher with over 15 years of work in epidemiology, contributing to "
    "healthcare improvements in Kenya. He is a servant leader who seeks to impact lives both within and "
    "beyond the church.</p>"
)


def sync_pastoral_copy(apps, schema_editor):
    DynamicPage = apps.get_model("main", "DynamicPage")
    row = DynamicPage.objects.filter(slug="pastoral").first()
    if not row:
        return
    DynamicPage.objects.filter(pk=row.pk).update(
        header_text="",
        content=DANIEL_BIO,
        alt_text="Lead Pastor — Rev. Collins Ouma and pastoral team",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0021_pastorate_nav_label"),
    ]

    operations = [
        migrations.RunPython(sync_pastoral_copy, migrations.RunPython.noop),
    ]
