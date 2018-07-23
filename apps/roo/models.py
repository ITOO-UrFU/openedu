import requests
from time import gmtime, strftime
from django.db import models
import logging

logger = logging.getLogger('celery_logging')

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

    class Meta:
        verbose_name = 'лектор'
        verbose_name_plural = 'лекторы'


class Course(models.Model):
    #  что приходит в api сейчас
    credits = models.CharField("Массив перезачётов", blank=True, null=True, max_length=512)
    record_end_at = models.CharField("Дата окончания записи на курс", blank=True, null=True, max_length=512)
    title = models.CharField("Наименование", blank=True, null=True, max_length=512)
    image = models.URLField("Изображение курса", blank=True, null=True)
    institution_id = models.CharField("Идентификатор Правообладателя", blank=True, null=True, max_length=512)
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
    directions = models.TextField("Массив идентификаторов направлений", blank=True, null=True)  # массив
    expert_rating_count = models.CharField("Количество оценок экспертов", blank=True, null=True,
                                           max_length=512)  # сильно не точно
    has_sertificate = models.BooleanField("Возможность получить сертификат",
                                          default=False)  # слово сертификат у них неправильно
    language = models.CharField("Язык контента", blank=True, null=True, max_length=512)
    course_item_url = models.CharField("", blank=True, null=True, max_length=512)  # неизвестная вестчь
    partner_id = models.CharField("Идентификатор Платформы", blank=True, null=True, max_length=512)
    content = models.TextField("Содержание онлайн-курса", blank=True, null=True, max_length=512)
    started_at = models.CharField("Дата ближайшего запуска", blank=True, null=True, max_length=512)
    rating = models.CharField("Рейтинг пользователей", blank=True, null=True, max_length=512)
    external_url = models.CharField("Ссылка на онлайн-курс на сайте Платформы", blank=True, null=True, max_length=512)
    lectures_number = models.IntegerField("Количество лекций", blank=True, null=True)
    activities = models.CharField("Массив идентификаторов областей деятельности", blank=True, null=True,
                                  max_length=512)  # массив
    visitors_rating_count = models.CharField("Количество пользовательских оценок", blank=True, null=True,
                                             max_length=512)  # наверно
    total_visitors_number =models.CharField("Количество слушателей", blank=True, null=True,
                                             max_length=512)
    experts_rating = models.CharField("Рейтинг экспертов", blank=True, null=True, max_length=512)
    requirements = models.TextField("Массив строк-требований", blank=True, null=True)  # массив
    cabinet_course_url = models.CharField("Ссылка на курс в кабинете", blank=True, null=True, max_length=512)
    teachers = models.ManyToManyField("Teacher", blank=True)  # список лекторов/аторов

    # наши поля
    newest = models.BooleanField("Самое новое содержание курса", default=False)

    # это еще Никита написал
    # grade_tools = models.TextField("Оценочные средства", blank=True, null=True)
    # prerequisites = models.TextField("Входные требования обучающихся", blank=True, null=True)
    # subject = models.CharField("Предмет курса", blank=True, null=True, max_length=512)
    # labor = models.CharField("Трудоемкость", blank=True, null=True, max_length=512)
    # proctoring_service = models.CharField("Используемый сервис прокторинга", blank=True, null=True, max_length=512)
    # version = models.IntegerField("Номер версии курса", blank=True, null=True)
    # opened = models.BooleanField("Открытый", default=False)
    # admin_email = models.EmailField("e-mail администратора платформы, правообладателя", blank=True, null=True)
    # short_description = models.CharField("Краткое описание", blank=True, null=True, max_length=512)
    # expertized = models.BooleanField("Прошел обязательную экспертизу", default=False)
    # domain = models.CharField("Предметная область", blank=True, null=True, max_length=512)
    # uploaded_roo = models.BooleanField("Загружен курс на РОО", default=False)
    # uploaded_prepod = models.BooleanField("Загружен ли курс на prepod", default=False)
    # owner = models.ForeignKey("Owner", verbose_name="Правообладатель", default='None')
    # platform = models.ForeignKey("Platform", verbose_name="Название платформы", default='None')
    # permission = models.BooleanField("Разрешение правообладателя на выгрузку", default=False)
    # comment = models.TextField("Комментарий", blank=True, null=True)

    def __str__(self):
        return f"Онлайн-курс: {self.title}"

    class Meta:
        verbose_name = 'онлайн-курс'
        verbose_name_plural = 'онлайн-курсы'

    def update_from_dict(self, d):
        for attr, val in d.items():
            if attr == "teachers":
                for teacher in d['teachers']:
                    if self.teachers.filter(title=teacher['title']).count() == 0:
                        t = Teacher(image=teacher['image'], description=teacher['description'], title=teacher['title'])
                        t.save()
                        self.teachers.add(t)
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
                    roo_course = False

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

        logger.info("Закончили: {0}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))


class Platform(models.Model):
    title = models.CharField("Наименование", blank=True, null=True, max_length=1024)
    global_id = models.CharField("ИД платформы на РОО", blank=True, null=True, max_length=512)
    image = models.CharField("Изображение платформы", blank=True, null=True, max_length=512)
    url = models.CharField("Ссылка на сайт платформы", blank=True, null=True, max_length=512)
    description = models.TextField("Описание платформы", blank=True, null=True)
    ogrn = models.CharField("ОГРН", blank=True, null=True, max_length=512)

    # наши поля
    newest = models.BooleanField("Самое новое содержание курса", default=False)

    # person = models.CharField("Данные контактного лица правообладателя телефон, почта", blank=True, null=True,
    #                           max_length=512)
    # connection_form = models.CharField("Форма связи с контактным лицом", blank=True, null=True, max_length=512)
    # connection_date = models.DateField("Дата связи с контактным лицом", blank=True, null=True)
    # contacts = models.CharField("Контакты института", blank=True, null=True, max_length=512)

    def __str__(self):
        return f"Платформа: {self.title}"

    class Meta:
        verbose_name = 'платформа'
        verbose_name_plural = 'платформы'

    @classmethod
    def update_from_dict_p(self, d):
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
    def updade_platform_from_roo(cls):
        login = 'vesloguzov@gmail.com'
        password = 'ye;yj,jkmitrjlf'

        def get_platform_from_page(page_url):
            request = requests.get(page_url, auth=(login, password), verify=False)
            response = request.json()
            platfroms = response["rows"]
            r = requests.get(f"https://online.edu.ru/ru/api/partners/v0/platform",
                             auth=('vesloguzov@gmail.com', 'ye;yj,jkmitrjlf'), verify=False)
            platfrom = r.json()
            #try:
            logger.info(platfrom['global_id'])
            #     roo_course = cls.objects.filter(global_id=platfrom['global_id']).first()
            # except cls.DoesNotExist:
            #     roo_course = False
            #
            # if roo_course:
            #     if not roo_course.newest:
            #         roo_course.update_from_dict_p(platfrom)
            # else:
            #     Course.create_from_dict_p(platfrom)


        get_platform_from_page('https://online.edu.ru/ru/api/partners/v0/platform')


class Expert(models.Model):
    login = models.CharField("Логин эксперта", blank=True, null=True, max_length=512)

    def __str__(self):
        return f"Эксперт: {self.login}"

    class Meta:
        verbose_name = 'эксперт'
        verbose_name_plural = 'эксперт'


class Owner(models.Model):
    title = models.CharField("Наименование", blank=True, null=True, max_length=512)

    def __str__(self):
        return f"Правообладатель: {self.title}"

    class Meta:
        verbose_name = 'правообладатель'
        verbose_name_plural = 'правообладатели'
