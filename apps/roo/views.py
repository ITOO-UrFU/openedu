# -*- coding: utf-8 -*-
import csv
import string

import re
import requests
from django import forms
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, CreateView
from django_tables2 import RequestConfig

from .decorators import roo_member_required
from .models import \
    CoursesTable, \
    Expertise, ExpertisesTable, \
    Expert, Teacher, SendedCourse
from .tasks import *

logger = logging.getLogger('celery_logging')


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
        exclude = ("in_archive", "identical",)


def merge(request, pk_1, pk_2):
    course1 = Course.objects.get(pk=pk_1)
    course2 = Course.objects.get(pk=pk_2)
    form1 = CourseForm(instance=course1)
    form2 = CourseForm(instance=course2)
    return render(request, "roo/merge.html", {"form1": form1, "form2": form2, "pk_1": pk_1, "pk_2": pk_2})


def some_view(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['roo_status', 'rating', 'duration', 'global_id', 'lectures_number', 'course_item_url', 'title',
         'communication_owner', 'expert_access', 'unapproved_changes', 'platform_responsible_comment', 'expert_account',
         'created_at', 'expert_rating_count', 'reg_data', 'total_visitors_number',
         'requirements', 'communication_platform', 'experts_rating', 'external_url', 'newest', 'competences',
         'contacts', 'finished_at', 'image', 'expertise_status', 'version', 'credits', 'has_sertificate', 'id',
         'platform_responsible', 'owner_responsible_comment', 'comment', 'passport_status',
         'language', 'visitors_rating', 'started_at', 'visitors_number', 'verified_cert', 'accreditation',
         'required_ratings_state', 'passport_responsible', 'record_end_at', 'unforced_ratings_state',
         'owner_responsible', 'description', 'content', 'cabinet_course_url', 'admin_email',
         'visitors_rating_count', 'partner', 'institution'])
    count = 0
    for course in Course.objects.all():
        try:
            courses_equal = Course.objects.filter(title=course.title, institution__title=course.institution.title,
                                                  partner__title=course.partner.title)
            if courses_equal.count() > 1:
                if courses_equal[0].global_id is not None and courses_equal[1].global_id is not None:
                    if courses_equal[0].global_id != courses_equal[1].global_id:
                        writer.writerow(
                            [courses_equal[0].roo_status, courses_equal[0].rating, courses_equal[0].duration,
                             courses_equal[0].global_id, courses_equal[0].lectures_number,
                             courses_equal[0].course_item_url, courses_equal[0].title,
                             courses_equal[0].communication_owner, courses_equal[0].expert_access,
                             courses_equal[0].unapproved_changes, courses_equal[0].platform_responsible_comment,
                             courses_equal[0].expert_account, courses_equal[0].created_at,
                             courses_equal[0].expert_rating_count, courses_equal[0].reg_data,
                             courses_equal[0].total_visitors_number,
                             courses_equal[0].requirements, courses_equal[0].communication_platform,
                             courses_equal[0].experts_rating, courses_equal[0].external_url, courses_equal[0].newest,
                             courses_equal[0].competences, courses_equal[0].contacts, courses_equal[0].finished_at,
                             courses_equal[0].image,
                             courses_equal[0].expertise_status, courses_equal[0].version, courses_equal[0].credits,
                             courses_equal[0].has_sertificate, courses_equal[0].id,
                             courses_equal[0].platform_responsible, courses_equal[0].owner_responsible_comment,
                             courses_equal[0].comment,
                             courses_equal[0].passport_status, courses_equal[0].language,
                             courses_equal[0].visitors_rating, courses_equal[0].started_at,
                             courses_equal[0].visitors_number, courses_equal[0].verified_cert,
                             courses_equal[0].accreditation, courses_equal[0].required_ratings_state,
                             courses_equal[0].passport_responsible, courses_equal[0].record_end_at,
                             courses_equal[0].unforced_ratings_state, courses_equal[0].owner_responsible,
                             courses_equal[0].description, courses_equal[0].content,
                             courses_equal[0].cabinet_course_url, courses_equal[0].admin_email,
                             courses_equal[0].visitors_rating_count, courses_equal[0].partner.title,
                             courses_equal[0].institution.title])
                        writer.writerow(
                            [courses_equal[1].roo_status, courses_equal[1].rating, courses_equal[1].duration,
                             courses_equal[1].global_id, courses_equal[1].lectures_number,
                             courses_equal[1].course_item_url, courses_equal[1].title,
                             courses_equal[1].communication_owner, courses_equal[1].expert_access,
                             courses_equal[1].unapproved_changes, courses_equal[1].platform_responsible_comment,
                             courses_equal[1].expert_account, courses_equal[1].created_at,
                             courses_equal[1].expert_rating_count, courses_equal[1].reg_data,
                             courses_equal[1].total_visitors_number,
                             courses_equal[1].requirements, courses_equal[1].communication_platform,
                             courses_equal[1].experts_rating, courses_equal[1].external_url, courses_equal[1].newest,
                             courses_equal[1].competences, courses_equal[1].contacts, courses_equal[1].finished_at,
                             courses_equal[1].image,
                             courses_equal[1].expertise_status, courses_equal[1].version, courses_equal[1].credits,
                             courses_equal[1].has_sertificate, courses_equal[1].id,
                             courses_equal[1].platform_responsible, courses_equal[1].owner_responsible_comment,
                             courses_equal[1].comment,
                             courses_equal[1].passport_status, courses_equal[1].language,
                             courses_equal[1].visitors_rating, courses_equal[1].started_at,
                             courses_equal[1].visitors_number, courses_equal[1].verified_cert,
                             courses_equal[1].accreditation, courses_equal[1].required_ratings_state,
                             courses_equal[1].passport_responsible, courses_equal[1].record_end_at,
                             courses_equal[1].unforced_ratings_state, courses_equal[1].owner_responsible,
                             courses_equal[1].description, courses_equal[1].content,
                             courses_equal[1].cabinet_course_url, courses_equal[1].admin_email,
                             courses_equal[1].visitors_rating_count, courses_equal[1].partner.title,
                             courses_equal[1].institution.title])
                        count += 1

        except:
            pass

    return response


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
    expertise_types = list(set(exel_expertise_types) & set(
        [et[1].lower() for et in
         Expertise.EX_TYPES]))  # оставляем в expertise_types только то, что ТОЧНО есть в EX_TYPES
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

        if not has_ex:
            _type = get_choises_id(e_type, Expertise.EX_TYPES)

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


def upload_comments(request):
    if request.method == "POST":
        courses = json.loads(request.POST.get("json_value", None))
        tbl = str.maketrans('', '', string.punctuation)
        course_count = 0
        sum = 0
        for course in courses:
            course_exsist = False
            print(course_count, "/", sum)
            for our_course in Course.objects.all():
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

                    expertise_count += 1
                    print('ОК:', expertise_count)
                    break

            if course_exist:
                pass
                # print(expertise_count, ' !')
            else:
                print('КУРСА НЕТУ!!!!!', expertise['course_title'])
                not_found_count += 1

        print('Курсов не найдено: ', not_found_count)
        return render(request, 'roo/upload_from_json.html')
    else:
        return render(request, 'roo/upload_from_json.html')


def upload_from_json(request):
    if request.method == 'POST':
        courses = json.loads(request.POST.get("json_value", None))
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
        context["courses_count"] = Course.objects.filter(in_archive=False).count()
        context["passport"] = Course.get_passport_responsibles()
        context["expertises_count"] = Expertise.objects.filter(type="0").count()
        context["main_expertise_count"] = Expertise.main_expertise_count()
        context["owners_count"] = Owner.objects.all().count()
        context["need_admin_owner"] = Course.objects.filter(communication_owner="2").count()
        context["need_platform_owner"] = Course.objects.filter(communication_platform="2").count()
        context["has_access_count"] = Course.objects.filter(expert_access="2").count()

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


def course_json(request, course_id):
    def clean_empty(d):
        print(type(d), d)
        if not isinstance(d, (dict, list)):
            return d
        if isinstance(d, list):
            return [v for v in (clean_empty(v) for v in d) if v]

        return {k: v for k, v in ((k, clean_empty(v)) for k, v in d.items()) if v}

    if request.method == "GET":
        course = Course.objects.get(pk=course_id)
        data = serialize('json', [course, ])
        struct = json.loads(data)[0]

        new_course = struct['fields']
        new_course['institution'] = Owner.objects.get(pk=new_course['institution']).global_id
        new_course['partner'] = Platform.objects.get(pk=new_course['partner']).global_id
        try:
            new_course['lectures'] = int(new_course['lectures_number'])
        except:
            pass
        if new_course['has_sertificate'] == "1":
            new_course['cert'] = True
        else:
            new_course['cert'] = False
        new_course["promo_url"] = ""
        new_course["promo_lang"] = ""
        new_course["subtitles_lang"] = ""
        new_course["estimation_tools"] = new_course["evaluation_tools_text"]
        new_course["proctoring_service"] = ""
        new_course["sessionid"] = ""

        new_course["enrollment_finished_at"] = new_course["record_end_at"]

        new_course['teachers'] = [{"image": x.image, "display_name": x.title, "description": x.description} for x in Teacher.objects.filter(pk__in=new_course['teachers'])]

        new_course['duration'] = {"code": "week", "value": int(new_course["duration"])}
        new_course['direction'] = [x.code for x in Direction.objects.filter(pk__in=new_course['directions'])]

        new_course['business_version'] = new_course["version"]
        del new_course['directions']
        del new_course['lectures_number']

        new_course['pk'] = struct['pk']

        passport = {"partnerId": new_course['partner'], "package": {"items": [new_course]}}
        passport = clean_empty(passport)

        if "promo_url" not in passport["package"]["items"][0].keys():
            passport["package"]["items"][0]["promo_url"] = ""
        if "promo_lang" not in passport["package"]["items"][0].keys():
            passport["package"]["items"][0]["promo_lang"] = passport["package"]["items"][0]["language"]
        if "subtitles_lang" not in passport["package"]["items"][0].keys():
            passport["package"]["items"][0]["subtitles_lang"] = ""
        if "proctoring_service" not in passport["package"]["items"][0].keys():
            passport["package"]["items"][0]["proctoring_service"] = ""
        if "sessionid" not in passport["package"]["items"][0].keys():
            passport["package"]["items"][0]["sessionid"] = ""

        try:
            passport["package"]["items"][0]["id"] = passport["package"]["items"][0]["global_id"]
        except:
            pass

        return JsonResponse(passport)


def expertises_json(request):
    if request.method == "GET":
        c_gids = ['54cedbec1bc74b4692ce968bde4e7cab', 'f950523f1b7447a984f442b5b1d20a97', 'c59203e806a94ca89d1eef5298653446', 'eb16df4b1c7c40b1802b069c123f60ce', 'd76e32a0fc0b40c5b90f89d88e8f7261', '1cc7fb72fc5d4ff6b2c4136ffd2fdbc0', '5fa492f65cdb4813822cd48f9f9d3de3',
                  '5f307bf4a8424f1491b85624cf71949a', '56001ace5efb41ea96b983121f26d194', '464d8ad728f446fbbe2865e698bc457e', 'ce5e5742362f48d38611d331f860ea08', '9cdf5794df574847908fafd4812dc0dd', 'd688e7182f8645d1aad368903f6a287e', '6adb8ae0aa9644c8b789c8740ab1fadb',
                  'f4b81135326a415786fcc37192b516e8', 'd48062b26c5c46bfb0abe727f29af74a', '74c256107eda4bd0a670ef503d0d7d32', '4b317b3fad484010a9415acf21c1b121', '728a44f3922d4bee85981e8ecb0145a7', 'ed0e1d77568a4fc6a81f94e6912a571f', 'a231e7dc2e184fceb04f7a65ae948859',
                  'b26956200cca4cb4a133bfc9e26d911b', '49937ba140df47528073f0e551e31d14', '042213cb37be4a54a8522aea432e6775', '469a2dae1af041b3947c4ed0581ab4e9', '3e784fb0cbe74168a1c9307f2fa74a73', '90b14a6d233340bab8f9b6e9ada274b0', 'b350525d40fd4e3d950cb3ede860f5f0',
                  '37a4677c19eb43bbb6de21af101d2d70', '0771aa02b35646d7a3dff6e7a279baa2', 'f250b078e6d344a8ae56eeecd3f6b176', '98bd18387f8540989502e5a41c8cefac', 'fefe45a212da4fb9a309c0eee8958b4d', '7b66792acd824baf8e1c18aaa90141c1', '86dd41fcdd074d2292c6d4330781b66f',
                  'a503a32fa4df4da481b3b108eaa44701', 'b35b77304ec743e59cb45d9b87a819ab', '9d9073657f8e40918b70fb01449cd713', '2a2ec19482174e3fbebe4912c6d0109b', '8684625269124ce191d5bcc1160fbfa7', '9f558a98f77a43399c42b77f743b4fd0', 'b80ee632ac8c44eb96fdc8185dfb4cf8',
                  '973650441830496a94b4cd5471fa4aa0', '32769bb651114ffab413c3d8c84a3703', 'd5db1abdde3648a3966f4a0a4429afae', 'dd3734bf277140088384877e327c4e4b', '58858076b5734191a80cd58ff99bc573', 'b7b48de851a24683902fedef01f70fc3', '2235641f09354079830f2b2a5f7498cc',
                  '74529676f27a47bd98848d4ad64a29f7', '9b5ba1e9914f4449a5aba4b576abf75b', 'ec7c9d69f5184bda8f953281efc94629', '30c878ee28124870bcb1126bbde364ed', 'eed9004ce23b4504961e50c4100638ed', 'eca059566c3d4d7ba9295680dde1052a', 'b67f5c7d43704ba8a8dc1c62fa6e127b',
                  '36448bcc4ae84accabaf36fa7c4cb818', 'f12e11485cd64c46b8dba0d930052b90', '496e7ed339474c57bcc906726351de47', '98d460c5c22e4467955038900e13c258', '0ca3e2c8ad684761a8259ccad383758e', '78363147332548859dd0674b7a873a39', 'a2a3391e55dc4857a32460a81a8276bf',
                  '0639b7a7e9f54d3abf0bce734c4c9867', '24e7c87a41024be1bc757bec4f0121a2', '1a2012cda5df4fc4853e8441c2f68256', 'a50d8732632546ad9e60d4e029b59ca3', '9280c599f86c4d4f91967e2fcc5b719c', '9c4a56350489498e8972fa502d3b5f7e', '2a63467ad23446008e8a7eb9ca942887',
                  '395e41f1663d4bfeadacd3f52f464e70', '8d79a724304042d49198eeeb3bb94282', '9b274cfa16fa44ddbb7e350baa13e96f', '4a0f3b02a0d84110b1924c9119889122', '4d3d55134ede4fe281497425c8b783e8', 'd060d169db9a4c999e15482c412350a0', 'e2d945ec777748b0ae01ce3080eeff0d',
                  'f99684712704446eb612a3f3b27f6f80', 'dedf51f21e8d482aa625fd0218744e3f', '657c4d004db54df0af3a11db7f1be942', 'a7b9ce82076b48978173eac29253ce39', '681d83abb3724fdf839a066448108d6a', '74789a6b19064aaba886de625feb2a3e', '69723ad7db3e4dc0a31666c8cb09773f',
                  '2d60ddcfaf4b4257b57bc774ed37559e', '881e8daf55644bcd9e13f5ee97773444', '04f4c791c7db499c9b198daed4d9444d', '6c1c700aff4c42a388c7917a12e90f29', 'e6bde89b7e0e408caf5de5c0fd5cf9c8', '1751ef82e73d4134b42f85ac13c9e45f', '9117d4dd1136455da6c7b6e56fe06c75',
                  'd1c95ac3dcf84d34aa2581db235470ca', '19b310c84cc24fdea73695bc2751dc63', '8efe9278283c434386653c62ed6c2b93', '62b85607081649d69bd30ea5e787cadd', 'dfe7a9cc08c54ad7bb01cf345e70590b', 'dafbd3b640a04c6990164edc20285b5c', '8da7e83c8d7a4cf0b248de19a19befca',
                  '0f359bf1f6cf487db28fa724407e116e', '7240900f798a4dcf8759df89e31a8ef4', 'e59ecec52cbb4ffcbcd631d68e03d8b0', '9cb38573a734456a9f4b3f33a3160738', '0b249d17f9d8471c94a774618ed361e0', '228d62fe27554023bfde97ec4ae36cae', 'aa975459acce4d6f80b28b7e8bcdf57c',
                  '8c55aeb5daee4087bd761135f93877ab', 'd02464077d5a4a1c9c93798074956f13', '900784df966543be8155bab4cc243264', '15658ced27bb46c499d248b541bd0925', 'f9c778ffb88244cda5e15a00e01d78f8', '6d5f2593ad6c42b9824ce276dfe5ecaa', 'f004751f4c9b41f2bedd575585712338',
                  'd3e6d7b09a2f47fea3f758bb2f6edf78', '47559574c3e44132a1cd19ee3d86116c', '14731ec028b44731b266598509db61a0', 'd184937530a34b60b55459e84268bde3', 'c2bd6e61363f45faadbd249a36522155', '9dd9a07303ac4fe69b1938738094ec61', '74f9f3d56cca45b693c31f3c3f7fc335',
                  '0d1effc1a0014b2eb2eb5ba115a0bbfc', 'a85ed7be4bbf4250bed2d4422b2730a4', '990e3bf195294aa5b0db8f82a8c476a7', '25f2c7c2483346a2bdd71e0c916bde23', 'e022b308b76540ea99833463151e6951', '9984d0231c4948fcb5015cf928ef9200', '99eabf33e9834b1fb9ae4066758b74e5',
                  'e1456df7d6e34301bb891839580d0cac', '559bd7f39e574feb9fffc9ec997e4f42', 'bb01b2087ae746f99596a59fbc2c8671', '55e454c1f88a4ff0a3d9e80dca03c59c', '66e0d7629d3a46d4b2d89797c7a68b13', 'af9c332206144da7be5e8e7a8df538d4', '2a4f5bcc89364f0ab92a3202283572b9',
                  '56f6f48a3ba442838456bc0c74ab43b9', '5cdd7a82d0d2446cab9d090a8a92f2c8', '10abd639159b4037b1b3df624fadceb9', '9bcc6c3ddf3e4a0c89b6068493960bcf', 'c8a55225360c4c3094af5018da6820a6', '5bde4ffc65db4dcd8568c0f6703e12e9', '7170466edc4c481fb49406798363ca3f',
                  '638ff324c2ff4d1a8dff94ebad7b8f80', '4ae6696b0d1440329e644e963f0169f3', 'c6c05d44139e4136a8950d2f4b8d3303', '02b137969fc24e37ba8dbc233962317a', '6a4ef7afa5f042dc9076867b28607799', '85a15d278a654ef78dedb1ed4e8d1f90', '85b88a55e6324921854d5564628246b7',
                  '5baf3d6261dd44288a71fefd67082c56', 'ca1f603ea4704f34a6b3e2d201aacea0', '623b023fad6740e3bc2924619c1e05dc', '4d111c840e0b4b7788a7b0a6b925a30a', '21579f4674d7481aabe6be624dd19c68', '277b1305a5934f45953d909aee63ac9c', '85ea98bce48c439eb3309f3a763d4862',
                  '8de7edb3cb994e95892995b564484b2a', 'a11355a5d2f4481788106943db3b1442', '95f2591afbff464099f1f5ed05ed6933', '0117d5f381774035a6cb19ef16f69d06', '30c31efec9cb4850b96ded50e77ddd63', 'b46be2ef8403457db9d7a15a9b499704', '5baf88689b864d66af97d96645cecab1',
                  '097dd26a5e244d3c9d96eaf5e957a5e6', '6dad1866c5c94c2a8db4e8ace60de6d0', '6283e1a7ac4b450baa43502fa54914de', 'b89a7e18e78f41a29c5ebb1d5535796a', '8157298952274e428d93c0535b58c03b', '2e11d05a06f843dfa78affc777c5f1d2', '980016d3c7c9493e93cf5083993e661b',
                  '45b2f558102b4be8a9cba0fadfe74e82', 'e73d57c262364c39b333c4854d29d801', '6f089ecebe2a4a5496b686a993362d1f', 'd9ef8853d15d4b0fa123d39b1d9ffa65', '628c8db5aeb848bf94ebbcd812a69015', 'c6ed2668b5eb4847a4ea0a230faa995c', 'e528c1fe76784e94aaa29069e0ab2589',
                  '8524b40533da473cbb0eea6bb583844b', 'a67fe1e9b1494e7a85127eddfa693203', '46a8b5aa419241288283255394ab4a28', '109d3ac49ea2402989561ed8b20d2c94', '4a3ce800f3fe4b21ac9d9a76a6680bb3', '50c9e03162bf4b94884c0ddfdb878d94', '1038bfdf79fe48459aeb915c46225b6f',
                  'fda99ff4640e449faaedbccd9efa6e7d', '9f23f8f88ca74e47b7cf34d9c66723e5', '2ed7e3b23be740c38c7958a4ca2aa0a5', '93775622bfb64275a72a824a1da2cf45', '440bc63f2354417094dfac03d0be20df', '70eb2b6e4fb14ee9b0d417b54b0436ff', '7e5fd714dc0549a3b064db8b5fc25e03',
                  '0f9d3920e38e419a9f63b725fab9c50f', '5f6030789bfc467885127ca9da5f5c5f', 'a65f313a3b734446be8fbeb09cd28a0a', 'c4b601380f014786b2996baf7678a354', '45afb4aa912c450aac8972a11ba40029', 'f8ae2a3a199445efaa2e8f7e852b4473', 'b88910b07eef49b0a5418c73ff919251',
                  '48250a3f54b141a289f166eb74b58bf7', 'f987d04ae86545dda14ca686c1b482aa', '1025d7e1ee404b09bdfe313d122e8d0d', '05ffccddbd404308b4f1010669d9faa9', '0abb44f12e124cd4b141fdb39ed6567e', '00177e6a85f24e1e9629946c27ed188d', 'dcbbd731317746a8af9bde14118f252b',
                  'd5a67207b7a6430190af75572b70a3ea', '24d9ff8a0eec4cce9882d71f506e0bad', '45c9740a0d2e4a42bc24384c16075a3e', 'a8fc8d3f06ce407ebb831ae97514ce66', 'f2a79364e07448ac8602cb09581d688d', '96e6d9c8569c4dfca08fad366c461132', 'e21def87309844c886841696a7238208',
                  'ba6f579fb9254d44a22ad9a0a0af1583', '6f369faf99a64c3683eafebf32acaa8e', 'dbb7898072874540944021176102a7be', '2163ec2dee0c47e1877b58315162b01f', '43b7e702a5c941088c9b72b67eca17bd', '5a2fb75a07e44bf693163cafebd4f4cc', '73390130c6164fa2b960d6fb8a145529',
                  '34d0058b4ba647529d738425055a26aa', '6b8c835f4d0440c599ddfe7dd1ba7e7c', '0f381f986d974c17b4b031f058d0c45d', 'd1c0bdd81efa4885a0ac3023ef6d5ea4', '363beb7ace2a48078181a8bf44f9fe26', '65c17fa3d9a147d79dad768bfbbf2c77', '4f468f24100e4ebdbafcece1822840d5',
                  '6c35932dc58f46c68db5c480fd0b2e08', '1775cd4ee40640cb9be4bcf25ffb388a', '796ff4160216415aa7f7f0d0e583d65d', '06964fc46eb74134ab203e4123a53e27', '380186880836473281ab016df771a6ed', 'd3ebb605cb9b4f219ea324b642a8ac2a', 'e1bd32ef3e464725aa9b279cdd22a6bb',
                  'f7af534f21294566bf3cde1511e57f54', 'cef8fa55d9a04699bbd72a7f14ebda96', 'eaf578e3235b452fa4d3db1e465ed7a8', '5315d17c2add47688dd9bd22bf777f95', 'e2892104f22d4f55ab113726b0398726', 'd38ed28e708c4f35a4be13dbddb571f4', 'c054b4eecb56470491ebee2718b8718d',
                  '6bd9208c2c5a4fc288c1725ad028aac2', 'e424a7ba36dc41b0a838b1c10c04230c', '814124ff90e145e1885cf5fa335f71c3', '1a1c2da40b894b3d9d65a5fe9789eb02', '9ed4660d7d4543838663528d93040de7', '23fcf22855df42d0a6cf6ac67f45b950', 'd05e60585d924933844a32fef5a1afb8',
                  'f2181bbbf0be4d0fb3f032981f4076d4', 'e584fbae2eca4c3485f21639db8ce793', 'f17d3fe201044003a3f836b1f30df2ef', '9c09003d55704e06b59e132f187a9f7c', '8b94785cb31e4878bb09eb2ee846c6b8', 'efd983ecabce497192ce88721234bfa7', 'f2843f43fdb14197a4fa030585bc23f1',
                  '35842500476e42158e84f9fe18983e40', '1cb1c36ad082483a80c46b4a08b5f2a0', '2a5010c43b30495d875ecc0e247383e3', '7f8f03eba48a4fcba076b7a5581cb767', '2d87bab8716c49f58ad5aa40e5c2632d', 'e2dfbfe5967843c3a961287ed1be451f', 'dd3d68c27e26444fa9955e3741b0683e',
                  'd3a4a9afb8c14e8c92a75a5c5ac795d0', 'e392cee693a84da698744cb84f970ab6', '563244b550df4978bfe5615a675db01d', '515e1e894d4d47809b453f68d0c34b4f', '899d2d420c5c4d67b6a30effe3f7d975', 'ad413061efaf4477a4574e7d825201a1', '26ddb723f886449aa6ab35903712dd71',
                  '7d43113cfe724994989c74b254aa0077', 'c623f71d72ea46139f3ed1781d2b6d23', 'd2456101698d4a5a8ea7281a5079a54e', '5bf7741b627146c695754be07e6eaeda', '129bea6f9b8d437f862be0da5a915533', '1680aa664f604a96b0938580c36750b9', '1577f5bee3d84de7b6f11dcae66a32a6',
                  'e95bc4a04e5249e6b30fe982a7142963', '00cd5688e22f4ce880dcacee1cde5340', 'fcbbdf62212d4393aa8b64e13e7e8395', '3633e0603376497aafb9c148d7694bcc', '27974062499847ceb7d4dd01310f9b6e', '1c77c7e47c424475bd762a793bdf6d70', 'b441eb525fcd41c784ca615db8ae9097',
                  '35f65024aa8a4681a467fa7e918fb119', '88b32693f23846aa98095f6eaf3c37fc', '2dfdf11829f04f949dc3165e3bf7d57f', 'e374254e06314d5c9caea9ec885cde9a', '8dad42567b3b4483b00d689b5d97a725', '189662d6454a4f078d5d3cc7c5b2506c', '9e22fec368634fa080151e12e9b5673e',
                  'd45962f58a4f441b8bf11f8d200509eb', '99f03ba188d14a8fadb66f87a774a6d4', '591db00e3e3046689ed5fbe1f6f40775', '0cc67ab9076d4c58b46d6ccbd4f2b173', '357aa0d475554de5bad30f9371e21443', '6fb7371ff096467a946496113192f894', 'df9351942ed94faeaf20fa6f25a78e10',
                  'd352d89a4ab147a393befadcb0b6299f', 'bbe361db1391487bb27481c15abcefd9', '56feda8b6b0042f2acbbf865cf8a05a9', '06594b2dd8ef45c6813667d6ed0e2492', 'aa77749c58624c338506b34cb102563c', 'd9392a73dfbb44ca810eaab373ca522f', 'd97f51e3be934d7780dcf5c0bd189437',
                  '60ca51288d6d481d8addeca7b19cfd6a', '7c2876eaee97415b8c4d2bcf5eb9a2d4', '661d1791b0dc435ba948be8aa1f87293', 'c377143a12e24788ad14ce20aa7b01b4', '775667b654ab4f2f98ba7b169053ac33', 'e2046c29e80c40fd8f6f622f9ba8476d', 'fea7cfff5b9c430abdc80b44b9d590b2',
                  '90340ab2693b42f0a37630a6fb851eb6', 'a202d4d857fd4ca3a719efd0e79050ef', 'b5fe26af4e9f4024b44222e300d8e60d', 'd313d5964fc643d5a9dbcbcf94bf5724', 'b49d25aae6154651a8efc6969ece3dea', 'b7794e5624a24c6fbc214740f149ea04', '091edff652c0410db4eafae5c2085abf',
                  'dd2b8360694c4c089a43bba35093b8b0', '13043aa645b54af7aec124e4589d13f6', 'eb44534b8caf44448bb327455b943240', 'a16a27c464884f4eac62cf57658b73f1', '4a4328b59d1c43e9bf18ad21fb37b626', '5158938bc78943c69c08470cd246e8e0', '9efd472cb1454cb7928c3ac82f94fdcc',
                  '450ad4d3cf9b4af7a94b0c286add744c', '7f952ca0109a4b33a3dd79a127c44eb8', '5d6557fb2e294c2cadfc443fde15f2e9', '39fb78f4416e4971bf3f5312d45796ff', 'efea5313e4354892902722862af07de6', 'f0288c184cb74b67a34c1243a7f5d1b8', '79aef8e5a50d44a89742d41a1125d9dc',
                  'a67ae631dd114745a87e908b9edb62b1', 'af1cf853a14646a8a9675aca9bf8d15b', '94fc624b69664a17856f6fb219123e16', '6c618bda370b4677845cc9a40a3887da', 'ae00a65eb81a4c518165cb9f1230f6de', '02d016c93d514cde99317a3a471246aa', 'fa01d1bf99b8478b88a716281b080f7c',
                  '3b02b88d5a6c4bb79db51b2f1db69add', 'dbb42b3e2e924c4d8fac6459af77c943', 'c8e96bdf06384d89bed351dbe7534626', 'e11975d79364490489ba0fc3cdf2bda3', 'f312c0852a3e4bfcbcdaa55ade2716e3', '38da403c34c444c3bb747ba32c7e21a1', 'c8933c0b098f4f0d817eed05a143e166',
                  'a1dfc265441b4967ae550666e0e7f8ea', '14690f6e1c124970a9091fa9ae48988d', 'f733acc8711e4556b3f9b7bf57925ce3', '5f509b62d80b415d8278ac03759a7999', 'cf8924e8b4ab4fc29f3b327f853c831d', '9868912c06624b5dafcb9ecb8c0e03ae', 'ecaaf31042e0428ebdd6bd0c26e39a35',
                  '6edf615205a740bd8dfcef8323800228', '3b271d9c6f19482885dc7a83033acab8', '8d0c41cd5f814e0ea1a46569b7822866', '23e66670998c424588cdac806ce955ca', '6782e4f7b4b940fabb7f9ecbc42edf56', 'b30b51086d634dce9a4b6de3f53e1a28', '90595095083f41918455810a8c6b8474',
                  '7997bc94b8d84fa6a756e0e08319960a', 'f6ab7b90f45642c4816f2ccc89e29753', '52bd793bd5db40f1b98380468c1587df', '2c561e598d6f47b88147cc1f1f35620e', '9cb2b2ab727e42f7b2b14665f7ce0df1', 'eb76cd582449429fa2763d5fcc8785b0', '70c49a0bd9374f3f844ac67d645557de',
                  '6f2cf0afc2f84524b6355e1b574952a9', 'c604e0ec9c884118bfa13870e35785ac', 'b7ce81acb50947ac89d5a14dbf5c8df8', '749976a5f3b7444898794f1f185e8252', '5e579a07ab1b4fab911752942e6c515e', 'd50809d091634d57ae97b9d561fa679d', '8455f3856a0b49569cd7f48bb884d47d',
                  'fef5768da0764828bf4d10ddbabaceea', '50bc2a4ff3994233b7bf320c6c5df6de', '1e1a5daecff1441484b923b371ac9731', '83c1cb71a0c14e69b124c756e6b0491f', '9215ac24d596467d881b780b5a90ffa6', '338b70062a754ba19cc41897ef998c4f', 'f830b86495ef4f7aab25282c990fb896',
                  'c7ca1aa8cc30458e92e48ac3dda52122', '5ad3b313762f43398722646621406f79', 'b3491b09e602476e94ba51af546d04b7', 'c9411c4f2eae485b8e7a22173063bb69', '5cf67ae7714945e6935e5a018ad7dc5a', '6e0d3a698b5c493b861089d67848a3eb', 'cc2806270e474026a17c5cfa4b6f8feb',
                  '9969e24d54284fcf9c822c379b900c88', 'ca456765902a464682462ef2486c3fc1', 'd42dfc07c0e94f3ebd57bfbaefc4b1e3', 'e2d49be68e064d5dbe04e66c99735890', 'cbe14f6c90db4cbdafb8e2e72c1227cd', '4615b6fb9a29463bb66784a52df0edff', '47d56fcd28c24d818bb4c39662a1d5ad',
                  '1cab833914b84ab5a3db7437524fe302', '30e07d369b1044cc8f3051fca6e5b7bb', '98a2202f222e49c282df071bb45524ca', '45d16a9d191341e38b4f7839602663d5', '4df6bbb72d834817a78a5b63a5c2a4ec', 'f2414d2577344ccda8f815023c08f343', 'd9a9c1a8bd374803b880de4cdfbe3ea2',
                  'ef4160918a124433b273a3903e988d08', '8b44beb737e34fca9f7eba37586f997c', 'd2452d7ada774cf6b1ca8c94b9b3f39e', '13a64f9f9ba640f0879486bc765b518d', 'bfd5605cd8844aa99498d5be73aa2722', 'a8ca4f85e9294d00905c89d94b96d97e', '1e455f31470a4d8e9744a11bb3fbf0b3',
                  '228abf75fecb481e929dbcecef685836', '3a89570c3a914ea9a4bfbf26c7f8181c', '473c70f6d4c844d9b9667147c4f3dd32', '6afc2ca0d9fb44a194a65db5c326148b', '4d083c15bcc8483d82800f9ff143c902', '8514bc6b541d4a33b94cb14456f4afbe', 'daeee19fcd8e42eb9230b6b12b873344',
                  '0dff432111f440fda2eae9798593e78a', '30b00013440643b5b3306abd4ca36850', '5774a89f313a46f3bbaed9220ca7bbec', '31b7cd412cde4b409df113858a07aa85', '23f51539441c440a95ccca1b7ba0d3db', '3aa7380862bc458ab8828b01a878d9f0', 'bae17302dab94214b79639abb14cafb2',
                  '6fce86aef87e45a9a1ee5c48ea3bf93e', 'c7bc157106ab4e71bc9d7797c4248472', 'ed32e9f5bebd425bb3e8080db7a0d67c', 'd706f36ed133445399b18c59473ba276', '0cf4c3168c7745feab12d15267f6c1f2', '789944358f504615af86cfa61ec85069', 'de7ac604a82c422baff5c787b5b1dad1',
                  '7bc81e7a9b1a44d7a2b130a6fd051c4e', 'f1247c5c8fdd4692a582d14dd76aa3d5', '90dda2ce37844e88ae34548293912413', 'e06889e066074efbb32a19f1766696ac', '9c3d4c1d091544f188017af421009f63', '463ab7e8d52746749d9c8505d7a50ba3', 'f34913a2b3d64c5b87371518be6fc093',
                  '79325aa75ac242cf9a210507de4acdaa', '7af6ad7e45e142269b1af0cd38689644', '8009924a30ef477399c4800a1e329002', '9b6396a9825b4f21903cdba7edc342ce', 'fbb1c8fb1436443aa98a41f5914b18b4', 'd0764070711c4667b19c87e6de2d61d3', '42291cba4d3a4c24b7ffd55ce9ab08e2',
                  'e00acfe0a0804cc0bd3c65d3903aae97', 'b2533f985f134a079c8ce55aa463d860', 'ac4758f75f96494ab8ca5af573538e88', '0bd040968572474397e659c6ae804749', '84f39d327d4f4d29a6adc6eab21b6f92', '30f427c4162e465aba023183f90922aa', 'd1a3818046364dd386bcd7b372503a3d',
                  'eafea300bda64e6fa36e7a2e39351155', '549c5c837fd343f6b8ec5e724e444dcb', 'afa6f5cb54c0431cbf867c1aa6ea0f8f', '6c0252d98dd040eebc56261e785d70f7', 'c7899b7bca8d471bab58339baa4c0eed', 'ed73a00146a74685a1b3f733cda385db', '5c944638e0a84cf091dc32ef7ed3430f',
                  'e9f7873ce899484a809f05470d6c0cd5', 'c39bead54fe746fca4bdadf69225dd59', '1a9029ff1da44eeebc06f47d6346e878', '9a8cd851d3394549bf0f160ea1e23d17', 'dabf06c7ae494e789a48f878df6b1dc0', 'e91c7aaa8c9a424387f72bca298c15e2', '41c2de14f8ab4f83a3f65ce343c8de2e',
                  '4e9ac8e52a5246a38e61eafebcd11dfc', '1fb0bb79a9584546b119751d2a72f357', '9b23b628be6e468086cab7f48ac21c80', '340559f175124147a500c54abdcb728f', '2933d136ca1e49709add419465f0d534', 'e156da8d18df4245ac37bbca5042e695', '34be1308153943ffa5757bcb7969fe7e',
                  'f77e8d61254746719ab158808ff92c2e', '99be219839ad458bb9d966be273e0bf2', '6b33aad0e9ec428f86e8fa6921a5fe5d', '6e17171e35374e98bda3237cdbe9a5c4', '06746414270d49bc814922731f0bd87d', 'e0d0e441db884b4c8248a183d4c317a4', '70c85996710e43a0b6017bf00027c2fa',
                  '0b1b54020a9342ef86cd6e59cd2b628d', 'd5224221ec724a1eb77409aa061cb9c7', '41688132ddd74db391ab5ab7df14886f', '6809a6e481254740b6361c81082072cd', 'd0b39b0ee0c74a81be94093178f0c1c7', '3b2206f101c54a77a90b6fdb03a5e1e8', '37394beded9d42bfa97dcf62244c4a81',
                  '670220d6099448e3bb3f158f526aeebd', 'ff7ab84989124559861860da89c37cd9', 'cb16f57ed7fb4646b49205973ab0d647', '1870e392aecd49829b3eafdad34246d9', '4c4a5e8a53644f24b2a807d4cfaa13b4', '8ad0ee039c41463f9158497c29a787e2', 'c7f73f3114954a75a7c23d3b55658931',
                  '17bf425a3a5a47fb877b4aed0325996e', '4472f6dfad434922ae42aa77aa4e7f42', '8303c095687344f38078e3c15ec630b2', '3a10c4fea6064ef798195d43d0407772', '2162fb056d9e44c5a3bfc9b7a249f174', '571fe58f5c114cc593121bb6a963642d', '09ac1c10250d41d99181a5a97d3d43fb',
                  '0f1481c4cc764afbaed20c8e804b74bc', 'e54cf24f7b02488ea69589c00220cd8b', 'd24f80c5b5b541c387864c581abf8893', '294377be6ef54cb881a0f1bdcf5f8c30', 'cbcd1d9f61184e089e3aefc7a9ff61d7', 'e8fead4c20bc4ccfa9b6d3cbd169484c', '0afedd6129b3451bb09e18daec9d2a33',
                  'a0086da8acc041b7bbc659bc13a560bd', '77b26d36f86d4ad29fb935c43a808f64', 'a2119d059f71439684aff7761b771b84', '5fb8708ada21494781c2f2b33be30358', '2d89940e2e5d45e8b5307326cfee6e11', '211fbaa526bd4745b5b5754cd2e4299e', '695f03fe12224f32adb5a5ff23ce0863',
                  'a5e3c421fe5e42728f132dec96688744', '0d4552b1636a4e5190fef0ac68aa9824', 'f6e6d6c3134d4c28abebbe3434f86ffa', 'fb403fa0c5244b28b28717e20a18253a', '19d6c71f00be4f73a81ecb80bb4e8214', '6a0e57e8c139469c89ba3b28897f9203', '83461e7e71134ac0a150fa41267d9c8d',
                  '53c64fee24764ca8b57176471776b087', '47d896a1c579467f9fcb021654ac15b5', '232c6c5e1b394921a58e968c4c01ba55', '31f2bb7c56e44d10bc60cdf08a2a5731', 'c4fb1b6ad2be4062a3f6766ae5eff3a2', '5c9b9f73da5b4668bdfec4b2db56ae59', '0a5a110a8b964203aff86d2fa26b2f06',
                  '2d2d3ee1214d404dbc9a3fb45ae336ad', 'f231e01e7d734ebfa1e2e01913b5ae5b', '8e666677e8374bbb858abd09ffa540b8', 'd854867a2a814a86bfb0109c879444b2', '1327e78f5f7e4a94b53bf279dfcc5ee4', '5d9b1eb30f4d4989a6289e9567696638', 'f283332e642b48d5b8d0a8a4efd95fbe',
                  'a110ed7964d8487e96822df214dd6d63', '19b1f7edfaf14699a4825a488fdbcbab', '73a5255a3cca4d579fe414d7147788a8', '807627fff4924068bd9b6e12f52e3039', 'f9a605aeaa414cfba3279be30093e754', 'd9923cd46d65491faa5a3b99bac39342', '731ef44564f549f9a5a0f17dc5bdb1bc',
                  'f2d1fe42e9a945ac93337f7b59879a7f', '7701d15d4d7b45ba973513097d2008ee', '06fb8f49c6114e81974a443a42366286', '2592a9fcd03645d3a3ac8b21cca06d35', '1a6bc5d530464d3d9a4d3ca738d8771c', '22ca2c9cb3df4864a5ef43059b18ca7f', '60a7f4c105c24c429455942a3741d7d0',
                  'f45ead96dd1c43feab3913689a01b5cc', '2e3bbe7167604798b880c2073c4c2d18', '9b2c49854b004e23b28a8560583fcc08', '3a6f9d4d321a4b479ad1921918734661', '65915282e6e540688534c9428bfd44e1', '04ad092a3e344c9480ed2cfac5dc160c', '9bed64621fd6418eb735bbdeca97dca5',
                  '32e7cbf29e6c4583bb588201f43e30ad', 'fe64f4cfb5fd4e99829946b61ec10da3', 'e83f5efdb70441fd8e3816a4044b10d0', '6b30dacfd6a74bcd8c93c7462d9e30e2', '658e9f52ef6547869f494b6592ea4af6', '6da52cdc67464309a955bc40e9bd6652', '4ac7c41773104bc38cf33fa2ebc6f823',
                  '199a62ae08724f579bd590e6982f14ba', 'aa4781a7ba844750aab8bb200c3b3c10', '8e7003c261494ef4af3639d9935c5e3f', '452c6f5e137c4890825e3ae88346188e', '931784aa3e81459580b33d9c3d3656df', '52e510ba0ba34a18a6726389873bd710', '8ec3b088d0a04935b712b925be697be4',
                  'bbe51470acc24c8d827b31facdc562d6', '4e9c5ba9671a4d1e8f4f7521dfa5a6af', '46f1084b23ec48e99530e52bef413ef8', 'df1e2609689c47b8897af30d88e7e8e3', '611fc48447d1418385dcb661d05d33e1', '7dce1281bb544cf7aaba5cf681575b9c', '9d7fcad6a3754103acc804af1bdd3b28',
                  'c6acb638c196475e959e4cd1bee68031', 'ab7287fb6aaa427fb832c9a8480380ec', '71dddcec044a4420b680e4c84f27e1ca', 'a57db529f0a64439b7fcf9926efa0bf1', '6b43f1cdccea43b9a6cc1c7272f0aa25', 'e326e1b66feb44a3836be8895a39edf1', '58e067e098f043f5b2c74bee4b92a4f4',
                  '69acc02c24314aa8b6d76fcd43a55f28', '39bf4664e2e9471b82de211511a2f5ea', '6ce44a476ccf44a398ef8d83b14b5319', '5814ed63957e420bb983566bf14a1e3a', '36bde29767cb4b069d3356a41094497e', 'f94ac775b93d47b89584ee5292bfcdeb', '48d63d072b824a9a9d9a8749d315c66b',
                  'f7e4a705643044b19e45d90b07b3a5ca', 'cc793a3f803a4a63af05fc5a86306f0f', '36e18c453fab44b6a1ce4ff6c8dfd2e2', '1ee24634937244a48f06794ef2666524', 'febc9c3c5df54f468ce220720054b405', 'cd2fa72194d74070ae5afc17acbcee0f', '85daea5463f7420ea311beca3210d546',
                  '66a11ce907f64a03ba28a12cf9ca217d', '653df488dac244008b4b17e26c4f2255', '06c381dcd36f48bb9bdcb092df0815e3', '0615897be24e4771aea7d916d1362d96', '6f1e3d4fa20c4b83afce50949fd97d3d', 'a379a28db18d453698916c8019293abb', '44d9da8ccafa42338d35be5faa2e89cf',
                  '1fd4b699938f4b02b6de5d91f9343ed9', 'f9fb215172bf414296f04b7316f8e278', 'e3c86c0d75ee48b0b117ba0fbfa8d3c8', '623902c1a5794bbd8b3fff6afeff4860', 'ecbf247da3cd451b8249c22610db0a58', 'e785ba8bff954c779c2895345b883408', '421cafb283a844e69dac614b296dc9c0',
                  'e6519d390bb0462ebfed7c01b0430d13', '358b6a5c27cd4697bdceb7715b84dbb7', '1ce3ae8b16e845a1a63e77a00af605e0', 'c8a265705d65480fa1153ae82234b76e', 'fd72d9a3f2c44877beff365f3a46e7dc', '43fa235234f54d9b9214dbdd0cceae04', '0c32d4f215c2499eb767ebeb832eae7a',
                  'f04beccc3e3b40e3b45b4e7999088050', '6857e2d778424303ba809aadbb2bd3b2', '60975958127d445da46b52a07879cf9f', '1ebce78581a947cdbc6321fef5ffe0af', '8a76a9e6208846a4b49efbdf729c92cf', '1112bd1cff4b4655a94b04f3049c1557', '8f73990b64d24594b75173980620f26f',
                  'a180fd987ad240ccb0be89495f83d77c', '8436afd678494280a4c6be17487ccc15', 'e7e94e58f5f140879b3eeae9593df251', 'b5660225c0b54507a7d9bff73c257054', '95a5fd1bdd5140f4b55ff39ddefa7b96', '0f13acd9eeaa447787bedb89ca509008', '407a724039334e82811c4cc8711decdc',
                  'ccea40e35b574eeeb21725b4f34a4afd', 'cfbc08c1134647d18ef57a41ba8b6e5a', '71b743a649fd4ddea509bcf534c7de9c', 'ad70d9cc4c1d4d7983d353ccf69ecc55', '0078a798bdab405a86c048c41f5aa064', '10ee45a84a554d4da2642c4557de4f62', 'b0bbd8614e51467b9ccea44ab32cd057',
                  '49584746bd3a4659b41e0aa45fa6c136', '425e6673e5a645a78dc42e74fc843d26', '3ac04a9f35804b339e9c6ac74080c446', '22acfc7944d44688a05c6ea0d7e0d328', 'f0387ccdd65b4630aa70323b46b2542d', 'e69876a14c394b698c9825f574d05046', 'e07800a73b5c429e9adb1e6ad738cd93',
                  '379a9f27a39e42f3b949fd4015d2f8e5', 'd159064d0b4240438c968cae307762ec', '0b65a12b635842ff8d00ef4f63dd9950', '6a3d698c003d4ac4bdb1cf6e11c8a301', 'df91f2120c074354b69ee73791d68037', 'd8cca471b85347fe9926ea3b2b6c1e60', 'a38cfa7678194593a703b0d31b44d1ed',
                  '74168248a67445df9928d529121dce93', '869b66785f4c4d368526e0fab4c1d2b1', 'bc2890f9d68c42589a3fa3de9680b929', '3b3ffdad408343daa86e18d9127d1398', '1e6a24eec0b742d88ae3b9560355a4ce', '80c60660a304490eb31f19b906ef945a', '264515dd838e4f9eb9f48cbf7e948b82',
                  'b39c33f2c6b045cfb501ec3e6a8a23c7', 'd38282b142f74ec9b1ea49b51af2fc13', '908668b8de0c451e9343fb2babbe0c1a', '31dec8047530493fab2636a5d8df20bf', 'f9089bbb0f874689ae75619e585ce465', 'eebf6f4c246045d98394f91114dfac8c', 'c4523278d7c9451492c085916624ce6b',
                  'b5d659d99a414dd8ac0a7a9eca4eb2ee', '7c73ee3df2da4858a1eac9c26b0837ef', '21abd20cb9794cf0a3a553da7fa2e66c', '195220cf9bc0412f9fee6fdcdf321d8a', 'd00d7b1fa0bc4f60b0c1add543fe0713', '2dba3f7f223b4c3bab5968920ecd42bd', '61e2773e74124f8e8cb5ba2a8834ec6e',
                  'edda6a18a7c94134b19939899d6e12f8', '7003f64ffd984bd1ae86c48ff8aec6ef', 'af569e66a5f1420f9a0e1ac0f1b9b694', '8e3b9d208af04d2792cf7481fe45bfe9', '7095987ad10d40029e87f02c947a3e23', '11aa15c82af34812a83047323afe07a4', 'bac789d12063490e80ade7c07d4a49b6',
                  'c9ff573cf11a48969f36479e8c4ba49d', 'b8a7960702914aff83d31e343b398b4b', '44a2f5ec98e146b88c36099fdff433a3', 'ba229599ffee4fdfad519a726237661f', 'd8dfc132d33c4c3db2bc8bb67d6855dd', '88ee26d19f8c45ff9dc39c4000a819f8', '8349f4c3e2ba4626a8797d024ca70c34',
                  'd076c23beedc457ca9ff3386b50569b5', 'c0e1f92d52404101be1db406a56dfe88', '1c591de84aa445f88d8123f602cef74f', '5dcb4e4d88f342c7b7f085e693511708', '0d204830699646909c2df9c229b9cd13', 'b294c7c9e5044bc689be71b43678ac72', 'a17ea7ac3c1642549fa51a8af94873b3',
                  '873ac856c1374611878e19855d5730a1', '37af616a071d4435956e55390e5a2808', '2f20a159a88d43f98f6329ba79da7c37', '49942f1babb041469977e52465881440', '8ed10108b6244228a45cec472eb0ec74', '374668fc2acb482e976808823d4f640f', '4da4b8f9a1c34c0e887f40a1cde5f1e1',
                  '583ab05b838b4a99b6d1c442acde9852', '7f5c0848536640e4b2a4ea061f19bcaa', '88e28dd676df48529b750b42b0cfab83', 'e79d7b80cd304075a376fe108fb520a1', '3d1d4824df54458690ca87ac26b4305b', '23320a25b1464cf18c8f7ae63fe753ef', '577b460b401e445fa979d28600eb5f3c',
                  '6e60574b04e740cfa1e87bc87e4e72f2', '348e27b075834010a4779a0bc4914c62', '74781f1e53ff40109a5636b458df6b77', 'ac1e3b7517e34e41a792993ddf4dd8da', '5663f214846441368efaaa1b06d5ee9d', 'dfeb31c2de8f45f1be6c6bebb34fa894', 'ed253a6412ef4a62aad07441c3bc48ea',
                  '4ff99f884da44615ac9655702617c6c6', '44c55bb59a17456b9fbed40a46800f4e', 'bbc6f5f925e24041a07841f6e1610414', '17c3af44058e493e91abb12b3c8549cf', 'ce60a18bdf92401dba9a86fd41d29b2b', 'c6dd80a17dd4464fb64e85fb92ffe52d', 'f8dd0d4b02a54b4cbdf646a2d1790dc2',
                  '3a6eff55770d4b9888b9577c87c960dd', '4df61588e819418a820e474876028afb', 'ea8d68cb6f7441e9b5ed9fc70c5f839a', 'f9314a66e58c4e51ae6a352ce298cd56', '4a963beed22c45cabda9a98a8400f6df', 'a1bfd7ea39d94433b38ca2688a238fc6', '9b77dba988f74ff38da3ccb7d65eb229',
                  'e97c0c2de29543bda0befe94543d2efb', '40db987e8df3493ea8f87cabf83221c9', 'b0de4da5b42b4d49a09ff88892646a8a', 'db005a072a24459ca51894a602cf343c', '690538d132224f99bb89bd94d0614989', 'b498701a695f4a2f970757c385900ff5', 'da7c86391ebd4a79898f335d46d8376a',
                  'dd5d3290e4724bc88d30bf4bd7d348fb', '1799a773c11342a9a874f2cc4ed64271', 'ed0201876f714890b5837a6520f117c5', 'f1a140289dc84157b6105ad7642d5ad4', 'e243800d917e40c8baf60c7d81f7a666', 'a0fb6f63719145bd829884f105b7c4b4', 'bdd5c4e156874cc9aa3928bc36485cde',
                  'bc6b140424964b89ae81b7138957ac9d', '210fa0c2afdf451c99407db1a664e5d8', '3dd3e2de93344170b4a372f153a7406d', 'b171c920104247f3856e309d85cd8767', 'd81c7903b48c4c3b9b405c4e22091aba', 'e13f42debf5c4aa7ba96def1b3c49f61', '0fd5f55d6350407791769614ab3e03ff',
                  '0945575522cb4e5fbcf4c910a3286a8d', '1a2e239f3a684a56ab932fc4de0f9186', 'a55cea5d61174a50a8f6355c77b69c9f', '61050a5ceee14904b2e435cc2ba6928b', '8ba04e1672f3483bbaf50f7686788ee2', 'e561442aeeae4dbdb882529beea68a15', '17623157c2e34aa88ba9396414783d0e',
                  '0385baf42f074bf18a214629ea6a10b5', '380af6b745c24e31812f60c028b275c0', 'b80b1e4c993d4932bee15c4a801e7da2', '498a00a0068b4803aa08fa0b8ccd7698', 'e9def374d2554029bd1f8a175ead0259', 'ed5da3666ade41a2b34c57b5f6d3535f', 'efd7433382c346eda65f926d4b394890',
                  'd70f9957c3544d239bcab7b6114c29f1', '737114b9ee1b48d39508c004d6ab4f0d', '8273d552a5a74e31842830524c978f52', '7cfa0561292340f68a8074d7733d9516', '89672159d35d4ebeb1790919a0942919', 'cef13ffa66f248cebd924d0a54c837d0', '38df5ca9fa5047db8e0f9619ee3b81b9',
                  '4e8ef706328848ef801e073bee398d41', 'd189a7dcf60f476498c4f420ea9b649f', 'e7819e8e9cb14c2eaee4b8c29e85c2b3', '639937111485490c9b1e026a14490bd4', '12d2aa9e13104364bc813900e649faac', '1e509ba8334c40c7af80b4c5cf13566f', '9b1a08c0e84c4096805addbe96347286',
                  'c88c09bcda63432397c904737408e058', '94bdec876f5544c7a9bd2ea3d57f40cf', 'a10ec4040ab24fa98cb7380a7c4ee61f', '2eae45146aa34de09a93636f820c4497', '98c584574e864c4087fa003e974ab3fb', '4adb99c926dc4f19bb7808d40722c02a', '4e26ea3338c64c8888899691166230f1',
                  'e191afb2cd6e4aeca935f6edf976e052', '082b75a3e315495dbb350cab196c34fc', 'f9e5e42bc110401d9bdb9c29a11bdeb6', '7f3c97e5d0e347a7a1ac1ca8c8fa0c8d', 'ea9063c69d95449986b1158cbaaad8f5', '2a27fbe3d18c4fe587c7ca70d450435a', '0f88110d0efd4c128da491a3ba386889',
                  '05edc24931d747a3a2c8a199d6fc042e', 'b5fa385c979741b1ad6bfa48655f17de', 'e1a487924dc44411811c27ee06dac819', 'bf7af864712c4c66a8550df61d575af0', '018ffaf875d54faeac3807817ff04328', '48578266845b4cffb66a4d764ec0537d', 'e77889d920e942abad143b5c8078a183',
                  'c31d0233548644da877cbc4b7d148cd0', '51bef61cd27b4704b37ff955cc9cc6a8', '73228b39debd4fdc812fc09ffad4d240', 'c1869e027db64ab886bf1eb4e2703539', '9b8a590187ed493d881cf0eb83adecde', 'f9a41af4e54646adac7d6241f8ffd02f', '1da8b578db2449f6ba1b8dabb3980166',
                  '2f0931e39821435892832a3805aa5dd9', 'f4c585f829c040c49918fac01f370177', 'c30b1283708a484b93e66e68de7d2e20', 'b806fb90e3a24186b5351dd0917e1a8a', 'e9e5fd8e62494fa38bb15944d17d7aa9', '3d8fac93385c47fd94d006f444ed9057', '0e0af4628b1544949ca64bce076264dc',
                  '052bfe72ec5840d7904b565a36ff390c', '875d6fc75fe84d5f9d7ed3f66d7da4b4', '57a317257a7a4ab6ae5ac1a4da211853', 'a69136dfdfc6430eab2ca5720bc14704', '7f0d14f034054bc095cd716a91b24184', '79babeff6a794b15aa714197df2de412', 'd3c3c01f9a30459da3a788eeccb75259',
                  'dec102003ab247d4b111ba1b7e3196a7', '8942d11f54e64487899a3133bdb41b67', '1e6478c92456427aacf99ce0dd39d002', '358571abe0d0489aaf7fb54e3a855e74', 'ae50b13451a647e5b9a3bcd826ecdcc9', 'f82b891f1b254a7682def0807fb8ee10', '831ed664bf7c49d2b8fb6b8c4c5fa1c6',
                  'b994bccdacdc41efbafc407f4dd1339a', '55a2b979280d4f47876cf58643636c68', 'f12bf6bd0925488394f5f6150253d3c4', '0275a3b7c0bf45179a4f9ed260220642', '521289bcd759468aab05780dab617e22', 'a743303a46e94253b7ee8ffc1b9fb7a0', '8bf30d3be6b04180bd960b5a392de8f5',
                  '18c3eb67d8b14d65b6e334044ce031c2', '57456dde793b4573b7adea058b86c373', '916ae2fdd3e346dfb7f9105e56dff808', '0eecddb0e1b64da1923b1c7a5dc5de63', '984cda4450e34951b58c4b19d8b7837e', 'da69f95446f144f88d7a34db30a5a801', 'd4378a1a515a4758b485ebf13d188f62',
                  '2d0194a6fab841dd9f9d9baf24c1accc', '874b79eb53bf436b89dfc823f0822485', '3d04e3aaf77c471dba3ca25d8e88d967', '82e4a9da2844481099b6a859f4e97d07', 'c3088942189c4c74a66112cc65d23493', '1e189ad28ad045c1b2517f5e81857e02', '5d20daa50e584163bee04e2c247b3666',
                  'ca9971ed088c4d9e8339199635b70a86', '1dd483ba100746af8209292af0cb731a', '9aba520c6b6442cca8d913e5dda65126', '33c33953a5a34d4e9adadaaffb5c0ad9', 'f47d524b67d5471e8f5de0a6209e3a67', '8edb751c415742f987c6a41df53e39ea', 'ca8e245bbe564994a13260a4097fa4d0',
                  'fe6b56287e1749fc9dac478d71951473', '587bf1396eea4e2082e0354e5113ed6e', '25e290b82aee43d9a8997a43e00bcd11', '47823b5717554327b192b57403008a4b', 'ea7cda9797f14d44ac5375f3c945426a', 'ae9b0335ab134ca393ada1af41025516', '33e05472c0424169ad4419acede07db4',
                  'fadb14c1960d43768cc83f73cf0e6ef9', '5685f5cb436f4c5ab32f7c5421a8e0e0', '2641efaaa60a4038bd4e662e66d3a3f3', '6dd2358e02ec4110ad67afc242941e79', '052546cf73e54d6b91bad6fc97723a51', '34146084f5ae45cb9c36645cf3370a57', '26b37f8f817449b3854482bba6b87da9',
                  '838a789367164475951239bdf9ed7876', 'fea4873b4bdb427bbdadf4005ec3a2cf', 'aafcad42f0d74c458b9542a59edc1f09', '5e1fd2f0094f4c22b0e891c308edb202', '914ade17f25a425ea8841eb0cd2bb63d', '770b5f249b9e4b9985dbb9cca55ca7f0', '22fe02a1421242d599fe6f83732586d0',
                  'fa605c7a4463404486a8412bb00f7b6d', '51acd4749d1943e881316c21a6ca18f6', 'd8bb07d308fa48e98f4eca52b5485756', '9a7b1891b7774696981b6f9602ef1612', '211c08353bea4d14bc12df4eac768d5d', 'e7063e005e224015b044e04c8e6b2003', '77a3892686fe45a2a9d80797cc1bc2be',
                  '1e8eea5089364405a76a4ea1a0779859', '6c71eaeb1fdc48bb8504b8119e37a7c7', '48b7fdff0bdd4234838967c9b58bb11f', '9f16486f7c3946c8846d1e4580d4fc9d', '3c3362e82e514b9e8b8ed95de62e4641', 'f61a395f88874ba6a045ec8d387beb52', 'a83b9dc32dfa49f2a89c6950341da49b',
                  '87243bdcf99a48d0b4fef6590805eed1', '9af5efa5610b45afb820dd5d68db35be', 'f5050d273e804f8ab593f4edbc1f4bc5', '62dab3b8802148429fce29a4398fc1b1', 'f9e208fc3478474aaa2e2f5e98e53cc5', 'a22ddb0a03ef4795ab746ab26b029dae', '9e3d1f1b3c0f459d8b87b481b1273304',
                  '486d4b380f824c88bcb703d0e8eeb8ab', '229b5a8498dd4b399cee3bb84ea8ae28', '690a8b2ec88f46cbaed14f8ba645ad05', '4026e6f4f2814cfab3d9727cdf0f4409', '9b72fe1dd7d048c986b70ba535c14f57', 'b0b72871fafe4a1b994b0ab9d7d7a8ee', 'e27be7c9da434e81b7531182ac5d171a',
                  'ffa01a8e27ff43e992eae7015c9cbbf0', '2344f42423974de5b90560551ebfd69e', '856e94cc0bd64adca527361d78e644d0', 'b3b9f87823024341916595ad2cc47eeb', '5851989a683a47809b99cb07e6417872', '8edf5f4f97754351bab1e9ea8e331fa0', '759bb7e5719d4bf7a351a63e2e9013fb',
                  'cdafd51f0ed5440aa710299d04aaeed0', '834493236d5c4fe2a08091bd78545f0d', '12c964e0e5eb459ba27854d947c182e6', 'afa5e293ffdb488fb5696ee616dc8182', '193289eccef6463abbf46ac12ee4bf83', '2583dc072a374e72aa78e4063eba5097', 'e70cc6a183ac45efba63bb77a8ecc74a',
                  'b93102b699624ab688e5423c4db0dfd7', '3beceb24dd64416da0d935d443fef59e', 'b8bb05e1c6e34cd7abde8e22eda5b990', 'd3192372c6ee47af8a0d205357ea8077', '892a542c368349fab730516253d08451', 'bc8c23711001454dbc38f1c0c3aa9096', 'f59753b9c91a4e2b93cdf029ef781d87',
                  'f006052ef2bf4dc98a58a28350b4a80c', '7f53375041044440ae329ffbb8901779', '362b5e3264b64ebab60845827cebcbaf', '47bbf72aee9d46c8b6d003169cb047a0', '36055e6fddc749668eddd7497a3db37c', 'af33e54e9a794ebe996e66f392697fdb', '8993ad790cc2466dbfe88fe5b8d48220',
                  '747211893a184183b660b6c8353cc209', 'd8712630e1f4495ea4844ce4b5a7d233', '9710ff20885a404e83d03353a01016d4', '5bdefb9edb814f5c92b2849e4ac6e4a8', 'e4e605e780c04b168ef805af85207940', '1f7ca95d44dc4f13b6e2159415106ddd', '72406054e961403a9a55fb811189cb49',
                  '7568074890ec4890a47d287064422914', 'd2f4f57d1b8946b49066e7ed5e8cdd8c', 'ffbae3d403ac493c9a141868d27d6834', '9f832fc2417e496d8c9266722a6e0f76', 'fad647223dbd4e948f523f024c5e3509', 'f7f68f10e6c84010a77017f071b7b419', 'a1e1e734f2d7433f988a542f33ecc1c1',
                  'ad9cbdad6ee64ef599ff5a28fc37d4ea', 'a2c829c62c8e4d70b26e9291f06df5fd', '73f3eb26955944a7803edb616be1df35', '3193f1fd102b4a6892aebfb5d3e0ab94', '3c1fedd1c866476f80157ff3bb14ba19', '3c84362604c943d6bd6abd02099679f0', '2d20c21ff5104d91ac567375218d5ae9',
                  '52609add816b4a3f9c494ee3d099cf15', '0fcc46cebcc249d7b612e6d69becaff3', 'f7ca872815204970b97bfa640460fe27', 'de0c62d0a5a04ca39dad88ef13280208', 'ebfeaa0a496b4fd2a949f663edefe218', 'dcfe5c3903974e5e91d6f741b15d7a27', '82e52266a4384072a69b36447e27ff6a',
                  'da12a2d7c7914eeda9b426903b345a0e', 'd745807784b8450793de0e87c9d85e30', '0077c70abc8a41c0a477bbdc1d214502', '5d39c0f8b24b4eb58a66defd44cd4826', '53959abd7c5449fc9c66a2e813593581', 'b1862da24b164046897ea3f7d578dcfb', 'b963ebeac97f4d0a87bf759452f1ceac',
                  '62a0c763be1c49cc9b2fd70ba1daad3a', '68b6b4cab4684c9a99e3fb3d8093079c', 'ed42c6825d774868ac067fb701de4c7c', 'ccc75b35c26c4d1e86f687b2550ad083', 'daa9f8d0428b41e2adde40701bd889b0', 'c1518d36b2504a588a894f01213fc5e6', '9d84c5de4bc04a5d864afe409ac2de82',
                  '58beb116d8104e45b6b520d94be7e8f5', '71c3340445bf4cf6a8ff075ebf40cec4', '4cb663513ec745ba9c7285bca5c97e62', '1bb6a815debc4c4c92f9e20432e58a91', 'f8bdfde7c006461fab5377a457437948', '31e1d11c22d349ba91f8108e9a4173f7', '055a24d633094230b177be599b93f818',
                  '755bc46f18bf45daacccfafea437d9e6', 'a6f008b346504af1a5dd24b88a59328f', '382641b410984f3a974aa15d6f4e5cec', 'c6d2e7fb3475409ab1fbca3b25283309', 'b5947b2e7df14ed1976a2ccdc763442b', 'e9d3d8b78d0045fcb82d3a8fd060cdee', 'd3d38e12055447aeb7911a86000e3e3c',
                  'b1f909bd9a064454be634a99e2e7ca46', 'cc47a4e352bf4e789c432ccb6491f904', '6c5d88f454484996ad7505ae3ba5131e', '4a62648839ae4725ab1f5748e663061e', '79f0b5a3275248a4af04ac5a013ea06d', '519e94ce0df74c72b62733dbf8cc5187', '88793645901b4d75a1f4e3cfa3f23efd',
                  'b6a95a379fb94fc586f80e86079c7ac8', '566b1ce010814404ac0c8521d03274dd', 'cca9afebf227435986c40e5435582912', '93576d16b7a643a992124178cd181993', 'f57eca7fa14b4b61a1ad6890d5c575a8', '9175230a56e94e4ba3bccf12508da704', 'c78fbf8d3d4c4c579e7a8db99452425c',
                  'e3d6942573594879aa7668e52282cf54', '85006017e8344795b05757c99b18b7fe', '280e18df7b974853a28cca82890fd842', '67918685278640c1ae0ade2f005e330e', '6c8d2bcb0b1543c2813d46f95bd80d6e', '6fe20ab6279c4f1c8de03c7a2402c8c9', 'b59d48b76b06459c980716030f9f15ab',
                  '7e85d6ed2189413fb2093f48596fee0d', '5faf5463baca4ed3bccce6b1979808d7', '06c2df5ffcff42ef8a4a047e0c965959', '7e65768ae8c640cdb311e634a6703e8e', '80c7d8c31a004edf85472172c752a20a', '856e35e8d1ea4bebac184a450e89b4f2', 'a5a4c00f99e84735a968869346271d5f',
                  '9a7bc943a61647d2ba73fa34e19e1b93', '50da976503e342b78460211d827cc621', '3eb635d63ba3491db68c2589eef46775', '0b8a76bfae5746be805a244bf2226aaa', '58eb880d94594c5083cf9ae8be2cd339', '7ac43c4cabd142148f056c4a66308b7e', '6bc0952b6a7540eea225317cfcee96bd',
                  '5b31fdda2e104e2a829eeacfa18b0479', 'f19e9c0cdb694173a10841726f9c4494', 'f32550ee089c472a9850ff364ecb7f2f', 'a648e8e6da294e31a2627656d93ca549', '634ad70bd8fd44b1b01346fb9ee9f041', '25cb21992ace4874b109789f7c9743df', 'f9c2f4038ccf44b4ba77721709206c15']

        exs = []
        cs = Course.objects.filter(global_id__in=c_gids, in_archive=False)
        print(cs.count())
        for c in cs:
            e = Expertise.objects.filter(course=c, type="0")
            exs.append(Expertise.objects.filter(course=c, type="0").latest("date"))
        # exs = Expertise.objects.filter(type="0", )
        data = serialize('json', exs, indent=4,
                         use_natural_foreign_keys=True, use_natural_primary_keys=True)

        response = HttpResponse(data, content_type='application/json')
        response['Content-Length'] = len(data)
        return response


def send_course(request, course_id):
    def clean_empty(d):
        if not isinstance(d, (dict, list)):
            return d
        if isinstance(d, list):
            return [v for v in (clean_empty(v) for v in d) if v]
        return {k: v for k, v in ((k, clean_empty(v)) for k, v in d.items()) if v}

    passport = ""

    def _pretty_print(req):
        print('{}\n{}\n{}\n\n{}'.format(
            '-----------START-----------',
            req.method + ' ' + req.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            req.body,
        ))

    if request.method == "GET":
        # try:
        if not request.user.is_superuser:
            return JsonResponse({"status": "Not allowed"}, status=403)

        course = Course.objects.get(pk=course_id)
        expertises = Expertise.objects.filter(course=course, type="0")
        expertise_json = serialize('json', expertises)
        data = serialize('json', [course, ])
        struct = json.loads(data)[0]

        new = True

        new_course = struct['fields']
        new_course['institution'] = Owner.objects.get(pk=new_course['institution']).global_id
        new_course['partner'] = Platform.objects.get(pk=new_course['partner']).global_id

        if new_course['has_sertificate'] == "1":
            new_course['cert'] = True
        else:
            new_course['cert'] = False

        new_course["promo_url"] = ""
        new_course["promo_lang"] = ""
        new_course["subtitles_lang"] = ""
        new_course["proctoring_service"] = ""
        new_course["sessionid"] = ""

        new_course["enrollment_finished_at"] = new_course["record_end_at"]
        new_course["estimation_tools"] = new_course["evaluation_tools_text"]

        new_course['teachers'] = [{"image": "" if not x.image else x.image, "display_name": x.title, "description": x.description} for x in Teacher.objects.filter(pk__in=new_course['teachers'])]
        new_course['direction'] = [x.code for x in Direction.objects.filter(pk__in=new_course['directions'])]
        new_course['business_version'] = new_course["version"]

        del new_course['directions']

        dates = ["started_at", "finished_at", "record_end_at", "created_at", "enrollment_finished_at"]

        for d in dates:
            if not new_course[d]:
                del new_course[d]

        if "ру" in new_course["language"].lower():
            new_course["language"] = 'ru'

        if "н" in new_course["duration"]:
            new_course["duration"] = int(re.search(r'\d+', new_course["duration"]).group())

        if new_course['lectures_number']:
            new_course['lectures'] = int(new_course['lectures_number'])
        else:
            new_course['lectures'] = int(new_course["duration"]) if int(new_course["duration"]) < 52 else ""

        new_course['duration'] = {"code": "week", "value": int(new_course["duration"])}
        new_course['pk'] = struct['pk']

        passport = {"partnerId": new_course['partner'], "package": {"items": [new_course]}}

        # Убираем None

        passport = clean_empty(passport)

        if "promo_url" not in passport["package"]["items"][0].keys():
            passport["package"]["items"][0]["promo_url"] = ""
        if "promo_lang" not in passport["package"]["items"][0].keys():
            passport["package"]["items"][0]["promo_lang"] = passport["package"]["items"][0]["language"]
        if "subtitles_lang" not in passport["package"]["items"][0].keys():
            passport["package"]["items"][0]["subtitles_lang"] = ""
        if "proctoring_service" not in passport["package"]["items"][0].keys():
            passport["package"]["items"][0]["proctoring_service"] = ""
        if "sessionid" not in passport["package"]["items"][0].keys():
            passport["package"]["items"][0]["sessionid"] = ""

        if "direction" not in passport["package"]["items"][0].keys():
            passport["package"]["items"][0]["direction"] = ""

        if new_course.get("global_id", True):
            # print("Обновляем курс", course.global_id is None)
            new = False
            passport["package"]["items"][0]["id"] = passport["package"]["items"][0]["global_id"]
            r = requests.Request('PUT', 'https://online.edu.ru/api/courses/v0/course', headers={'Authorization': 'Basic bi52LmlnbmF0Y2hlbmtvOl9fX0NhbnRkM3N0cm9Z'}, json=passport)  # токен на Никиту
        else:
            # print("Отправляем новый курс", course.global_id)
            new = True
            r = requests.Request('POST', 'https://online.edu.ru/api/courses/v0/course', headers={'Authorization': 'Basic bi52LmlnbmF0Y2hlbmtvOl9fX0NhbnRkM3N0cm9Z'}, json=passport)  # токен на Никиту

        prepared = r.prepare()
        # _pretty_print(prepared)

        s = requests.Session()
        resp = s.send(prepared)

        if resp.text == "":
            re_resp = " нормально!"
        else:
            re_resp = resp.json()
        # print(resp.text)

        if resp.status_code == 200:
            SendedCourse.objects.create(
                title=course.title,
                course_json=passport,
                expertise_json=expertise_json
            )
            if new:
                course.global_id = resp.json()["course_id"]
                course.save()
            course.roo_status = "3"
            course.save()

        return JsonResponse({"status": resp.status_code, "resp_raw": str(re_resp), "data": passport})
        # except Exception as e:
        #     return JsonResponse({"exception": str(e), "status": 206, "data": passport}, status=206)


@roo_member_required
def show_description(request, course_id):
    course = Course.objects.get(pk=course_id)
    course_labor = int(re.search(r'\d+', course.labor).group()) * 36
    return render(request, 'roo/description.html', {"course": course, "course_labor": course_labor})


def TableCourseUpdate(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        course = Course.objects.get(pk=request_data['pk'])
        # course.credits = request_data['credits']
        # course.record_end_at = request_data['record_end_at']k
        # course.title = request_data['title']
        # course.image = request_data['image']
        # course.created_at = request_data['created_at']
        # course.visitors_rating = request_data['visitors_rating']
        # course.duration = request_data['duration']
        # course.finished_at = request_data['finished_at']
        # course.competences = request_data['competences']
        # course.accreditation = request_data['accreditation']
        # course.description = request_data['description']
        # course.expert_rating_count = request_data['expert_rating_count']
        # course.has_sertificate = request_data['has_sertificate']
        # course.language = request_data['language']
        # course.course_item_url = request_data['course_item_url']
        # course.content = request_data['content']
        # course.started_at = request_data['started_at']
        # course.rating = request_data['rating']
        # course.external_url = request_data['external_url']
        # course.lectures_number = request_data['lectures_number']
        # course.version = request_data['version']
        # course.visitors_rating_count = request_data['visitors_rating_count']
        # course.total_visitors_number = request_data['total_visitors_number']
        # course.experts_rating = request_data['experts_rating']
        # course.requirements = request_data['requirements']
        # course.cabinet_course_url = request_data['cabinet_course_url']
        # course.admin_email = request_data['admin_email']
        # course.newest = request_data['newest']
        # course.expert_account = request_data['expert_account']
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
        # course.responsible_comment = request_data.get('responsible_comment', "")
        course.platform_responsible_comment = request_data['platform_responsible_comment']
        course.owner_responsible_comment = request_data['owner_responsible_comment']
        course.passport_responsible = request_data['passport_responsible']
        course.save()
        data = serialize('json', [course, ])
        struct = json.loads(data)[0]
        new_course = struct['fields']
        new_course['pk'] = struct['pk']
        new_course['num'] = request_data['num']
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
    context["platforms"] = Platform.objects.all().order_by('title')
    context["owners"] = Owner.objects.all().order_by('title')
    return render(request, "roo/courses_edit.html", context)


@roo_member_required
def courses_edit(request):
    # context = dict()
    # return render(request, "roo/courses_edit.html", context)
    data = serialize('json', Course.objects.filter(in_archive=False))
    return_data = []
    i = 1
    for course in json.loads(data):
        new_course = course['fields']
        new_course['pk'] = course['pk']
        new_course['num'] = i
        i += 1
        # new_course['partner_id'] =
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
    exclude = ("in_archive", "identical")
    template_name_suffix = '_update_form'
    success_url = '/roo/close/'

    def post(self, request, *args, **kwargs):
        if request.POST.get('archive_course_id'):
            arch_course = Course.objects.get(pk=request.POST.get('archive_course_id'))

            for arch_ex in Expertise.objects.filter(course=arch_course):
                arch_ex.pk = None
                arch_ex.course = self.get_object()
                if arch_ex.type == "0" and arch_ex.executed == True:  # если у оставляемого курса есть пройденная обязательная экспертиза, ставим статус курса "Экспертиза пройдена"
                    self.get_object().expertise_status = "3"
                    self.get_object().save()
                arch_ex.save()

            arch_course.in_archive = True
            arch_course.save()
            self.get_object().set_identical()
        return super(CourseUpdate, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CourseUpdate, self).get_context_data(**kwargs)
        context['expertises'] = Expertise.objects.filter(course=self.object)
        context["course_id"] = self.object.id
        return context


class ExpertiseCreate(CreateView):
    model = Expertise
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = '/roo/close/'


class ExForm(forms.ModelForm):
    class Meta:
        model = Expertise
        fields = '__all__'


def new_expertise(request, course_id=None):
    if request.method == 'POST':
        form = ExForm(request.POST, request.FILES)
        if form.is_valid():

            ex = form.save(commit=False)
            if course_id:
                ex.course = Course.objects.get(id=course_id)
                ex.type = "0"

            ex.save()
        return redirect('/roo/close/')

    args = {}
    # args.update(csrf(request))
    args.update({"course_id": course_id})
    if course_id:
        args.update({"course": Course.objects.get(id=course_id)})
    args['form'] = ExForm()

    return render(request, 'roo/expertise_update_form.html', args)


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
        for attr, value in kwargs.items():
            setattr(self.object, attr, value)
            self.object.save()
        self.object.type = "0"
        self.object.save()
        return super(ExpertiseUpdate, self).post(request, *args, **kwargs)
