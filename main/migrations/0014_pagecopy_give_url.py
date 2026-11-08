# Data migration: /donate → /give (PageCopy slug + CTA button links)

from django.db import migrations


def forwards(apps, schema_editor):
    PageCopy = apps.get_model("main", "PageCopy")
    CallToActionBlock = apps.get_model("main", "CallToActionBlock")

    if PageCopy.objects.filter(page_slug="give").exists():
        PageCopy.objects.filter(page_slug="donate").delete()
    else:
        PageCopy.objects.filter(page_slug="donate").update(page_slug="give")

    CallToActionBlock.objects.filter(primary_button_url="/donate").update(
        primary_button_url="/give"
    )


def backwards(apps, schema_editor):
    PageCopy = apps.get_model("main", "PageCopy")
    CallToActionBlock = apps.get_model("main", "CallToActionBlock")

    if PageCopy.objects.filter(page_slug="donate").exists():
        PageCopy.objects.filter(page_slug="give").delete()
    else:
        PageCopy.objects.filter(page_slug="give").update(page_slug="donate")

    CallToActionBlock.objects.filter(primary_button_url="/give").update(
        primary_button_url="/donate"
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0013_plugin_page_proxy"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
