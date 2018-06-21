from django.db import models


class Expertise(models.Model):
    course = models.ForeignKey("Course", verbose_name="Курс")
    state = models.CharField("состояние процесса (этап)", )
    date = models.DateField("Дата", )
    type = models.CharField("Вид экспертизы", )
    executed = models.BooleanField("Отметка об исполнении эксперизы", )
    expert = models.ForeignKey("Expert", verbose_name="Эксперт")
    supervisor = models.CharField("Кто от ИТОО контролирует", )
    organizer = models.CharField("Организатор экспертизы сотрудники или партнеры", )

    def __str__(self):
        return f"Экспертиза: {self.course}, Тип: {self.type}"

    class Meta:
        verbose_name = 'экспертиза'
        verbose_name_plural = 'экспертизы'


class Course(models.Model):
    title = models.CharField("Наименование")
    expertized = models.BooleanField("Прошел обязательную экспертизу", default=False)
    domain = models.CharField("Предметная область", )
    uploaded_roo = models.BooleanField("Загружен курс на РОО", default=False)
    uploaded_prepod = models.BooleanField("Загружен ли курс на prepod", default=False)
    platform = models.ForeignKey("Platform", verbose_name="Название платформы", )
    url = models.URLField("URL курса на платформе", )
    owner = models.ForeignKey("Owner", verbose_name="Правообладатель", )
    permission = models.BooleanField("Разрешение правообладателя на выгрузку", )

    def __str__(self):
        return f"Онлайн-курс: {self.title}"

    class Meta:
        verbose_name = 'онлайн-курс'
        verbose_name_plural = 'онлайн-курсы'


class Platform(models.Model):
    title = models.CharField("Наименование")
    person = models.CharField("Данные контактного лица правообладателя телефон, почта", )
    connection_form = models.CharField("Форма связи с контактным лицом", )
    connection_date = models.DateField("Дата связи с контактным лицом")
    contacts = models.CharField("Контакты института", )

    def __str__(self):
        return f"Платформа: {self.title}"

    class Meta:
        verbose_name = 'платформа'
        verbose_name_plural = 'платформы'


class Expert(models.Model):
    login = models.CharField("Логин эксперта", )

    def __str__(self):
        return f"Эксперт: {self.login}"

    class Meta:
        verbose_name = 'эксперт'
        verbose_name_plural = 'эксперт'


class Owner(models.Model):
    title = models.CharField("Наименование")

    def __str__(self):
        return f"Правообладатель: {self.title}"

    class Meta:
        verbose_name = 'правообладатель'
        verbose_name_plural = 'правообладатели'
