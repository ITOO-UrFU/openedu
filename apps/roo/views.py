# -*- coding: utf-8 -*-
import csv
import string

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
    Expert, Teacher
from .tasks import *

logger = logging.getLogger('celery_logging')


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
        exclude = ("in_archive", "identical",)
    # exclude = (
    #      "credits", "record_end_at", "global_id", "created_at", "visitors_rating", "duration", "finished_at",
    #      "language",
    #      "content", "started_at", "started_at", "requirements", "competences", "accreditation", "description",
    #      "image")


def merge(request, pk_1, pk_2):
    course1 = Course.objects.get(pk=pk_1)
    course2 = Course.objects.get(pk=pk_2)
    form1 = CourseForm(instance=course1)
    form2 = CourseForm(instance=course2)
    return render(request, "roo/merge.html", {"form1": form1, "form2": form2, "pk_1": pk_1, "pk_2": pk_2})


def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
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
            if (courses_equal.count() > 1):
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

    # writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

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
        context["courses_count"] = Course.objects.filter(in_archive=False).count()
        context["passport"] = Course.get_passport_responsibles()
        context["expertises_count"] = Expertise.objects.filter(type="0").count()
        context["main_expertise_count"] = Expertise.main_expertise_count()
        context["owners_count"] = Owner.objects.all().count()
        context["need_admin_owner"] = Course.objects.filter(communication_owner="2").count()
        context["need_platform_owner"] = Course.objects.filter(communication_platform="2").count()

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
    if request.method == "GET":
        course = Course.objects.get(pk=course_id)
        data = serialize('json', [course, ])
        struct = json.loads(data)[0]

        new_course = struct['fields']
        new_course['institution'] = Owner.objects.get(pk=new_course['institution']).global_id
        new_course['partner'] = Platform.objects.get(pk=new_course['partner']).global_id
        new_course['lectures'] = int(new_course['lectures_number'])
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

        return JsonResponse({"partnerId": new_course['partner'], "package": {"items": [new_course]}})


def TableCourseUpdate(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        course = Course.objects.get(pk=request_data['pk'])
        course.credits = request_data['credits']
        # course.record_end_at = request_data['record_end_at']
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
