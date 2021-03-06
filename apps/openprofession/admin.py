from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.html import format_html
from reversion.admin import VersionAdmin

from .models import Entry, PersonalData, Program, QuotesAvailable, Report, ReportEntry, CourseUserGrade, PDAvailable, \
    SimulizatorData, ProctoredReportEntry, SeminarData, EdcrunchPersonalData, OratorPersonalData


@admin.register(Entry)
class MinorAdmin(VersionAdmin):
    list_display = ('student_id',)


@admin.register(ReportEntry)
class ReportEntryAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('email', 'user_id', 'grade')


@admin.register(SimulizatorData)
class SimulizatorDataAdmin(admin.ModelAdmin):
    list_display = ('fio', 'email', 'phone', 'username', 'password', 'created_at', 'agreement')
    search_fields = ('fio', 'email', 'phone')


@admin.register(Program)
class ProgramAdmin(VersionAdmin):
    list_display = ('title', 'course_id', 'session', 'active', 'has_report', 'start', 'get_url', 'get_data_download', 'program_actions')
    search_fields = ('course_id', 'session', 'active')
    list_filter = ('course_id', 'session', 'active', 'start')

    def get_url(self, obj):
        return f"<a class='button' href=\"https://learn.openprofession.ru/courses/course-v1:{obj.org}+{obj.course_id}+{obj.session}/courseware/\" target=\"_blank\">Courseware</a>"

    def get_data_download(self, obj):
        return f"<a class='button' href=\"https://learn.openprofession.ru/courses/course-v1:{obj.org}+{obj.course_id}+{obj.session}/instructor#view-data_download\" target=\"_blank\">Скачивание данных</a>"

    get_url.allow_tags = True
    get_url.short_description = "Ссылки"

    get_data_download.allow_tags = True
    get_data_download.short_description = "Скачивание данных"

    def program_actions(self, obj):
        if obj.active:
            return format_html(
                '<a class="button" href="{}">Add session</a>&nbsp;',
                reverse('admin:new_session', args=[obj.pk]),
            )
        else:
            return "<p style='color:red;'>Неактивна</p>"

    def process_session(self, request, program_id, *args, **kwargs):
        program = Program.objects.get(pk=program_id)
        program.add_session()
        return redirect('/admin/openprofession/program/')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<program_id>.+)/new_session/$',
                self.admin_site.admin_view(self.process_session),
                name='new_session',
            ),
        ]
        return custom_urls + urls

    program_actions.short_description = 'Program Actions'
    program_actions.allow_tags = True


@admin.register(CourseUserGrade)
class CourseUserGradeAdmin(admin.ModelAdmin):
    list_display = ('program', 'user', 'grade', 'created_at')
    list_filter = ('program__course_id', 'user')


@admin.register(PersonalData)
class PersonalDataAdmin(AdminAdvancedFiltersMixin, VersionAdmin):
    list_display = ('fio', 'diploma_scan', 'program', 'city', 'exam_name', 'exam_grade', 'created_at', 'updated_at')
    search_fields = ('last_name', 'first_name', 'second_name', "email")
    list_filter = ('program__start', 'in_quote', 'paid', 'proctoring_status')
    advanced_filter_fields = ('program__start', 'in_quote', 'paid')
    raw_id_fields = ("program",)
    exclude = ("entries", "courses")


@admin.register(SeminarData)
class SeminarDataAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('last_name', 'first_name', 'second_name', "email", "type_of_participation", "job", "position", "created_at")
    search_fields = ('last_name', 'first_name', 'second_name', "email")
    list_filter = ('type_of_participation',)


@admin.register(Report)
class ReportAdmin(VersionAdmin):
    list_display = ('title', 'report_file', 'date', 'course_id', 'session', 'processed')
    list_filter = ('processed', 'report_type')


@admin.register(QuotesAvailable)
class QuotesAvailableAdmin(admin.ModelAdmin):
    list_display = ('available',)


@admin.register(PDAvailable)
class PDAvailableAdmin(admin.ModelAdmin):
    list_display = ('available',)


@admin.register(ProctoredReportEntry)
class ProctoredReportEntryAdmin(admin.ModelAdmin):
    list_display = ('email', 'exam_name', 'status')
    list_filter = ('status',)


@admin.register(EdcrunchPersonalData)
class EdcrunchPersonalDataAdmin(AdminAdvancedFiltersMixin, VersionAdmin):
    list_display = ('fio', 'diploma_scan', 'city', 'created_at', 'updated_at')
    search_fields = ('last_name', 'first_name', 'second_name', "email")
    exclude = ("entries", "courses")


@admin.register(OratorPersonalData)
class OratorPersonalDataAdmin(AdminAdvancedFiltersMixin, VersionAdmin):
    list_display = ('fio', 'diploma_scan', 'city', 'created_at', 'updated_at')
    search_fields = ('last_name', 'first_name', 'second_name', "email")
    exclude = ("entries", "courses")
