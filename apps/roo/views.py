# -*- coding: utf-8 -*-
import json
import string

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django import forms
from django.views.generic.edit import UpdateView
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

import logging

from openedu.celery import app
from .tasks import *

from .decorators import roo_member_required

from .models import \
    Course, CoursesTable, \
    Expertise, ExpertisesTable, \
    Owner, Expert
from django_tables2 import RequestConfig

logger = logging.getLogger('celery_logging')


def get_choises_id(q, choises):
    for e in choises:
        if e[1].lower().strip() == q.lower().strip():
            return e[0]
    return None


def get_choises_display(q, choises):
    for e in choises:
        if e[0] == q:
            return e[1]
    return None


def add_expertises(course, our_course):
    if course["expertise_types"] is None:
        return False
    exel_expertise_types = [e.strip().lower() for e in course["expertise_types"].split(',')]
    # print(course["title"], exel_expertise_types)
    expertise_types = list(set(exel_expertise_types) & set(
        [et[1].lower() for et in
         Expertise.EX_TYPES]))  # оставляем в expertise_types только то, что ТОЧНО есть в EX_TYPES
    # print("TYPES: ", exel_expertise_types, "  ", expertise_types)
    for e_type in expertise_types:
        has_ex = False
        for expertise in Expertise.objects.filter(course=our_course):
            if get_choises_display(expertise.type, expertise.EX_TYPES).lower() == e_type:
                expertise.supervisor = course["supervisor"]
                expertise.state = course["state"]
                print(course["title"], course["expertise_passed"])
                expertise.executed = True if course["expertise_passed"].strip().lower() == "да" else False

                expertise.organizer = course["organizer"]
                expertise.ex_date = course["date"]

                has_ex = True

                if course["expert"] is not None:
                    experts = Expert.objects.filter(expert=course["expert"])
                    if experts.count() > 0:
                        expertise.expert = experts.first()
                    else:
                        expert = Expert.objects.create(expert=course["expert"], login=course["expert_login"],
                                                       contacts=course["contacts"])
                        expertise.expert = expert
                expertise.save()

                # if course.get("expert", ""):
                #     if len(str(course["expert"]).strip()) > 0:
                #         expert = Expert.objects.filter(expert=course["expert"])
                #
                #         if len(expert) == 0:
                #             expert = Expert.objects.create(expert=course["expert"], login=course["expert_login"],
                #                                            contacts=course["contacts"])
                #             expertise.expert = expert
                #             expertise.save()
                #         else:
                #             expertise.expert = expert[0]
                #             expertise.save()
        if not has_ex:
            _type = get_choises_id(e_type, Expertise.EX_TYPES)
            # if course["expert"]:
            #     expert =
            expertise = Expertise.objects.create(course=our_course, supervisor=course["supervisor"], type=_type,
                                                 state=course["state"], organizer=course["organizer"],
                                                 ex_date=course["date"], executed=True if course[
                                                                                              "expertise_passed"].strip().lower() == "да" else False)
            if course["expert"] is not None:
                experts = Expert.objects.filter(expert=course["expert"])
                if experts.count() > 0:
                    expertise.expert = experts.first()
                else:
                    expert = Expert.objects.create(expert=course["expert"], login=course["expert_login"],
                                                   contacts=course["contacts"])
                    expertise.expert = expert
            expertise.save()

            # if course.get("expert", ""):
            #     if len(str(course["expert"]).strip()) > 0:
            #         expert = Expert.objects.filter(expert=course["expert"])
            #
            #         if len(expert) == 0:
            #             expert = Expert.objects.create(expert=course["expert"], login=course["expert_login"],
            #                                            contacts=course["contacts"])
            #             expertise.expert = expert
            #             expertise.save()
            #         else:
            #             expertise.expert = expert[0]
            #             expertise.save()


def upload_from_json(request):
    if request.method == 'POST':
        courses = json.loads(request.POST.get("json_value", None))
        # logger.info(courses)
        i = 0
        tbl = str.maketrans('', '', string.punctuation)
        for course in courses:
            if course["title"] is None or course["platform"] is None or course["owner"] is None:
                pass
            else:
                if course["expertise_status"] is None:
                    course["expertise_status"] = ''
                if course["expertise_passed"] is None:
                    course["expertise_passed"] = ''
                if course["communication_owner"] is None:
                    course["communication_owner"] = ''
                # Смотрим, есть ли такой owner в базе
                institution = None
                for owner in Owner.objects.all():
                    if owner.title.lower().translate(tbl).replace(' ', '') == course["owner"].lower().translate(
                            tbl).replace(' ', ''):
                        institution = owner
                        break
                if institution:
                    institution.save()
                else:
                    institution = Owner.objects.create(title=course["owner"])

                # Смотрим, есть ли такой partner в базе
                partner = None
                for platform in Platform.objects.all():
                    if platform.title.lower().translate(tbl).replace(' ', '') == course["platform"].lower().translate(
                            tbl).replace(' ', ''):
                        partner = platform
                        break
                if partner:
                    partner.save()
                else:
                    partner = Platform.objects.create(title=course["platform"])

                has_course = False
                for our_course in Course.objects.all():

                    if (
                            our_course.title.lower().translate(tbl).replace(' ', '') == course[
                        "title"].lower().translate(tbl).replace(' ', '') and
                            our_course.institution.title.lower().translate(tbl).replace(' ', '') == course[
                        "owner"].lower().translate(tbl).replace(' ', '') and
                            our_course.partner.title.lower().translate(tbl).replace(' ', '') == course[
                        "platform"].lower().translate(tbl).replace(' ', '')):
                        # print(course)
                        has_course = True
                        our_course.expertise_status = 3 if course["expertise_status"].strip().lower() == "да" else 0

                        if our_course.roo_status != 3:
                            if course["communication_owner"].strip().lower() == "да":
                                our_course.communication_owner = 3
                                our_course.communication_platform = 3
                            elif course["communication_owner"].strip().lower() in ["отказ", "нет"]:
                                our_course.communication_owner = 4
                                our_course.communication_platform = 4
                            else:
                                our_course.communication_owner = 0
                                our_course.communication_platform = 0

                        our_course.save()
                        add_expertises(course, our_course)

                        break

                if not has_course:
                    new_course = Course(title=course["title"])
                    new_course.institution = institution
                    new_course.partner = partner
                    new_course.expertise_status = 3 if course["expertise_status"].strip().lower() == "да" else 0

                    if course["communication_owner"].strip().lower() == "да":
                        our_course.communication_owner = 3
                        our_course.communication_platform = 3
                    elif course["communication_owner"].strip().lower() in ["отказ", "нет"]:
                        our_course.communication_owner = 4
                        our_course.communication_platform = 4
                    else:
                        our_course.communication_owner = 0
                        our_course.communication_platform = 0
                    # try:

                    new_course.save()
                    add_expertises(course, new_course)

                i += 1
                # print("!: ", i, course["title"])

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


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        # if isinstance(obj, YourCustomType):
        #     return str(obj)
        return super().default(obj)


@roo_member_required
def courses_list(request):
    context = dict()
    return render(request, "roo/courses_edit.html", context)


@roo_member_required
def courses_edit(request):
    # context = dict()
    # return render(request, "roo/courses_edit.html", context)
    data = serialize('json', Course.objects.all(), use_natural_foreign_keys=True)
    return_data = []
    for course in json.loads(data):
        new_course = course['fields']
        new_course['pk'] = course['pk']
        return_data.append(new_course)
    return HttpResponse(json.dumps(return_data), content_type='application/json')


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
    success_url = '/roo/close/'

    def get_context_data(self, **kwargs):
        context = super(CourseUpdate, self).get_context_data(**kwargs)
        context['expertises'] = Expertise.objects.filter(course=self.object)
        return context


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


class CourseStatusLayout(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['expertise_status']


class ExpertiseUpdate(UpdateView):
    form_class = ExpertiseLayout
    model = Expertise
    second_model = Course
    second_form_class = CourseStatusLayout
    template_name_suffix = '_update_form'
    title = forms.CharField(disabled=True)
    context_object_name = "expertise"
    pk_url_kwarg = 'course__id'

    def get_context_data(self, **kwargs):
        context = super(ExpertiseUpdate, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            details_form = self.second_form_class(self.request.POST, prefix='details')
        else:
            details_object = self.second_model.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
            details_form = self.second_form_class(instance=details_object, prefix='details')

        context['details_form'] = details_form
        return context

    def post(self, request, *args, **kwargs):
        response = super(ExpertiseUpdate, self).post(request, *args, **kwargs)
        details_form = self.second_form_class(self.request.POST, prefix='details')
        if details_form.is_valid():
            task = self.get_object()
            self.second_model.objects.filter(task=task).update(**details_form.cleaned_data)
            return response

        return render(request, self.template_name, {
            'form': self.get_form(self.get_form_class()),
            'details_form': details_form,
        })
        # success_url = TODO: сделать ссылку с закрытием окна
