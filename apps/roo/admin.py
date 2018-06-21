from django.contrib import admin
from .models import Course, Platform, Expert, Expertise, Owner


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Course._meta.get_fields()]


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Platform._meta.get_fields()]


@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Expert._meta.get_fields()]


@admin.register(Expertise)
class ExpertiseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Expertise._meta.get_fields()]


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ("title", "person", "connection_form", "connection_date", "contacts" )
