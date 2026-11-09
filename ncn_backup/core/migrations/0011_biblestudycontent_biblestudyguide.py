from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0010_mens_image_secondary_womens_image_secondary"),
    ]

    operations = [
        migrations.CreateModel(
            name="BibleStudyContent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("heading", models.CharField(default="Bible Study", max_length=200)),
                (
                    "body",
                    models.TextField(help_text="Main page text. Use line breaks to separate paragraphs."),
                ),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                ("is_published", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Bible Study content",
                "verbose_name_plural": "Bible Study content",
                "ordering": ["sort_order", "id"],
            },
        ),
        migrations.CreateModel(
            name="BibleStudyGuide",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("study_date", models.DateField(help_text="Select the posting/study date.")),
                ("notes", models.CharField(help_text="Short notes text for this row.", max_length=255)),
                (
                    "guide_file",
                    models.FileField(
                        blank=True,
                        help_text="Upload the Bible study guide file.",
                        null=True,
                        upload_to="bible_study/guides/",
                    ),
                ),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                ("is_published", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Bible Study guide row",
                "verbose_name_plural": "Bible Study guide rows",
                "ordering": ["-study_date", "sort_order", "id"],
            },
        ),
    ]

