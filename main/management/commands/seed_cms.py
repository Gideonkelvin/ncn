"""
Seed CMS with current site content. Run: python manage.py seed_cms
Uses placeholder image paths (/img/...) until Cloudinary URLs are set from admin.
"""
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from main.models import (
    SiteSettings,
    HeroSlide,
    Service,
    WhatWeDoItem,
    AboutPreview,
    FounderPurposeBlock,
    CallToActionBlock,
    BlogCategory,
    BlogPost,
    Product,
    PageCopy,
    DynamicPage,
    Event,
)
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = "Load default CMS content from current site copy"

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Clear existing content before seeding (optional)")

    def handle(self, *args, **options):
        if options.get("clear"):
            HeroSlide.objects.all().delete()
            Service.objects.all().delete()
            WhatWeDoItem.objects.all().delete()
            BlogPost.objects.all().delete()
            Product.objects.all().delete()
            AboutPreview.objects.filter(pk=1).delete()
            FounderPurposeBlock.objects.filter(pk=1).delete()
            CallToActionBlock.objects.filter(pk=1).delete()
            PageCopy.objects.all().delete()
            DynamicPage.objects.all().delete()
            self.stdout.write("Cleared existing CMS content.")

        # Site settings (singleton)
        SiteSettings.objects.update_or_create(
            pk=1,
            defaults={
                "site_name": "Nairobi Chapel Ngong Hills",
                "tagline": "A Community of Faith, Love & Purpose",
                "contact_email": "info@ncngonghills.org",
                "contact_location": "Ngong Hills, Kenya",
                "footer_copyright": "Nairobi Chapel Ngong Hills, All Rights Reserved.",
                "credits_url": "https://www.bkgconsultants.com/",
                "credits_text": "Website by BKG Consulting",
                "newsletter_heading": "Stay Connected",
                "newsletter_description": "Get updates on our services, events, and community life.",
                "instagram_url": "https://instagram.com/ncngonghills",
                "youtube_url": "https://www.youtube.com/@ncngonghills",
                "linkedin_url": "",
                "facebook_url": "https://facebook.com/ncngonghills",
                "whatsapp_url": "https://wa.me/254797559118",
                "map_embed_url": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3988.789856789!2d36.643456789!3d-1.423456789!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x182f155e1234567%3A0x1234567890abcdef!2sNgong%20Hills%2C%20Kenya!5e0!3m2!1sen!2ske!4v1635000000000!5m2!1sen!2ske",
            },
        )

        # Hero slides
        hero_data = [
            {
                "title": "Welcome to Nairobi Chapel Ngong Hills",
                "subtitle": "A welcoming community of believers committed to loving God, loving people, and making a difference in our nation and beyond.",
                "cta_text": "Join Us This Sunday",
                "cta_url": "/contact",
                "image_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1773940927/WhatsApp-Image-2026-03-08-at-18.45.33_bffaps.jpg",
                "alt_text": "Nairobi Chapel Ngong Hills worship service",
                "order": 0,
            },
            {
                "title": "Grow in Your Faith",
                "subtitle": "Connect with others, study God's Word, and deepen your relationship with Him through our various ministries and groups.",
                "cta_text": "Find a Group",
                "cta_url": "/egroups",
                "image_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1773940927/WhatsApp-Image-2026-03-08-at-18.45.33_bffaps.jpg",
                "alt_text": "Fellowship and community",
                "order": 1,
            },
            {
                "title": "Make a Difference",
                "subtitle": "Use your gifts and talents to serve our community and impact the nation for Christ.",
                "cta_text": "Get Involved",
                "cta_url": "/volunteer",
                "image_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1773940927/WhatsApp-Image-2026-03-08-at-18.45.33_bffaps.jpg",
                "alt_text": "Serving our community",
                "order": 2,
            },
        ]
        for i, d in enumerate(hero_data):
            HeroSlide.objects.update_or_create(
                order=d["order"],
                defaults={
                    "title": d["title"],
                    "subtitle": d["subtitle"],
                    "cta_text": d["cta_text"],
                    "cta_url": d["cta_url"],
                    "image_url": d["image_url"],
                    "alt_text": d["alt_text"],
                    "is_active": True,
                },
            )

        # Services
        services_data = [
            {
                "title": "Children's Service",
                "description": "Sunday school and children's ministry for ages 0-12",
                "day_time": "11:30 am - 1:00 pm",
                "location": "Nairobi Chapel Ngong Hills",
                "place": "Quest Classrooms",
                "image_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774086292/world-book-day-celebration_1_v5bea0.jpg",
                "learn_more_url": "/quest",
                "order": 0,
            },
            {
                "title": "Teens Service",
                "description": "Youth service for teenagers aged 13-18",
                "day_time": "11:30 am - 1:00 pm",
                "location": "Nairobi Chapel Ngong Hills",
                "place": "Teens Tent",
                "image_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774086303/world-book-day-celebration_t5h9j9.jpg",
                "learn_more_url": "/club-fusion",
                "order": 1,
            },
            {
                "title": "Adult Service",
                "description": "Main worship service for adults",
                "day_time": "9:00 - 11:00 am\n11:30 am - 1:00 pm",
                "location": "Nairobi Chapel Ngong Hills",
                "place": "Main Tent",
                "image_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774086291/people-meeting-seminar-office-concept_vvrhtg.jpg",
                "learn_more_url": "/contact",
                "order": 2,
            },
        ]
        for i, d in enumerate(services_data):
            Service.objects.update_or_create(
                title=d["title"],
                defaults={
                    "description": d["description"],
                    "day_time": d["day_time"],
                    "location": d["location"],
                    "place": d["place"],
                    "image_url": d["image_url"],
                    "learn_more_url": d["learn_more_url"],
                    "is_active": True,
                    "order": d["order"],
                },
            )

        # What We Do items
        what_we_do = [
            {"title": "Worship Together", "description": "Join us for vibrant, Spirit-led worship services that inspire and transform. Experience God's presence in a welcoming, family-friendly environment.", "icon_url": "/img/icons/icon-2.png", "order": 0},
            {"title": "Grow in Community", "description": "Connect with others through our various groups and ministries. Find your tribe, build lasting friendships, and grow together in faith.", "icon_url": "/img/icons/icon-3.png", "order": 1},
            {"title": "Serve Others", "description": "Make a difference in our community through outreach programmes, missions, and volunteer opportunities that impact lives for Christ.", "icon_url": "/img/icons/icon-4.png", "order": 2},
        ]
        what_we_do = [
            {"title": "Worship Together", "description": "Join us for vibrant, Spirit-led worship services that inspire and transform. Experience God's presence in a welcoming, family-friendly environment.", "icon_url": "/img/icons/icon-2.png", "order": 0},
            {"title": "Grow in Community", "description": "Connect with others through our various groups and ministries. Find your tribe, build lasting friendships, and grow together in faith.", "icon_url": "/img/icons/icon-3.png", "order": 1},
            {"title": "Serve Others", "description": "Make a difference in our community through outreach programmes, missions, and volunteer opportunities that impact lives for Christ.", "icon_url": "/img/icons/icon-4.png", "order": 2},
        ]
        for item in what_we_do:
            WhatWeDoItem.objects.update_or_create(
                order=item["order"],
                defaults=item,
            )

        # About preview (home)
        AboutPreview.objects.update_or_create(
            pk=1,
            defaults={
                "heading": "Welcome to Nairobi Chapel Ngong Hills",
                "subheading": "A Place Where Everyone Belongs",
                "body_paragraph_1": "Nairobi Chapel Ngong Hills is more than just a church—it's a family of believers committed to knowing God, making Him known, and transforming our community and nation.",
                "body_paragraph_2": "Located in the beautiful Ngong Hills area, our church is a welcoming space where people from all walks of life come together to worship, learn, and grow in their faith journey.",
                "stat_number": "500",
                "stat_label_line1": "Plus",
                "stat_label_line2": "Growing",
                "stat_label_line3": "Family",
                "cta_text": "Learn More",
                "cta_url": "/about",
                "image_1_url": "/img/about-3.jpg",
                "image_2_url": "/img/about-4.jpg",
            },
        )

        # Founder & Purpose (home)
        FounderPurposeBlock.objects.update_or_create(
            pk=1,
            defaults={
                "section_title": "Our Story",
                "subheading": "A Church with a Vision",
                "intro_paragraph_1": "Nairobi Chapel Ngong Hills has been a beacon of hope and faith in our community for years. Our journey began with a simple vision: to create a place where people can experience God's love, find meaningful connections, and grow in their purpose.",
                "intro_paragraph_2": "Today, we continue to pursue that vision with passion, welcoming everyone who walks through our doors into a community of faith, hope, and love.",
                "bullet_1_title": "Our Mission",
                "bullet_1_text": "To love God, love people, and make a difference in our nation and beyond through the message and life of Jesus Christ.",
                "bullet_2_title": "Our Values",
                "bullet_2_text": "We are committed to worship, community, Discipleship, serving others, and sharing the hope we have in Christ.",
                "bullet_3_title": "Our Vision",
                "bullet_3_text": "To be a church that transforms lives, impacts our nation, and reaches the world for Christ.",
                "image_1_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774087752/african-senior-woman-portrait_ztgaxx.jpg",
                "image_2_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774087992/open-bible-closeup-christianity-concept-reading-gods-holy-bible_yxlyqc.jpg",
            },
        )

        # Call to action (home)
        CallToActionBlock.objects.update_or_create(
            pk=1,
            defaults={
                "heading": "Join Our Family",
                "subheading": "Experience the Love of God with Us",
                "body": "Whether you're looking for a church home, exploring faith, or just curious about Christianity, we welcome you to join us. Experience warm hospitality, uplifting worship, and a community that cares about you.",
                "primary_button_text": "Visit Us This Sunday",
                "primary_button_url": "/contact",
                "secondary_button_text": "Get in Touch",
                "secondary_button_url": "/contact",
            },
        )

        # Blog categories
        for order, (slug, name) in enumerate([("all", "All"), ("sermons", "Sermons"), ("events", "Events"), ("ministry", "Ministry"), ("community", "Community"), ("news", "News")]):
            BlogCategory.objects.get_or_create(slug=slug, defaults={"name": name, "order": order})
        cats = list(BlogCategory.objects.all().order_by("order")[:6])
        blog_posts_data = [
            ("Walking in Faith: A sermon on Trusting God's Plan", "walking-in-faith", "Discover how trusting God's plan can transform your life and bring peace even in the most challenging circumstances.", "/img/carousel-1.jpg", 0),
            ("Love in Action: Serving Our Community", "love-in-action", "Our recent community outreach brought together volunteers from all walks of life to make a difference in our neighborhood.", "/img/about-3.jpg", 1),
            ("Growing Together: The Power of Small Groups", "growing-together", "Our eGroups have become the heart of community life at Nairobi Chapel. Discover how these groups are transforming lives.", "/img/founder-1.jpg", 2),
            ("Sunday Service Highlights: A Week of Celebration", "sunday-service-highlights", "Reflecting on the powerful worship experience from this Sunday and the message that touched many hearts.", "/img/carousel-2.jpg", 3),
            ("Youth Revolution: Club Fusion's Impact", "youth-revolution", "Our young people are making waves in the community through Club Fusion. See how they're shining their light for Christ.", "/img/about-5.jpg", 4),
            ("Prayer Requests: Standing Together in Faith", "prayer-requests", "The power of prayer united our community this week as we lifted up various needs together in faith.", "/img/founder-2.jpg", 5),
        ]
        pub = timezone.now()
        for i, (title, slug, excerpt, img, order) in enumerate(blog_posts_data):
            BlogPost.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "excerpt": excerpt,
                    "featured_image_url": img,
                    "category": cats[i % len(cats)] if cats else None,
                    "published_at": pub,
                    "is_published": True,
                    "order": order,
                    "body": excerpt,
                },
            )

        # Products (shop)
        products_data = [
            ("Nairobi Chapel T-Shirt", "nairobi-chapel-tshirt", Decimal("1500"), "/img/lens-1.png", "Bestseller", [("#eab308", "Yellow"), ("#1f2937", "Charcoal")]),
            ("Nairobi Chapel Hoodie", "nairobi-chapel-hoodie", Decimal("3500"), "/img/lens-2.png", "", [("#1f2937", "Black"), ("#3b82f6", "Blue")]),
            ("Nairobi Chapel Cap", "nairobi-chapel-cap", Decimal("800"), "/img/lens-1.png", "New"),
            ("Nairobi Chapel Mug", "nairobi-chapel-mug", Decimal("500"), "/img/lens-2.png", ""),
            ("Nairobi Chapel Notebook", "nairobi-chapel-notebook", Decimal("300"), "/img/lens-1.png", ""),
            ("Nairobi Chapel Wristband", "nairobi-chapel-wristband", Decimal("100"), "/img/lens-2.png", ""),
        ]
        # products_data is inconsistent: some tuples include optional color swatches
        # as the 6th element, others do not.
        # The current Product model doesn't store swatches, so we ignore it.
        for i, product in enumerate(products_data):
            name, slug, price, img, badge = product[:5]
            Product.objects.update_or_create(
                slug=slug,
                defaults={"name": name, "price": price, "image_url": img, "badge": badge, "is_active": True, "order": i},
            )

        # Page copies
        PageCopy.objects.update_or_create(
            page_slug="give",
            defaults={
                "meta_title": "Give | Nairobi Chapel Ngong Hills – Support Our Mission",
                "meta_description": "Support Nairobi Chapel Ngong Hills. Your generous giving helps us continue our ministries, community outreach, and mission work.",
                "heading": "Partner with Us",
                "subheading": "Your Giving Makes a Difference",
                "body": "Thank you for considering supporting the work of Nairobi Chapel Ngong Hills. Your generous gifts enable us to continue sharing God's love with our community and beyond.\n\nWays to Give\n\nYou can give through M-Pesa, bank transfer, or in person during our services. Every contribution, no matter the size, makes a meaningful impact in furthering our mission.\n\nFor questions about giving or to set up recurring donations, please contact our finance team. We are committed to transparency and accountability in how your gifts are used.",
            },
        )
        PageCopy.objects.update_or_create(
            page_slug="404",
            defaults={
                "meta_title": "Page Not Found",
                "heading": "Page Not Found",
                "subheading": "The page you are looking for does not exist or has been moved.",
                "body": "",
            },
        )
        PageCopy.objects.update_or_create(
            page_slug="contact",
            defaults={
                "meta_title": "Contact | Nairobi Chapel Ngong Hills",
                "meta_description": "Get in touch with Nairobi Chapel Ngong Hills. We'd love to hear from you!",
                "heading": "Contact Us",
                "subheading": "We'd Love to Hear from You",
                "body": "Whether you have a question, want to know more about our church, or would like to visit us, we're here to help. Fill out the form below and we'll get back to you soon.",
            },
        )
        PageCopy.objects.update_or_create(
            page_slug="shop",
            defaults={
                "meta_title": "Shop | Nairobi Chapel Ngong Hills",
                "meta_description": "Get your Nairobi Chapel merchandise and show your church pride.",
                "heading": "Church Shop",
                "subheading": "Wear Your Chapel Pride",
                "body": "Browse our collection of Nairobi Chapel merchandise. All proceeds support our ministries and community outreach programmes.",
            },
        )

        # Dynamic Pages
        dynamic_pages = [
            {
                "slug": "pastoral",
                "title": "Pastorate",
                "subtitle": "Connect through Pastoral",
                "template": "split",
                "header_text": "",
                "content": (
                    "<p>Daniel Aswa is a devoted husband to his wife, Ressy, and together they have two 11-year-old twins, "
                    "Immanuel and Ariel. A lifelong servant of the Lord, Daniel gave his life to Christ in 2003 and has "
                    "faithfully served in ministry from his home church in Busia to university fellowships, IVC Church in "
                    "Eldoret, and now Nairobi Chapel.</p>"
                    "<p>He is passionate about discipleship, mentorship, intercessory prayer, and pastoral care, especially "
                    "mentoring young boys and supporting ministry teams. Professionally, Daniel is an experienced Data "
                    "Scientist and public health researcher with over 15 years of work in epidemiology, contributing to "
                    "healthcare improvements in Kenya. He is a servant leader who seeks to impact lives both within and "
                    "beyond the church.</p>"
                ),
                "content_2": "",
                "image_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774088922/group-four-gorgeous-african-american-womans-wear-summer-hat-holding-hands-praying-green-grass-park_ncwcwr.jpg",
                "alt_text": "Lead Pastor — Rev. Collins Ouma and pastoral team",
                "cta_text": "",
                "cta_url": "",
                "menu_placement": "about",
                "menu_order": 1,
                "show_in_menu": True,
                "is_active": True,
                "order": 0,
            },
            {
                "slug": "egroups",
                "title": "eGroups",
                "subtitle": "Connect through eGroups",
                "template": "full_width",
                "header_text": "eGroups are small groups that meet regularly to build community, study God's Word, and support one another.",
                "content": "<p>Join an eGroup and experience the power of community. Our groups meet in homes across the city and provide a welcoming environment for everyone.</p><p><strong>Why Join an eGroup?</strong></p><ul><li>Build meaningful relationships</li><li>Grow in your faith</li><li>Receive pastoral care and support</li><li>Connect with people from all walks of life</li></ul>",
                "image_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774088737/closeup-shot-male-sitting-park-while-holding-bible_ansfw7.jpg",
                "cta_text": "Find an eGroup",
                "cta_url": "/contact",
                "menu_placement": "ministries",
                "menu_order": 0,
                "show_in_menu": True,
                "is_active": True,
                "order": 1,
            },
            {
                "slug": "prayer",
                "title": "Plug-In",
                "subtitle": "How do I find My Purpose?",
                "template": "content_only",
                "header_text": "",
                "content": "",
                "content_2": "",
                "image_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774088737/closeup-shot-male-sitting-park-while-holding-bible_ansfw7.jpg",
                "alt_text": "Plug-In ministry",
                "cta_text": "",
                "cta_url": "",
                "menu_placement": "ministries",
                "menu_order": 1,
                "show_in_menu": True,
                "is_active": True,
                "order": 2,
            },
            {
                "slug": "club-fusion",
                "title": "Club Fusion",
                "subtitle": "Teens' Church · Nairobi Chapel",
                "template": "content_only",
                "header_text": "",
                "content": "",
                "content_2": "",
                "image_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774088737/closeup-shot-male-sitting-park-while-holding-bible_ansfw7.jpg",
                "alt_text": "Club Fusion teens ministry",
                "cta_text": "Get in touch",
                "cta_url": "/contact",
                "menu_placement": "ministries",
                "menu_order": 2,
                "show_in_menu": True,
                "is_active": True,
                "order": 3,
            },
            {
                "slug": "quest",
                "title": "Quest",
                "subtitle": "Children's Ministry",
                "template": "content_only",
                "header_text": "",
                "content": "",
                "content_2": "",
                "image_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774088922/group-four-gorgeous-african-american-womans-wear-summer-hat-holding-hands-praying-green-grass-park_ncwcwr.jpg",
                "alt_text": "QUEST children's ministry",
                "cta_text": "Contact us about Quest",
                "cta_url": "/contact",
                "menu_placement": "ministries",
                "menu_order": 3,
                "show_in_menu": True,
                "is_active": True,
                "order": 4,
            },
            {
                "slug": "mens-ministry",
                "title": "Men\u2019s Ministry",
                "subtitle": "Jabari — growing in biblical manhood",
                "template": "content_only",
                "header_text": "",
                "content": (
                    '<blockquote class="blockquote border-start border-3 ps-3 ms-1 mb-4" '
                    'style="border-color: var(--bs-primary) !important;">'
                    "<p class=\"mb-0\">&ldquo;&hellip; They were brave warriors, ready for battle and able to handle "
                    "the shield and spear. Their faces were the faces of lions, and they were as swift as gazelles in "
                    "the mountains.&rdquo;</p>"
                    '<footer class="blockquote-footer mt-2">1 Chronicles 12:8</footer>'
                    "</blockquote>"
                    "<p>The Jabari Men&rsquo;s Ministry is a gathering place for men to grow their faith in depth as "
                    "they address faith issues relevant to men. Jabari aims to create an environment for men to encounter "
                    "and relate with Jesus Christ unashamedly, and become disciples who live out their faith at home, in "
                    "the church, in community and in the marketplace.</p>"
                    "<p>Have you ever seen the funny street interview video on the web where random men on the street "
                    "were asked &ldquo;What is a man?&rdquo; Very few could answer. Try it with your friends. Short of "
                    "saying men are men; and men procreate, most men don&rsquo;t know what it means to be a man. No-one "
                    "teaches them today on what it means to be a man, and what a man&rsquo;s role in society is?</p>"
                ),
                "content_2": (
                    "<p>Some of the initiatives implemented towards this vision include:</p>"
                    '<h3 class="h4 mt-4 mb-3">jabariMan Enough</h3>'
                    "<p>This is a 10-week, entry-point, discipleship program that seeks to answer that question from the "
                    "bible. What is biblical manhood and what is the place of a godly man in today&rsquo;s society? What "
                    "does God expect of men and what special mandate has he given men? Man Enough leads men to discover "
                    "their identity, clearly states the 5-fold marks of a man, and helps men catch a vision of how to live "
                    "more effective lives at home, at work, in the community, in the church, and within the nation.</p>"
                    '<h3 class="h4 mt-4 mb-3">The King&rsquo;s Gathering</h3>'
                    "<p>This is a monthly breakfast gathering of men for a Kings feast. The meeting creates a safe space "
                    "for men to discuss matters pertinent to them, foster community, and inspires men to step out and stand "
                    "out in society as Godly men.</p>"
                    '<h3 class="h4 mt-4 mb-3">jabari24th Man Prayer Ministry</h3>'
                    "<p>The Kings Gathering also affords an opportunity for men to pray together. This they do in bonded "
                    "3 men prayer groups, inviting the 4th Man (Jesus) to come join with them. The bible story in Daniel 3 "
                    "talks of Daniel&rsquo;s 3 friends who were thrown into a blazing hot furnace. But when the King looked "
                    "to see if they had been burned at all, he exclaimed in shock &ldquo;Nebuchadnezzar leaped to his feet "
                    "in amazement and asked his advisers, &lsquo;Weren&rsquo;t there three men that we tied up and threw into "
                    "the fire?&rsquo; They replied, &lsquo;Certainly, Your Majesty.&rsquo; He said, &lsquo;Look! I see four "
                    "men walking around in the fire, unbound and unharmed, and the fourth looks like a son of the "
                    "gods.&rsquo;&rdquo; (Daniel 3:24)</p>"
                    "<p>No matter how hot the furnace of business, survival, integrity, home or career gets, when the 4th "
                    "man is there, men can come through shining instead of singed. Men&rsquo;s values, integrity, and honour "
                    "does not have to be sacrificed. There is a way to prevail &ndash; by ensuring the 4th Man is there!</p>"
                ),
                "image_url": "",
                "alt_text": "",
                "cta_text": "",
                "cta_url": "",
                "cta_text_2": "",
                "cta_url_2": "",
                "meta_title": "Men\u2019s Ministry (Jabari)",
                "meta_description": (
                    "Jabari Men\u2019s Ministry: discipleship, the King\u2019s Gathering, and jabari24th Man prayer — "
                    "men growing in faith at Nairobi Chapel Ngong Hills."
                ),
                "menu_placement": "ministries",
                "menu_order": 4,
                "show_in_menu": True,
                "is_active": True,
                "order": 5,
            },
            {
                "slug": "womens-ministry",
                "title": "Women\u2019s Ministry",
                "subtitle": "Glow — authentic relationships and growing in faith",
                "template": "content_only",
                "header_text": "",
                "content": (
                    "<p>Glow seeks to provide ladies young and old, with opportunities to build authentic relationships. "
                    "We aim to encourage ladies to function in their true identity, as we empower them on issues of life "
                    "and faith.</p>"
                    "<p>When women work together, it&rsquo;s a bond unlike any other. Strong women stand together, lift "
                    "each other up and empower one another through prayer. Women don&rsquo;t always get to choose "
                    "life&rsquo;s circumstances but we do get to choose how we&rsquo;ll respond: with Strength, Stamina "
                    "and a Staying Perseverance. That can only be possible if we choose to have God walk with us. Glow "
                    "lays the foundation to make that possible.</p>"
                    "<p>Why is being a part of the Glow Circle the best decision you could make? Because we all need each "
                    "other. This is what Glow is about.</p>"
                    '<ol class="womens-ministry-page__steps">'
                    "<li>Glow encourages all ladies to function in their true identity, through forums that increase "
                    "their knowledge of God, and strengthen their personal faith.</li>"
                    "<li>Glow creates opportunities for fellowship and accountability for ladies to walk with, challenge "
                    "and support one another as they grow to the next levels.</li>"
                    "<li>Glow also gives ladies a safe forum to connect emotionally, socially, spiritually and "
                    "psychologically as they develop new friendships.</li>"
                    "</ol>"
                ),
                "content_2": "",
                "image_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774086292/world-book-day-celebration_1_v5bea0.jpg",
                "alt_text": "Women\u2019s ministry \u2014 Glow fellowship and celebration",
                "cta_text": "",
                "cta_url": "",
                "cta_text_2": "",
                "cta_url_2": "",
                "meta_title": "Women\u2019s Ministry (Glow)",
                "meta_description": (
                    "Glow Women\u2019s Ministry at Nairobi Chapel Ngong Hills: authentic relationships, fellowship, "
                    "and growing together in faith."
                ),
                "menu_placement": "ministries",
                "menu_order": 5,
                "show_in_menu": True,
                "is_active": True,
                "order": 6,
            },
            {
                "slug": "plug-in",
                "title": "Plug-In (legacy URL)",
                "subtitle": "",
                "template": "content_only",
                "header_text": "",
                "content": "",
                "image_url": "",
                "alt_text": "",
                "menu_placement": "none",
                "menu_order": 0,
                "show_in_menu": False,
                "is_active": False,
                "order": 10,
            },
            {
                "slug": "sermon",
                "title": "Sermons",
                "subtitle": "Sermon Archive",
                "template": "content_only",
                "header_text": "Listen to our weekly sermons. Browse our archive of past messages and grow in your faith.",
                "content": "<p>Our preaching is biblical, practical, and relevant to everyday life. Whether you missed a service or want to revisit a message, our sermon archive has you covered.</p><p>We upload new sermons every week. Subscribe to our podcast to never miss a message.</p>",
                "menu_placement": "resources",
                "menu_order": 0,
                "show_in_menu": True,
                "is_active": True,
                "order": 6,
            },
            {
                "slug": "bible-study",
                "title": "Bible Study",
                "subtitle": "",
                "template": "split",
                "header_text": "Join our Wednesday Bible study as we dive deeper into God's Word and learn how to apply it to our lives.",
                "content": "<p>Our Bible study sessions are designed to help you understand the Bible better and grow in your relationship with God. We cover books of the Bible verse by verse.</p><p><strong>What to Expect:</strong></p><ul><li>In-depth Bible teaching</li><li>Discussion groups</li><li>Prayer time</li><li>Fellowship</li></ul>",
                "content_2": "",
                "image_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774088737/closeup-shot-male-sitting-park-while-holding-bible_ansfw7.jpg",
                "alt_text": "Bible study and fellowship",
                "cta_text": "Join Bible Study",
                "cta_url": "/contact",
                "menu_placement": "resources",
                "menu_order": 1,
                "show_in_menu": True,
                "is_active": True,
                "order": 7,
            },
            {
                "slug": "membership",
                "title": "Membership",
                "subtitle": "Become a Member",
                "template": "split",
                "header_text": "Join the family. Become a member of our church and take your next step in faith.",
                "content": "<p>Church membership is about belonging to a family of faith. It's a commitment to walk alongside other believers and serve together in building God's kingdom.</p><p><strong>Membership Class Topics:</strong></p><ul><li>Our vision and values</li><li>What we believe</li><li>How to get involved</li><li>Leadership structure</li></ul>",
                "content_2": "",
                "image_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774088922/group-four-gorgeous-african-american-womans-wear-summer-hat-holding-hands-praying-green-grass-park_ncwcwr.jpg",
                "alt_text": "Church membership and community",
                "cta_text": "Sign Up for Class",
                "cta_url": "/contact",
                "menu_placement": "engage",
                "menu_order": 0,
                "show_in_menu": True,
                "is_active": True,
                "order": 8,
            },
            {
                "slug": "volunteer",
                "title": "Volunteer",
                "subtitle": "Join Our Team",
                "template": "split",
                "header_text": "Use your gifts to serve. Join our volunteer team and make a difference in our community.",
                "content": "<p>We believe that every person has unique gifts and talents that can be used to serve others. Volunteering is a great way to grow, connect, and make an impact.</p><p><strong>Volunteer Opportunities:</strong></p><ul><li>Welcome team</li><li>Media and production</li><li>Kids and youth ministry</li><li>Outreach and evangelism</li><li>Events support</li></ul>",
                "content_2": "",
                "image_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774088922/group-four-gorgeous-african-american-womans-wear-summer-hat-holding-hands-praying-green-grass-park_ncwcwr.jpg",
                "alt_text": "Volunteers serving together",
                "cta_text": "Start Serving",
                "cta_url": "/contact",
                "menu_placement": "engage",
                "menu_order": 1,
                "show_in_menu": True,
                "is_active": True,
                "order": 9,
            },
        ]
        
        for page_data in dynamic_pages:
            DynamicPage.objects.update_or_create(
                slug=page_data["slug"],
                defaults=page_data,
            )

        # Events
        now = timezone.now()
        events_data = [
            {
                "title": "Sunday Worship Service",
                "slug": "sunday-worship",
                "excerpt": "Join us for our weekly Sunday worship service.",
                "description": "Experience the presence of God through worship, prayer, and biblical preaching.",
                "event_date": now + timedelta(days=7),
                "location": "Main Tent, Nairobi Chapel Ngong Hills",
                "image_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774088737/closeup-shot-male-sitting-park-while-holding-bible_ansfw7.jpg",
                "watch_online_url": "",
                "is_published": True,
                "order": 0,
            },
            {
                "title": "Youth Fellowship - Club Fusion",
                "slug": "youth-fellowship",
                "excerpt": "A time of fun, fellowship, and growth for our young people.",
                "description": "Youth from ages 13-25 come together for worship, games, and Bible study.",
                "event_date": now + timedelta(days=3),
                "location": "Youth Center",
                "image_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774088922/group-four-gorgeous-african-american-womans-wear-summer-hat-holding-hands-praying-green-grass-park_ncwcwr.jpg",
                "watch_online_url": "",
                "is_published": True,
                "order": 1,
            },
            {
                "title": "Wednesday Bible Study",
                "slug": "bible-study-wednesday",
                "excerpt": "Dive deeper into God's Word every Wednesday.",
                "description": "Join us as we study the Bible verse by verse and learn how to apply it to our daily lives.",
                "event_date": now + timedelta(days=2),
                "location": "Main Sanctuary",
                "image_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774088737/closeup-shot-male-sitting-park-while-holding-bible_ansfw7.jpg",
                "watch_online_url": "",
                "is_published": True,
                "order": 2,
            },
            {
                "title": "Prayer Meeting",
                "slug": "prayer-meeting",
                "excerpt": "A time of corporate prayer for our church and community.",
                "description": "We gather together to pray for our church, community, and nation.",
                "event_date": now + timedelta(days=5),
                "location": "Prayer Room",
                "image_url": "https://res.cloudinary.com/dqng2ekwm/image/upload/v1774088922/group-four-gorgeous-african-american-womans-wear-summer-hat-holding-hands-praying-green-grass-park_ncwcwr.jpg",
                "watch_online_url": "",
                "is_published": True,
                "order": 3,
            },
        ]
        
        for event_data in events_data:
            Event.objects.update_or_create(
                slug=event_data["slug"],
                defaults=event_data,
            )

        self.stdout.write(self.style.SUCCESS("CMS seed completed. Content is ready for the admin dashboard."))
