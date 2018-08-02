# -*- coding: utf-8 -*-
import json

from django.shortcuts import render, redirect
from django.http import JsonResponse
import logging

from openedu.celery import app
from .tasks import *

from .decorators import roo_member_required

from .models import Course ,RooTable

logger = logging.getLogger('celery_logging')


@roo_member_required
def index(request):
    course_queryset = Course.objects.all()
    logger.info(course_queryset)
    table = RooTable(course_queryset)
    context["table"] = table
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
            return redirect("/roo/")
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
