import json
import time
import uuid

import os
from django import forms
from django.db import models
from multiupload.fields import MultiFileField


def generate_new_filename(instance, filename):
    f, ext = os.path.splitext(filename)
    filename = '%s%s' % (uuid.uuid4().hex, ext)
    fullpath = f"openprofession/{time.strftime('%Y-%m')}/{filename}"
    return fullpath


def generate_new_seminar_filename(instance, filename):
    f, ext = os.path.splitext(filename)
    filename = '%s%s' % (uuid.uuid4().hex, ext)
    fullpath = f"openprofession/seminar_files/{time.strftime('%Y-%m')}/{filename}"
    return fullpath


def generate_new_report_filename(instance, filename):
    f, ext = os.path.splitext(filename)
    filename = '%s%s' % (uuid.uuid4().hex, ext)
    fullpath = f"openprofession/reports/{time.strftime('%Y-%m')}/{filename}"
    return fullpath


class Entry(models.Model):
    student_id = models.CharField(blank=False, null=False, max_length=255, unique=True)
    state = models.TextField()
    result = models.TextField()

    def __str__(self):
        return u"{}".format(self.student_id)

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'записи'


class Report(models.Model):
    title = models.CharField('Имя файла отчета', max_length=1024, blank=False, null=False)
    report_file = models.FileField("Файл отчета", upload_to=generate_new_report_filename, null=True)
    report_type = models.CharField('Тип отчета', max_length=32, blank=False, null=False)
    date = models.DateTimeField('Дата генерации отчета', blank=False, null=False)
    course_id = models.CharField('ИД курса', max_length=32, blank=False, null=False)
    session = models.CharField('Сессия', max_length=32, blank=False, null=False)
    processed = models.BooleanField("Обработано", default=False)
    entries = models.ManyToManyField("ReportEntry")
    proctored_entries = models.ManyToManyField("ProctoredReportEntry")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'отчет'
        verbose_name_plural = 'отчеты'


class ReportEntry(models.Model):
    user_id = models.CharField("Идентификатор студента", max_length=255, null=False, blank=False)
    email = models.CharField("Электронная почта", max_length=255, null=False, blank=False)
    username = models.CharField("Имя пользователя", max_length=255, null=False, blank=False)
    grade = models.DecimalField('Оценка за весь курс', max_digits=5, decimal_places=2)
    cohort_name = models.CharField("Название когорты", blank=False, null=False, max_length=255)
    enrollment_track = models.CharField("Тип подписка", max_length=255)
    certificate_eligible = models.BooleanField("Проходит ли на сертификат", default=False)
    certificate_delivered = models.CharField("Сертификат доставлен", max_length=255)
    certificate = models.CharField("Сертификат", max_length=255, blank=True, null=True)
    raw_data = models.TextField("Raw", default="")


class ProctoredReportEntry(models.Model):
    email = models.CharField("Электронная почта", max_length=255, null=False, blank=False)
    exam_name = models.CharField("Название экзамена", max_length=255, null=False, blank=True)
    allowed_time_limit_mins = models.IntegerField("Длительность экзамена", default=-1)
    is_sample_attempt = models.BooleanField("Пробная попытка", default=False)
    started_at = models.CharField("Начало экзамена", max_length=255, null=True, blank=True)
    completed_at = models.CharField("Окончание экзамена", max_length=255, null=True, blank=True)
    status = models.CharField("Статус сдачи", max_length=255, null=False, blank=False)
    raw_data = models.TextField("Raw", default="")


class CourseUserGrade(models.Model):
    program = models.ForeignKey('Program')
    user = models.ForeignKey('PersonalData')
    grade = models.DecimalField('Оценка за весь курс', max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class Program(models.Model):
    title = models.CharField('Название программы(курса)', max_length=1024, blank=False, null=False)
    active = models.BooleanField('Активна', default=False)
    session = models.CharField('Название сессии', max_length=1024, blank=False, null=False)
    course_id = models.CharField('Ид курса', max_length=1024, blank=False, null=False, default="-")
    start = models.IntegerField("Старт", default=-1)
    org = models.CharField('ИД организации', max_length=1024, blank=True, null=True)

    reports = models.ManyToManyField('Report', blank=True)

    # def get_url(self):
    #     return f"https://courses.openprofession.ru/courses/course-v1:{self.org}+{self.course_id}+{self.session}/courseware/"

    def is_active(self):
        return self.active

    def has_report(self):
        return self.reports.count()

    def __str__(self):
        return f"{self.session} - {self.title}"

    class Meta:
        verbose_name = 'программа'
        verbose_name_plural = 'программы'

    def add_session(self):
        self.active = False
        Program.objects.create(
            title=self.title,
            active=True,
            session=f"session_{str(int(self.session.split('_')[1]) + 1).rjust(2, '0')}",
            course_id=self.course_id,
            start=self.start + 1,
            org=self.org
        )

        self.save()


class SimulizatorData(models.Model):
    fio = models.CharField("ФИО", max_length=2048, null=False, blank=False)
    email = models.EmailField("Email")
    phone = models.CharField("Телефон", max_length=255, null=False, blank=False)

    username = models.CharField("username", max_length=255, null=True, blank=True, unique=True)
    password = models.CharField("password", max_length=255, null=True, blank=True)

    agreement = models.BooleanField("Согласие на обработку перс. данных", default=False, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.fio} - {self.email} - {self.phone}"

    class Meta:
        verbose_name = 'заявка на участие в симуляторе'
        verbose_name_plural = 'заявки на участие в симуляторе'


class PersonalData(models.Model):
    SEX = (('m', 'мужской'), ('f', 'женский'))
    DOCUMENT_TYPES = (('u', 'Удостоверение'), ('s', 'Сертификат'), ('n', 'Неуспеваемость'))
    STATUSES = (('f', 'Физ.лицо'), ('j', 'Физ.лицо по договору с юр.лицом'))
    EDUCATION_LEVEL = (('M', 'Среднее профессиональное'), ('H', 'Высшее'))
    program = models.ForeignKey('Program', blank=False, null=True)
    first_name = models.CharField("Имя", max_length=255, null=False, blank=False)
    last_name = models.CharField("Фамилия", max_length=255, null=False, blank=False)
    second_name = models.CharField("Отчество", max_length=255, null=True, blank=True)
    sex = models.CharField("Пол", max_length=1, choices=SEX, null=False, blank=False)
    city = models.CharField("Город", max_length=256, null=True, blank=False)

    birth_date = models.CharField("Дата рождения", max_length=16, null=False, blank=False)
    phone = models.CharField("Телефон", max_length=255, null=False, blank=False)
    email = models.EmailField("Email")
    job = models.CharField("Место работы", max_length=2048, null=True, blank=False)
    position = models.CharField("Должность", max_length=2048, null=True, blank=False)
    address_register = models.TextField("Адрес регистрации", blank=True, null=True)

    claim_scan = models.FileField("Скан заявления", upload_to=generate_new_filename)

    series = models.CharField("Серия", max_length=8, null=True, blank=True)
    number = models.CharField("Номер", max_length=8, null=True, blank=True)
    issued_by = models.TextField("Кем выдан", null=True, blank=True)
    unit_code = models.CharField("Код подразделения", max_length=16, null=True, blank=True)
    issue_date = models.CharField("Дата выдачи", max_length=16, null=True, blank=True)
    passport_scan = models.FileField("Скан заявления", upload_to=generate_new_filename, null=True, blank=True)

    education_level = models.CharField("Уровень базового образования", max_length=1, choices=EDUCATION_LEVEL,
                                       null=False, blank=False)
    diploma_scan = models.FileField("Скан диплома", upload_to=generate_new_filename, null=False, blank=False)
    another_doc = models.FileField("Иной документ", upload_to=generate_new_filename, null=True, blank=True)

    quote = models.BooleanField("Заявка на попадание в квоту", default=False)

    agreement = models.BooleanField("Согласие на обработку перс. данных", default=False, blank=False, null=False)

    in_quote = models.BooleanField("Попал в квоту", default=False)
    paid = models.BooleanField("Оплатил", default=False)

    document_type = models.CharField("Тип выдаваемого документа", max_length=1, choices=DOCUMENT_TYPES, null=True,
                                     blank=True)
    status = models.CharField("Статус", max_length=1, choices=STATUSES, null=True,
                              blank=True)
    all_docs = models.BooleanField("Слушатель прикрепил документы: скан заявления, документ об образовании",
                                   default=False)
    all_scans = models.BooleanField("Прикреплены все необоходимые сканы документов", default=False)
    all_valid = models.BooleanField("Данные в доках слушателя совпадают и корректны", default=False)

    doc_forwarding = models.FileField("Скан заявления о пересылке", upload_to=generate_new_filename, null=True,
                                      blank=True)

    mail_index = models.CharField("Почтовый индекс", max_length=255, null=True, blank=True)
    country = models.CharField("Страна", default='Россия', max_length=255, null=True, blank=True)
    address_living = models.TextField("Адрес проживания", max_length=255, blank=True, null=True)

    possible_id = models.IntegerField(blank=True, default=0)
    courses = models.ManyToManyField(Program, related_name='%(class)s_requests_created', blank=True)
    entries = models.ManyToManyField(ReportEntry, related_name='%(class)s_requests_created', blank=True)
    program_grade = models.CharField("Оценка за выбранный курс", default="-1", max_length=32, blank=True, null=True)
    exam_name = models.CharField("Название итогового мероприятия", default="", max_length=32, blank=True, null=True)
    exam_grade = models.CharField("Оценка за экзамен по программе", default="-1", max_length=32, blank=True, null=True)
    proctoring_status = models.CharField("Статус прокторинга за выбранный курс", default="None", max_length=32,
                                         blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def fio(self):
        if self.second_name:
            return f"{self.last_name} {self.first_name} {self.second_name}"
        else:
            return f"{self.last_name} {self.first_name}"

    def __str__(self):
        return self.email

    def get_grades(self):
        result = {}
        cugs = CourseUserGrade.objects.filter(user=self).order_by("program__course_id", "program__session",
                                                                  "created_at")
        for cug in cugs:
            result[str(cug.program.id)] = float(cug.grade)
        return json.dumps(result)

    class Meta:
        verbose_name = 'слушатель'
        verbose_name_plural = 'слушатели'


class SeminarData(models.Model):
    ## Город надо??
    TYPE_OF_PARTICIPATION = (('away', 'заочно'), ('internally', 'очно без сертификата'), ('internally_cert', 'очно с сертификатом'))
    SEX = (('m', 'мужской'), ('f', 'женский'))
    first_name = models.CharField("Имя", max_length=255, null=False, blank=False)
    last_name = models.CharField("Фамилия", max_length=255, null=False, blank=False)
    second_name = models.CharField("Отчество", max_length=255, null=True, blank=True)
    email = models.EmailField("Email")
    phone = models.CharField("Телефон", max_length=255, null=False, blank=False)
    job = models.CharField("Место работы", max_length=2048, null=True, blank=False)
    position = models.CharField("Должность", max_length=2048, null=True, blank=False)

    sex = models.CharField("Пол", max_length=1, choices=SEX, null=False, blank=False)
    type_of_participation = models.CharField("Тип участия", max_length=15, choices=TYPE_OF_PARTICIPATION, null=False, blank=False)
    with_udostoverenie = models.BooleanField("С получением удостоверения о повышении квалификации", default=False)
    diploma_scan = models.FileField("Cкан документа о базовом образовании", upload_to=generate_new_seminar_filename,
                                    null=True,
                                    blank=True)
    another_doc = models.FileField("Документ о смене персональных данных", upload_to=generate_new_seminar_filename,
                                   null=True,
                                   blank=True)
    education_bid = models.FileField("Скан заявления о зачислении на обучение", upload_to=generate_new_seminar_filename, null=True,
                                     blank=True)
    doc_forwarding = models.FileField("Скан заявления о пересылке", upload_to=generate_new_seminar_filename, null=True,
                                      blank=True)
    agreement = models.BooleanField("Согласие на обработку перс. данных", default=False, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def fio(self):
        if self.second_name:
            return f"{self.last_name} {self.first_name} {self.second_name}"
        else:
            return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = 'участник семинара'
        verbose_name_plural = 'участники семинара'


class QuotesAvailable(models.Model):
    available = models.BooleanField("Квота доступна", default=False)

    def is_available(self):
        return self.available


class PDAvailable(models.Model):
    available = models.BooleanField("Страница подачи заявки доступна", default=False)

    def is_available(self):
        return self.available


class ReportUploadForm(forms.Form):
    report_files = MultiFileField(label="Загрузка отчетов", min_num=1, max_num=100, max_file_size=1024 * 1024 * 50)


class EdcrunchPersonalData(models.Model):
    SEX = (('m', 'мужской'), ('f', 'женский'))
    DOCUMENT_TYPES = (('u', 'Удостоверение'), ('s', 'Сертификат'), ('n', 'Неуспеваемость'))
    STATUSES = (('f', 'Физ.лицо'), ('j', 'Физ.лицо по договору с юр.лицом'))
    EDUCATION_LEVEL = (('M', 'Среднее профессиональное'), ('H', 'Высшее'))
    # program = models.ForeignKey('Program', blank=False, null=True)
    first_name = models.CharField("Имя", max_length=255, null=False, blank=False)
    last_name = models.CharField("Фамилия", max_length=255, null=False, blank=False)
    second_name = models.CharField("Отчество", max_length=255, null=True, blank=True)
    sex = models.CharField("Пол", max_length=1, choices=SEX, null=False, blank=False)
    city = models.CharField("Город", max_length=256, null=True, blank=False)

    birth_date = models.CharField("Дата рождения", max_length=16, null=False, blank=False)
    phone = models.CharField("Телефон", max_length=255, null=False, blank=False)
    email = models.EmailField("Email")
    job = models.CharField("Место работы", max_length=2048, null=True, blank=False)
    position = models.CharField("Должность", max_length=2048, null=True, blank=False)
    address_register = models.TextField("Адрес регистрации", blank=True, null=True)

    claim_scan = models.FileField("Скан заявления", upload_to=generate_new_filename)

    series = models.CharField("Серия", max_length=8, null=True, blank=True)
    number = models.CharField("Номер", max_length=8, null=True, blank=True)
    issued_by = models.TextField("Кем выдан", null=True, blank=True)
    unit_code = models.CharField("Код подразделения", max_length=16, null=True, blank=True)
    issue_date = models.CharField("Дата выдачи", max_length=16, null=True, blank=True)
    passport_scan = models.FileField("Скан заявления", upload_to=generate_new_filename, null=True, blank=True)

    education_level = models.CharField("Уровень базового образования", max_length=1, choices=EDUCATION_LEVEL,
                                       null=False, blank=False)
    diploma_scan = models.FileField("Скан диплома", upload_to=generate_new_filename, null=False, blank=False)
    another_doc = models.FileField("Иной документ", upload_to=generate_new_filename, null=True, blank=True)

    agreement = models.BooleanField("Согласие на обработку перс. данных", default=False, blank=False, null=False)

    document_type = models.CharField("Тип выдаваемого документа", max_length=1, choices=DOCUMENT_TYPES, null=True,
                                     blank=True)
    status = models.CharField("Статус", max_length=1, choices=STATUSES, null=True,
                              blank=True)
    all_docs = models.BooleanField("Слушатель прикрепил документы: скан заявления, документ об образовании",
                                   default=False)
    all_scans = models.BooleanField("Прикреплены все необоходимые сканы документов", default=False)
    all_valid = models.BooleanField("Данные в доках слушателя совпадают и корректны", default=False)

    doc_forwarding = models.FileField("Скан заявления о пересылке", upload_to=generate_new_filename, null=True,
                                      blank=True)

    mail_index = models.CharField("Почтовый индекс", max_length=255, null=True, blank=True)
    country = models.CharField("Страна", default='Россия', max_length=255, null=True, blank=True)
    address_living = models.TextField("Адрес проживания", max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def fio(self):
        if self.second_name:
            return f"{self.last_name} {self.first_name} {self.second_name}"
        else:
            return f"{self.last_name} {self.first_name}"

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'слушатель edcrunch'
        verbose_name_plural = 'слушатели edcrunch'


class OratorPersonalData(models.Model):
    SEX = (('m', 'мужской'), ('f', 'женский'))
    DOCUMENT_TYPES = (('u', 'Удостоверение'), ('s', 'Сертификат'), ('n', 'Неуспеваемость'))
    STATUSES = (('f', 'Физ.лицо'), ('j', 'Физ.лицо по договору с юр.лицом'))
    EDUCATION_LEVEL = (('M', 'Среднее профессиональное'), ('H', 'Высшее'))
    first_name = models.CharField("Имя", max_length=255, null=False, blank=False)
    last_name = models.CharField("Фамилия", max_length=255, null=False, blank=False)
    second_name = models.CharField("Отчество", max_length=255, null=True, blank=True)
    sex = models.CharField("Пол", max_length=1, choices=SEX, null=False, blank=False)
    city = models.CharField("Город", max_length=256, null=True, blank=False)

    birth_date = models.CharField("Дата рождения", max_length=16, null=False, blank=False)
    phone = models.CharField("Телефон", max_length=255, null=False, blank=False)
    email = models.EmailField("Email")
    job = models.CharField("Место работы", max_length=2048, null=True, blank=False)
    position = models.CharField("Должность", max_length=2048, null=True, blank=False)
    address_register = models.TextField("Адрес регистрации", blank=True, null=True)

    claim_scan = models.FileField("Скан заявления", upload_to=generate_new_filename)

    series = models.CharField("Серия", max_length=8, null=True, blank=True)
    number = models.CharField("Номер", max_length=8, null=True, blank=True)
    issued_by = models.TextField("Кем выдан", null=True, blank=True)
    unit_code = models.CharField("Код подразделения", max_length=16, null=True, blank=True)
    issue_date = models.CharField("Дата выдачи", max_length=16, null=True, blank=True)

    education_level = models.CharField("Уровень базового образования", max_length=1, choices=EDUCATION_LEVEL,
                                       null=False, blank=False)
    diploma_scan = models.FileField("Скан диплома", upload_to=generate_new_filename, null=False, blank=False)
    another_doc = models.FileField("Иной документ", upload_to=generate_new_filename, null=True, blank=True)

    agreement = models.BooleanField("Согласие на обработку перс. данных", default=False, blank=False, null=False)

    document_type = models.CharField("Тип выдаваемого документа", max_length=1, choices=DOCUMENT_TYPES, null=True,
                                     blank=True)
    status = models.CharField("Статус", max_length=1, choices=STATUSES, null=True,
                              blank=True)
    all_docs = models.BooleanField("Слушатель прикрепил документы: скан заявления, документ об образовании",
                                   default=False)
    all_scans = models.BooleanField("Прикреплены все необоходимые сканы документов", default=False)
    all_valid = models.BooleanField("Данные в доках слушателя совпадают и корректны", default=False)

    doc_forwarding = models.FileField("Скан заявления о пересылке", upload_to=generate_new_filename, null=True,
                                      blank=True)

    mail_index = models.CharField("Почтовый индекс", max_length=255, null=True, blank=True)
    country = models.CharField("Страна", default='Россия', max_length=255, null=True, blank=True)
    address_living = models.TextField("Адрес проживания", max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def fio(self):
        if self.second_name:
            return f"{self.last_name} {self.first_name} {self.second_name}"
        else:
            return f"{self.last_name} {self.first_name}"

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'слушатель «Публичные выступления и ораторское мастерство»'
        verbose_name_plural = 'слушатели «Публичные выступления и ораторское мастерство»'