from django.conf.urls import url

from .views import courses

urlpatterns = [
    url(r'^$', courses, name='courses'),
]
