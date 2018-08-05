from django.conf.urls import url
from django.views.generic.base import RedirectView
from .views import data, get_active_tasks, courses, CourseUpdate, expertises

urlpatterns = [
    url(r'^.*$', RedirectView.as_view(url='/roo/courses/', permanent=False), name='index'),
    url(r'^(?P<pk>[0-9])', CourseUpdate.as_view(), name="detail"),
    url(r'data/$', data, name='data'),
    url(r'courses/', courses, name='courses'),
    url(r'expertises/', expertises, name='expertises'),
    url(r'data/get_active_tasks/$', get_active_tasks, name='get_active_tasks'),
]
