from django.db import migrations, models


def seed_quest_defaults(apps, schema_editor):
    Quest = apps.get_model("core", "Quest")
    if Quest.objects.exists():
        return

    Quest.objects.create(
        heading="Introduction",
        body=(
            "“Train a child in the way He should go, and when he is old he will not turn from it.” "
            "(Proverbs 22:6). QUEST, our Children’s Ministry, embodies the great adventure of knowing "
            "God, discovering His Word and enjoying His people. Here, we seek to draw the young ones "
            "into a closer walk with Jesus and to empower them to reveal His love to others along the way. "
            "Over the years, we have established a time-honored custom of giving special treatment to "
            "children due to the importance they hold as far as future generations are concerned. Our "
            "commitment to nurture children of faith is underpinned by the belief that a strong children’s "
            "ministry translates into a strong social fabric."
        ),
        sort_order=0,
        is_published=True,
    )

    Quest.objects.create(
        heading="Our Vision",
        body=(
            "Our vision falls into the general vision of the Nairobi Chapel. We seek to grow Kids D.E.E.P "
            "to Reach W.I.D.E, whose acronyms stand for:"
        ),
        bullet_points=(
            "D – Daily reading my Bible\n"
            "E – Enjoying God’s people\n"
            "E – Enjoying serving Others\n"
            "P – Promising to do what I learn each Sunday\n"
            "W – Witness (tell others about Jesus)\n"
            "I – Impact (Change where I am for Jesus)\n"
            "D – Disciple (Help others grow in Jesus)\n"
            "E – Establish churches (Help others find a place to attend church)"
        ),
        image="pastorate/easter2.png",
        image_on_right=True,
        sort_order=1,
        is_published=True,
    )

    Quest.objects.create(
        heading="Our Strategy",
        body="We strive to fulfill our vision through the following significant ways:",
        bullet_points=(
            "Partnering with parents: We believe that the ultimate responsibility for spiritual development "
            "of children rests on parents. Our role basically, is to work closely with them to complement "
            "their efforts and reinforce their spiritual mandate (Deut 4:9). There are however exceptions – "
            "children who come from homes where they don’t receive any spiritual nurture. In such cases we "
            "work hard to bridge the gap.\n"
            "The teacher’s role: The Sunday school teacher is to be an evangelist, an encourager, a disciple "
            "maker, and an excellent role model for the children. They are to use their spiritual gifts in "
            "cooperation with the Holy Spirit to see transformation in the lives of the children.\n"
            "Bible based programs: Our Sunday school seeks to be age appropriate, application oriented, and "
            "in the context of intentional shepherding and mentoring. Our curriculum is derived from two main "
            "sources: Christian Evangelistic Fellowship (CEF) and Jubilee Station from our partner churches. "
            "It is usually taught in units which can take as long as 8 weeks depending on the prevailing "
            "season (e.g. Easter, Christmas etc)."
        ),
        sort_order=2,
        is_published=True,
    )

    Quest.objects.create(
        heading="Ministry Set Up",
        body=(
            "Creche – Below 2 years\n"
            "We have a crèche for parents with children below the age of two, which is situated next to "
            "Hyperdome or main tent. Here, the parents can keep up with the service through large screen "
            "televisions as they nurse their kids in this spacious area. A crèche attendant looks after "
            "their welfare, serving tea to the parents, and providing toys for the children.\n\n"
            "“Itibari” (Faith Buds) – 2 year olds\n"
            "Sunday school basically begins here. The “Itibari” kids are transitioned from the crèche where "
            "they are entrusted to the care of Sunday school teachers, who teach, nurse, and keep an eye on them.\n\n"
            "For security reasons, parents are required to sign in their children whenever they bring them to "
            "class. Each parent will receive a tag with a number which MUST be presented at the end of the service. "
            "Only then will the child be released. We discourage siblings from bringing children to class.\n\n"
            "“Neema” (Grace) – 3 year olds\n"
            "This class ministers to the 3 year olds who by now have settled in Sunday School. They are often "
            "a very curious lot and generally love their worship and Bible story time. In addition to the regular "
            "teacher, we have shepherds who help to care for the children in the two classes: Neema ‘Yellow’ and ‘Purple’.\n\n"
            "“Imani” (Faith) – 4 to 5 year olds\n"
            "This is our last class in the NEST, our pre-school Sunday School space. The class is normally large "
            "so we divide the Imani class into ‘Blue’, ‘Green’ and ‘Red’, allowing us to keep a good teacher-student "
            "ratio of 1:10.\n\n"
            "When the children turn 6, they then transition to QUEST our older Children’s space where they have an "
            "in-depth study of the Word of God. A major Characteristic of our QUEST space is the large group worship "
            "for all the classes, after which the children disperse to their respective classes. Many of our children "
            "receive the Lord while in this space, having attained the knowledge of Him from their early days. The "
            "children are more participatory in worship, as shepherds to the younger children and serve as ushers and "
            "greeters, welcoming others into the service.\n\n"
            "“Sifa” (Praise) – 6 to 7 year olds\n"
            "“Sifa” (Praise) comprises 6 to 7 year olds who have just graduated from the Imani class. Their curriculum "
            "is relatively more advanced than that of Neema and Imani and includes Bible lessons, Scripture Memorization "
            "and crafts to reinforce the lesson.\n\n"
            "“Shangwe” (Jubilant) – 8 to 9 year olds\n"
            "This class ministers to the 8 to 9 year old children who have graduated from the Sifa 7 class. Their "
            "curriculum is similar to that of the “Sifa” class.\n\n"
            "“Johari” (Jewel) – 10 to 11 year olds\n"
            "“Johari”, or Jewel, is the summit of the Sunday school experience. We realize that transitions are beginning "
            "at this age and to minister effectively to the needs of this age group, the classes are divided by gender. "
            "The female teachers walk with the girls while the male teachers provide godly mentoring to the boys. At this "
            "point the 10 to 11 year old children are taught various lessons including Water Baptism and the significance "
            "of Holy Communion. At the end, they take part in these exercises. In addition, they get a take home devotional "
            "which coincides with their Sunday lessons for them to go through during the week. After graduation, the Johari "
            "children progress to the Youth Ministry’s “GUZA” class."
        ),
        sort_order=3,
        is_published=True,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_seed_clubfusion"),
    ]

    operations = [
        migrations.CreateModel(
            name="Quest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("heading", models.CharField(max_length=200)),
                ("body", models.TextField(blank=True, help_text="Main paragraph text. Use line breaks to separate paragraphs.")),
                ("bullet_points", models.TextField(blank=True, help_text="Optional bullet points. Add one item per line.")),
                ("image", models.ImageField(blank=True, help_text="Optional image for this section.", null=True, upload_to="quest/")),
                ("image_on_right", models.BooleanField(default=True, help_text="If image is set, show it on the right on large screens.")),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                ("is_published", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Quest",
                "verbose_name_plural": "Quest",
                "ordering": ["sort_order", "id"],
            },
        ),
        migrations.RunPython(seed_quest_defaults, migrations.RunPython.noop),
    ]

