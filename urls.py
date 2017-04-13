from django.conf.urls import url
from . import views

from .settings import conf

urlpatterns = [
    url(r'^'+ conf['url'] +'visit.svg$', views.trackerSVG, name='trackerSVG'),
    url(r'^'+ conf['url'] +'visit.svg/(?P<visitor>.{1,32})/$', views.trackerSVG, name='trackerSVG'),
    url(r'^'+ conf['url'] +'visit.html$', views.trackerDATAS, name='trackerDATAS'),
    url(r'^'+ conf['url'] +'visit.html/(?P<domain>.{1,32})/$', views.trackerDATAS, name='trackerDATAS'),
]