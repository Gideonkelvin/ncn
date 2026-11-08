# Remove Church Services CMS page and proxy admin model.

from django.db import migrations


def delete_services_dynamic_page(apps, schema_editor):
    DynamicPage = apps.get_model("main", "DynamicPage")
    DynamicPage.objects.filter(slug="services").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0016_prayer_plug_in_content"),
    ]

    operations = [
        migrations.RunPython(delete_services_dynamic_page, migrations.RunPython.noop),
        migrations.DeleteModel(
            name="ServicesPage",
        ),
    ]
