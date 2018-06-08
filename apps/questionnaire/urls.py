from django.conf.urls import url
from .views import eios, Thanks

urlpatterns = [
    url(r'^eios/$', eios, name="eios"),
    url(r'^thanks/$', Thanks.as_view(), name="eios"),
    ]