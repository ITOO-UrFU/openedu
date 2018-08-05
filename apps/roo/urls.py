from django.conf.urls import url
from .views import data, get_active_tasks, courses, CourseUpdate, expertises

urlpatterns = [
    url(r'^(?P<pk>[0-9])', CourseUpdate.as_view(), name="detail"),
    url(r'data/$', data, name='data'),
    url(r'courses/', courses, name='courses'),
    url(r'expertises/', expertises, name='expertises'),
    url(r'data/get_active_tasks/$', get_active_tasks, name='get_active_tasks'),
]
