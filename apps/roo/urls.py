from django.conf.urls import url
from django.views.generic.base import RedirectView, TemplateView
from .views import *

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/roo/courses/', permanent=False), name='index'),
    url(r'^(?P<pk>\d+)', CourseUpdate.as_view(), name="detail"),
    url(r'^expertise/(?P<pk>\d+)/$', ExpertiseUpdate.as_view(), name="detail"),
    url(r'course_json/(?P<course_id>\d+)/$', course_json, name='course_json'),
    url(r'^merge/(?P<pk_1>\d+)/(?P<pk_2>\d+)/$', merge, name="merge"),
    url(r'data/$', data, name='data'),
    url(r'some_view/', some_view, name='some_view'),
    url(r'visible_columns_courses/', visible_columns_courses, name='visible_columns_courses'),
    url(r'visible_columns_expertises/', visible_columns_expertises, name='visible_columns_expertises'),
    url(r'courses/', courses_list, name='courses_list'),
    # url(r'expertises/', expertises, name='expertises'),
    url(r'expertises/', expertises_list, name='expertises_list'),
    url(r'expertises_new/', expertises_list, name='expertises_list'),
    url(r'expertises_edit/', expertises_edit, name='expertises_edit'),
    url(r'data/get_active_tasks/$', get_active_tasks, name='get_active_tasks'),

    url(r'upload_json/', upload_comments, name='upload_comments'),
    url(r'courses_edit/', courses_edit, name='courses_edit'),
    url(r'courses_list/', courses_list, name='courses_list'),
    url(r'create_expertise/(?P<course_id>\d+)/$', new_expertise, name='create_expertise'),
    url(r'create_teacher/', TeacherCreate.as_view(), name='create_teacher'),
    url(r'create_course/', CourseCreate.as_view(), name='create_course'),
    url(r'update_course/', TableCourseUpdate, name='update_course'),
    url(r'update_expertise/', TableExpertiseUpdate, name='update_expertise'),
    url(r'^close/$', TemplateView.as_view(template_name='roo/close.html')),


]
