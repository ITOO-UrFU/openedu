from django.conf.urls import url
from .views import data, get_active_tasks, course_table

urlpatterns = [
    url(r'data/$', data, name='data'),
    url(r'course_table/', course_table, name='course_table'),
    url(r'^get_active_tasks/$', get_active_tasks, name='get_active_tasks'),
]
