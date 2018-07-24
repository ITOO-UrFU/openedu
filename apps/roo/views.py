# -*- coding: utf-8 -*-
import json

from django.core.exceptions import ObjectDoesNotExist
from django.template.context_processors import csrf
from django.shortcuts import render, redirect
import logging

from celery.task.control import inspect


logger = logging.getLogger('celery_logging')


def index(request):
    task = request.GET.get("task", None)
    i = inspect()
    print(i)
    context = {}
    context["active"] = i.active()

    try:
        if task:
            globals()[task].delay()
            context["start_list"] = task
            return redirect("/roo/")
    except:
        context["start_list"] = "None"
    return render(request, "roo/index.html", context)
