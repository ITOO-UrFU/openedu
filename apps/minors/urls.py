from django.conf.urls import url
from .views import mainpage, detail, add_bid, bidforminor, bidforoop, quotebid

urlpatterns = [
    url(r'^$', mainpage),
    url(r'^(?P<pk>\d+)$', detail, name="minor"),
    url(r'^(?P<pk>\d+)/bid/$', add_bid, name="add_bid"),
    url(r'^bid/$', bidforminor, name="add_bid_full"),
    url(r'^oop/bid/$', bidforoop, name="bidforoop"),
    url(r'^quotes/bid/$', quotebid, name="quotebid"),
]
