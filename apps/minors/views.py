# -*- coding: utf-8 -*-
import json

from django.shortcuts import render_to_response, redirect, HttpResponse

from django.views.generic import ListView
from django.utils import timezone
from .models import Minor, OOPBid


class MinorsListView(ListView):

    model = Minor
    template_name = "minors/main.html"

    def get_context_data(self, **kwargs):
        context = super(MinorsListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

mainpage = MinorsListView.as_view()
# def detail(request, pk):
#     context = {}
#     try:
#         minor = Minor.objects.get(id=pk)
#     except ObjectDoesNotExist:
#         raise Http404
#     form = BidForm()
#     context["form"] = form
#     context["minor"] = minor
#     context["csrftoken"] = csrf(request)["csrf_token"]
#     return render_to_response('minor.html', context)
#
#
# def add_bid(request, pk):
#     try:
#         minor = Minor.objects.get(id=pk)
#     except ObjectDoesNotExist:
#         raise Http404
#
#     if request.method == 'POST':
#         form = BidForm(request.POST)
#         if form.is_valid():
#             bid = form.save(commit=False)
#             bid.minor = minor
#             bid.save()
#             return HttpResponse(json.dumps({'result': "success"}))
#
#         else:
#             return HttpResponse(json.dumps({'result': "failed"}))
#     else:
#         raise Http404
#
#
# def bidforminor(request):
#     if request.method == 'POST':
#         form = BidForm(request.POST)
#         if form.is_valid():
#             bid = form.save(commit=False)
#             bid.save()
#             return HttpResponse(json.dumps({'result': "success"}))
#         else:
#             return HttpResponse(json.dumps({'result': "failed"}))
#     elif request.method == 'GET':
#         minors = Minor.objects.all()
#         form = BidForm()
#         context = {}
#         context["form"] = form
#         context["csrftoken"] = csrf(request)["csrf_token"]
#         context["minors"] = minors
#         return render_to_response('bidforminor.html', context)
#
#
# def openprograms(request):
#     return render_to_response('openprograms.html')
#
#
# @csrf_exempt
# def bidforoop(request):
#     if request.method == 'POST':
#         form = OOPBidForm(request.POST)
#         if form.is_valid():
#             bid = form.save(commit=False)
#             bid.save()
#             return redirect("/landing/")
#         else:
#             return HttpResponse(status=500)
#     elif request.method == 'GET':
#         return redirect("/landing/")
#
#
# @receiver(post_save, sender=OOPBid, dispatch_uid="bid_add")
# def bid_add(sender, instance, **kwargs):
#     admin_emails = settings.BID_ADMINS
#     unread = OOPBid.objects.filter(done=False).count()
#     send_mail(
#         'Landing',
#         'Получена новая заявка! Всего необработанных заявок: {unread}'.format(unread=unread),
#         settings.DEFAULT_FROM_EMAIL,
#         admin_emails,
#         fail_silently=False,
#     )
#
