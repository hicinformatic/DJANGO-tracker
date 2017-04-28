from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/(?P<domain>.{1,36})/downlad.js$', views.downloadJS, name='downloadJS'),
    url(r'^/(?P<domain>.{1,36})/visit.svg$',  views.trackerSVG, name='trackerSVG'),
    url(r'^/(?P<domain>.{1,36})/visit.svg?visitor=(?P<visitor>.{1,36})$', views.trackerSVG, name='trackerSVG'),
    url(r'^/(?P<domain>.{1,36})/visit.js$',   views.trackerJS,    name='trackerJS'),
    url(r'^/(?P<domain>.{1,36})/visit.html$', views.trackerDATAS, name='trackerDATAS'),

    url(r'^tracker/ndatas.csv$',  views.ndatasCSV,  name='ndatasCSV'),
    url(r'^tracker/ndatas.json$', views.ndatasJSON, name='ndatasJSON'),
    url(r'^tracker/ndatas.txt$',  views.ndatasTXT,  name='ndatasTXT'),

    url(r'^tracker/task/(?P<task>\d+)/(?P<command>(order|start|running|complete))/task.json$', views.taskJSON, name='taskJSON'),
    url(r'^tracker/task/(?P<task>\d+)/(?P<command>(order|start|running|complete))/task.json?message=(?P<message>.+)/$', views.taskJSON, name='taskJSON'),
    url(r'^tracker/task/(?P<task>\d+)/(?P<command>(order|start|running|complete))/task.txt$', views.taskTXT, name='taskTXT'),
    url(r'^tracker/task/(?P<task>\d+)/(?P<command>(order|start|running|complete))/task.txt?message=(?P<message>.+)/$', views.taskTXT, name='taskTXT'),
    url(r'^tracker/task/(?P<task>\d+)/(?P<command>(order|start|running|complete))/task.html$', views.taskHTML, name='taskHTML'),
    url(r'^tracker/task/(?P<task>\d+)/(?P<command>(order|start|running|complete))/task.html?message=(?P<message>.+)/$', views.taskHTML, name='taskHTML'),
]