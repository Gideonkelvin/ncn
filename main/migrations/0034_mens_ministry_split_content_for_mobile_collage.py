# Split Men's Ministry HTML so mobile can show polaroid pairs between copy blocks.

from django.db import migrations


def split_mens_ministry_content(apps, schema_editor):
    DynamicPage = apps.get_model("main", "DynamicPage")
    page = DynamicPage.objects.filter(slug="mens-ministry").first()
    if not page:
        return
    # Only split when still single-block (avoid re-running on customized DB)
    if page.content_2:
        return
    full = (page.content or "").strip()
    needle = "<p>Some of the initiatives implemented towards this vision include:</p>"
    if needle in full:
        idx = full.index(needle)
        page.content = full[:idx].strip()
        page.content_2 = full[idx:].strip()
        page.save(update_fields=["content", "content_2"])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0033_bible_study_resources"),
    ]

    operations = [
        migrations.RunPython(split_mens_ministry_content, noop_reverse),
    ]
