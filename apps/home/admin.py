from django.contrib import admin
from .models import ContentItem, Page


@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    search_fields = ("title", "weight")
    list_display = ("title", "weight")


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    search_fields = ("title", "link")
    list_display = ("title", "link")
    filter_horizontal = ("contents", )


