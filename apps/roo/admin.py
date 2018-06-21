from django.contrib import admin
from .models import Course, Platform, Expert, Expertise, Owner


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "short_description", "description",
                    "roo_id", "competences", "results",
                    "grade_tools", "photo", "authors", "prerequisites",
                    "content", "directions", "subject", "activity",
                    "language", "enrollment_end_date", "start_date",
                    "duration", "labor", "certificate", "proctoring_service",
                    "version", "opened", "admin_email", "expertized",
                    "domain", "uploaded_roo", "uploaded_prepod",
                    "platform", "url", "roo_url", "owner",
                    "permission", "comment"
                    )


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ("title", "person", "connection_form", "connection_date", "contacts")


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
