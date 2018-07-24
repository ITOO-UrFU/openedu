# -*- coding: utf-8 -*-
import json

from django.core.exceptions import ObjectDoesNotExist
from django.template.context_processors import csrf
from django.shortcuts import render, redirect
import logging

from openedu.celery import app
from .tasks import *

logger = logging.getLogger('celery_logging')


def index(request):
    task = request.GET.get("task", None)
    i = app.control.inspect()
    context = dict()
    context["active"] = []
    for tasks in i.active().values():
        context["active"] += tasks

    print([t["name"].split('.')[2] for t in context["active"]])

    if task:
        if task not in [t["name"].split('.')[2] for t in context["active"]]:
            globals()[task].delay()
            context["start_list"] = task
            return redirect("/roo/")
        else:
            context["status"] = f"{task} already running!"

    return render(request, "roo/index.html", context)
