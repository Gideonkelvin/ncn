# Data migration: /prayer is Plug-In; retire duplicate /plug-in menu row

from django.db import migrations

HERO_IMG = (
    "https://res.cloudinary.com/dqng2ekwm/image/upload/"
    "v1774088737/closeup-shot-male-sitting-park-while-holding-bible_ansfw7.jpg"
)


def forwards(apps, schema_editor):
    DynamicPage = apps.get_model("main", "DynamicPage")
    DynamicPage.objects.filter(slug="prayer").update(
        title="Plug-In",
        subtitle="How do I find My Purpose?",
        template="content_only",
        header_text="",
        content="",
        content_2="",
        image_url=HERO_IMG,
        alt_text="Plug-In ministry",
        cta_text="",
        cta_url="",
        menu_placement="ministries",
        show_in_menu=True,
    )
    DynamicPage.objects.filter(slug="plug-in").update(
        is_active=False,
        show_in_menu=False,
        menu_placement="none",
    )


def backwards(apps, schema_editor):
    DynamicPage = apps.get_model("main", "DynamicPage")
    DynamicPage.objects.filter(slug="prayer").update(
        title="Prayer Services",
        subtitle="Connect through Prayer",
        template="full_width",
        header_text=(
            "Prayer is at the heart of everything we do. Join us for prayer services "
            "and experience the power of communal prayer."
        ),
        content=(
            "<p>We believe that prayer changes lives and communities. Our prayer services "
            "are open to everyone who wants to seek God's presence and experience His peace."
            "</p><p><strong>Prayer Meeting Times:</strong></p><ul>"
            "<li>Wednesday evenings: 6:00 PM</li><li>Sunday mornings: 8:30 AM</li></ul>"
        ),
        cta_text="Join Prayer Meeting",
        cta_url="/contact",
    )
    DynamicPage.objects.filter(slug="plug-in").update(
        is_active=True,
        show_in_menu=True,
        menu_placement="ministries",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0015_event_watch_online_url"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
