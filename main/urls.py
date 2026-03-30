from django.urls import path
from django.views.generic import RedirectView
from . import views
from . import dashboard_views

urlpatterns = [
    # Dashboard (admin)
    path("dashboard/login/", dashboard_views.dashboard_login, name="dashboard_login"),
    path("dashboard/logout/", dashboard_views.dashboard_logout, name="dashboard_logout"),
    path("dashboard", RedirectView.as_view(url="/dashboard/", permanent=True)),
    path("dashboard/", dashboard_views.dashboard_home, name="dashboard_home"),
    path("dashboard/upload-image/", dashboard_views.dashboard_upload_image, name="dashboard_upload_image"),
    # Home and main pages (dynamic CMS)
    path("", views.home_view, name="home"),
    path("index", views.home_view, name="index"),
    path("about", views.about_view, name="about"),
    path("shop", views.shop_view, name="shop"),
    path("give", views.donate_view, name="give"),
    path("donate", RedirectView.as_view(url="/give", permanent=True), name="donate"),
    path("blog", views.blog_view, name="blog"),
    path("blog/<slug:slug>/", views.blog_detail_view, name="blog_detail"),
    path("contact", views.contact_view, name="contact"),
    # Legacy pages - now served from DynamicPage
    path("pastoral", views.generic_page_view, name="pastoral"),
    path("egroups", views.generic_page_view, name="egroups"),
    path("prayer", views.generic_page_view, name="prayer"),
    path("services", RedirectView.as_view(url="/", permanent=True), name="services"),
    path("club-fusion", views.generic_page_view, name="club_fusion"),
    path("quest", views.generic_page_view, name="quest"),
    path("sermon", views.generic_page_view, name="sermon"),
    path("plug-in/", RedirectView.as_view(url="/prayer/", permanent=True), name="plug_in"),
    path("plug-in", RedirectView.as_view(url="/prayer/", permanent=True)),
    path("bible-study", views.generic_page_view, name="bible_study"),
    path("membership", views.generic_page_view, name="membership"),
    path("volunteer", views.generic_page_view, name="volunteer"),
    # Catch-all for dynamic pages - MUST be last
    path("<slug:slug>/", views.dynamic_page_catchall, name="dynamic_page"),
    path("<slug:slug>", views.dynamic_page_catchall, name="dynamic_page_no_trailing_slash"),
    # Redirects from .html URLs to clean URLs (for backward compatibility)
    path('index.html', RedirectView.as_view(url='/', permanent=True), name='index_redirect'),
    path('about.html', RedirectView.as_view(url='/about', permanent=True), name='about_redirect'),
    path('shop.html', RedirectView.as_view(url='/shop', permanent=True), name='shop_redirect'),
    path('donate.html', RedirectView.as_view(url='/give', permanent=True), name='donate_redirect'),
    path('blog.html', RedirectView.as_view(url='/blog', permanent=True), name='blog_redirect'),
    path('contact.html', RedirectView.as_view(url='/contact', permanent=True), name='contact_redirect'),
    # Redirects for removed pages
    path('speaking.html', RedirectView.as_view(url='/about', permanent=True), name='speaking_redirect'),
    path('resources.html', RedirectView.as_view(url='/about', permanent=True), name='resources_redirect'),
    # Static assets (template uses relative paths: css/, js/, lib/, img/)
    path('css/<path:path>', views.serve_static_css, name='static_css'),
    path('js/<path:path>', views.serve_static_js, name='static_js'),
    path('lib/<path:path>', views.serve_static_lib, name='static_lib'),
    path('img/<path:path>', views.serve_static_img, name='static_img'),
]
