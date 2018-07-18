"""openedu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.views.static import serve

from auth_backends.urls import oauth2_urlpatterns

urlpatterns = oauth2_urlpatterns + [
    url(r'^' + settings.STATIC_URL[1:] + '(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),
    url(r'^' + settings.MEDIA_URL[1:] + '(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include('smuggler.urls')),
    url(r'^export_action/', include("export_action.urls", namespace="export_action")),
    url(r'^admin/', admin.site.urls),
    url(r'^minors/', include('minors.urls', namespace="minors")),
    url(r'^openprofession/', include('openprofession.urls', namespace="openprofession")),
    url(r'^questionnaire/', include('questionnaire.urls', namespace="questionnaire")),
    url(r'^ellada_api/', include('ellada_api.urls', namespace="ellada_api")),
    url(r'^other/', include('other.urls', namespace="other")),
    url(r'^roo/', include('roo.urls', namespace="roo")),
    url(r'^courses/', include('courses.urls', namespace="courses")),
    url(r'^', include('home.urls')),
    url(r'^advanced_filters/', include('advanced_filters.urls'))
]
