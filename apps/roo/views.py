# -*- coding: utf-8 -*-
import json

from django.shortcuts import render_to_response, redirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.template.context_processors import csrf
from django.http import Http404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .tasks import update_courses_from_roo_task
from celery.task.control import revoke
import logging


logger = logging.getLogger('celery_logging')


def index(request):
    template = loader.get_template('roo/index.html')
    context = {
     'latest_question_list': "Kektorium",
    }
    return HttpResponse(template.render(context, request))


def start_tasks_celery(request):
    template = loader.get_template('roo/index.html')
    update_courses_from_roo_task.delay()
    context = {
     'start_list': "Started!",
    }
    return HttpResponse(template.render(context, request))


def stop_tasks_celery(request):
    template = loader.get_template('roo/index.html')
    update_courses_from_roo_task.revoke()
    logger.info("VIEW_STOP : {0}".format(request))
    #logger.info("VIEW : {0}".format(task_id))
    #revoke(task_id, terminate=True)
    # остановка таски
    context = {
        'stop_list': "Stoped!",
    }
    return HttpResponse(template.render(context, request))
    # update_courses_from_roo_task.delay()