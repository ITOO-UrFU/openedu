from django.conf.urls import url

from .views import page_view

urlpatterns = [
    url(r'^$', page_view, name='page_view'),
    url(r'^(?P<link>.*)/$', page_view, name='page_view'),
]
