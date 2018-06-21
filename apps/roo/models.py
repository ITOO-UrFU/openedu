from django.db import models


class Expertise(models.Model):
    course = models.ForeignKey("Course", verbose_name="Курс")
    state = models.CharField("состояние процесса (этап)", blank=True, null=True, max_length=1024)
    date = models.DateField("Дата", blank=True, null=True)
    type = models.CharField("Вид экспертизы", blank=True, null=True, max_length=1024)
    executed = models.BooleanField("Отметка об исполнении эксперизы", )
    expert = models.ForeignKey("Expert", verbose_name="Эксперт")
    supervisor = models.CharField("Кто от ИТОО контролирует", blank=True, null=True, max_length=1024)
    organizer = models.CharField("Организатор экспертизы сотрудники или партнеры", blank=True, null=True, max_length=1024)

    def __str__(self):
        return f"Экспертиза: {self.course}, Тип: {self.type}"

    class Meta:
        verbose_name = 'экспертиза'
        verbose_name_plural = 'экспертизы'


class Course(models.Model):
    title = models.CharField("Наименование", blank=True, null=True, max_length=1024)
    short_description = models.CharField("Краткое описание", blank=True, null=True, max_length=1024)
    description = models.TextField("Описание", blank=True, null=True)
    roo_id = models.IntegerField("ИД на РОО", blank=True, null=True)
    competences = models.TextField("Формируемые компетенции", blank=True, null=True)
    results = models.TextField("Результаты обучения", blank=True, null=True)
    grade_tools = models.TextField("Оценочные средства", blank=True, null=True)
    photo = models.CharField("Фото автора", blank=True, null=True, max_length=1024)
    authors = models.TextField("Авторы", blank=True, null=True)
    prerequisites = models.TextField("Входные требования обучающихся", blank=True, null=True)
    content = models.TextField("Содержание", blank=True, null=True)
    directions = models.TextField("Направления подготовки", blank=True, null=True)
    subject = models.CharField("Предмет курса", blank=True, null=True, max_length=1024)
    activity = models.CharField("Область деятельности", blank=True, null=True, max_length=1024)
    language = models.CharField("Язык контента", blank=True, null=True, max_length=1024)
    enrollment_end_date = models.CharField("Дата окончания записи", blank=True, null=True, max_length=1024)
    start_date = models.CharField("Дата запуска", blank=True, null=True, max_length=1024)
    duration = models.CharField("Длительность курса", blank=True, null=True, max_length=1024)
    labor = models.CharField("Трудоемкость", blank=True, null=True, max_length=1024)
    certificate = models.BooleanField("Трудоемкость", default=False, blank=True, null=True)
    proctoring_service = models.CharField("Используемый сервис прокторинга", blank=True, null=True, max_length=1024)
    version = models.IntegerField("Номер версии курса", blank=True, null=True)
    opened = models.BooleanField("Открытый", default=False, blank=True, null=True)
    admin_email = models.EmailField("e-mail администратора платформы, правообладателя", blank=True, null=True)

    expertized = models.BooleanField("Прошел обязательную экспертизу", default=False)
    domain = models.CharField("Предметная область", blank=True, null=True, max_length=1024)
    uploaded_roo = models.BooleanField("Загружен курс на РОО", default=False)
    uploaded_prepod = models.BooleanField("Загружен ли курс на prepod", default=False)
    platform = models.ForeignKey("Platform", verbose_name="Название платформы", blank=True, null=True)
    url = models.URLField("URL курса на платформе", blank=True, null=True)
    roo_url = models.URLField("URL курса на РОО", blank=True, null=True)
    owner = models.ForeignKey("Owner", verbose_name="Правообладатель", blank=True, null=True)
    permission = models.BooleanField("Разрешение правообладателя на выгрузку", blank=True, null=True)
    comment = models.TextField("Комментарий")

    def __str__(self):
        return f"Онлайн-курс: {self.title}"

    class Meta:
        verbose_name = 'онлайн-курс'
        verbose_name_plural = 'онлайн-курсы'


class Platform(models.Model):
    title = models.CharField("Наименование", blank=True, null=True, max_length=1024)
    person = models.CharField("Данные контактного лица правообладателя телефон, почта", blank=True, null=True, max_length=1024)
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
