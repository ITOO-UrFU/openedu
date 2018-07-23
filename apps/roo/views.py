# -*- coding: utf-8 -*-
import json

from django.shortcuts import render_to_response, redirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.template.context_processors import csrf
from django.http import Http404
from django.http import HttpResponse
from django.template import loader
from .tasks import update_courses_from_roo_task


# def index(request):
#     template = loader.get_template('roo/index.html')
#     context = {
#         'latest_question_list': "kektorium",
#     }
#     return HttpResponse(template.render(context, request))


def index(request):
    update_courses_from_roo_task.delay()
    return HttpResponse('work kicked off!')
