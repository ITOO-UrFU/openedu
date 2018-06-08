from django.db import models


class EIOS(models.Model):
    YN = (("y", "Да"), ("n", "Нет"))
    SCALE = (
        ("0", "Абсолютно не согласен"),
        ("1", "Частично не согласен"),
        ("2", "Затрудняюсь ответить"),
        ("3", "Частично согласен"),
        ("4", "Абсолютно согласен"),
    )
    SEX = (("m", "Мужской"), ("f", "Женский"))
    EXPERIENCE = (
        ("0", "1-5 лет"),
        ("1", "6-10 лет"),
        ("2", "11-15 лет"),
        ("3", "16-20 лет"),
        ("4", "Больше 21 года")
    )

    ACADEMIC_DEGREE = (
        ("0", "Нет"),
        ("1", "Кандидат наук"),
        ("2", "Доктор наук")
    )

    q1 = models.CharField("Есть ли у вас опыт работы в сфере онлайн-обучения", max_length=1, default="n", choices=YN)
    q2 = models.CharField("Какими корпоративными сервисами Уральского федерального университета вы пользуетесь?", max_length=1024, )
    q3 = models.CharField("Мне понятен термин “электронная информационно-образовательная среда”", max_length=1, default="2", choices=SCALE)
    q4 = models.CharField("Я понимаю, зачем нужно внедрять онлайн-обучение в образовательную деятельность",
                          max_length=1, default="2", choices=SCALE)
    q5 = models.CharField("Я знаю, с помощью каких инструментов осуществляется онлайн-обучение", max_length=1,
                          default="2", choices=SCALE)
    q6 = models.CharField("Меня интересует онлайн-обучение", max_length=1, default="2", choices=SCALE)
    q7 = models.CharField("Я понимаю финансовые аспекты использования открытых онлайн-курсов", max_length=1,
                          default="2", choices=SCALE)
    q8 = models.CharField("Я понимаю, кто такой тьютор в онлайн-обучении", max_length=1, default="2", choices=SCALE)
    q9 = models.CharField(
        "Мне понятны особенности планирования и реализации учебного процесса для разных моделей включения онлайн-курсов в образовательные программы",
        max_length=1, default="2", choices=SCALE)
    q10 = models.TextField("Интернет-ресурсы(сайты) наиболее полезные в вашей профессиональной деятельности",
                           blank=True, null=True)
    q11 = models.CharField("Укажите ваш пол:", max_length=1, default="m", choices=SEX)
    q12 = models.PositiveSmallIntegerField("Ваш возраст:", default=0)
    q13 = models.CharField("Каков ваш опыт работы в качестве преподавателя?", max_length=10, choices=EXPERIENCE, default="0")
    q14 = models.CharField("Наличие ученой степени:", max_length=10, default="0", choices=ACADEMIC_DEGREE)
    q15 = models.EmailField("Контактная почта:")
    q16 = models.CharField("Интересно ли вам дальнейшее информирование про мероприятия, связанные с онлайн-обучением?",
                           max_length=1, default="y", choices=YN)
