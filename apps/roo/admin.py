from django.contrib import admin
from .models import Course, Platform, Expert, Expertise, Owner, Teacher


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "description")


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ("title", "person", "connection_form", "connection_date", "contacts")


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("title", "description")


@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_display = ("login",)


@admin.register(Expertise)
class ExpertiseAdmin(admin.ModelAdmin):
    list_display = ("course",
                    "state",
                    "date",
                    "type",
                    "executed",
                    "expert",
                    "supervisor",
                    "organizer",
                    )


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ("title",)
