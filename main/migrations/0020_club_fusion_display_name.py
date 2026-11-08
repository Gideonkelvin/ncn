"""Rename Club Xpressions → Club Fusion in admin labels and CMS row."""

from django.db import migrations


def rename_club_fusion_page(apps, schema_editor):
    DynamicPage = apps.get_model("main", "DynamicPage")
    DynamicPage.objects.filter(slug="club-fusion").update(
        title="Club Fusion",
        alt_text="Club Fusion teens ministry",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0019_bible_study_page_layout"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="clubfusionpage",
            options={
                "verbose_name": "Page · Club Fusion (teens)",
                "verbose_name_plural": "Page · Club Fusion (teens)",
            },
        ),
        migrations.RunPython(rename_club_fusion_page, migrations.RunPython.noop),
    ]
