# -*- coding: utf-8 -*-
import json

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django import forms
from django.views.generic.edit import UpdateView

import logging

from openedu.celery import app
from .tasks import *

from .decorators import roo_member_required

from .models import Course, RooTable
from django_tables2 import RequestConfig

logger = logging.getLogger('celery_logging')


@roo_member_required
def data(request):
    task = request.GET.get("task", None)
    i = app.control.inspect()
    context = dict()
    context["active"] = []
    for tasks in i.active().values():
        context["active"] += tasks

    if task:
        if task not in [t["name"].split('.')[2] for t in context["active"]]:
            globals()[task].delay()
            context["start_list"] = task
            return redirect("/roo/data/")
        else:
            context["status"] = f"{task} already running!"

    return render(request, "roo/index.html", context)


def get_active_tasks(request):
    if request.method == "POST":
        i = app.control.inspect()
        active_tasks = []
        for tasks in i.active().values():
            active_tasks += tasks
        return JsonResponse({"active_tasks": active_tasks})

@roo_member_required
def course_table(request):
    table = RooTable(Course.objects.all())
    RequestConfig(request, paginate=False).configure(table)
    context = dict()
    context["table"] = table
    return render(request, "roo/course_table.html", context)


class CourseUpdate(UpdateView):
    model = Course
    fields =  '__all__'
    template_name_suffix = '_update_form'
    title = forms.CharField(disabled=True)


