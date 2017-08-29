from django.db import models
from django.utils.translation import ugettext_lazy as _


class Author(models.Model):
    name = models.CharField(_("ФИО"), max_length=1024)
    regalia = models.CharField(_("Регалии"), max_length=1024)
    achievements = models.CharField(_("Достижения"), max_length=1024, blank=True)
    description = models.CharField(_("Описание"), max_length=1024, blank=True)
    image = models.ImageField(_("Фото"), upload_to='../uploads/authors/', null=True, blank=True)

    def __str__(self):
        return u"{}".format(self.name)

    class Meta:
        verbose_name = 'автор'
        verbose_name_plural = 'авторы'


class Minor(models.Model):
    name = models.CharField(_("Название"), max_length=1024, null=True)
    description = models.TextField(_("Описание"), max_length=256, blank=True)
    author = models.CharField(_("Автор"), max_length=64, null=True)
    authors = models.ManyToManyField(Author, blank=True)
    institute = models.CharField(_("Институт"), max_length=64, null=True)
    laboriousness = models.FloatField(_("Трудоёмкость"), default=0)
    weight = models.CharField(_("Стоимость"), max_length=64, null=True)
    annotation = models.TextField(_("Аннотация"), max_length=32768, null=True)
    author_about = models.TextField(_("Об авторе"), max_length=4096, null=True)
    startdate = models.DateTimeField(_("Дата начала"), null=True)
    enddate = models.DateTimeField(_("Дата завершения"), null=True)
    image = models.ImageField(_("Изображение"), upload_to='../uploads/minors/', null=True)
    schedule = models.CharField(_("Расписание"), max_length=64, blank=True)

    published = models.BooleanField(_("Опубликовано"), default=False)

    def get_absolute_url(self):
        return "minor/%i/" % self.id

    def __str__(self):
        return u"{}".format(self.name)

    @property
    def get_next(self):
        next = Minor.objects.filter(published=True, id__gt=self.id)
        if next:
            return next[0].id
        return Minor.objects.filter(published=True)[0].id

    @property
    def get_prev(self):
        prev = Minor.objects.filter(published=True, id__lt=self.id).order_by('-id')
        if prev:
            return prev[0].id
        return list(Minor.objects.filter(published=True).reverse())[-1].id

    class Meta:
        verbose_name = 'майнор'
        verbose_name_plural = 'майноры'


class Bid(models.Model):
    minor = models.ForeignKey(Minor, blank=True, null=True)
    name = models.CharField(_("ФИО"), max_length=1024)
    email = models.EmailField(blank=True)
    phone = models.CharField("Phone number", max_length=16, blank=True)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'заявка на майнор'
        verbose_name_plural = 'заявки на майнор'


class OOPBid(models.Model):
    name = models.CharField(_("Имя"), max_length=2048, blank=True, null=True)
    email = models.CharField(_("Email"), max_length=2048, blank=True, null=True)
    phone = models.CharField(_("Телефон"), max_length=2048, blank=True, null=True)
    program = models.CharField(_("Программа"), max_length=2048, blank=True, null=True)
    message = models.TextField(_("Сообщение"), blank=True, null=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return u"{}".format(self.name)

    class Meta:
        verbose_name = 'заявка на открытую программу'
        verbose_name_plural = 'заявки на открытую программу'
