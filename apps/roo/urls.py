from django.conf.urls import url
from .views import index, get_active_tasks

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^get_active_tasks/$', get_active_tasks, name='get_active_tasks'),
]
