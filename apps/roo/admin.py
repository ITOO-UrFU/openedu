from django.contrib import admin
from .models import Course, Platform, Expert, Expertise, Owner, Teacher, Area, Direction, Competence, Result, \
    EvaluationTool, ProctoringService
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

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


# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ("title", "get_platform", "institution", "get_description", "get_image")
#     list_filter = ("partner", "roo_status", "institution")
#     filter_horizontal = ("directions", "activities", "teachers")
#     search_fields = ("title",)


class CourseResource(resources.ModelResource):
    directions_all = Field()
    class Meta:
        model = Course
        fields = ('id', 'title', 'institution__title', 'directions_all')

    def dehydrate_directions_all(self, course):
        dirs = ""
        for direction in course.directions.objects():
            dirs += direction.title + "/n"
        return dirs

@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    resource_class = CourseResource
    list_display = ("title", "get_platform", "institution", "get_description", "get_image")
    list_filter = ("partner", "roo_status", "institution")
    filter_horizontal = ("directions", "activities", "teachers")
    search_fields = ("title",)


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ("title", "get_description", "get_image")


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "get_image")
    search_fields = ("title",)


@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_display = ("expert", "login", "contacts")


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
    list_filter = ("type",)
    search_fields = ("course__title",)


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
