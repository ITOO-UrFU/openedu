from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from .models import Course, Platform, Expert, Expertise, Owner, Teacher, Area, Direction, Competence, Result, \
    EvaluationTool, ProctoringService


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
    # expertise_status = Field(
    #     attribute='get_expertise_status_display',
    #     column_name='Статус экспертизы'
    # )

    title = Field(attribute='title', column_name='Наименование')
    partner__title = Field(attribute='partner__title', column_name='Платформа')
    institution__title = Field(attribute='institution__title', column_name='Правообладатель')

    directions_all = Field(column_name='Массив идентификаторов направлений')
    activities_all = Field(column_name='Массив идентификаторов областей деятельности')
    competences = Field(attribute='competences', column_name='Формируемые компетенции')
    in_archive = Field(attribute="in_archive", column_name="Архивный")
    roo_status = Field(attribute="roo_status", column_name="Статус загрузки на РОО")
    results = Field(attribute="results", column_name="Результаты обучения")
    expertise_status = Field(attribute="expertise_status")

    class Meta:
        model = Course
        fields = ('title', 'institution__title', 'partner__title', 'competences', 'directions_all', 'activities_all', 'in_archive', 'roo_status', 'results', 'expertise_status')

    def dehydrate_directions_all(self, course):
        dirs = ""
        for direction in course.directions.all():
            dirs += direction.title + "\n"
        return dirs

    def dehydrate_results_all(self, course):
        results = ""
        for result in course.results.all():
            results += result.title + "\n"
        return results

    def dehydrate_activities_all(self, course):
        activs = ""
        for activ in course.activities.all():
            activs += activ.title + "\n"
        return activs


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
