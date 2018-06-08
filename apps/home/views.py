from django.shortcuts import render
from django.http import Http404

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from .models import Page


def page_view(request, link="home"):
    page = Page.objects.filter(link=link).first()
    if page:
        return render(request, "home/page.html", {"page": page})
    else:
        raise Http404

