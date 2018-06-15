from django.conf.urls import url
from .views import api

urlpatterns = [
    url(r'^(?P<table>.*)/(?P<id>.*)/$', api, name="api"),
    url(r'^(?P<table>.*)/$', api, name="api"),
    ]
