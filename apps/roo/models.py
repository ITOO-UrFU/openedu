# -*- coding: utf-8 -*-
# from time import gmtime, strftime
import json

import django_tables2 as tables
import re
import requests
# from django.db import models
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import truncatewords_html
from fuzzywuzzy import fuzz


# import logging

# logger = logging.getLogger('celery_logging')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # bio = models.TextField(max_length=500, blank=True)
    courses_columns = models.TextField("Колонки курсы", blank=True, null=True, default="{}")
    expertise_columns = models.TextField("Колонки эксперты", blank=True, null=True, default="{}")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except:
        Profile.objects.create(user=instance)


class Base(models.Model):
    class Meta:
        abstract = True

    def update_from_dict(self, d):
        for attr, val in d.items():
            setattr(self, attr, val)
            self.save()

    @classmethod
    def create_from_dict(cls, d):
        c = cls.objects.create(title=d["title"])
        for attr, val in d.items():
            setattr(c, attr, val)
            c.save()

    @classmethod
    def update_base_from_roo(cls, url, filter_by):
        login = 'vesloguzov@gmail.com'
        password = 'ye;yj,jkmitrjlf'

        def get_base_from_page(cls, page_url):
            request = requests.get(page_url, auth=(login, password), verify=False)
            response = request.json()
            items = response["rows"]
            for item in items:
                try:
                    roo_base = cls.objects.filter(Q(**{filter_by: item[filter_by]})).first()
                except:
                    roo_base = None

                if roo_base:
                    print(roo_base, item)
                    roo_base.update_from_dict(item)
                else:
                    print(item)
                    cls.create_from_dict(item)

        get_base_from_page(cls, url)


class Expertise(models.Model):
    EX_TYPES = (
        ("0", "Обязательная"),
        ("1", "ОО"),
        ("2", "Независимая"),
        ("3", "Работодатель"),
        ("4", "Пользовательская"),
        ("5", "ФУМО"),
        ("6", "Большие данные"),
        ("7", "Лучшие практики")
    )
    course = models.ForeignKey("Course", verbose_name="Курс", null=True, blank=True)
    state = models.CharField("состояние процесса (этап)", blank=True, null=True, max_length=512)
    date = models.DateField("Дата", auto_now_add=True, blank=True, null=True)
    ex_date = models.CharField("Дата", blank=True, null=True, max_length=512)
    type = models.CharField("Вид экспертизы", choices=EX_TYPES,
                            blank=True, null=True, max_length=1)
    executed = models.BooleanField("Экспертиза пройдена", default=False)
    # passed = models.BooleanField("Прошел обязательную экспертизу")
    expert = models.ForeignKey("Expert", verbose_name="Эксперт", null=True, blank=True)
    supervisor = models.CharField("Кто от ИТОО контролирует", blank=True, null=True, max_length=512)
    organizer = models.CharField("Организатор экспертизы сотрудники или партнеры", blank=True, null=True,
                                 max_length=512)
    comment = models.TextField("Примечание", blank=True, null=True)
    comment_fieldset_1 = models.TextField("Комментарии по отсутствию обязательных полей ОК", blank=True, null=True)
    comment_fieldset_2 = models.TextField("Комментарии по отсутствию обязательных полей ОК претендующих на зачет ОП",
                                          blank=True, null=True)

    # Passport
    has_length = models.BooleanField("Длительность", default=False)
    has_description = models.BooleanField("Описание", default=False)
    has_authors = models.BooleanField("Авторы", default=False)
    language = models.CharField("Язык содержания", default="русский", blank=True, null=True, max_length=255)
    has_prerequisites = models.BooleanField("Рекомендуемые \"входные\" требования к обучающемуся", default=False)
    has_certificate = models.BooleanField("Сертификат (выдается или нет)", default=False)
    has_dates = models.BooleanField("Даты ближайшего запуска", default=False)
    has_admin_email = models.BooleanField("Адрес эл. почты администратора ОК", default=False)
    has_labor = models.BooleanField("Трудоемкость", default=False)
    has_competences = models.BooleanField("Компетенции", default=False)
    has_results = models.BooleanField("Результаты обучения", default=False)
    has_evaluation_tools = models.BooleanField("Оценочные средства", default=False)
    has_recommended_directions = models.BooleanField("Рекомендуемые направления подготовки", default=False)
    has_proctoring = models.BooleanField("Наличие подтвержденного сертификата (сервис прокторинга)", default=False)
    has_labor_costs = models.BooleanField("Трудозатраты", default=False)
    has_short_description = models.BooleanField("Короткое описание", default=False)
    has_learning_plan = models.BooleanField("Учебный план", default=False)
    has_promo_clip = models.BooleanField("Проморолик", default=False)
    language_video = models.CharField("Язык видео", default="русский", blank=True, null=True, max_length=255)
    language_subtitles = models.CharField("Язык субтитров", default="русский", blank=True, null=True, max_length=255)
    has_course_subject = models.BooleanField("Предмет курса", default=False)
    is_open = models.BooleanField("Открытость курса", default=False)
    has_expertises_types = models.BooleanField("Типы экспертиз для допуска", default=False)
    has_ownership_document_scan = models.BooleanField("Скан документа, подтверждающего правообладание", default=False)
    has_not_prohibited = models.BooleanField("В курсе отсутствуют запрещенные материалы", default=False)
    has_text_materials = models.BooleanField("Текстовые материалы", default=False)
    has_illustrations = models.BooleanField("Иллюстрации", default=False)
    has_audio = models.BooleanField("Аудиоматериалы", default=False)
    has_video = models.BooleanField("Видеоматериалы", default=False)
    has_quality_checking = models.CharField("прошел проверку обязательной оценки качества", blank=True, null=True,
                                            max_length=512)
    no_permission_of_owners = models.TextField("Нет разрешения правообладелей", null=True, blank=True)
    got_into_record = models.CharField("попал в отчет", max_length=255, null=True, blank=True)
    got_expertise_2018 = models.CharField("прошел экспертизу в 2018 (1 квартал)", default=False, blank=True, null=True,
                                          max_length=512)
    additional_info = models.TextField("Дополнительная информация", null=True, blank=True)

    def get_platform(self):
        return self.course.partner.title

    def __str__(self):
        return f"Экспертиза: {self.course}, Тип: {self.type}"

    class Meta:
        verbose_name = 'экспертиза'
        verbose_name_plural = 'экспертизы'

    @classmethod
    def main_expertise_count(cls):
        return cls.objects.filter(type="0").count()


class Teacher(models.Model):
    title = models.CharField("ФИО лектора", blank=True, null=True, max_length=512)
    image = models.CharField("Ссылка на изображение", blank=True, null=True, max_length=512)
    description = models.TextField("Описание", blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

    def get_image(self):
        if self.image:
            return "<img height=\"100\" src=\"" + self.image + "\"></img>"
        else:
            return ""

    get_image.allow_tags = True

    def get_json(self):
        return {
            "title": self.title,
            "image": self.image,
            "description": self.description
        }

    class Meta:
        verbose_name = 'лектор'
        verbose_name_plural = 'лекторы'


class Competence(models.Model):
    identifier = models.CharField("Идентификатор компетенции", max_length=1024, blank=False, null=False, db_index=True)
    title = models.CharField("Наименование компетенции", max_length=1024, blank=False, null=False)
    source = models.CharField("Источник компетенции", max_length=1024, blank=False, null=False)
    indicators = models.TextField("Индикаторы достижения компетенции", blank=True)
    levels = models.TextField("Уровни освоением компетенции", blank=True)
    evaluation_tools = models.ManyToManyField("EvaluationTool", blank=True)
    correlating = models.TextField(
        "Соотнесение компетенции и индикаторов ее достижения с компетенциями, включенными в ФГОС и ПООП", blank=True)


class Result(models.Model):
    title = models.TextField("Результат обучения", blank=True)
    competence = models.ForeignKey("Competence")


class EvaluationTool(models.Model):
    title = models.TextField("Оценочное средство", blank=True)
    result = models.ForeignKey("Result")


class ProctoringService(models.Model):
    title = models.CharField("Сервис прокторинга", max_length=255, blank=False, null=False)


class PlatformManager(models.Manager):
    def get_by_natural_key(self, title):
        return self.get(title=title)


class OwnerManager(models.Manager):
    def get_by_natural_key(self, title):
        return self.get(title=title)


class CourseDiff(models.Model):
    course = models.ForeignKey("Course")
    diff = models.TextField("json с отличающимися полями", default="{}", blank=True, null=True)
    date = models.DateTimeField("Дата и время сравнения", auto_now_add=True)


class Course(models.Model):
    CERTS = (
        ("0", "Нет данных"),
        ("1", "Выдается"),
        ("2", "Не выдается")
    )
    #  что приходит в api сейчас
    credits = models.CharField("Массив перезачётов", default='[]', blank=True, null=True, max_length=512)
    record_end_at = models.CharField("Дата окончания записи на курс", blank=True, null=True, max_length=512)
    title = models.CharField("Наименование", blank=True, null=True, max_length=512)
    institution = models.ForeignKey("Owner", verbose_name="Правообладатель", blank=True, null=True)
    partner = models.ForeignKey("Platform", verbose_name="Платформа", null=True)
    external_url = models.CharField("Ссылка на онлайн-курс на сайте Платформы", blank=True, null=True, max_length=512)
    image = models.URLField("Изображение курса", blank=True, null=True, max_length=512)
    global_id = models.CharField("ИД курса на РОО", blank=True, null=True, max_length=512)
    created_at = models.CharField("Дата создания онлайн-курса", blank=True, null=True, max_length=512)
    visitors_rating = models.CharField("Оценка посетителей РОО", blank=True, null=True,
                                       max_length=512)  # но это не точно

    labor = models.CharField("Трудоемкость (з.е.)", blank=True, null=True, max_length=512)
    duration = models.CharField("Длительность в неделях", blank=True, null=True, max_length=512)
    finished_at = models.CharField("Дата окончания онлайн-курса", blank=True, null=True, max_length=512)
    competences = models.TextField("Формируемые компетенции", blank=True, null=True)
    accreditation = models.TextField("Аккредитация", blank=True, null=True, max_length=512)
    description = models.TextField("Описание", blank=True, null=True)
    visitors_number = models.IntegerField("Количество записавшихся на курс", blank=True, null=True)
    directions = models.ManyToManyField("Direction", verbose_name="Массив идентификаторов направлений", blank=True)  # массив
    expert_rating_count = models.CharField("Количество оценок экспертов", blank=True, null=True,
                                           max_length=512)  # сильно не точно
    has_sertificate = models.CharField("Тип выдаваемого сертификата",
                                       default="0", max_length=512, choices=CERTS)  # слово сертификат у них неправильно
    verified_cert = models.BooleanField("Возможность получить подтвержденный сертификат", default=False)
    language = models.CharField("Язык контента", blank=True, null=True, max_length=512)
    course_item_url = models.CharField("", blank=True, null=True, max_length=512)  # неизвестная вестчь

    content = models.TextField("Содержание онлайн-курса", blank=True, null=True)
    started_at = models.CharField("Дата ближайшего запуска", blank=True, null=True, max_length=512)
    rating = models.CharField("Рейтинг пользователей", blank=True, null=True, max_length=512)

    lectures_number = models.IntegerField("Количество лекций", blank=True, null=True)
    version = models.IntegerField("Версия курса", default=1)
    activities = models.ManyToManyField("Area", verbose_name="Массив идентификаторов областей деятельности", blank=True)  # массив
    visitors_rating_count = models.CharField("Количество пользовательских оценок", blank=True, null=True,
                                             max_length=512)  # наверно
    total_visitors_number = models.CharField("Количество слушателей", blank=True, null=True,
                                             max_length=512)
    experts_rating = models.CharField("Рейтинг экспертов", blank=True, null=True, max_length=512)
    requirements = models.TextField("Входные требования", blank=True, null=True)  # массив
    cabinet_course_url = models.CharField("Ссылка на курс в кабинете", blank=True, null=True, max_length=512)
    teachers = models.ManyToManyField("Teacher", blank=True)  # список лекторов/аторов
    admin_email = models.CharField("Адрес эл. почты администратора ОК", blank=True, null=True, max_length=512)

    # наши поля
    newest = models.BooleanField("Самое новое содержание курса", default=False)

    # необязательные поля
    # learning_plan = models.TextField("Учебный план", blank=True, null=True)
    results = models.TextField("Результаты", blank=True, null=True)  # = models.ManyToManyField("Result", blank=True)
    evaluation_tools = models.ManyToManyField("EvaluationTool", blank=True)
    evaluation_tools_text = models.TextField("Оценочные средства (текстом)", blank=True, null=True)
    proctoring_service = models.ForeignKey("ProctoringService", blank=True, null=True)
    expert_account = models.TextField("Комментарий эксперта", blank=True, null=True)

    COMMUNICATION_OWNER_STATES = (
        ("0", "Согласование не начато"),
        ("1", "В процессе согласования"),
        ("1", "В процессе согласования"),
        ("2", "Требуется участие администрации"),
        ("3", "Согласовано"),
        ("4", "Отказано"),
        ("5", "Согласовано с РОО")
    )

    COMMUNICATION_PLATFORM_STATES = (
        ("0", "Согласование не начато"),
        ("1", "В процессе согласования"),
        ("2", "Требуется участие администрации"),
        ("3", "Согласовано"),
        ("4", "Отказано"),
        ("5", "Согласовано с РОО")
    )

    EX_STATES = (
        ("0", "Не проводилась"),
        ("2", "Требует доработки"),
        ("3", "Прошел"),
        ("4", "Отправлен запрос на доступ к платформе"),
        ("5", "Доступ предоставлен"),
        ("6", "Нет доступа"),
        ("7", "Почти прошел"),
    )

    PASSPORT_STATES = (
        ("0", "Не заполнен"),
        ("1", "Не проверен"),
        ("2", "Требует доработки"),
        ("3", "На согласовании с правообладателем"),
        ("4", "Готов"),
        ("5", "Готов без перезачета")
    )

    EX_ACCESSES = (
        ("0", "Не предоставлен"),
        ("1", "Отправлен запрос"),
        ("2", "Предоставлен"),
    )

    ROO_STATES = (
        ("0", "Не готов"),
        ("1", "Ждем ID платформы"),
        ("2", "К загрузке"),
        ("3", "Загружен"),
        ("4", "Ожидает загрузки с РОО")
    )

    REQUIRED_RATINGS_STATES = (
        ("0", "Не загружены"),
        ("1", "Загружены")
    )
    UNFORCED_RATINGS_STATES = (
        ("0", "Не загружены"),
        ("1", "Загружены частично"),
        ("2", "Загружены")
    )

    platform_responsible_STATES = (
        ("0", "Не выбрано"),
        ("1", "Шарыпова Е.А."),
        ("2", "Рачёва Н.И.")
    )
    owner_responsible_STATES = (
        ("0", "Не выбрано"),
        ("1", "Шарыпова Е.А."),
        ("2", "Рачёва Н.И.")
    )
    passport_responsible_STATES = (
        ("0", "Не выбрано"),
        ("1", "Возисова О.С."),
        ("2", "Талапов В.А.")
    )

    communication_owner = models.CharField("Статус коммуникации с правообладателем", max_length=1,
                                           choices=COMMUNICATION_OWNER_STATES, default="0")
    communication_platform = models.CharField("Статус коммуникации с платформой", max_length=1,
                                              choices=COMMUNICATION_PLATFORM_STATES, default="0")
    expertise_status = models.CharField("Статус экспертизы", max_length=1, choices=EX_STATES, default="0")
    passport_status = models.CharField("Статус паспорта", max_length=1, choices=PASSPORT_STATES, default="0")
    roo_status = models.CharField("Статус загрузки на роо", max_length=1, choices=ROO_STATES, default="0")
    required_ratings_state = models.CharField("Состояние загрузки обязательных оценок", max_length=1,
                                              choices=REQUIRED_RATINGS_STATES, default="0")
    unforced_ratings_state = models.CharField("Состояние загрузки добровольных оценок", max_length=1,
                                              choices=UNFORCED_RATINGS_STATES, default="0")
    comment = models.TextField("Примечание Шарыпова-Рачёва", blank=True, null=True)
    expert_access = models.CharField("Доступ к курсу для экспертов обязательной оценки", choices=EX_ACCESSES,
                                     max_length=1, default="0")
    reg_data = models.TextField("Регистрационные данные для доступа к курсу", blank=True)
    contacts = models.TextField("Контакты", blank=True, null=True)

    platform_responsible = models.CharField("Ответсвенный за платформу", max_length=1,
                                            choices=platform_responsible_STATES, default="0", blank=True, null=True)
    owner_responsible = models.CharField("Ответсвенный за правообладателя", max_length=1,
                                         choices=owner_responsible_STATES, default="0", blank=True, null=True)
    unapproved_changes = models.TextField("Несогласованные изменения", blank=True, null=True)

    # responsible_comment = models.TextField("Комментарий ответсвенного", blank=True, null=True)
    platform_responsible_comment = models.TextField("Комментарий ответсвенного за платформу", blank=True, null=True)
    owner_responsible_comment = models.TextField("Комментарий ответсвенного за правообладателя", blank=True, null=True)

    passport_responsible = models.CharField("Ответсвенный за паспорт", max_length=1,
                                            choices=passport_responsible_STATES, default="0", null=True, blank=True)

    identical = models.CharField("Список таких же", max_length=512, default="[]", null=True, blank=True)
    in_archive = models.BooleanField("Курс находится в архиве", default=False)
    course_item_url = models.CharField("Ссылка на РОО", max_length=512, blank=True, null=True)
    redacted = models.BooleanField("Подверглось редакторской правке", default=False)

    def get_required_expertises_links(self):
        ex_links = ""
        exs = Expertise.objects.filter(course=self, type="0")
        for idx, ex in enumerate(exs):
            ex_links += ("\n" if idx > 0 else "") + "http://openedu.urfu.ru/roo/expertise/" + str(ex.pk) + "/"
        return ex_links

    def append_identaical(self, x):
        if str(x.pk) not in [x['id'] for x in json.loads(self.identical)]:
            identical_list = json.loads(self.identical)
            identical_list.append({"id": str(x.pk)})
            self.identical = json.dumps(identical_list)
            self.save()
        else:
            pass

    def get_identical(self):
        result = Course.objects.filter(in_archive=False, pk__in=[x['id'] for x in json.loads(self.identical)])
        return result

    def find_identical(self):
        courses_identical = []
        if self.institution is not None:
            courses_identical = Course.objects.filter(in_archive=False, title=self.title,
                                                      institution__title=self.institution.title,
                                                      partner__title=self.partner.title).exclude(id=self.id)
        # else:
        #     courses_identical = Course.objects.filter(title=self.title, partner__title=self.partner.title)
        return courses_identical

    def set_identical(self):
        self.identical = "[]"
        self.save()
        for course in self.find_identical():
            self.append_identaical(course)
            course.identical = "[]"
            course.save()
            for sub_course in course.find_identical():
                course.append_identaical(sub_course)
        self.save()

    def natural_key(self):
        return (self.title, self.partner.title, self.institution.title, self.global_id, self.id)

    def __str__(self):
        return f"Онлайн-курс: {self.title}"

    class Meta:
        verbose_name = 'онлайн-курс'
        verbose_name_plural = 'онлайн-курсы'

    def get_image(self):
        if self.image:
            return f"<img height=\"100\" src=\"{self.image}\"></img>"
        else:
            return ""

    def get_description(self):
        return truncatewords_html(self.description, 15)

    def has_gid(self):
        return self.global_id != ""

    def get_platform(self):
        if self.partner:
            if self.partner.image:
                return f"<img height=\"100\" src=\"{self.partner.image}\"></img><p>{self.partner.title}</p>"

    @classmethod
    def find_duplicates(cls):
        for c in cls.objects.filter(in_archive=False):
            c.set_identical()
            c.save()

    @classmethod
    def get_passport_responsibles(cls):
        rs = []
        for r in cls.passport_responsible_STATES[1:]:
            rs.append(cls.objects.filter(in_archive=False, passport_responsible=r[0]).count())

        return f'''
          <div class="statistic">
            <div class="value">
              {rs[0]}
            </div>
            <div class="label">
              Возисова О.С.
            </div>
          </div>
          <div class="statistic">
            <div class="value">
              {rs[1]}
            </div>
            <div class="label">
              Талапов В.А.
            </div>
          </div>
        '''

    get_image.allow_tags = True
    get_description.allow_tags = True
    get_platform.allow_tags = True
    get_passport_responsibles.allow_tags = True

    get_image.short_description = "Изображение курса"
    get_description.short_description = "Описание"
    get_platform.short_description = "Платформа"

    def update_from_dict(self, d):
        for attr, val in d.items():
            if attr == "teachers":
                for teacher in d['teachers']:
                    if self.teachers.filter(title=teacher['title']).count() == 0:
                        t = Teacher(image=teacher['image'], description=teacher['description'], title=teacher['title'])
                        t.save()
                        self.teachers.add(t)
            elif attr == "directions":
                for direction in d["directions"]:
                    direction_object = Direction.objects.get(code=direction)
                    self.directions.add(direction_object)
            elif attr == "activities":
                for activity in d["activities"]:
                    activity_object = Area.objects.get(global_id=int(activity))
                    self.activities.add(activity_object)
            elif attr == "institution_id":
                institution_object = Owner.objects.get(global_id=d["institution_id"])
                self.institution = institution_object
                self.save()
            elif attr == "partner_id":
                partner_object = Platform.objects.get(global_id=d["partner_id"])
                self.partner = partner_object
                self.save()
            elif attr == "has_sertificate":
                if val:
                    self.has_sertificate = "1"
                else:
                    self.has_sertificate = "2"
            else:
                try:
                    setattr(self, attr, val)
                except:
                    pass

            # self.set_identical()  # Надо ли вот
            # self.in_archive = False  # это вот все?
            # self.communication_owner = 5
            # self.communication_platform = 5
            self.save()

    def update_field_from_dict(self, d, attr):

        if attr == "teachers":
            for teacher in d['teachers']:
                if self.teachers.filter(title=teacher['title']).count() == 0:
                    t = Teacher(image=teacher['image'], description=teacher['description'], title=teacher['title'])
                    t.save()
                    self.teachers.add(t)
        elif attr == "directions":
            for direction in d["directions"]:
                direction_object = Direction.objects.get(code=direction)
                self.directions.add(direction_object)
        elif attr == "activities":
            for activity in d["activities"]:
                activity_object = Area.objects.get(global_id=int(activity))
                self.activities.add(activity_object)
        elif attr == "institution_id":
            institution_object = Owner.objects.get(global_id=d["institution_id"])
            self.institution = institution_object
        elif attr == "partner_id":
            partner_object = Platform.objects.get(global_id=d["partner_id"])
            self.partner = partner_object
        else:
            # try:
            setattr(self, attr, d[attr])
            # except:
            #     pass

        # self.set_identical()  # Надо ли вот
        # self.in_archive = False  # это вот все?
        # self.communication_owner = 5
        # self.roo_status = "3"

        return self
        # self.save()

    def send_to_roo(self):
        def clean_empty(d):
            if not isinstance(d, (dict, list)):
                return d
            if isinstance(d, list):
                return [v for v in (clean_empty(v) for v in d) if v]
            return {k: v for k, v in ((k, clean_empty(v)) for k, v in d.items()) if v}

        passport = ""

        course = self
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

        try:
            new_course['duration'] = {"code": "week", "value": int(new_course["duration"])}
        except:
            pass
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
            new = False
            passport["package"]["items"][0]["id"] = passport["package"]["items"][0]["global_id"]
            r = requests.Request('PUT', 'https://online.edu.ru/api/courses/v0/course', headers={'Authorization': 'Basic bi52LmlnbmF0Y2hlbmtvOl9fX0NhbnRkM3N0cm9Z'}, json=passport)  # токен на Никиту
        else:
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

        print(re_resp)

    @classmethod
    def create_from_dict(cls, d):
        c = cls.objects.create(title=d["title"])
        for attr, val in d.items():
            if attr == "teachers":
                for teacher in d['teachers']:
                    t = Teacher(image=teacher['image'], description=teacher['description'], title=teacher['title'])
                    t.save()
                    c.teachers.add(t)
            elif attr == "directions":
                for direction in d["directions"]:
                    direction_object = Direction.objects.get(code=direction)
                    c.directions.add(direction_object)
            elif attr == "activities":
                for activity in d["activities"]:
                    activity_object = Area.objects.get(global_id=int(activity))
                    c.activities.add(activity_object)
            elif attr == "institution_id":
                institution_object = Owner.objects.get(global_id=d["institution_id"])
                c.institution = institution_object
                c.save()
            elif attr == "partner_id":
                partner_object = Platform.objects.get(global_id=d["partner_id"])
                c.partner = partner_object
                c.save()
            elif attr == "has_sertificate":
                if val:
                    c.has_sertificate = "1"
                else:
                    c.has_sertificate = "2"
            else:
                try:
                    setattr(c, attr, val)
                except:
                    pass
            c.communication_owner = 5
            c.communication_platform = 5
            c.roo_status = 3
            c.save()
        return c

    @classmethod
    def updade_courses_from_roo(cls):
        login = 'vesloguzov@gmail.com'
        password = 'ye;yj,jkmitrjlf'

        def levenshtein_equal(a, b):
            return True if fuzz.token_sort_ratio(a, b) > 0.95 else False

        def almost_equal(raw_a, raw_b, field_name):

            a = raw_a
            b = raw_b

            if a == "None":
                a = None
            if b == "None":
                b = None

            if a is None and b is None:
                return True, a, b

            if 'ManyRelatedManager' in str(type(a)) and isinstance(b, list):
                if field_name in ["activities"]:
                    a = [item.global_id for item in a.all()]
                elif field_name in ["teachers"]:
                    a = [item.title for item in a.all()]
                    b = [item["title"] for item in b]
                elif field_name in ["directions"]:
                    a = [item.code for item in a.all()]
                return set(a) == set(b), raw_a, raw_b

            elif isinstance(a, str) and isinstance(b, str):
                return levenshtein_equal(a, b), raw_a, raw_b

            else:
                if field_name in ["visitors_number", "rating", "duration", "visitors_rating_count", "lectures_number",
                                  "expert_rating_count"]:
                    return str(b) in str(a).split(' '), raw_a, raw_b
                elif field_name == "partner_id":
                    a = Platform.objects.get(pk=a)
                    a = a.global_id
                elif field_name == "institution_id":
                    a = Owner.objects.get(pk=a)
                    a = a.global_id
                elif field_name in ["has_sertificate"]:
                    if a == "1":
                        a = True
                    else:
                        a = False
                elif field_name in ["accreditation", "requirements", "competences", "description", "credits"]:
                    if not a or a == "":
                        a = ""
                    if not b or b == "":
                        b = ""
                    return levenshtein_equal(a, b), raw_a, raw_b

                if (a is None or b is None) and a != b:
                    return False, raw_a, raw_b

                return a == b, raw_a, raw_b

        def find_actual(fieldname, a, b):
            if a == "":
                a = None
            if b == "":
                b = None

            if a is None and b is not None:
                return {"value": b, "source": "roo"}
            if b is None and a is not None:
                return {"value": a, "source": "our"}

            if fieldname in ["partner_id", "institution_id"]:
                return {"value": b, "source": "roo"}

            if fieldname in ["activities", "teachers", "directions"]:
                if len(b) > len(a):
                    return {"value": b, "source": "roo"}
                else:
                    return {"value": a, "source": "our"}

            return {"value": a, "source": "our"}

        def get_courses_from_page(page_url):
            request = requests.get(page_url, auth=(login, password), verify=False)
            response = request.json()
            courses = response["rows"]
            for c in courses:
                r = requests.get(f"https://online.edu.ru/api/courses/v0/course/{c['global_id']}",
                                 auth=('vesloguzov@gmail.com', 'ye;yj,jkmitrjlf'), verify=False)
                course = r.json()
                try:
                    roo_course = cls.objects.filter(global_id=course['global_id']).first()

                except cls.DoesNotExist:

                    try:
                        roo_course = cls.objects.filter(in_archive=False, title=course['title'],
                                                        partner__global_id=course['partner_id'],
                                                        institution__global_id=course['institution_id']).first()
                    except:
                        roo_course = None

                if roo_course:
                    print(f"-----------{roo_course}-------------")
                    diff = dict()
                    for field in course.keys():
                        is_almost_equal, almost_equal_a, almost_equal_b = almost_equal(getattr(roo_course, field), course[field], field)
                        if not is_almost_equal:

                            # if field == "teachers":
                            # print(field, almost_equal_a, almost_equal_b)
                            if field in ["activities", "teachers", "directions"]:
                                almost_equal_a = [x.get_json() for x in almost_equal_a.all()]

                            diff[field] = {"our": almost_equal_a, "roo": almost_equal_b, "actual": find_actual(field, almost_equal_a, almost_equal_b)}

                            if diff[field]['actual']['source'] == "roo":
                                print("Я перезаписываю: ", roo_course.id, field, diff[field]['actual'])
                                roo_course = roo_course.update_field_from_dict(course, field)
                                print(roo_course)
                                roo_course.save()
                    roo_course.roo_status = 3
                    roo_course.save()

                    if len(diff.keys()) > 0:
                        course_diff, created = CourseDiff.objects.get_or_create(course=roo_course)

                        course_diff.diff = json.dumps(diff)
                        course_diff.save()

                    # print(field, '-------', getattr(roo_course, field), course[field])

                # if roo_course:
                #     if not roo_course.newest:
                #         roo_course.update_from_dict(course)
                else:
                    print(course)
                    roo_course = Course.create_from_dict(course)
                    roo_course.save()

            if response["next"] is not None:
                get_courses_from_page(response["next"])
            else:
                return

        get_courses_from_page('https://online.edu.ru/api/courses/v0/course')

        # logger.info("Закончили Courses: {0}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))


class Platform(Base):
    objects = PlatformManager()

    title = models.CharField("Наименование", blank=True, null=True, max_length=1024)
    global_id = models.CharField("ИД платформы на РОО", null=True, blank=True, max_length=512)
    image = models.CharField("Изображение платформы", blank=True, null=True, max_length=512)
    url = models.CharField("Ссылка на сайт платформы", blank=True, null=True, max_length=512)
    description = models.TextField("Описание платформы", blank=True, null=True)
    ogrn = models.CharField("ОГРН", blank=True, null=True, max_length=512)
    contacts = models.TextField("Контакты", blank=True, null=True)

    def natural_key(self):
        return self.title

    def get_image(self):
        if self.image:
            return f"<img height=\"200\" src=\"{self.image}\"></img>"
        else:
            return ""

    def get_description(self):
        return truncatewords_html(self.description, 15)

    get_image.allow_tags = True
    get_description.allow_tags = True
    get_image.short_description = "Изображение"
    get_description.short_description = "Описание"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'платформа'
        verbose_name_plural = 'платформы'

    @classmethod
    def get(cls):
        cls.update_base_from_roo('https://online.edu.ru/ru/api/partners/v0/platform', 'global_id')

        # logger.info("Закончили Platform: {0}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))


class Expert(models.Model):
    login = models.CharField("Логин эксперта", blank=True, null=True, max_length=512)
    expert = models.TextField(blank=True)
    contacts = models.TextField(blank=True)

    def natural_key(self):
        return (self.expert)

    def __str__(self):
        if self.expert:
            return self.expert
        else:
            return self.login

    class Meta:
        verbose_name = 'эксперт'
        verbose_name_plural = 'эксперт'


class Owner(Base):
    objects = OwnerManager()

    title = models.CharField("Наименование", blank=True, null=True, max_length=512)
    global_id = models.CharField("ИД Правообладателя на РОО", max_length=512, null=True, blank=True, db_index=True)
    ogrn = models.CharField("ОГРН", blank=True, null=True, max_length=512)
    image = models.CharField("Изображение", blank=True, null=True, max_length=1024)
    contacts = models.TextField("Контакты", blank=True, null=True)
    from_roo = models.BooleanField("Существует на РОО", default=True)

    def natural_key(self):
        return (self.title)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'правообладатель'
        verbose_name_plural = 'правообладатели'

    def get_image(self):
        if self.image:
            return f"<img height=\"100\" src=\"{self.image}\"></img>"
        else:
            return ""

    get_image.allow_tags = True
    get_image.short_description = "Изображение курса"

    # def save(self, *args, **kwargs):
    #
    #     rdata = {
    #         "q": f"logo {self.title}",
    #         "num": 1,
    #         "start": 1,
    #         # "filetype": "jpg",
    #         "key": "AIzaSyBaLNSE02AM6vjEJ9npNwD9uagQzSlMnhg",
    #         "cx": "012036972007253236562:btl9gjd-nti",
    #         "searchType": "image",
    #         "gl": "ru",
    #     }
    #
    #     r = requests.get("https://www.googleapis.com/customsearch/v1", params=urlencode(rdata))
    #     items = json.loads(r.content).get("items", None)
    #     if items:
    #         self.image = items[0]["link"]
    #     super(Owner, self).save(*args, **kwargs)

    @classmethod
    def get(cls):
        cls.update_base_from_roo('https://online.edu.ru/api/partners/v0/rightholder', 'title')

        # logger.info("Закончили Owner: {0}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))


class Area(Base):
    title = models.CharField("Наименование", blank=True, null=True, max_length=512)
    global_id = models.CharField("ИД областей деятельности на РОО", blank=True, null=True, max_length=512,
                                 db_index=True)

    def __str__(self):
        return self.title

    def get_json(self):
        return {
            "title": self.title,
            "global_id": self.global_id
        }

    class Meta:
        verbose_name = 'область деятельности'
        verbose_name_plural = 'области деятельности'

    @classmethod
    def get(cls):
        cls.update_base_from_roo('https://online.edu.ru/api/courses/v0/activity', 'title')


class Direction(models.Model):
    title = models.CharField("Наименование направления", blank=True, null=True, max_length=512, db_index=True)
    activity = models.ForeignKey("Area", verbose_name="Область деятельности", null=True)
    # activity_title = models.CharField("Наименование области деятельности", blank=True, null=True, max_length=512)
    code = models.CharField("Код направления", blank=True, null=True, max_length=512, db_index=True)

    def __str__(self):
        return f"направление подготовки: {self.title}"

    def get_json(self):
        return {
            "title": self.title,
            "activity": self.activity.get_json(),
            "code": self.code
        }

    class Meta:
        verbose_name = 'направление подготовки'
        verbose_name_plural = 'направления подготовки'

    def update_from_dict(self, d):
        for attr, val in d.items():
            if attr == "activity_id":
                print(d["activity_id"], type(d["activity_id"]))
                activity_object = Area.objects.get(global_id=d["activity_id"])
                self.activity = activity_object
                self.save()
            else:
                setattr(self, attr, val)
                self.save()

    @classmethod
    def create_from_dict(cls, d):
        c = cls.objects.create(title=d["title"])
        for attr, val in d.items():
            if attr == "activity_id":
                activity_object = Area.objects.get(global_id=d["activity_id"])
                c.activity = activity_object
                c.save()
            else:
                setattr(c, attr, val)
                c.save()

    @classmethod
    def update_base_from_roo(cls, url):
        login = 'vesloguzov@gmail.com'
        password = 'ye;yj,jkmitrjlf'

        def get_base_from_page(cls, page_url):
            request = requests.get(page_url, auth=(login, password), verify=False)
            response = request.json()
            items = response["rows"]
            for item in items:
                try:
                    roo_base = cls.objects.get(title=item["title"])
                except:
                    roo_base = None

                if roo_base:
                    roo_base.update_from_dict(item)
                else:
                    cls.create_from_dict(item)

        get_base_from_page(cls, url)

    @classmethod
    def get(cls):
        cls.update_base_from_roo('https://online.edu.ru/api/courses/v0/direction')


class ChoiceColumn(tables.Column):
    def __init__(self, choices, *args, **kwargs):
        self.choices = choices
        super(ChoiceColumn, self).__init__(*args, **kwargs)

    def render(self, value):
        return self.get_display(value)

    def get_display(self, value):
        return self.choices[int(value)][1]


class CoursesTable(tables.Table):
    class Meta:
        model = Course
        template_name = "django_tables2/bootstrap.html"
        exclude = (
            "credits", "record_end_at", "global_id", "created_at", "visitors_rating", "duration", "finished_at",
            "language",
            "content", "started_at", "started_at", "requirements", "competences", "accreditation", "description",
            "image")
        fields = (
            "title", "partner", "platform_responsible", "institution", "owner_responsible", "communication_owner",
            "communication_platform", "expertise_status",
            "passport_status", "required_ratings_state", "unforced_ratings_state", "comment", "roo_status",
            "responsible_comment", "passport_responsible")
        attrs = {'class': 'ui celled striped table', 'id': 'coursesTable'}

    title = tables.TemplateColumn(
        '<a href="#" onClick="CourseEdit=window.open(\'http://openedu.urfu.ru/roo/{{ record.id }}\',\'{{ record.title }}\',width=600,height=300); return false;">{{ record.title }}</a',
        footer="Наименование")
    competences = tables.TemplateColumn('{{ record.description | truncatewords_html:5 |safe}}')
    description = tables.TemplateColumn('{{ record.description | truncatewords_html:5 |safe}}')
    content = tables.TemplateColumn('{{ record.description | truncatewords_html:5 |safe}}')
    image = tables.TemplateColumn('<img src="{{record.image}}" height="100"/>')


class ExpertisesTable(tables.Table):
    class Meta:
        model = Expertise
        template_name = "django_tables2/bootstrap.html"
        fields = ("course", "state", "date", "type", "executed", "expert", "supervisor", "organizer", "comment")
        attrs = {'class': 'ui celled striped table', 'id': 'expertisesTable'}

    course = tables.TemplateColumn(
        '<a href="#" onClick="ExpertiseEdit=window.open(\'http://openedu.urfu.ru/roo/expertise/{{ record.id }}\',\'{{ record.course }}\',width=600,height=300); return false;">{{ record.course }}</a',
        footer="Курс")


class SendedCourse(models.Model):
    title = models.CharField("Наименование", blank=False, null=False, max_length=2048)
    course_json = models.TextField("Отправленный JSON", blank=False, null=False)
    expertise_json = models.TextField("JSON обязательной экспертизы", blank=False, null=False)
    date = models.DateTimeField("Дата и время отправки", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'отправленный курс'
        verbose_name_plural = 'отправленные курсы'
