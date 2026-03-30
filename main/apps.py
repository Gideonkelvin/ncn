from django.apps import AppConfig


class MainConfig(AppConfig):
    name = "main"
    verbose_name = "Website content"

    def ready(self):
        from django.contrib import admin

        admin.site.site_header = "Nairobi Chapel Ngong Hive"
        admin.site.site_title = "Ngong Hive Admin"
        admin.site.index_title = "Manage pages, home content, blog, and messages"
