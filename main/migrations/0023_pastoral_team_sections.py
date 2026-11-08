# Pastoral /pastoral/ page: five alternating profile sections + remove CTA button.

from django.db import migrations, models

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
GROUP_IMG = (
    "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774088922/"
    "group-four-gorgeous-african-american-womans-wear-summer-hat-holding-hands-praying-green-grass-park_ncwcwr.jpg"
)
BIBLE_IMG = (
    "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774088737/"
    "closeup-shot-male-sitting-park-while-holding-bible_ansfw7.jpg"
)
FIRST_SECTION_IMG = (
    "https://res.cloudinary.com/dogxiekul/image/upload/v1774715728/"
    "WhatsApp_Image_2026-03-28_at_15.35.32_1_lauxoj.jpg"
)
SECOND_SECTION_IMG = (
    "https://res.cloudinary.com/dogxiekul/image/upload/v1774716501/"
    "WhatsApp_Image_2026-03-28_at_19.45.29_l9yt0f.jpg"
)
ERICK_BIO = (
    "<p>At Nairobi Chapel Ngong Hills, I am an associate pastor and also the pastor in charge of missions. "
    "My passion is to see God's people grow, serve, and share Christ in the spaces God has placed them.</p>"
    "<p>I am happy to be part of a well-knit faith community at Nairobi Chapel Ngong Hills. "
    "My hobby is cycling.</p>"
)


def seed_pastoral_sections_and_clear_cta(apps, schema_editor):
    PastoralTeamSection = apps.get_model("main", "PastoralTeamSection")
    DynamicPage = apps.get_model("main", "DynamicPage")
    if not PastoralTeamSection.objects.exists():
        rows = [
            {
                "order": 0,
                "eyebrow": "Lead Pastor",
                "name_heading": "Rev. Collins Ouma",
                "subheading": "Daniel Aswa",
                "body": DANIEL_BIO,
                "image_url": FIRST_SECTION_IMG,
                "alt_text": "Lead Pastor — Rev. Collins Ouma and pastoral team",
            },
            {
                "order": 1,
                "eyebrow": "Associate Pastor",
                "name_heading": "Pst. Erick Wanjala",
                "subheading": "",
                "body": ERICK_BIO,
                "image_url": SECOND_SECTION_IMG,
                "alt_text": "Pst. Erick Wanjala — Associate Pastor",
            },
            {
                "order": 2,
                "eyebrow": "Pastoral team",
                "name_heading": "Team member",
                "subheading": "",
                "body": "<p>Biography coming soon.</p>",
                "image_url": GROUP_IMG,
                "alt_text": "Pastoral team",
            },
            {
                "order": 3,
                "eyebrow": "Pastoral team",
                "name_heading": "Team member",
                "subheading": "",
                "body": "<p>Biography coming soon.</p>",
                "image_url": BIBLE_IMG,
                "alt_text": "Pastoral team",
            },
            {
                "order": 4,
                "eyebrow": "Pastoral Care And Discipleship",
                "name_heading": "Pst. Daniel Aswa",
                "subheading": "",
                "body": (
                    "<p>Daniel Aswa is a devoted husband to his wife, Ressy, and father to their 11-year-old twins, "
                    "Immanuel and Ariel. He gave his life to Christ in 2003 and has faithfully served in ministry "
                    "from Busia to university fellowships, IVC Church Eldoret, and now Nairobi Chapel.</p>"
                    "<p>He is passionate about discipleship, mentorship, intercessory prayer, and pastoral care. "
                    "Professionally, he is a Data Scientist and public health researcher with over 15 years of "
                    "experience, contributing to healthcare improvements in Kenya. Daniel is a servant leader committed "
                    "to impacting lives both in and beyond the church.</p>"
                ),
                "image_url": FIRST_SECTION_IMG,
                "alt_text": "Pst. Daniel Aswa — Pastoral care and discipleship",
            },
        ]
        for r in rows:
            PastoralTeamSection.objects.create(is_active=True, **r)
    DynamicPage.objects.filter(slug="pastoral").update(cta_text="", cta_url="")


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0022_pastoral_team_copy"),
    ]

    operations = [
        migrations.CreateModel(
            name="PastoralTeamSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveSmallIntegerField(db_index=True, default=0)),
                (
                    "eyebrow",
                    models.CharField(
                        blank=True,
                        help_text='Small label above the name (e.g. "Lead Pastor")',
                        max_length=120,
                    ),
                ),
                (
                    "name_heading",
                    models.CharField(
                        help_text="Primary name line (e.g. Rev. Collins Ouma)",
                        max_length=200,
                    ),
                ),
                (
                    "subheading",
                    models.CharField(
                        blank=True,
                        help_text="Secondary line (e.g. Daniel Aswa)",
                        max_length=200,
                    ),
                ),
                ("body", models.TextField(blank=True, help_text="Biography (HTML allowed)")),
                ("image_url", models.URLField(blank=True, help_text="Cloudinary or other image URL")),
                ("alt_text", models.CharField(blank=True, max_length=200)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Pastoral page · team section",
                "verbose_name_plural": "Pastoral page · team sections",
                "ordering": ["order", "id"],
            },
        ),
        migrations.RunPython(seed_pastoral_sections_and_clear_cta, migrations.RunPython.noop),
    ]
