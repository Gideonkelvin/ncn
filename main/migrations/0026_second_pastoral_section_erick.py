# Second pastoral block (order=1): Pst. Erick Wanjala — Associate Pastor.

from django.db import migrations

SECOND_IMG = (
    "https://res.cloudinary.com/dogxiekul/image/upload/v1774716501/"
    "WhatsApp_Image_2026-03-28_at_19.45.29_l9yt0f.jpg"
)
ERICK_BIO = (
    "<p>At Nairobi Chapel Ngong Hills, I am an associate pastor and also the pastor in charge of missions. "
    "My passion is to see God's people grow, serve, and share Christ in the spaces God has placed them.</p>"
    "<p>I am happy to be part of a well-knit faith community at Nairobi Chapel Ngong Hills. "
    "My hobby is cycling.</p>"
)


def update_second_section(apps, schema_editor):
    PastoralTeamSection = apps.get_model("main", "PastoralTeamSection")
    PastoralTeamSection.objects.filter(order=1).update(
        eyebrow="Associate Pastor",
        name_heading="Pst. Erick Wanjala",
        subheading="",
        body=ERICK_BIO,
        image_url=SECOND_IMG,
        alt_text="Pst. Erick Wanjala — Associate Pastor",
    )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0025_first_pastoral_section_image"),
    ]

    operations = [
        migrations.RunPython(update_second_section, noop_reverse),
    ]
