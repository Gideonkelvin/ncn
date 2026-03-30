"""Navbar label: Pastoral Care → Pastorate."""

from django.db import migrations


def set_pastorate_title(apps, schema_editor):
    DynamicPage = apps.get_model("main", "DynamicPage")
    DynamicPage.objects.filter(slug="pastoral").update(title="Pastorate")


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0020_club_fusion_display_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="pastoralcarepage",
            options={
                "verbose_name": "Page · Pastorate",
                "verbose_name_plural": "Page · Pastorate",
            },
        ),
        migrations.RunPython(set_pastorate_title, migrations.RunPython.noop),
    ]
