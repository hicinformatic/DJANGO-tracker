from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<domain>.{1,36})/downlad.js/?$', views.downloadJS, name='downloadJS'),

    url(r'^(?P<domain>.{1,36})/visit.svg/?$',  views.trackerSVG,   name='trackerSVG'),
    url(r'^(?P<domain>.{1,36})/visit.js/?$',   views.trackerJS,    name='trackerJS'),
    url(r'^(?P<domain>.{1,36})/visit.html/?$', views.trackerDATAS, name='trackerDATAS'),
    url(r'^(?P<domain>.{1,36})/visit.svg/(?P<visitor>.{1,36})/?$',  views.trackerSVG,   name='trackerSVG'),
    url(r'^(?P<domain>.{1,36})/visit.js/(?P<visitor>.{1,36})/?$',   views.trackerJS,    name='trackerJS'),
    url(r'^(?P<domain>.{1,36})/visitd.html/(?P<visitor>.{1,36})/?$', views.trackerDATAS, name='trackerDATAS'),
    url(r'^(?P<domain>.{1,36})/visitv.html/(?P<visitor>.{1,36})/?$', views.trackerDATAS, name='trackerDATAS'),

    url(r'^tracker/ndatas.csv/?$',  views.ndatasCSV,  name='ndatasCSV'),
    url(r'^tracker/ndatas.json/?$', views.ndatasJSON, name='ndatasJSON'),
    url(r'^tracker/ndatas.txt/?$',  views.ndatasTXT,  name='ndatasTXT'),

    url(r'^tracker/(?P<task>\d+)/add.csv/?',  views.addCSV,  name='addCSV'),
    url(r'^tracker/(?P<task>\d+)/add.json/?', views.addJSON, name='addJSON'),
    url(r'^tracker/(?P<task>\d+)/add.txt/?',  views.addTXT,  name='addTXT'),

    url(r'^tracker/task/(?P<task>\d+)/(?P<command>(error|order|start|running|complete))/task.json/?$', views.taskJSON, name='taskJSON'),
    url(r'^tracker/task/(?P<task>\d+)/(?P<command>(error|order|start|running|complete))/task.json/(?P<message>.+)/?$', views.taskJSON, name='taskJSON'),
    url(r'^tracker/task/(?P<task>\d+)/(?P<command>(error|order|start|running|complete))/task.txt/?$', views.taskTXT, name='taskTXT'),
    url(r'^tracker/task/(?P<task>\d+)/(?P<command>(error|order|start|running|complete))/task.txt/(?P<message>.+)/?$', views.taskTXT, name='taskTXT'),
    url(r'^tracker/task/(?P<task>\d+)/(?P<command>(error|order|start|running|complete))/task.html/?$', views.taskHTML, name='taskHTML'),
    url(r'^tracker/task/(?P<task>\d+)/(?P<command>(error|order|start|running|complete))/task.html/(?P<message>.+)/?$', views.taskHTML, name='taskHTML'),
]