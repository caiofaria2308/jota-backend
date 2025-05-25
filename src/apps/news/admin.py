from django.contrib import admin

from apps.news.models import New


@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the New model.
    """

    list_display = ("title", "subtitle", "author", "published_at", "status")
    list_filter = ("status", "is_exclusive")
    search_fields = ("title", "subtitle", "content")
    ordering = ("-published_at",)
    list_per_page = 20
    raw_id_fields = ("author",)
