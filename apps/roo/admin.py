from django.contrib import admin
from .models import Course, Platform, Expert, Expertise, Owner, Teacher, Area, Direction, Competence, Result, EvaluationTool, ProctoringService


@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(EvaluationTool)
class EvaluationToolAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(ProctoringService)
class ProctoringServiceAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "get_platform", "institution", "get_description", "get_image")
    list_filter = ("partner", "roo_status")
    filter_horizontal = ("directions", "activities", "teachers")
    search_fields = ("title",)


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ("title", "get_description", "get_image")


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "get_image")


@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_display = ("login",)


@admin.register(Expertise)
class ExpertiseAdmin(admin.ModelAdmin):
    list_display = ("course",

                    )


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ("title", "get_image")


@admin.register(Area)
class AreasAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ("title", "code", "activity")
    list_filter = ("activity",)
