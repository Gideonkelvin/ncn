"""Fifth pastoral team block: Pastoral Care And Discipleship / Pst. Daniel Aswa + updated bio."""

from django.db import migrations

FIFTH_BODY = (
    "<p>Daniel Aswa is a devoted husband to his wife, Ressy, and father to their 11-year-old twins, "
    "Immanuel and Ariel. He gave his life to Christ in 2003 and has faithfully served in ministry from Busia "
    "to university fellowships, IVC Church Eldoret, and now Nairobi Chapel.</p>"
    "<p>He is passionate about discipleship, mentorship, intercessory prayer, and pastoral care. Professionally, "
    "he is a Data Scientist and public health researcher with over 15 years of experience, contributing to "
    "healthcare improvements in Kenya. Daniel is a servant leader committed to impacting lives both in and beyond "
    "the church.</p>"
)


def update_fifth_section(apps, schema_editor):
    PastoralTeamSection = apps.get_model("main", "PastoralTeamSection")
    PastoralTeamSection.objects.filter(order=4).update(
        eyebrow="Pastoral Care And Discipleship",
        name_heading="Pst. Daniel Aswa",
        subheading="",
        body=FIFTH_BODY,
        alt_text="Pst. Daniel Aswa — Pastoral care and discipleship",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0023_pastoral_team_sections"),
    ]

    operations = [
        migrations.RunPython(update_fifth_section, migrations.RunPython.noop),
    ]
