from django.db import migrations


def seed_clubfusion_defaults(apps, schema_editor):
    ClubFusion = apps.get_model("core", "ClubFusion")
    if ClubFusion.objects.exists():
        return

    rows = [
        {
            "title": "Club Fusion",
            "kicker": "Introduction",
            "body": (
                "Club Fusion is our Teens’ Church at Nairobi Chapel Ngong Hills. We take great joy in "
                "welcoming every teen into our community every Sunday. Our Teens’ Church offers a variety "
                "of programs designed to nurture, inspire, empower, and holistically develop young people "
                "through the teachings of the Lord Jesus Christ."
            ),
            "image": "pastorate/easter2.png",
            "image_on_left": False,
            "sort_order": 0,
            "is_published": True,
        },
        {
            "title": "Crossroads",
            "kicker": "Program Journey",
            "body": (
                "This is a 2-year transformational journey that prepares pre-teens for the transition into "
                "maturity—guiding boys into manhood and girls into womanhood, from childhood to adulthood. "
                "The program is rooted in God’s Word and helps teens develop a deeper understanding of God "
                "while strengthening their faith.\n\nWe partner with parents and the community to support "
                "the physical, spiritual, emotional, and social development of every teen."
            ),
            "image": "pastorate/easter2.png",
            "image_on_left": True,
            "sort_order": 1,
            "is_published": True,
        },
        {
            "title": "Crossroad 1 (12-Year-Olds)",
            "kicker": "Crossroads Stage",
            "body": (
                "This stage focuses on discipleship for pre-teens who are beginning to ask important life "
                "questions such as: Who am I? Why am I here? Do I matter? What do my friends think of me?\n\n"
                "We meet every Sunday during service to guide them through these questions using Biblical "
                "teachings, shared experiences, and wisdom. They are also prepared for the physical and "
                "emotional changes they are experiencing, as well as expectations from the world around them.\n\n"
                "Activities include camps, Bible trivia, and social justice outreach."
            ),
            "image": "",
            "image_on_left": False,
            "sort_order": 2,
            "is_published": True,
        },
        {
            "title": "Crossroad 2 (13-Year-Olds)",
            "kicker": "Crossroads Stage",
            "body": (
                "This stage focuses on five key areas:\n\nTurning over a new leaf – Understanding what it means "
                "to follow Christ\nContemporary teen culture – Building life skills in today’s environment\n"
                "Pink and Blue – Addressing sexuality topics\nWho’s the Boss – Exploring family, church, and "
                "leadership development\nRites of Passage – A culminating camp experience marking growth and "
                "transition\n\nTeens also learn from biblical role models, drawing practical life lessons from "
                "Scripture."
            ),
            "image": "",
            "image_on_left": False,
            "sort_order": 3,
            "is_published": True,
        },
        {
            "title": "Services",
            "kicker": "Weekly Gatherings",
            "body": (
                "We hold two services every Sunday at 9:00 AM and 11:00 AM.\n\nClub Fusion services are known "
                "as W.I.D.E Services, where we address relevant youth issues and reach out to unchurched young "
                "people.\n\nEvery second Sunday of the month, we hold D.E.E.P (SCOPE) Services, which focus on "
                "in-depth Bible study in small groups led by trained adult volunteers. These sessions encourage "
                "teens to actively read and engage with Scripture."
            ),
            "image": "",
            "image_on_left": False,
            "sort_order": 4,
            "is_published": True,
        },
        {
            "title": "VUMA",
            "kicker": "Leadership Development",
            "body": (
                "VUMA is an 8-month residential program designed for recent high school graduates, focusing on "
                "discipleship and personal leadership development.\n\nVUMA stands for:\nVibrant in Purpose – "
                "Discovering calling and career direction\nUnveiled in Potential – Identifying talents and "
                "spiritual gifts\nMature in Person – Developing self-awareness\nAnchored in Principle – Building "
                "a strong spiritual foundation\n\nThis program includes practical ministry experience in churches "
                "and schools through mission work. By the end of the program, participants are expected to grow "
                "into confident young adults who understand their identity in Christ and their role in society, "
                "fully prepared to embrace college life."
            ),
            "image": "",
            "image_on_left": False,
            "sort_order": 5,
            "is_published": True,
        },
    ]

    for row in rows:
        ClubFusion.objects.create(**row)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_clubfusion"),
    ]

    operations = [
        migrations.RunPython(seed_clubfusion_defaults, migrations.RunPython.noop),
    ]

