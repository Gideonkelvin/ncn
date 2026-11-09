from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_womens"),
    ]

    operations = [
        migrations.AddField(
            model_name="mens",
            name="image_secondary",
            field=models.ImageField(
                blank=True,
                help_text="Optional second image for collage layout.",
                null=True,
                upload_to="mens/",
            ),
        ),
        migrations.AddField(
            model_name="womens",
            name="image_secondary",
            field=models.ImageField(
                blank=True,
                help_text="Optional second image for collage layout.",
                null=True,
                upload_to="womens/",
            ),
        ),
    ]

