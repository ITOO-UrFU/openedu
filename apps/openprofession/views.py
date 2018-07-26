from django.http import Http404, JsonResponse
from django.shortcuts import render_to_response, render, redirect
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.template.context_processors import csrf
from django.views.generic.edit import FormView
from django.conf import settings
import os
import csv

import random
from string import digits, ascii_lowercase

import logging
import datetime
import json
from celery import Celery
from openedu.celery import app
from cacheback.decorators import cacheback

from .models import Entry, PersonalData, QuotesAvailable, Program, ReportUploadForm, Report, ReportEntry, \
    CourseUserGrade, PDAvailable, SimulizatorData, ProctoredReportEntry, SeminarData

from django.contrib.auth.decorators import user_passes_test

logger = logging.getLogger(__name__)


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""

    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups, login_url="admin:login")


@group_required('manager')
# @cacheback(lifetime=10 * 60, fetch_on_miss=True)
def personal_data_list(request):
    not_exists_reports = Program.objects.filter(reports=None)

    if request.GET.get('test_mode') == 'true':
        return render(request, 'openprofession/show_test_mode.html',
                      {"not_exists_reports": not_exists_reports, 'csrftoken': csrf(request)["csrf_token"]})
    else:
        return render(request, 'openprofession/show.html',
                      {"not_exists_reports": not_exists_reports, 'csrftoken': csrf(request)["csrf_token"]})


def entry(request, pk):
    _entry = Entry.objects.filter(student_id=pk).first()
    return JsonResponse({'student_id': _entry.student_id,
                         'state': _entry.state,
                         'result': _entry.result
                         })


def entry_list(request):
    _entry_list = Entry.objects.all()
    return JsonResponse([{'student_id': _entry.student_id,
                          'state': _entry.state,
                          'result': _entry.result}
                         for _entry in _entry_list
                         ], safe=False)


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super(EntryForm, self).__init__(*args, **kwargs)


@csrf_exempt
def add_entry(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            _entry = form.save(commit=False)
            _entry.save()
            return JsonResponse({'result': "success"})

        else:
            return JsonResponse({'result': "failed"})
    else:
        raise Http404


class PersonalDataForm(forms.ModelForm):
    class Meta:
        model = PersonalData
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super(PersonalDataForm, self).__init__(*args, **kwargs)


def thanks(request):
    return render(request, "openprofession/thanks.html")


@csrf_exempt
def add_pd(request):
    if request.method == 'POST':
        form = PersonalDataForm(request.POST, request.FILES)
        if form.is_valid():
            _pd = form.save(commit=False)
            _pd.save()
            return redirect("/openprofession/thanks/")

        else:
            for field in form:
                if field.errors:
                    print(field, field.errors)
            return render_to_response("openprofession/personaldata_form.html", {"form": form})
    else:
        QA = QuotesAvailable.objects.first()
        PDA = PDAvailable.objects.first()
        programs = Program.objects.filter(active=True)
        return render(request, "openprofession/personaldata_form.html", {"QA": QA, "PDA": PDA, 'programs': programs})


class SeminarDataForm(forms.ModelForm):
    class Meta:
        model = SeminarData
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super(SeminarDataForm, self).__init__(*args, **kwargs)


def seminar_thanks(request):
    return render(request, "openprofession/seminar_thanks.html")


@csrf_exempt
def add_seminar_bid(request):
    if request.method == 'POST':
        form = SeminarDataForm(request.POST, request.FILES)
        if form.is_valid():
            _pd = form.save(commit=False)
            _pd.save()
            return redirect("/openprofession/seminar_thanks/")

        else:
            for field in form:
                if field.errors:
                    print(field, field.errors)
            return render_to_response("seminar/seminar_form.html", {"form": form})
    else:
        return render(request, "seminar/seminar_form.html")


# @group_required('manger')
class ReportUploadView(FormView):
    template_name = 'openprofession/upload.html'
    form_class = ReportUploadForm
    success_url = '/openprofession/upload/'

    def get(self, request, *args, **kwargs):
        if request.user and (request.user.groups.filter(name__in=['manager']) or request.user.is_superuser):
            reports = Report.objects.all()
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            return self.render_to_response(self.get_context_data(form=form, reports=reports))
        else:
            return redirect('/admin/login?next=' + self.success_url)

    # @group_required('manger')
    def form_valid(self, form, *args):
        for each in form.cleaned_data['report_files']:
            parsed = str(each).split('.')[0].split("(")[0].strip().split("_")

            org = parsed[0]
            parsed.pop(0)
            date = datetime.datetime.strptime(parsed[-1], "%Y-%m-%d-%H%M").date()
            parsed.pop(-1)

            course_ids = Program.objects.order_by().values_list("course_id", flat=True).distinct()

            for id in course_ids:
                if id.lower() == str(each).split(f"{org}_")[1].split("_session")[0].lower():
                    course_id = id

            sessions = Program.objects.order_by().values_list("session", flat=True).distinct()
            for s in sessions:
                if s in str(each):
                    session = s

            try:
                for item in session.split("_") + course_id.split("_"):
                    parsed.remove(item)
            except:
                pass

            report_type = "_".join(parsed)

            report = Report(report_file=each, title=str(each), date=date, course_id=course_id, session=session,
                            report_type=report_type)
            report.save()
            program = Program.objects.filter(session=session, course_id=course_id).first()
            program.reports.add(report)

        return super(ReportUploadView, self).form_valid(form)


@app.task(bind=True)
def set_program_grade(*args):
    for user in PersonalData.objects.all():
        if user.program and user.program.reports.count() > 0:
            report = user.program.reports.filter(report_type="grade_report").latest("date")
            entry = report.entries.filter(user_id=user.possible_id).first()
            if entry:
                user.program_grade = entry.grade
                keys = list(json.loads(entry.raw_data).keys())
                possible_keys = ["Final Avg", "ИТ", "Final Exam Avg", "Exam Avg"]
                for pk in possible_keys:
                    if pk in keys:
                        user.exam_name = pk
                        user.exam_grade = json.loads(entry.raw_data)[pk]
                        user.save()

                user.save()
            else:
                user.program_grade = "-1"
                user.save()


@app.task(bind=True)
def set_proctoring_status(request, *args):
    for user in PersonalData.objects.all():
        if user.program and user.program.reports.count() > 0:
            report = user.program.reports.filter(report_type="proctored_exam_results_report").latest("date")
            entry = report.proctored_entries.filter(email=user.email).first()
            if entry:
                user.proctoring_status = entry.status
                user.save()
            else:
                user.proctoring_status = "None"
                user.save()


@app.task(bind=True)
def set_course_user_grade(*args):
    for user in PersonalData.objects.filter(possible_id__gt=0):
        for program in Program.objects.exclude(reports=None):
            report = program.reports.latest("date")
            entry = report.entries.filter(user_id=user.possible_id).first()
            if entry:
                course_user_grade = \
                    CourseUserGrade.objects.get_or_create(user=user, program=program, grade=entry.grade)[0]
                course_user_grade.save()


@app.task(bind=True)
def set_possible_id(*args):
    for user in PersonalData.objects.filter(possible_id=0).iterator():
        entry = ReportEntry.objects.filter(email=user.email)
        if entry:
            user.possible_id = entry.first().user_id
            user.save()


@app.task(bind=True)
def handle_report(*args):
    report = Report.objects.filter(processed=False).first()
    if report:
        address = settings.BASE_DIR.split(os.path.sep) + report.report_file.url.split(os.path.sep)
        filepath = str(os.path.sep).join(address)
        if report.report_type == "grade_report":
            with open(filepath, 'r') as report_file:
                reader = csv.DictReader(report_file)
                for row in reader:
                    try:
                        cohort_name = row["Cohort Name"]
                    except:
                        cohort_name = "Default"
                    report.entries.add(ReportEntry.objects.create(user_id=row["id"],
                                                                  email=row["email"],
                                                                  username=row["username"],
                                                                  grade=row["grade"],
                                                                  cohort_name=cohort_name,
                                                                  enrollment_track=row["Enrollment Track"],
                                                                  certificate_eligible=True if row[
                                                                                                   "Certificate Eligible"] == "Y" else False,
                                                                  certificate_delivered=row["Certificate Delivered"],
                                                                  raw_data=json.dumps(row)))
                    report.processed = True
                    report.save()
        elif report.report_type == "proctored_exam_results_report":
            with open(filepath, 'r') as report_file:
                reader = csv.DictReader(report_file)
                for row in reader:
                    report.proctored_entries.add(ProctoredReportEntry.objects.create(
                        email=row["user_email"],
                        exam_name=row["exam_name"],
                        allowed_time_limit_mins=row["allowed_time_limit_mins"],
                        is_sample_attempt=row["is_sample_attempt"],
                        started_at=row["started_at"],
                        completed_at=row["completed_at"],
                        status=row["status"]
                    ))
                    report.processed = True
                    report.save()


# app.control.rate_limit('openprofession.views.handle_report', '100/m')
# app.control.rate_limit('openprofession.views.set_possible_id', '5/m')
# app.control.rate_limit('openprofession.views.set_course_user_grade', '5/m')
# app.control.rate_limit('openprofession.views.set_program_grade', '100/m')
# app.control.rate_limit('openprofession.views.set_proctoring_status', '100/m')


# @app.task(bind=True)
# def search_user(*args):
#     user = PersonalData.objects.filter(possible_id=None).first()
#     if user:
#         if user.program:
#             reports = Report.objects.filter(course_id=user.program.course_id, session=user.program.session)
#             possible_id = ReportEntry.objects.filter(report__in=reports).first()
#             if possible_id:
#                 user.possible_id = possible_id
#             user.save()

def updatePD(request):
    if request.method == 'POST':
        try:
            id = request.POST.get("user_id", )
            field = request.POST.get('field_name')
            field_val = request.POST.get("value")
            if field_val.lower() in ['true', 'on', 'checked']:
                field_val = True
            else:
                field_val = False
            pd = PersonalData.objects.get(pk=id)
            setattr(pd, field, field_val)
            pd.save()
            return JsonResponse({"result": "success"})
        except:
            return JsonResponse({"result": "false"})


def _pw(pwtype="password", length=6):
    s = ''
    if pwtype == "password":
        for i in range(length):
            s += random.choice(digits + ascii_lowercase)
        return s
    elif pwtype == "username":
        for i in range(length):
            s += random.choice(digits)
        return s


class SimulizatorDataForm(forms.ModelForm):
    class Meta:
        model = SimulizatorData
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super(SimulizatorDataForm, self).__init__(*args, **kwargs)


def sim_thanks(request):
    return render(request, "openprofession/sim_thanks.html")


@csrf_exempt
def add_sim_data(request):
    if request.method == 'POST':
        form = SimulizatorDataForm(request.POST, request.FILES)
        if form.is_valid():
            _pd = form.save(commit=False)
            _pd.username = f"User{_pw('username', 4)}"
            _pd.password = f"{_pw('password')}"
            _pd.save()
            return render_to_response("openprofession/sim_thanks.html", {'pd': _pd})

        else:
            return render_to_response("openprofession/sim_personaldata_form.html", {"form": form})
    else:
        return render(request, "openprofession/sim_personaldata_form.html")
