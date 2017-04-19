from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^visit.js/(?P<domain>.{1,36})/$', views.trackerJS, name='trackerJS'),
    url(r'^visit.svg/(?P<domain>.{1,36})/$', views.trackerSVG, name='trackerSVG'),
    url(r'^visit.svg/(?P<domain>.{1,36})/(?P<visitor>.{1,36})/$', views.trackerSVG, name='trackerSVG'),
    url(r'^visit.html/(?P<domain>.{1,36})/$', views.trackerDATAS, name='trackerDATAS'),
    url(r'^downlad.js/(?P<domain>.{1,36})/$', views.downloadJS, name='downloadJS'),
    url(r'^ndatas.json$', views.NjsonDATAS, name='NjsonDATAS'),
    url(r'^tracker/task/order/(?P<task>\d+)/$', views.Order, name='Order'),
    url(r'^tracker/task/start/(?P<task>\d+)/$', views.Start, name='Start'),
    url(r'^tracker/task/running/(?P<task>\d+)/$', views.Running, name='Running'),
    url(r'^tracker/task/complete/(?P<task>\d+)/$', views.Complete, name='Complete'),
    url(r'^tracker/task/error/(?P<task>\d+)/$', views.Error, name='Error'),
]