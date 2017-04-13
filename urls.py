from django.conf.urls import url
from . import views

from .settings import conf

urlpatterns = [
    url(r'^visit.js/(?P<domain>.{1,32})/$', views.trackerJS, name='trackerJS'),
    url(r'^visit.svg/(?P<visitor>.{1,32})/$', views.trackerSVG, name='trackerSVG'),
    url(r'^visit.html/(?P<domain>.{1,32})/$', views.trackerDATAS, name='trackerDATAS'),
    url(r'^downlad.js/(?P<domain>.{1,32})/$', views.downloadJS, name='downloadJS'),
]