# -*- coding: utf-8 -*-
import json

from django.shortcuts import render_to_response, redirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.template.context_processors import csrf
from django.http import Http404
from django import forms
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import send_mail

from django.views.generic import ListView
from django.utils import timezone
from .models import Minor, OOPBid, Bid, QuoteBid


class MinorsListView(ListView):
    model = Minor
    template_name = "minors/minors.html"

    def get_queryset(self):
        return Minor.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super(MinorsListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


mainpage = MinorsListView.as_view()


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        ordering = ('id',)
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super(BidForm, self).__init__(*args, **kwargs)
            self.fields['minor'].required = False
            self.fields['done'].required = False


class OOPBidForm(forms.ModelForm):
    class Meta:
        model = OOPBid
        ordering = ('id',)
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super(OOPBidForm, self).__init__(*args, **kwargs)


@csrf_exempt
def detail(request, pk):
    context = {}
    try:
        minor = Minor.objects.get(id=pk)
    except ObjectDoesNotExist:
        raise Http404
    form = BidForm()
    context["STATIC_URL"] = settings.STATIC_URL
    context["form"] = form
    context["minor"] = minor
    return render_to_response('minors/minor.html', context)


@csrf_exempt
def add_bid(request, pk):
    try:
        minor = Minor.objects.get(id=pk)
    except ObjectDoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.minor = minor
            bid.save()
            return HttpResponse(json.dumps({'result': "success"}))

        else:
            return HttpResponse(json.dumps({'result': "failed"}))
    else:
        raise Http404


@csrf_exempt
def bidforminor(request):
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.save()
            return HttpResponse(json.dumps({'result': "success"}))
        else:
            return HttpResponse(json.dumps({'result': "failed"}))
    elif request.method == 'GET':
        minors = Minor.objects.filter(active=True)
        form = BidForm()
        context = {}
        context["STATIC_URL"] = settings.STATIC_URL
        context["form"] = form
        context["minors"] = minors
        return render_to_response('minors/bid.html', context)


@csrf_exempt
def bidforoop(request):
    if request.method == 'POST':
        form = OOPBidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.save()
            return redirect("/landing/")
        else:
            return HttpResponse(status=500)
    elif request.method == 'GET':
        return redirect("/landing/")


@receiver(post_save, sender=OOPBid, dispatch_uid="bid_add")
def bid_add(sender, instance, **kwargs):
    admin_emails = settings.BID_ADMINS
    unread = OOPBid.objects.filter(done=False).count()
    send_mail(
        'Landing',
        'Получена новая заявка! Всего необработанных заявок: {unread}'.format(unread=unread),
        settings.DEFAULT_FROM_EMAIL,
        admin_emails,
        fail_silently=False,
    )


# ____ QUOTES

class QuoteBidForm(forms.ModelForm):
    class Meta:
        model = QuoteBid
        ordering = ('id',)
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super(QuoteBidForm, self).__init__(*args, **kwargs)


@csrf_exempt
def quotebid(request):
    if request.method == 'POST':
        form = QuoteBidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            if bid.agreement:
                bid.save()
            else:
                return HttpResponse("Требуется согласие на обработку персональных данных и согласие с политикой конфиденциальности.")
            return redirect("/quotes/done.html")
        else:
            return HttpResponse(status=500)
    elif request.method == 'GET':
        return redirect("/quotes/")


