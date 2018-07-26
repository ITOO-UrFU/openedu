import requests
from time import gmtime, strftime
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import truncatewords_html
import requests
import json
from urllib.parse import urlencode
import logging

logger = logging.getLogger('celery_logging')


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
                    roo_base.update_from_dict(item)
                else:
                    cls.create_from_dict(item)

        get_base_from_page(cls, url)


class Expertise(models.Model):
    course = models.ForeignKey("Course", verbose_name="Курс", default='None')
    state = models.CharField("состояние процесса (этап)", blank=True, null=True, max_length=512)
    date = models.DateField("Дата", blank=True, null=True)
    type = models.CharField("Вид экспертизы", blank=True, null=True, max_length=512)
    executed = models.BooleanField("Отметка об исполнении эксперизы", default=False)
    expert = models.ForeignKey("Expert", verbose_name="Эксперт", default='None')
    supervisor = models.CharField("Кто от ИТОО контролирует", blank=True, null=True, max_length=512)
    organizer = models.CharField("Организатор экспертизы сотрудники или партнеры", blank=True, null=True,
                                 max_length=512)

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
    activities = models.ManyToManyField("Area", verbose_name="Массив идентификаторов областей деятельности")  # массив
    visitors_rating_count = models.CharField("Количество пользовательских оценок", blank=True, null=True,
                                             max_length=512)  # наверно
    total_visitors_number = models.CharField("Количество слушателей", blank=True, null=True,
                                             max_length=512)
    experts_rating = models.CharField("Рейтинг экспертов", blank=True, null=True, max_length=512)
    requirements = models.TextField("Массив строк-требований", blank=True, null=True)  # массив
    cabinet_course_url = models.CharField("Ссылка на курс в кабинете", blank=True, null=True, max_length=512)
    teachers = models.ManyToManyField("Teacher", blank=True)  # список лекторов/аторов

    # наши поля
    newest = models.BooleanField("Самое новое содержание курса", default=False)

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
            c.save()

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
                try:
                    roo_course = cls.objects.filter(global_id=course['global_id']).first()
                except cls.DoesNotExist:
                    roo_course = None

                if roo_course:

                    if not roo_course.newest:
                        roo_course.update_from_dict(course)
                else:
                    Course.create_from_dict(course)

            if response["next"] is not None:
                get_courses_from_page(response["next"])
            else:
                return

        get_courses_from_page('https://online.edu.ru/api/courses/v0/course')

        logger.info("Закончили Courses: {0}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))


class Platform(Base):
    title = models.CharField("Наименование", blank=True, null=True, max_length=1024)
    global_id = models.CharField("ИД платформы на РОО", null=True, max_length=512, db_index=True)
    image = models.CharField("Изображение платформы", blank=True, null=True, max_length=512)
    url = models.CharField("Ссылка на сайт платформы", blank=True, null=True, max_length=512)
    description = models.TextField("Описание платформы", blank=True, null=True)
    ogrn = models.CharField("ОГРН", blank=True, null=True, max_length=512)

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
        return f"Платформа: {self.title}"

    class Meta:
        verbose_name = 'платформа'
        verbose_name_plural = 'платформы'

    @classmethod
    def get(cls):
        cls.update_base_from_roo('https://online.edu.ru/ru/api/partners/v0/platform', 'global_id')

        logger.info("Закончили Platform: {0}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))


class Expert(models.Model):
    login = models.CharField("Логин эксперта", blank=True, null=True, max_length=512)

    def __str__(self):
        return f"Эксперт: {self.login}"

    class Meta:
        verbose_name = 'эксперт'
        verbose_name_plural = 'эксперт'


class Owner(Base):
    title = models.CharField("Наименование", blank=True, null=True, max_length=512)
    global_id = models.CharField("ИД Правообладателя на РОО", max_length=512, null=True, db_index=True)
    ogrn = models.CharField("ОГРН", blank=True, null=True, max_length=512)
    image = models.CharField("Изображение", blank=True, null=True, max_length=1024)

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

    def save(self, *args, **kwargs):

        rdata = {
            "q": f"logo {self.title}",
            "num": 1,
            "start": 1,
            # "filetype": "jpg",
            "key": "AIzaSyBaLNSE02AM6vjEJ9npNwD9uagQzSlMnhg",
            "cx": "012036972007253236562:btl9gjd-nti",
            "searchType": "image",
            "gl": "ru",
        }

        r = requests.get("https://www.googleapis.com/customsearch/v1", params=urlencode(rdata))
        items = json.loads(r.content).get("items", None)
        if items:
            self.image = items[0]["link"]
        super(Owner, self).save(*args, **kwargs)

    @classmethod
    def get(cls):
        cls.update_base_from_roo('https://online.edu.ru/api/partners/v0/rightholder', 'title')

        logger.info("Закончили Owner: {0}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))


class Area(Base):
    title = models.CharField("Наименование", blank=True, null=True, max_length=512)
    global_id = models.CharField("ИД областей деятельности на РОО", blank=True, null=True, max_length=512, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'область деятельности'
        verbose_name_plural = 'области деятельности'

    @classmethod
    def get(cls):
        cls.update_base_from_roo('https://online.edu.ru/api/courses/v0/activity', 'title')

        logger.info("Закончили Areas: {0}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))


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

        logger.info("Закончили Direction: {0}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
