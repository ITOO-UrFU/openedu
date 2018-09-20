# -*- coding: utf-8 -*-
import string

from django import forms
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView
from django_tables2 import RequestConfig

from .decorators import roo_member_required
from .models import \
    CoursesTable, \
    Expertise, ExpertisesTable, \
    Expert, Teacher
from .tasks import *

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


def upload_comments(request):
    if request.method == "POST":
        courses = json.loads(request.POST.get("json_value", None))
        tbl = str.maketrans('', '', string.punctuation)
        course_count = 0
        sum = 0
        # course_exsist = False
        for course in courses:
            # if course["comment"] == "":
            #     break
            # print(course["course_title"])
            course_exsist = False
            print(course_count, "/", sum)
            for our_course in Course.objects.all():
                # if our_course.title.lower().translate(tbl).replace(' ', '') == course["course_title"].lower().translate(tbl).replace(' ',''):
                #     if our_course.partner.title == 'OpenProfession' and our_course.institution.title == "Уральский федеральный университет имени первого Президента России Б.Н.Ельцина, ТГУ":
                #         our_course.external_url = course["external_url"]
                #         our_course.save()
                #         print(course["course_title"])
                #         # print(course_count, "/", sum)
                #         # Геометрия: аналитический метод решения задач
                our_course_url = "" if our_course.external_url is None else our_course.external_url
                if our_course_url.lower().translate(tbl).replace(' ', '') == course["external_url"].lower().translate(
                        tbl).replace(' ', '') and our_course.title.lower().translate(tbl).replace(' ', '') == course[
                    "course_title"].lower().translate(tbl).replace(' ',
                                                                   '') and our_course.partner.title.lower().translate(
                    tbl).replace(' ', '') == course["course_partner"].lower().translate(tbl).replace(' ', ''):
                    course_count += 1
                    our_course.comment = course["comment"]
                    our_course.save()
                    course_exsist = True
                    break
                elif our_course_url.lower().translate(tbl).replace(' ', '') == course[
                    "external_url"].lower().translate(tbl).replace(' ', '') and our_course.title.lower().translate(
                    tbl).replace(' ', '') == course[
                    "course_title"].lower().translate(tbl).replace(' ',
                                                                   '') and our_course.institution.title.lower().translate(
                    tbl).replace(' ', '') == course["course_institution"].lower().translate(tbl).replace(' ', ''):
                    course_count += 1
                    our_course.comment = course["comment"]
                    our_course.save()
                    course_exsist = True
                    break
            if not course_exsist:
                print(course["course_title"], course["comment"])

            sum += 1

        print('Курсов найдено: ', course_count)
        return render(request, 'roo/upload_from_json.html')
    else:
        return render(request, 'roo/upload_from_json.html')


def upload_expertises(request):
    if request.method == "POST":
        expertises = json.loads(request.POST.get("json_value", None))
        tbl = str.maketrans('', '', string.punctuation)
        expertise_count = 0
        not_found_count = 0
        for expertise in expertises:
            course_exist = False
            for our_course in Course.objects.all():
                if our_course.title.lower().translate(tbl).replace(' ', '') == expertise[
                    "course_title"].lower().translate(tbl).replace(' ',
                                                                   '') and our_course.institution.title.lower().translate(
                    tbl).replace(' ', '') == expertise["course_institution"].lower().translate(tbl).replace(' ',
                                                                                                            '') and our_course.partner.title.lower().translate(
                    tbl).replace(' ', '') == expertise["course_partner"].lower().translate(tbl).replace(' ', ''):
                    course_exist = True

                    if our_course.external_url is None or our_course.external_url == "":
                        our_course.external_url = expertise["external_url"]
                    our_course.save()
                    # ex = Expertise.objects.create(course=our_course, type="0", executed=expertise["executed"],
                    #                               supervisor=expertise["supervisor"], organizer=expertise["organizer"],
                    #                               comment=expertise["comment"],
                    #                               comment_fieldset_1=expertise["comment_fieldset_1"],
                    #                               comment_fieldset_2=expertise["comment_fieldset_2"],
                    #                               has_length=expertise["has_length"],
                    #                               has_description=expertise["has_description"],
                    #                               has_authors=expertise["has_authors"],
                    #                               language=expertise["language"],
                    #                               has_prerequisites=expertise["has_prerequisites"],
                    #                               has_certificate=expertise["has_certificate"],
                    #                               has_dates=expertise["has_dates"],
                    #                               has_admin_email=expertise["has_admin_email"],
                    #                               has_labor=expertise["has_labor"],
                    #                               has_competences=expertise["has_competences"],
                    #                               has_results=expertise["has_results"],
                    #                               has_evaluation_tools=expertise["has_evaluation_tools"],
                    #                               has_recommended_directions=expertise["has_recommended_directions"],
                    #                               has_proctoring=expertise["has_proctoring"],
                    #                               has_labor_costs=expertise["has_labor_costs"],
                    #                               has_short_description=expertise["has_short_description"],
                    #                               has_learning_plan=expertise["has_learning_plan"],
                    #                               has_promo_clip=expertise["has_promo_clip"],
                    #                               language_video=expertise["language_video"],
                    #                               language_subtitles=expertise["language_subtitles"],
                    #                               has_course_subject=expertise["has_course_subject"],
                    #                               is_open=expertise["is_open"],
                    #                               has_expertises_types=expertise["has_expertises_types"],
                    #                               has_ownership_document_scan=expertise["has_ownership_document_scan"],
                    #                               has_not_prohibited=expertise["has_not_prohibited"],
                    #                               has_text_materials=expertise["has_text_materials"],
                    #                               has_illustrations=expertise["has_illustrations"],
                    #                               has_audio=expertise["has_audio"], has_video=expertise["has_video"],
                    #                               has_quality_checking=expertise["has_quality_checking"],
                    #                               no_permission_of_owners=expertise["no_permission_of_owners"],
                    #                               got_into_record=expertise["got_into_record"],
                    #                               got_expertise_2018=expertise["got_expertise_2018"],
                    #                               additional_info=expertise["additional_info"])
                    # if expertise["expert"] is not None:
                    #     ex.expert = Expert.objects.filter(expert=expertise["expert"]).first()
                    #     ex.save()

                    expertise_count += 1
                    print('ОК:', expertise_count)
                    break

            if course_exist:
                pass
                # print(expertise_count, ' !')
            else:
                print('КУРСА НЕТУ!!!!!', expertise['course_title'])
                not_found_count += 1
                # print(expertise_count, expertise['course_title'])
                # print(expertise_count, expertise['course_partner'])

        print('Курсов не найдено: ', not_found_count)
        return render(request, 'roo/upload_from_json.html')
    else:
        return render(request, 'roo/upload_from_json.html')


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
        context["passport"] = Course.get_passport_responsibles()
        context["expertises_count"] = Expertise.objects.filter(type="0").count()
        context["main_expertise_count"] = Expertise.main_expertise_count()
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


def TableExpertiseUpdate(request):
    if request.method == "POST":
        try:
            request_data = json.loads(request.body)
            expertise = Expertise.objects.get(pk=request_data['pk'])
            expertise.additional_info = request_data['additional_info']
            expertise.comment = request_data['comment']
            expertise.comment_fieldset_1 = request_data['comment_fieldset_1']
            expertise.comment_fieldset_2 = request_data['comment_fieldset_2']
            expertise.ex_date = request_data['ex_date']
            expertise.executed = request_data['executed']
            expertise.got_expertise_2018 = request_data['got_expertise_2018']
            expertise.got_into_record = request_data['got_into_record']
            expertise.has_admin_email = request_data['has_admin_email']
            expertise.has_audio = request_data['has_audio']
            expertise.has_authors = request_data['has_authors']
            expertise.has_certificate = request_data['has_certificate']
            expertise.has_competences = request_data['has_competences']
            expertise.has_course_subject = request_data['has_course_subject']
            expertise.has_dates = request_data['has_dates']
            expertise.has_description = request_data['has_description']
            expertise.has_evaluation_tools = request_data['has_evaluation_tools']
            expertise.has_expertises_types = request_data['has_expertises_types']
            expertise.has_illustrations = request_data['has_illustrations']
            expertise.has_labor = request_data['has_labor']
            expertise.has_labor_costs = request_data['has_labor_costs']
            expertise.has_learning_plan = request_data['has_learning_plan']
            expertise.has_length = request_data['has_length']
            expertise.has_not_prohibited = request_data['has_not_prohibited']
            expertise.has_ownership_document_scan = request_data['has_ownership_document_scan']
            expertise.has_prerequisites = request_data['has_prerequisites']
            expertise.has_proctoring = request_data['has_proctoring']
            expertise.has_promo_clip = request_data['has_promo_clip']
            expertise.has_quality_checking = request_data['has_quality_checking']
            expertise.has_recommended_directions = request_data['has_recommended_directions']
            expertise.has_results = request_data['has_results']
            expertise.has_short_description = request_data['has_short_description']
            expertise.has_text_materials = request_data['has_text_materials']
            expertise.has_video = request_data['has_video']
            expertise.is_open = request_data['is_open']
            expertise.language = request_data['language']
            expertise.language_subtitles = request_data['language_subtitles']
            expertise.language_video = request_data['language_video']
            expertise.no_permission_of_owners = request_data['no_permission_of_owners']
            expertise.organizer = request_data['organizer']
            expertise.state = request_data['state']
            expertise.supervisor = request_data['supervisor']
            expertise.type = request_data['type']

            expertise.save()
            data = serialize('json', [expertise, ], use_natural_foreign_keys=True)
            struct = json.loads(data)[0]
            new_expertise = struct['fields']
            new_expertise['pk'] = struct['pk']
            return JsonResponse(new_expertise)
        except:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=500)


def TableCourseUpdate(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        course = Course.objects.get(pk=request_data['pk'])
        course.credits = request_data['credits']
        course.record_end_at = request_data['record_end_at']
        course.title = request_data['title']
        course.image = request_data['image']
        course.created_at = request_data['created_at']
        course.visitors_rating = request_data['visitors_rating']
        course.duration = request_data['duration']
        course.finished_at = request_data['finished_at']
        course.competences = request_data['competences']
        course.accreditation = request_data['accreditation']
        course.description = request_data['description']
        course.expert_rating_count = request_data['expert_rating_count']
        course.has_sertificate = request_data['has_sertificate']
        course.language = request_data['language']
        course.course_item_url = request_data['course_item_url']
        course.content = request_data['content']
        course.started_at = request_data['started_at']
        course.rating = request_data['rating']
        course.external_url = request_data['external_url']
        course.lectures_number = request_data['lectures_number']
        course.version = request_data['version']
        course.visitors_rating_count = request_data['visitors_rating_count']
        course.total_visitors_number = request_data['total_visitors_number']
        course.experts_rating = request_data['experts_rating']
        course.requirements = request_data['requirements']
        course.cabinet_course_url = request_data['cabinet_course_url']
        course.admin_email = request_data['admin_email']
        course.newest = request_data['newest']
        course.expert_account = request_data['expert_account']
        course.communication_owner = request_data['communication_owner']
        course.communication_platform = request_data['communication_platform']
        course.expertise_status = request_data['expertise_status']
        course.passport_status = request_data['passport_status']
        course.roo_status = request_data['roo_status']
        course.required_ratings_state = request_data['required_ratings_state']
        course.unforced_ratings_state = request_data['unforced_ratings_state']
        course.comment = request_data['comment']
        course.expert_access = request_data['expert_access']
        course.reg_data = request_data['reg_data']
        course.contacts = request_data['contacts']
        course.platform_responsible = request_data['platform_responsible']
        course.owner_responsible = request_data['owner_responsible']
        course.responsible_comment = request_data.get('responsible_comment', "")
        course.passport_responsible = request_data['passport_responsible']
        course.save()
        data = serialize('json', [course, ], use_natural_foreign_keys=True)
        struct = json.loads(data)[0]
        new_course = struct['fields']
        new_course['pk'] = struct['pk']
        return JsonResponse(new_course)


def get_active_tasks(request):
    if request.method == "POST":
        i = app.control.inspect()
        active_tasks = []
        for tasks in i.active().values():
            active_tasks += tasks
        return JsonResponse({"active_tasks": active_tasks})


def visible_columns_expertises(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == "POST":
        user.profile.expertise_columns = request.body
        user.save()
        return JsonResponse(json.dumps({"success": True}), safe=False)
    elif request.method == "GET":
        return JsonResponse(user.profile.expertise_columns, safe=False)
    else:
        return HttpResponse(json.dumps({}), content_type='application/json')


def visible_columns_courses(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == "POST":
        user.profile.courses_columns = request.body
        user.save()
        return JsonResponse(json.dumps({"success": True}), safe=False)
    elif request.method == "GET":
        return JsonResponse(user.profile.courses_columns, safe=False)
    else:
        return HttpResponse(json.dumps({}), content_type='application/json')


# def visible_columns_courses(request):
#     if request.method == "POST":
#         # request_data = json.loads(request.body)
#         user = User.objects.get(pk=request.user.id)
#         user.profile.courses_columns = request.body
#         user.save()
#         request_data = json.loads(request.body)
#         return JsonResponse(request_data, safe=False)
#     elif request.method == "GET":
#         user = User.objects.get(pk=request.user.id)
#         # user.profile.courses_columns = request.body
#         # return HttpResponse(, content_type='application/json')
#         return JsonResponse(user.profile.courses_columns, safe=False)
#     else:
#         return HttpResponse(json.dumps({}), content_type='application/json')

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
def expertises_edit(request):
    # context = dict()
    # return render(request, "roo/courses_edit.html", context)
    data = serialize('json', Expertise.objects.all(), use_natural_foreign_keys=True)
    return_data = []
    for course in json.loads(data):
        new_course = course['fields']
        new_course['pk'] = course['pk']
        return_data.append(new_course)
    return HttpResponse(json.dumps(return_data), content_type='application/json')


@roo_member_required
def expertises_list(request):
    context = dict()
    return render(request, "roo/expertises_edit.html", context)


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


class ExpertiseCreate(CreateView):
    model = Expertise
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = '/roo/close/'


class CourseCreate(CreateView):
    model = Course
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = '/roo/close/'


class TeacherCreate(CreateView):
    model = Teacher
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = '/roo/close/'


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
    # second_model = Course
    # second_form_class = CourseStatusLayout
    template_name_suffix = '_update_form'
    title = forms.CharField(disabled=True)
    # context_object_name = "expertise"
    # pk_url_kwarg = 'course__id'
    success_url = '/roo/close/'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print(kwargs, args)
        for attr, value in kwargs.items():
            setattr(self.object, attr, value)
            self.object.save()
        self.object.type = "0"
        return super(ExpertiseUpdate, self).post(request, *args, **kwargs)


class ExpertiseUpdate1(UpdateView):
    form_class = ExpertiseLayout
    model = Expertise
    template_name_suffix = '_update_form1'
