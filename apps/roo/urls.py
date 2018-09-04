from django.conf.urls import url
from django.views.generic.base import RedirectView, TemplateView
from .views import data, get_active_tasks, courses, CourseUpdate, expertises, ExpertiseUpdate, upload_from_json, \
    courses_list, courses_edit, ExpertiseCreate, TeacherCreate, upload_expertises, CourseCreate, TableCourseUpdate, expertises_list

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/roo/courses/', permanent=False), name='index'),
    url(r'^(?P<pk>\d+)', CourseUpdate.as_view(), name="detail"),
    url(r'^expertise/(?P<pk>\d+)/$', ExpertiseUpdate.as_view(), name="detail"),
    url(r'data/$', data, name='data'),
    url(r'courses/', courses_list, name='courses_list'),
    url(r'expertises/', expertises, name='expertises'),
    url(r'expertises_new/', expertises_list, name='expertises_list'),
    url(r'data/get_active_tasks/$', get_active_tasks, name='get_active_tasks'),

    url(r'upload_json/', upload_expertises, name='upload_expertises'),
    url(r'courses_edit/', courses_edit, name='courses_edit'),
    url(r'courses_list/', courses_list, name='courses_list'),
    url(r'create_expertise/', ExpertiseCreate.as_view(), name='create_expertise'),
    url(r'create_teacher/', TeacherCreate.as_view(), name='create_teacher'),
    url(r'create_course/', CourseCreate.as_view(), name='create_course'),
    url(r'update_course/', TableCourseUpdate, name='update_course'),
    url(r'^close/$', TemplateView.as_view(template_name='roo/close.html')),
]
