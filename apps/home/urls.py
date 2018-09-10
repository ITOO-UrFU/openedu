from django.conf.urls import url

from .views import page_view, login

urlpatterns = [
    url(r'login/', login, name='login'),
    url(r'^$', page_view, name='page_view'),
    url(r'^(?P<link>.*)/$', page_view, name='page_view'),
]
