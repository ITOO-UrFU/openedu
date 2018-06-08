from django.contrib import admin
from .models import EIOS


@admin.register(EIOS)
class EIOSAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EIOS._meta.get_fields()]

# Register your models here.
