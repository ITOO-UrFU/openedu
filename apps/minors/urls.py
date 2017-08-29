from django.conf.urls import url
from .views import mainpage

urlpatterns = [
    url(r'^$', mainpage),
    # url(r'^minor/(?P<pk>\d+)$', 'minors.views.detail', name="minor"),
    # url(r'^minor/(?P<pk>\d+)/bid/$', 'minors.views.add_bid', name="add_bid"),
    # url(r'^minors/bid/$', 'minors.views.bidforminor', name="add_bid_full"),
    # url(r'^oop/bid/$', 'minors.views.bidforoop', name="bidforoop"),
]
