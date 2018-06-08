from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import File, PPS


@admin.register(PPS)
class PPSAdmin(VersionAdmin):
    list_display = (
        "name",
        "conditions",
        "position",
        "disciplines",
        "education",
        "ppk",
        "weight",
        "experience",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "name",
        "conditions",
        "position",
        "disciplines",
        "education",
        "ppk",
        "weight",
        "experience",
    )


@admin.register(File)
class FileAdmin(VersionAdmin):
    list_display = ('id', 'file', 'done', "created_at")
