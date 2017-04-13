from django.conf.urls import url
from . import views

from .settings import conf

urlpatterns = [
    url(r'^visit.js/(?P<domain>.{1,36})/$', views.trackerJS, name='trackerJS'),
    url(r'^visit.svg/(?P<domain>.{1,36})/$', views.trackerSVG, name='trackerSVG'),
    url(r'^visit.svg/(?P<domain>.{1,36})/(?P<visitor>.{1,36})/$', views.trackerSVG, name='trackerSVG'),
    url(r'^visit.html/(?P<domain>.{1,36})/$', views.trackerDATAS, name='trackerDATAS'),
    url(r'^downlad.js/(?P<domain>.{1,36})/$', views.downloadJS, name='downloadJS'),
]