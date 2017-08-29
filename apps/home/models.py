from django.db import models


class Page(models.Model):
    title = models.CharField("Название", max_length=256)
    contents = models.ManyToManyField("ContentItem", blank=True)

    link = models.CharField("Ссылка", max_length=32)

    class Meta:
        verbose_name = 'страница'
        verbose_name_plural = 'страницы'

    def __str__(self):
        return self.title


class ContentItem(models.Model):
    title = models.CharField("Название", max_length=256)
    content = models.TextField("Контент")
    weight = models.IntegerField("Вес", default=1)

    class Meta:
        verbose_name = 'блок контента'
        verbose_name_plural = 'блоки контента'
        ordering = ['-weight']

    def __str__(self):
        return self.title


