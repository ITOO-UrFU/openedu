import requests
# from time import gmtime, strftime
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import truncatewords_html, truncatewords
import requests
import json
from urllib.parse import urlencode
import django_tables2 as tables


# import logging

# logger = logging.getLogger('celery_logging')


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
        (0, "Обязательная"),
        (1, "ОО"),
        (2, "Независимая"),
        (3, "Работодатель"),
        (4, "Пользовательская"),
        (5, "ФУМО"),
        (6, "Большие данные"),
        (7, "Лучшие практики")
    )
    course = models.ForeignKey("Course", verbose_name="Курс", null=True, blank=True)
    state = models.CharField("состояние процесса (этап)", blank=True, null=True, max_length=512)
    date = models.DateField("Дата", blank=True, null=True)
    ex_date = models.CharField("Дата", blank=True, null=True, max_length=512)
    type = models.CharField("Вид экспертизы", choices=EX_TYPES,
                            blank=True, null=True, max_length=1)
    executed = models.BooleanField("Отметка об исполнении эксперизы", default=True)
    # passed = models.BooleanField("Прошел обязательную экспертизу")
    expert = models.ForeignKey("Expert", verbose_name="Эксперт", null=True, blank=True)
    supervisor = models.CharField("Кто от ИТОО контролирует", blank=True, null=True, max_length=512)
    organizer = models.CharField("Организатор экспертизы сотрудники или партнеры", blank=True, null=True,
                                 max_length=512)
    comment = models.TextField("Примечание", blank=True, null=True)
    comment_fieldset_1 = models.TextField("Комментарии по отсутствию обязательных полей ОК", blank=True, null=True)
    comment_fieldset_2 = models.TextField("Комментарии по отсутствию обязательных полей ОК претендующих на зачет ОП", blank=True, null=True)

    # Passport
    has_length = models.BooleanField("Длительность", default=False)
    has_description = models.BooleanField("Описание", default=False)
    has_authors = models.BooleanField("Авторы", default=False)
    language = models.CharField("Язык содержания", default="русский", max_length=255)
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
    language_video = models.CharField("Язык видео", default="русский", max_length=255)
    language_subtitles = models.CharField("Язык субтитров", default="русский", max_length=255)
    has_course_subject = models.BooleanField("Предмет курса", default=False)
    is_open = models.BooleanField("Открытость курса", default=False)
    has_expertises_types = models.BooleanField("Типы экспертиз для допуска", default=False)
    has_ownership_document_scan = models.BooleanField("Скан документа, подтверждающего правообладание", default=False)
    has_not_prohibited = models.BooleanField("В курсе отсутствуют запрещенные материалы", default=False)
    has_text_materials = models.BooleanField("Текстовые материалы", default=False)
    has_illustrations = models.BooleanField("Иллюстрации", default=False)
    has_audio = models.BooleanField("Аудиоматериалы", default=False)
    has_video = models.BooleanField("Видеоматериалы", default=False)
    has_quality_checking = models.BooleanField("прошел проверку обязательной оценки качества", default=False)
    got_into_record = models.CharField("попал в отчет", max_length=255, null=True, blank=True)
    got_expertise_2018 = models.BooleanField("прошел экспертизу в 2018 (1 квартал)", default=False)
    additional_info = models.TextField("Дополнительная информация", null=True, blank=True)

    def get_platform(self):
        return self.course.platform.title

    def __str__(self):
        return f"Экспертиза: {self.course}, Тип: {self.type}"

    class Meta:
        verbose_name = 'экспертиза'
        verbose_name_plural = 'экспертизы'


class Teacher(models.Model):
    title = models.CharField("ФИО лектора", blank=True, null=True, max_length=512)
    image = models.CharField("Ссылка на изображение", blank=True, null=True, max_length=512)
    description = models.TextField("Описание", blank=True, null=True)

    def __str__(self):
        return f"Лектор: {self.title}"

    def get_image(self):
        if self.image:
            return "<img height=\"100\" src=\"" + self.image + "\"></img>"
        else:
            return ""

    get_image.allow_tags = True

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
    correlating = models.TextField("Соотнесение компетенции и индикаторов ее достижения с компетенциями, включенными в ФГОС и ПООП", blank=True)


class Result(models.Model):
    title = models.TextField("Результат обучения", blank=True)
    competence = models.ForeignKey("Competence")


class EvaluationTool(models.Model):
    title = models.TextField("Оценочное средство", blank=True)
    result = models.ForeignKey("Result")


class ProctoringService(models.Model):
    title = models.CharField("Сервис прокторинга", max_length=255, blank=False, null=False)


class Course(models.Model):
    #  что приходит в api сейчас
    credits = models.CharField("Массив перезачётов", blank=True, null=True, max_length=512)
    record_end_at = models.CharField("Дата окончания записи на курс", blank=True, null=True, max_length=512)
    title = models.CharField("Наименование", blank=True, null=True, max_length=512)
    image = models.URLField("Изображение курса", blank=True, null=True)
    institution = models.ForeignKey("Owner", verbose_name="Правообладатель", blank=True, null=True)
    global_id = models.CharField("ИД курса на РОО", blank=True, null=True, max_length=512)
    created_at = models.CharField("Дата создания онлайн-курса", blank=True, null=True, max_length=512)
    visitors_rating = models.CharField("Оценка посетителей РОО", blank=True, null=True,
                                       max_length=512)  # но это не точно
    duration = models.CharField("Длительность в неделях", blank=True, null=True, max_length=512)
    finished_at = models.CharField("Дата окончания онлайн-курса", blank=True, null=True, max_length=512)
    competences = models.TextField("Формируемые компетенции", blank=True, null=True, max_length=512)
    accreditation = models.TextField("Аккредитация", blank=True, null=True, max_length=512)
    description = models.TextField("Описание", blank=True, null=True)
    visitors_number = models.IntegerField("Количество записавшихся на курс", blank=True, null=True)
    directions = models.ManyToManyField("Direction", verbose_name="Массив идентификаторов направлений")  # массив
    expert_rating_count = models.CharField("Количество оценок экспертов", blank=True, null=True,
                                           max_length=512)  # сильно не точно
    has_sertificate = models.BooleanField("Возможность получить сертификат",
                                          default=False)  # слово сертификат у них неправильно
    language = models.CharField("Язык контента", blank=True, null=True, max_length=512)
    course_item_url = models.CharField("", blank=True, null=True, max_length=512)  # неизвестная вестчь
    partner = models.ForeignKey("Platform", verbose_name="Платформа", null=True)
    content = models.TextField("Содержание онлайн-курса", blank=True, null=True, max_length=512)
    started_at = models.CharField("Дата ближайшего запуска", blank=True, null=True, max_length=512)
    rating = models.CharField("Рейтинг пользователей", blank=True, null=True, max_length=512)
    external_url = models.CharField("Ссылка на онлайн-курс на сайте Платформы", blank=True, null=True, max_length=512)
    lectures_number = models.IntegerField("Количество лекций", blank=True, null=True)
    version = models.IntegerField("Версия курса", default=0)
    activities = models.ManyToManyField("Area", verbose_name="Массив идентификаторов областей деятельности")  # массив
    visitors_rating_count = models.CharField("Количество пользовательских оценок", blank=True, null=True,
                                             max_length=512)  # наверно
    total_visitors_number = models.CharField("Количество слушателей", blank=True, null=True,
                                             max_length=512)
    experts_rating = models.CharField("Рейтинг экспертов", blank=True, null=True, max_length=512)
    requirements = models.TextField("Массив строк-требований", blank=True, null=True)  # массив
    cabinet_course_url = models.CharField("Ссылка на курс в кабинете", blank=True, null=True, max_length=512)
    teachers = models.ManyToManyField("Teacher", blank=True)  # список лекторов/аторов
    admin_email = models.CharField("Адрес эл. почты администратора ОК", blank=True, null=True, max_length=512)

    # наши поля
    newest = models.BooleanField("Самое новое содержание курса", default=False)

    # необязательные поля
    # learning_plan = models.TextField("Учебный план", blank=True, null=True)
    results = models.ManyToManyField("Result", blank=True)
    evaluation_tools = models.ManyToManyField("EvaluationTool", blank=True)
    proctoring_service = models.ForeignKey("ProctoringService", blank=True, null=True)
    expert_account = models.TextField("Доступ эксперта", blank=True, null=True)

    COMMUNICATION_OWNER_STATES = (
        (0, "Согласование не начато"),
        (1, "В процессе согласования"),
        (2, "Требуется участие администрации"),
        (3, "Согласовано"),
        (4, "Отказано"),
        (5, "Согласовано с РОО")
    )

    COMMUNICATION_PLATFORM_STATES = (
        (0, "Согласование не начато"),
        (1, "В процессе согласования"),
        (2, "Требуется участие администрации"),
        (3, "Согласовано"),
        (4, "Отказано"),
        (5, "Согласовано с РОО")
    )

    EX_STATES = (
        (0, "Не проводилась"),
        (1, "Отравлен на экспертизу"),
        (2, "Требует доработки"),
        (3, "Прошел"),
        (4, "Отправлен запрос на доступ к платформе"),
        (5, "Доступ предоставлен")
    )
    PASSPORT_STATES = (
        (0, "Не заполнен"),
        (1, "Не проверен"),
        (1, "Требует доработки"),
        (2, "На согласовании с правообладателем"),
        (3, "Готов"),
    )

    EX_ACCESSES = (
        (0, "Не предоставлен"),
        (1, "Отправлен запрос"),
        (2, "Предоставлен"),
    )

    ROO_STATES = (
        (0, "Не готов"),
        (1, "Ждем ID платформы"),
        (2, "К загрузке"),
        (3, "Загружен"),
        (4, "Ожидает загрузки с РОО")
    )

    REQUIRED_RATINGS_STATES = (
        (0, "Не загружены"),
        (1, "Загружены")
    )
    UNFORCED_RATINGS_STATES = (
        (0, "Не загружены"),
        (1, "Загружены частично"),
        (2, "Загружены")
    )

    communication_owner = models.CharField("Статус коммуникации с правообладателем", max_length=1,
                                           choices=COMMUNICATION_OWNER_STATES, default=0)
    communication_platform = models.CharField("Статус коммуникации с платформой", max_length=1,
                                              choices=COMMUNICATION_PLATFORM_STATES, default=0)
    expertise_status = models.CharField("Статус экспертизы", max_length=1, choices=EX_STATES, default=0)
    passport_status = models.CharField("Статус паспорта", max_length=1, choices=PASSPORT_STATES, default=0)
    roo_status = models.CharField("Статус загрузки на роо", max_length=1, choices=ROO_STATES, default=0)
    required_ratings_state = models.CharField("Состояние загрузки обязательных оценок", max_length=1,
                                              choices=REQUIRED_RATINGS_STATES, default=0)
    unforced_ratings_state = models.CharField("Состояние загрузки добровольных оценок", max_length=1,
                                              choices=UNFORCED_RATINGS_STATES, default=0)
    comment = models.TextField("Примечание", blank=True, null=True)
    expert_access = models.CharField("Доступ к курсу для экспертов обязательной оценки", choices=EX_ACCESSES, max_length=1, default=0)
    reg_data = models.TextField("Регистрационные данные для доступа к курсу", blank=True)
    contacts = models.TextField("Контакты", blank=True, null=True)

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

    def get_platform(self):
        if self.partner:
            if self.partner.image:
                return f"<img height=\"100\" src=\"{self.partner.image}\"></img><p>{self.partner.title}</p>"

    get_image.allow_tags = True
    get_description.allow_tags = True
    get_platform.allow_tags = True

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
            else:
                setattr(self, attr, val)
            self.communication_owner = 5
            self.communication_platform = 5
            self.save()

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
            else:
                setattr(c, attr, val)
            c.communication_owner = 5
            c.communication_platform = 5
            c.roo_status = 3
            c.save()
        return c

    @classmethod
    def updade_courses_from_roo(cls):
        login = 'vesloguzov@gmail.com'
        password = 'ye;yj,jkmitrjlf'

        def get_courses_from_page(page_url):
            request = requests.get(page_url, auth=(login, password), verify=False)
            response = request.json()
            courses = response["rows"]
            for c in courses:
                r = requests.get(f"https://online.edu.ru/api/courses/v0/course/{c['global_id']}",
                                 auth=('vesloguzov@gmail.com', 'ye;yj,jkmitrjlf'), verify=False)
                course = r.json()
                print(course["title"])
                try:
                    roo_course = cls.objects.filter(global_id=course['global_id']).first()

                except cls.DoesNotExist:
                    roo_course = None

                if roo_course:

                    if not roo_course.newest:
                        roo_course.update_from_dict(course)
                else:
                    roo_course = Course.create_from_dict(course)

                #roo_course.save()

            if response["next"] is not None:
                get_courses_from_page(response["next"])
            else:
                return

        get_courses_from_page('https://online.edu.ru/api/courses/v0/course')

        # logger.info("Закончили Courses: {0}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))


class Platform(Base):
    title = models.CharField("Наименование", blank=True, null=True, max_length=1024)
    global_id = models.CharField("ИД платформы на РОО", null=True, blank=True, max_length=512)
    image = models.CharField("Изображение платформы", blank=True, null=True, max_length=512)
    url = models.CharField("Ссылка на сайт платформы", blank=True, null=True, max_length=512)
    description = models.TextField("Описание платформы", blank=True, null=True)
    ogrn = models.CharField("ОГРН", blank=True, null=True, max_length=512)
    contacts = models.TextField("Контакты", blank=True, null=True)

    # наши поля
    # newest = models.BooleanField("Самое новое содержание курса", default=False)

    # person = models.CharField("Данные контактного лица правообладателя телефон, почта", blank=True, null=True,
    #                           max_length=512)
    # connection_form = models.CharField("Форма связи с контактным лицом", blank=True, null=True, max_length=512)
    # connection_date = models.DateField("Дата связи с контактным лицом", blank=True, null=True)
    # contacts = models.CharField("Контакты института", blank=True, null=True, max_length=512)

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

    def __str__(self):
        if self.expert:
            return f"Эксперт: {self.expert}"
        else:
            return f"Эксперт: {self.login}"

    class Meta:
        verbose_name = 'эксперт'
        verbose_name_plural = 'эксперт'


class Owner(Base):
    title = models.CharField("Наименование", blank=True, null=True, max_length=512)
    global_id = models.CharField("ИД Правообладателя на РОО", max_length=512, null=True, db_index=True)
    ogrn = models.CharField("ОГРН", blank=True, null=True, max_length=512)
    image = models.CharField("Изображение", blank=True, null=True, max_length=1024)
    contacts = models.TextField("Контакты", blank=True, null=True)
    from_roo = models.BooleanField("Существует на РОО", default=True)

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

    class Meta:
        verbose_name = 'область деятельности'
        verbose_name_plural = 'области деятельности'

    @classmethod
    def get(cls):
        cls.update_base_from_roo('https://online.edu.ru/api/courses/v0/activity', 'title')

        # logger.info("Закончили Areas: {0}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))


class Direction(models.Model):
    title = models.CharField("Наименование направления", blank=True, null=True, max_length=512, db_index=True)
    activity = models.ForeignKey("Area", verbose_name="Область деятельности", null=True)
    # activity_title = models.CharField("Наименование области деятельности", blank=True, null=True, max_length=512)
    code = models.CharField("Код направления", blank=True, null=True, max_length=512, db_index=True)

    def __str__(self):
        return f"направление подготовки: {self.title}"

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

        # logger.info("Закончили Direction: {0}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))


class ChoiceColumn(tables.Column):
    def __init__(self, choices, *args, **kwargs):
        self.choices = choices
        super(ChoiceColumn, self).__init__(*args, **kwargs)

    def render(self, value):
        return self.get_display(value)

    def get_display(self, value):
        try:
            return self.choices[int(value)][1]
        except:
            return "Ошибка"


class CoursesTable(tables.Table):
    class Meta:
        model = Course
        template_name = "django_tables2/bootstrap.html"
        exclude = (
            "credits", "record_end_at", "global_id", "created_at", "visitors_rating", "duration", "finished_at", "language",
            "content", "started_at", "started_at", "requirements", "competences", "accreditation", "description", "image")
        fields = (
            "title", "partner", "institution", "communication_owner", "communication_platform", "expertise_status",
            "passport_status", "required_ratings_state", "unforced_ratings_state", "comment")
        attrs = {'class': 'ui celled table', 'id': 'coursesTable'}

    title = tables.TemplateColumn(
        '<a href="#" onClick="CourseEdit=window.open(\'http://openedu.urfu.ru/roo/{{ record.id }}\',\'{{ record.title }}\',width=600,height=300); return false;">{{ record.title }}</a', footer="Наименование")
    competences = tables.TemplateColumn('{{ record.description | truncatewords_html:5 |safe}}')
    description = tables.TemplateColumn('{{ record.description | truncatewords_html:5 |safe}}')
    content = tables.TemplateColumn('{{ record.description | truncatewords_html:5 |safe}}')
    image = tables.TemplateColumn('<img src="{{record.image}}" height="100"/>')
    roo_status = ChoiceColumn(Course.ROO_STATES)
    communication_owner = ChoiceColumn(Course.COMMUNICATION_OWNER_STATES)
    communication_platform = ChoiceColumn(Course.COMMUNICATION_PLATFORM_STATES)
    expertise_status = ChoiceColumn(Course.EX_STATES)
    passport_status = ChoiceColumn(Course.PASSPORT_STATES)
    required_ratings_state = ChoiceColumn(Course.REQUIRED_RATINGS_STATES)
    unforced_ratings_state = ChoiceColumn(Course.UNFORCED_RATINGS_STATES)


class ExpertisesTable(tables.Table):
    class Meta:
        model = Expertise
        template_name = "django_tables2/bootstrap.html"
        fields = ("course", "state", "date", "type", "executed", "expert", "supervisor", "organizer", "comment")

    course = tables.TemplateColumn(
        '<a href="#" onClick="ExpertiseEdit=window.open(\'http://openedu.urfu.ru/roo/expertise/{{ record.id }}\',\'{{ record.course }}\',width=600,height=300); return false;">{{ record.course }}</a')
