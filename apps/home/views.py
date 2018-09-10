from django.http import Http404
from django.shortcuts import render

from .models import Page


def page_view(request, link="home"):
    page = Page.objects.filter(link=link).first()
    if page:
        return render(request, "home/page.html", {"page": page})
    else:
        raise Http404


def login(request):
    return render(request, "home/login.html")
