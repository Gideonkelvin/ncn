"""Expose CMS content to all templates."""
from types import SimpleNamespace

from .models import SiteSettings, DynamicPage


def cms_context(request):
    """Add site_settings and dynamic navigation to template context."""
    # Get site settings with fallback
    try:
        site_settings = SiteSettings.get()
    except Exception:
        site_settings = SimpleNamespace(
            site_name="Nairobi Chapel Ngong Hills",
            contact_email="info@ncngonghills.org",
            contact_location="Ngong Hills, Kenya",
            contact_phone="+254 797 559118",
            footer_copyright="Nairobi Chapel Ngong Hills, All Rights Reserved.",
            credits_url="https://www.bkgconsultants.com/",
            credits_text="Website by BKG Consulting",
            newsletter_heading="Stay Connected",
            newsletter_description="Get updates on our services, events, and community life.",
            logo_url="",
            map_embed_url="",
            instagram_url="https://instagram.com/ncngonghills",
            youtube_url="https://www.youtube.com/@ncngonghills",
            linkedin_url="",
            facebook_url="https://facebook.com/ncngonghills",
            whatsapp_url="https://wa.me/254797559118",
        )
    
    # Get dynamic navigation menu items
    try:
        menu_pages = DynamicPage.objects.filter(
            is_active=True,
            show_in_menu=True
        ).order_by('menu_order', 'order', 'title')
        
        # Organize pages by menu placement
        nav_about = []
        nav_ministries = []
        nav_resources = []
        nav_engage = []
        
        for page in menu_pages:
            page_data = {
                'title': page.title,
                'slug': page.slug,
                'url': f'/{page.slug}/',
            }
            if page.menu_placement == 'about':
                nav_about.append(page_data)
            elif page.menu_placement == 'ministries':
                nav_ministries.append(
                    {
                        **page_data,
                        '_order': page.menu_order,
                    }
                )
            elif page.menu_placement == 'resources':
                nav_resources.append(page_data)
            elif page.menu_placement == 'engage':
                nav_engage.append(page_data)

        # Plug-In is served at /prayer/; ensure it appears under Ministries when active.
        prayer_page = DynamicPage.objects.filter(slug="prayer", is_active=True).first()
        if prayer_page and not any(p["slug"] == "prayer" for p in nav_ministries):
            nav_ministries.append(
                {
                    "title": prayer_page.title,
                    "slug": prayer_page.slug,
                    "url": f"/{prayer_page.slug}/",
                    "_order": prayer_page.menu_order,
                }
            )
        nav_ministries.sort(key=lambda p: (p.get('_order', 999), p['title']))
        for p in nav_ministries:
            p.pop('_order', None)

        dynamic_nav = {
            'about': nav_about,
            'ministries': nav_ministries,
            'resources': nav_resources,
            'engage': nav_engage,
        }
    except Exception:
        dynamic_nav = {
            'about': [],
            'ministries': [],
            'resources': [],
            'engage': [],
        }
    
    return {
        "site_settings": site_settings,
        "dynamic_nav": dynamic_nav,
    }
