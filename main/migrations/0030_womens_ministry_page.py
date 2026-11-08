# Women's Ministry page under Ministries nav (Glow).

from django.db import migrations

WOMENS_MINISTRY_CONTENT = (
    "<p>Glow seeks to provide ladies young and old, with opportunities to build authentic relationships. We aim to "
    "encourage ladies to function in their true identity, as we empower them on issues of life and faith.</p>"
    "<p>When women work together, it&rsquo;s a bond unlike any other. Strong women stand together, lift each other up "
    "and empower one another through prayer. Women don&rsquo;t always get to choose life&rsquo;s circumstances but we do "
    "get to choose how we&rsquo;ll respond: with Strength, Stamina and a Staying Perseverance. That can only be possible "
    "if we choose to have God walk with us. Glow lays the foundation to make that possible.</p>"
    "<p>Why is being a part of the Glow Circle the best decision you could make? Because we all need each other. "
    "This is what Glow is about.</p>"
    "<p><strong>Glow</strong> encourages all ladies to function in their true identity, through forums that increase "
    "their knowledge of God, and strengthen their personal faith.</p>"
    "<p><strong>Glow</strong> creates opportunities for fellowship and accountability for ladies to walk with, challenge "
    "and support one another as they grow to the next levels.</p>"
    "<p><strong>Glow</strong> also gives ladies a safe forum to connect emotionally, socially, spiritually and "
    "psychologically as they develop new friendships.</p>"
)


def add_womens_ministry(apps, schema_editor):
    DynamicPage = apps.get_model("main", "DynamicPage")
    DynamicPage.objects.update_or_create(
        slug="womens-ministry",
        defaults={
            "title": "Women\u2019s Ministry",
            "subtitle": "Glow — authentic relationships and growing in faith",
            "meta_title": "Women\u2019s Ministry (Glow)",
            "meta_description": (
                "Glow Women\u2019s Ministry at Nairobi Chapel Ngong Hills: authentic relationships, fellowship, "
                "and growing together in faith."
            ),
            "template": "content_only",
            "header_text": "",
            "content": WOMENS_MINISTRY_CONTENT,
            "content_2": "",
            "image_url": "",
            "alt_text": "",
            "cta_text": "",
            "cta_url": "",
            "cta_text_2": "",
            "cta_url_2": "",
            "menu_placement": "ministries",
            "menu_order": 5,
            "show_in_menu": True,
            "is_active": True,
            "order": 6,
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0029_mens_ministry_page"),
    ]

    operations = [
        migrations.RunPython(add_womens_ministry, migrations.RunPython.noop),
    ]
