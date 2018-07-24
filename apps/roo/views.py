# -*- coding: utf-8 -*-
import json

from django.shortcuts import render_to_response, redirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.template.context_processors import csrf
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from .tasks import update_courses_from_roo_task, update_platform_from_roo_task
import logging


logger = logging.getLogger('celery_logging')


def index(request):
    task = request.GET.get("task", None)
    context = {}
    try:
        if task:
            globals()[task].delay()
            context["start_list"] = task
            return redirect("/roo/")
    except:
        context["start_list"] = "None"
    return render(request, "roo/index.html", context)
