from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/pastorate/", views.pastorate, name="pastorate"),
    path("contact/", views.contact, name="contact"),
    path("ministries/egroups/", views.egroups, name="ministries_egroups"),
    path("ministries/plugin/", views.plugin, name="ministries_plugin"),
    path("ministries/club-fusion/", views.club_fusion, name="ministries_club_fusion"),
    path("ministries/quest/", views.quest, name="ministries_quest"),
    path("ministries/mens-ministry/", views.mens_ministry, name="ministries_mens_ministry"),
    path(
        "ministries/womens-ministry/",
        views.womens_ministry,
        name="ministries_womens_ministry",
    ),
    path("resources/sermon/", views.sermon, name="resources_sermon"),
    path("resources/bible-study/", views.bible_study, name="resources_bible_study"),
    path("engage/membership/", views.membership, name="engage_membership"),
    path("engage/volunteer/", views.volunteer, name="engage_volunteer"),
    path("engage/events/", views.events, name="engage_events"),
    path("engage/gallery/", views.gallery_list, name="engage_gallery"),
    path("engage/gallery/<slug:slug>/", views.gallery_detail, name="engage_gallery_detail"),
    path("give/", views.give, name="give"),
]
