# -*- coding: utf-8 -*-
import json
import string

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django import forms
from django.views.generic.edit import UpdateView

import logging

from openedu.celery import app
from .tasks import *

from .decorators import roo_member_required

from .models import \
    Course, CoursesTable, \
    Expertise, ExpertisesTable, \
    Owner
from django_tables2 import RequestConfig

logger = logging.getLogger('celery_logging')


def upload_from_json(request):
    if request.method == 'POST':
        courses = json.loads(request.POST.get("json_value", None))
        # logger.info(courses)
        i = 0
        tbl = str.maketrans('','',string.punctuation)
        for course in courses:
            if course["title"] is None or course["platform"] is None or course["owner"] is None:
                pass
            else:
                print("!!!!!!!!!!!!!!!!!!!!!!: ", i)
                for our_course in Course.objects.all():
                    if our_course.title.lower().translate(tbl) == course["title"].lower().translate(tbl) and our_course.institution.title.lower().translate(tbl) == course["owner"].lower().translate(tbl) and our_course.partner.title.lower().translate(tbl) == course["platform"].lower().translate(tbl):
                        print(course)
                        i += 1


        return render(request, 'roo/upload_from_json.html')
    else:
        return render(request, 'roo/upload_from_json.html')


@roo_member_required
def data(request):
    if request.method == "GET":

        i = app.control.inspect()
        context = dict()
        context["active"] = []

        # Statistics
        context["courses_count"] = Course.objects.all().count()
        context["expertises_count"] = Expertise.objects.all().count()
        context["owners_count"] = Owner.objects.all().count()

        for tasks in i.active().values():
            context["active"] += tasks

        return render(request, "roo/data.html", context)

    elif request.method == "POST":
        i = app.control.inspect()
        context = dict()
        context["active"] = []
        for tasks in i.active().values():
            context["active"] += tasks
        task = request.POST.get("task", None)
        if task:
            if task not in [t["name"].split('.')[2] for t in context["active"]]:
                globals()[task].delay()

        return JsonResponse({"status": "sucess"})


def get_active_tasks(request):
    if request.method == "POST":
        i = app.control.inspect()
        active_tasks = []
        for tasks in i.active().values():
            active_tasks += tasks
        return JsonResponse({"active_tasks": active_tasks})


@roo_member_required
def courses(request):
    table = CoursesTable(Course.objects.all())
    RequestConfig(request, paginate=False).configure(table)
    context = dict()
    context["table"] = table
    return render(request, "roo/courses.html", context)


@roo_member_required
def expertises(request):
    table = ExpertisesTable(Expertise.objects.all())
    RequestConfig(request, paginate=False).configure(table)
    context = dict()
    context["table"] = table
    return render(request, "roo/expertises.html", context)


class CourseUpdate(UpdateView):
    model = Course
    fields = '__all__'
    template_name_suffix = '_update_form'
    title = forms.CharField(disabled=True)


class ExpertiseLayout(forms.ModelForm):
    platform = forms.ModelChoiceField(queryset=Platform.objects.all(), required=False)
    owner = forms.ModelChoiceField(queryset=Owner.objects.all(), required=False)

    class Meta:
        model = Expertise
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ExpertiseLayout, self).__init__(*args, **kwargs)
        self.fields['platform'].initial = self.instance.course.partner
        self.fields['owner'].initial = self.instance.course.institution


class ExpertiseUpdate(UpdateView):
    form_class = ExpertiseLayout
    model = Expertise
    template_name_suffix = '_update_form'
    title = forms.CharField(disabled=True)
    context_object_name = "expertise"

    # success_url = TODO: сделать ссылку с закрытием окна
