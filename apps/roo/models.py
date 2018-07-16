import requests
from time import gmtime, strftime
from django.db import models


class Expertise(models.Model):
    course = models.ForeignKey("Course", verbose_name="Курс")
    state = models.CharField("состояние процесса (этап)", blank=True, null=True, max_length=1024)
    date = models.DateField("Дата", blank=True, null=True)
    type = models.CharField("Вид экспертизы", blank=True, null=True, max_length=1024)
    executed = models.BooleanField("Отметка об исполнении эксперизы", default=False)
    expert = models.ForeignKey("Expert", verbose_name="Эксперт")
    supervisor = models.CharField("Кто от ИТОО контролирует", blank=True, null=True, max_length=1024)
    organizer = models.CharField("Организатор экспертизы сотрудники или партнеры", blank=True, null=True,
                                 max_length=1024)

    def __str__(self):
        return f"Экспертиза: {self.course}, Тип: {self.type}"

    class Meta:
        verbose_name = 'экспертиза'
        verbose_name_plural = 'экспертизы'


class Teacher(models.Model):
    title = models.CharField("ФИО лектора", blank=True, null=True, max_length=1024)
    image = models.CharField("Ссылка на изображение", blank=True, null=True, max_length=1024)
    description = models.CharField("Описание", blank=True, null=True, max_length=1024)

    def __str__(self):
        return f"Лектор: {self.title}"

    class Meta:
        verbose_name = 'лектор'
        verbose_name_plural = 'лекторы'


class Course(models.Model):
    #  что приходит в api сейчас
    credits = models.CharField("", blank=True, null=True, max_length=1024)  # я не знаю что это
    record_end_at = models.CharField("Дата окончания записи на курс", blank=True, null=True, max_length=1024)
    title = models.CharField("Наименование", blank=True, null=True, max_length=1024)
    image = models.URLField("Изображение курса", blank=True, null=True, max_length=1024)
    institution_id = models.CharField("Идентификатор Правообладателя", blank=True, null=True, max_length=1024)
    global_id = models.CharField("ИД курса на РОО", blank=False, null=False, max_length=1024)
    created_at = models.CharField("Дата создания онлайн-курса", blank=False, null=False, max_length=1024)
    visitors_rating = models.CharField("Оценка посетителей РОО", blank=True, null=True, max_length=1024)  # но это не точно
    duration = models.CharField("Длительность в неделях", blank=True, null=True, max_length=1024)
    finished_at = models.CharField("Дата окончания онлайн-курса", blank=False, null=False)
    competences = models.TextField("Формируемые компетенции", blank=True, null=True)
    accreditation = models.TextField("Аккредитация", blank=True, null=True)
    description = models.TextField("Описание", blank=False, null=True)
    visitors_number = models.IntegerField("Количество записавшихся на курс", blank=True, null=True)
    directions = models.CharField("Массив идентификаторов направлений", blank=True, null=True)  # массив
    expert_rating_count = models.CharField("Количество оценок экспертов", blank=True, null=True)  # сильно не точно
    has_sertificate = models.BooleanField("Возможность получить сертификат", blank=True, null=True)  # слово сертификат у них неправильно
    language = models.CharField("Язык контента", blank=True, null=True, max_length=1024)
    course_item_url = models.CharField("", blank=True, null=True, max_length=1024)  # неизвестная вестчь
    partner_id = models.CharField("Идентификатор Платформы", blank=True, null=True)
    content = models.TextField("Содержание онлайн-курса", blank=True, null=True)
    started_at = models.CharField("Дата ближайшего запуска", blank=True, null=True, max_length=1024)
    rating = models.CharField("Рейтинг пользователей", blank=True, null=True, max_length=1024)
    external_url = models.CharField("Ссылка на онлайн-курс на сайте Платформы", blank=True, null=True, max_length=1024)
    lectures_number = models.IntegerField("Количество лекций", blank=True, null=True)
    activities = models.CharField("Массив идентификаторов областей деятельности", blank=True, null=True, max_length=1024)  # массив
    visitors_rating_count = models.CharField("Количество пользовательских оценок", blank=True, null=True, max_length=1024)  # наверно
    experts_rating = models.CharField("Рейтинг экспертов", blank=True, null=True, max_length=1024)
    requirements = models.CharField("Массив строк-требований", blank=True, null=True, max_length=1024)  # массив
    cabinet_course_url = models.CharField("Ссылка на курс в кабинете", blank=True, null=True, max_length=1024)
    teachers = models.ManyToManyField("Teacher")  # список лекторов/аторов

    # это еще Никита написал
    grade_tools = models.TextField("Оценочные средства", blank=True, null=True)
    prerequisites = models.TextField("Входные требования обучающихся", blank=True, null=True)
    subject = models.CharField("Предмет курса", blank=True, null=True, max_length=1024)
    labor = models.CharField("Трудоемкость", blank=True, null=True, max_length=1024)
    proctoring_service = models.CharField("Используемый сервис прокторинга", blank=True, null=True, max_length=1024)
    version = models.IntegerField("Номер версии курса", blank=True, null=True)
    opened = models.BooleanField("Открытый", default=False)
    admin_email = models.EmailField("e-mail администратора платформы, правообладателя", blank=True, null=True)
    short_description = models.CharField("Краткое описание", blank=True, null=True, max_length=1024)
    expertized = models.BooleanField("Прошел обязательную экспертизу", default=False)
    domain = models.CharField("Предметная область", blank=True, null=True, max_length=1024)
    uploaded_roo = models.BooleanField("Загружен курс на РОО", default=False)
    uploaded_prepod = models.BooleanField("Загружен ли курс на prepod", default=False)
    platform = models.ForeignKey("Platform", verbose_name="Название платформы")
    permission = models.BooleanField("Разрешение правообладателя на выгрузку", default=False)
    comment = models.TextField("Комментарий", blank=True, null=True)

    def __str__(self):
        return f"Онлайн-курс: {self.title}"

    class Meta:
        verbose_name = 'онлайн-курс'
        verbose_name_plural = 'онлайн-курсы'

    def updade_courses_from_roo():
        request = requests.get('https://online.edu.ru/api/courses/v0/course',
                               auth=('vesloguzov@gmail.com', 'ye;yj,jkmitrjlf'))
        courses = request.json()["rows"]
        for course in courses:
            print(course['global_id'])
            r = requests.get('https://online.edu.ru/api/courses/v0/course/' + course['global_id'],
                             auth=('vesloguzov@gmail.com', 'ye;yj,jkmitrjlf'))
            roo_course, created = Course.objects.get_or_create(roo_id=course['global_id'])[0]
            roo_course.save()

            print(r.json())
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "len(rows): ", len(courses))


class Platform(models.Model):
    title = models.CharField("Наименование", blank=True, null=True, max_length=1024)
    person = models.CharField("Данные контактного лица правообладателя телефон, почта", blank=True, null=True,
                              max_length=1024)
    connection_form = models.CharField("Форма связи с контактным лицом", blank=True, null=True, max_length=1024)
    connection_date = models.DateField("Дата связи с контактным лицом", blank=True, null=True)
    contacts = models.CharField("Контакты института", blank=True, null=True, max_length=1024)

    def __str__(self):
        return f"Платформа: {self.title}"

    class Meta:
        verbose_name = 'платформа'
        verbose_name_plural = 'платформы'


class Expert(models.Model):
    login = models.CharField("Логин эксперта", blank=True, null=True, max_length=1024)

    def __str__(self):
        return f"Эксперт: {self.login}"

    class Meta:
        verbose_name = 'эксперт'
        verbose_name_plural = 'эксперт'


class Owner(models.Model):
    title = models.CharField("Наименование", blank=True, null=True, max_length=1024)

    def __str__(self):
        return f"Правообладатель: {self.title}"

    class Meta:
        verbose_name = 'правообладатель'
        verbose_name_plural = 'правообладатели'
