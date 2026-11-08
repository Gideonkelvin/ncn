# Men's Ministry page under Ministries nav (Jabari).

from django.db import migrations

MENS_MINISTRY_CONTENT = (
    '<blockquote class="blockquote border-start border-3 ps-3 ms-1 mb-4" style="border-color: var(--bs-primary) !important;">'
    "<p class=\"mb-0\">&ldquo;&hellip; They were brave warriors, ready for battle and able to handle the shield and spear. "
    "Their faces were the faces of lions, and they were as swift as gazelles in the mountains.&rdquo;</p>"
    '<footer class="blockquote-footer mt-2">1 Chronicles 12:8</footer>'
    "</blockquote>"
    "<p>The Jabari Men&rsquo;s Ministry is a gathering place for men to grow their faith in depth as they address faith "
    "issues relevant to men. Jabari aims to create an environment for men to encounter and relate with Jesus Christ "
    "unashamedly, and become disciples who live out their faith at home, in the church, in community and in the marketplace.</p>"
    "<p>Have you ever seen the funny street interview video on the web where random men on the street were asked "
    "&ldquo;What is a man?&rdquo; Very few could answer. Try it with your friends. Short of saying men are men; and men "
    "procreate, most men don&rsquo;t know what it means to be a man. No-one teaches them today on what it means to be a man, "
    "and what a man&rsquo;s role in society is?</p>"
    "<p>Some of the initiatives implemented towards this vision include:</p>"
    '<h3 class="h4 mt-4 mb-3">jabariMan Enough</h3>'
    "<p>This is a 10-week, entry-point, discipleship program that seeks to answer that question from the bible. What is "
    "biblical manhood and what is the place of a godly man in today&rsquo;s society? What does God expect of men and what "
    "special mandate has he given men? Man Enough leads men to discover their identity, clearly states the 5-fold marks of a "
    "man, and helps men catch a vision of how to live more effective lives at home, at work, in the community, in the church, "
    "and within the nation.</p>"
    '<h3 class="h4 mt-4 mb-3">The King&rsquo;s Gathering</h3>'
    "<p>This is a monthly breakfast gathering of men for a Kings feast. The meeting creates a safe space for men to discuss "
    "matters pertinent to them, foster community, and inspires men to step out and stand out in society as Godly men.</p>"
    '<h3 class="h4 mt-4 mb-3">jabari24th Man Prayer Ministry</h3>'
    "<p>The Kings Gathering also affords an opportunity for men to pray together. This they do in bonded 3 men prayer groups, "
    "inviting the 4th Man (Jesus) to come join with them. The bible story in Daniel 3 talks of Daniel&rsquo;s 3 friends who "
    "were thrown into a blazing hot furnace. But when the King looked to see if they had been burned at all, he exclaimed in "
    "shock &ldquo;Nebuchadnezzar leaped to his feet in amazement and asked his advisers, &lsquo;Weren&rsquo;t there three men "
    "that we tied up and threw into the fire?&rsquo; They replied, &lsquo;Certainly, Your Majesty.&rsquo; He said, &lsquo;Look! "
    "I see four men walking around in the fire, unbound and unharmed, and the fourth looks like a son of the gods.&rsquo;&rdquo; "
    "(Daniel 3:24)</p>"
    "<p>No matter how hot the furnace of business, survival, integrity, home or career gets, when the 4th man is there, men "
    "can come through shining instead of singed. Men&rsquo;s values, integrity, and honour does not have to be sacrificed. "
    "There is a way to prevail &ndash; by ensuring the 4th Man is there!</p>"
)


def add_mens_ministry(apps, schema_editor):
    DynamicPage = apps.get_model("main", "DynamicPage")
    DynamicPage.objects.update_or_create(
        slug="mens-ministry",
        defaults={
            "title": "Men\u2019s Ministry",
            "subtitle": "Jabari — growing in biblical manhood",
            "meta_title": "Men\u2019s Ministry (Jabari)",
            "meta_description": (
                "Jabari Men\u2019s Ministry: discipleship, the King\u2019s Gathering, and jabari24th Man prayer — "
                "men growing in faith at Nairobi Chapel Ngong Hills."
            ),
            "template": "content_only",
            "header_text": "",
            "content": MENS_MINISTRY_CONTENT,
            "content_2": "",
            "image_url": "",
            "alt_text": "",
            "cta_text": "",
            "cta_url": "",
            "cta_text_2": "",
            "cta_url_2": "",
            "menu_placement": "ministries",
            "menu_order": 4,
            "show_in_menu": True,
            "is_active": True,
            "order": 5,
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0028_pastoral_team_six_members"),
    ]

    operations = [
        migrations.RunPython(add_mens_ministry, migrations.RunPython.noop),
    ]
