from django.conf.urls import url
from .views import index, start_tasks_celery

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'/start_tasks_celery/', start_tasks_celery, name='start_tasks_celery'),
]
