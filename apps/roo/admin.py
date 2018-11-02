from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.widgets import ManyToManyWidget

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
#     communication_owner = models.CharField("Статус коммуникации с правообладателем", max_length=1,
#                                            choices=COMMUNICATION_OWNER_STATES, default="0")
#     communication_platform = models.CharField("Статус коммуникации с платформой", max_length=1,
#                                               choices=COMMUNICATION_PLATFORM_STATES, default="0")
    # expertise_status = models.CharField("Статус экспертизы", max_length=1, choices=EX_STATES, default="0")
    # passport_status = models.CharField("Статус паспорта", max_length=1, choices=PASSPORT_STATES, default="0")
    # roo_status = models.CharField("Статус загрузки на роо", max_length=1, choices=ROO_STATES, default="0")
    # required_ratings_state = models.CharField("Состояние загрузки обязательных оценок", max_length=1,
    #                                           choices=REQUIRED_RATINGS_STATES, default="0")
    # unforced_ratings_state = models.CharField("Состояние загрузки добровольных оценок", max_length=1,
    #                                           choices=UNFORCED_RATINGS_STATES, default="0")
    # comment = models.TextField("Примечание Шарыпова-Рачёва", blank=True, null=True)
    # expert_access = models.CharField("Доступ к курсу для экспертов обязательной оценки", choices=EX_ACCESSES,
    #                                  max_length=1, default="0")
     # = Field(
     #        attribute='get__display',
     #        column_name=''
     #    )

class CourseResource(resources.ModelResource):
    expertises = fields.Field(widget=ManyToManyWidget(Expertise))

    title = Field(attribute='title', column_name='Наименование')
    partner__title = Field(attribute='partner__title', column_name='Платформа')
    institution__title = Field(attribute='institution__title', column_name='Правообладатель')

    directions_all = Field(column_name='Массив идентификаторов направлений')
    activities_all = Field(column_name='Массив идентификаторов областей деятельности')
    course_link_all = Field(column_name='Курс в базе')
    ex_link_all = Field(column_name='Обязательные экспертизы в базе')
    competences = Field(attribute='competences', column_name='Формируемые компетенции')
    in_archive = Field(attribute="in_archive", column_name="Архивный")
    roo_status = Field(attribute="roo_status", column_name="Статус загрузки на РОО")
    results = Field(attribute="results", column_name="Результаты обучения")
    expertise_status = Field(
        attribute='get_expertise_status_display',
        column_name='Статус экспертизы'
    )
    expert_access = Field(
        attribute='get_expert_access_display',
        column_name='Доступ к курсу для экспертов обязательной оценки'
    )
    unforced_ratings_state = Field(
        attribute='get_unforced_ratings_state_display',
        column_name='Состояние загрузки добровольных оценок'
    )
    required_ratings_state = Field(
        attribute='get_required_ratings_state_display',
        column_name='Состояние загрузки обязательных оценок'
    )
    roo_status = Field(
        attribute='get_roo_status_display',
        column_name='Статус загрузки на роо'
    )
    passport_status = Field(
        attribute='get_passport_status_display',
        column_name='Статус паспорта'
    )
    communication_owner = Field(
        attribute='get_communication_owner_display',
        column_name='Статус коммуникации с правообладателем'
    )
    communication_platform = Field(
        attribute='get_communication_platform_display',
        column_name='Статус коммуникации с платформой'
    )

    course_item_url = Field(attribute="course_item_url", column_name="Ссылка на РОО")

    class Meta:
        model = Course
        fields = ('title', 'institution__title', 'partner__title', 'course_link_all', 'ex_link_all', 'competences', 'directions_all', 'activities_all', 'in_archive', 'roo_status', 'results', 'expertise_status', 'expert_access', 'unforced_ratings_state', 'required_ratings_state', 'roo_status', 'passport_status', 'communication_owner', 'communication_platform', 'course_item_url')

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

    def dehydrate_course_link_all(self, course):
        course_link = "http://openedu.urfu.ru/roo/"+str(course.pk)
        # for activ in course.activities.all():
        #     activs += activ.title + "\n"
        return course_link

    def dehydrate_ex_link_all(self, course, expertises):
        ex_links = ""
        for idx,ex in expertises.filter(course=course):
            ex_links += "\n" if idx > 0 else "" + "http://openedu.urfu.ru/roo/expertise/" + str(ex.pk) + "/"
        return ex_links


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
