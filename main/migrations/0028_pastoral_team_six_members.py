# Six team blocks on /pastoral/: renumber Daniel to order 5, add Mario (order 4), refresh titles.

from django.db import migrations

PLACEHOLDER = "<p>Biography coming soon.</p>"
GROUP_IMG = (
    "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774088922/"
    "group-four-gorgeous-african-american-womans-wear-summer-hat-holding-hands-praying-green-grass-park_ncwcwr.jpg"
)


def pastoral_team_six_members(apps, schema_editor):
    PastoralTeamSection = apps.get_model("main", "PastoralTeamSection")
    # Former fifth block (Daniel) becomes sixth
    PastoralTeamSection.objects.filter(order=4).update(order=5)

    PastoralTeamSection.objects.filter(order=0).update(
        eyebrow="Lead Pastor",
        name_heading="Rev. Collins Ouma",
        subheading="",
        alt_text="Rev. Collins Ouma — Lead Pastor",
    )
    PastoralTeamSection.objects.filter(order=1).update(
        eyebrow="Associate Pastor",
        name_heading="Pst. Erick B. Wanjala",
        alt_text="Pst. Erick B. Wanjala — Associate Pastor",
    )
    PastoralTeamSection.objects.filter(order=2).update(
        eyebrow="Admin and Club Fusion Pastor",
        name_heading="Pst. Brian Nyamuhu",
        subheading="",
        body=PLACEHOLDER,
        alt_text="Pst. Brian Nyamuhu — Admin and Club Fusion Pastor",
    )
    PastoralTeamSection.objects.filter(order=3).update(
        eyebrow="Children's Ministry",
        name_heading="Pst. Jecinta",
        subheading="",
        body=PLACEHOLDER,
        alt_text="Pst. Jecinta — Children's Ministry",
    )

    PastoralTeamSection.objects.create(
        is_active=True,
        order=4,
        eyebrow="Services and Worship",
        name_heading="Pst. Mario Omondi",
        subheading="",
        body=PLACEHOLDER,
        image_url=GROUP_IMG,
        alt_text="Pst. Mario Omondi — Services and Worship",
    )

    PastoralTeamSection.objects.filter(order=5).update(
        eyebrow="Pastoral Care and Discipleship",
        name_heading="Pst. Daniel Aswa",
        subheading="",
        alt_text="Pst. Daniel Aswa — Pastoral care and discipleship",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0027_fifth_pastoral_section_same_image_as_first"),
    ]

    operations = [
        migrations.RunPython(pastoral_team_six_members, migrations.RunPython.noop),
    ]
