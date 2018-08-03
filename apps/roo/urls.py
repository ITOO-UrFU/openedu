from django.conf.urls import url
from .views import index, get_active_tasks, course_table

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'course_table/', course_table, name='course_table'),
    url(r'^get_active_tasks/$', get_active_tasks, name='get_active_tasks'),
]
