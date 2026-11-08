# Women's Ministry body: numbered list + optional main polaroid image URL.

from django.db import migrations

WOMENS_CONTENT = (
    "<p>Glow seeks to provide ladies young and old, with opportunities to build authentic relationships. We aim to "
    "encourage ladies to function in their true identity, as we empower them on issues of life and faith.</p>"
    "<p>When women work together, it&rsquo;s a bond unlike any other. Strong women stand together, lift each other up "
    "and empower one another through prayer. Women don&rsquo;t always get to choose life&rsquo;s circumstances but we do "
    "get to choose how we&rsquo;ll respond: with Strength, Stamina and a Staying Perseverance. That can only be possible "
    "if we choose to have God walk with us. Glow lays the foundation to make that possible.</p>"
    "<p>Why is being a part of the Glow Circle the best decision you could make? Because we all need each other. "
    "This is what Glow is about.</p>"
    '<ol class="womens-ministry-page__steps">'
    "<li>Glow encourages all ladies to function in their true identity, through forums that increase their knowledge of "
    "God, and strengthen their personal faith.</li>"
    "<li>Glow creates opportunities for fellowship and accountability for ladies to walk with, challenge and support "
    "one another as they grow to the next levels.</li>"
    "<li>Glow also gives ladies a safe forum to connect emotionally, socially, spiritually and psychologically as they "
    "develop new friendships.</li>"
    "</ol>"
)

TOP_POLAROID_IMG = (
    "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774086292/world-book-day-celebration_1_v5bea0.jpg"
)


def update_womens_ministry_layout(apps, schema_editor):
    DynamicPage = apps.get_model("main", "DynamicPage")
    DynamicPage.objects.filter(slug="womens-ministry").update(
        content=WOMENS_CONTENT,
        image_url=TOP_POLAROID_IMG,
        alt_text="Women\u2019s ministry \u2014 Glow fellowship and celebration",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0030_womens_ministry_page"),
    ]

    operations = [
        migrations.RunPython(update_womens_ministry_layout, migrations.RunPython.noop),
    ]
