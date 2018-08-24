from django.conf.urls import url
from django.views.generic.base import RedirectView
from .views import data, get_active_tasks, courses, CourseUpdate, expertises, ExpertiseUpdate, upload_from_json, get_courses, courses_edit

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/roo/courses/', permanent=False), name='index'),
    url(r'^(?P<pk>\d+)', CourseUpdate.as_view(), name="detail"),
    url(r'^expertise/(?P<pk>\d+)/$', ExpertiseUpdate.as_view(), name="detail"),
    url(r'data/$', data, name='data'),
    url(r'courses/', courses, name='courses'),
    url(r'expertises/', expertises, name='expertises'),
    url(r'data/get_active_tasks/$', get_active_tasks, name='get_active_tasks'),

    url(r'upload_json/', upload_from_json, name='upload_from_json'),
    url(r'courses_edit/', courses_edit, name='courses_edit'),
    url(r'get_courses/', get_coursesl, name='get_courses'),
]
