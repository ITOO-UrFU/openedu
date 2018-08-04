from django.conf.urls import url
from .views import data, get_active_tasks, course_table, CourseUpdate

urlpatterns = [
    url(r'^(?P<pk>[0-9])', CourseUpdate.as_view(), name="detail"),
    url(r'data/$', data, name='data'),
    url(r'course_table/', course_table, name='course_table'),
    url(r'data/get_active_tasks/$', get_active_tasks, name='get_active_tasks'),
]
