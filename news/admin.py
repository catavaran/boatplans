"""Admin for news application."""

from django.contrib import admin

from news.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Modeladmin for news."""

    list_display = ('title', 'slug', 'created_at')
