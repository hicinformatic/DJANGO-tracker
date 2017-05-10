from django.http import HttpResponse, HttpResponseServerError, JsonResponse, StreamingHttpResponse
from django.contrib.auth.decorators import permission_required
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from .settings import conf
from .functions import isTrack, firsTrack, order, start, running, complete, error, addTask
from .decorators import localcall, localcalloradmin, localcalloradminorstaff
from .forms import trackFormDatas, trackFormEvents
from .models import Tracked, Visitor, DataAssociated, Task

from datetime import datetime, timedelta
import subprocess, csv

@localcalloradminorstaff
def downloadJS(request, domain):
    context = { 'domain': domain, 'url': request.META['HTTP_HOST'], }
    response = render(request, 'tracker/tracker.js', context=context, content_type=conf['contenttype_js'],)
    response['Content-Disposition'] = 'attachment; filename=visit.js'
    return response

def trackerSVG(request, domain, visitor=''):
    visitor = isTrack(request, visitor)
    if firsTrack(request):
        Tracked.objects.bulk_create([
            Tracked(visitor=visitor, key='User-Agent', value=request.META['HTTP_USER_AGENT'], domain=domain),
            Tracked(visitor=visitor, key='AcceptLanguage', value=request.META['HTTP_ACCEPT_LANGUAGE'], domain=domain),
        ])
    response = HttpResponse('<svg width="0" height="0"><text>%s</text></svg>' % visitor, content_type=conf['contenttype_svg'])
    request.session[conf['store']] = visitor
    request.session[conf['first']] = visitor
    response.set_signed_cookie(conf['store'], visitor, salt=conf['salt'], max_age=conf['maxage'])
    response.set_signed_cookie(conf['first'], visitor, salt=conf['salt'], max_age=conf['maxage'])
    return response

def trackerJS(request, domain):
    context = { 'domain': domain, 'url': request.META['HTTP_HOST'], }
    return render(request, 'tracker/tracker.js', context=context, content_type=conf['contenttype_js'],)

@csrf_exempt
def trackerDATAS(request, domain, visitor=''):
    response = HttpResponse('KO', content_type=conf['contenttype_txt'])
    if request.method == 'POST':
        form = trackFormDatas(request.POST)
        if form.is_valid():
            url = title = None
            visitor = isTrack(request, visitor)
            if form.cleaned_data['url'] != '': url = form.cleaned_data.pop('url')
            if form.cleaned_data['title'] != '': title = form.cleaned_data.pop('title')
            datas = []
            if firsTrack(request):
                datas.append(Tracked(visitor=visitor, key='User-Agent', value=request.META['HTTP_USER_AGENT'], domain=domain, url=url, title=title))
                datas.append(Tracked(visitor=visitor, key='AcceptLanguage', value=request.META['HTTP_ACCEPT_LANGUAGE'], domain=domain, url=url, title=title))
            for key,value in form.cleaned_data.items():
                if value != '': datas.append(Tracked(visitor=visitor, key=key, value=value, domain=domain, url=url, title=title))
            Tracked.objects.bulk_create(datas)
        response = HttpResponse('OK', content_type=conf['contenttype_txt'])
        request.session[conf['store']] = visitor
        request.session[conf['first']] = visitor
        response.set_signed_cookie(conf['store'], visitor, salt=conf['salt'], max_age=conf['maxage'])
        response.set_signed_cookie(conf['first'], visitor, salt=conf['salt'], max_age=conf['maxage'])
    else:
        form = trackFormDatas()
    return HttpResponse('<form method="POST">%s<input type="submit"></form>' % form)

@csrf_exempt
def trackerEVENTS(request, domain, visitor=''):
    response = HttpResponse('KO', content_type=conf['contenttype_txt'])
    if request.method == 'POST':
        form = trackFormEvents(request.POST)
        if form.is_valid():
            url = title = None
            visitor = isTrack(request, visitor)
            if form.cleaned_data['url'] != '': url = form.cleaned_data.pop('url').encode('utf-8')
            if form.cleaned_data['title'] != '': title = form.cleaned_data.pop('title').encode('utf-8')
            datas = []
            if firsTrack(request):
                datas.append(Tracked(visitor=visitor, key='User-Agent', value=request.META['HTTP_USER_AGENT'], domain=domain, url=url, title=title))
                datas.append(Tracked(visitor=visitor, key='AcceptLanguage', value=request.META['HTTP_ACCEPT_LANGUAGE'], domain=domain, url=url, title=title))
            for key,value in form.cleaned_data.items():
                if value != '': datas.append(Tracked(visitor=visitor, key=key, value=value.encode('utf-8'), event=True, domain=domain, url=url, title=title))
            Tracked.objects.bulk_create(datas)
        response = HttpResponse('OK', content_type=conf['contenttype_txt'])
        request.session[conf['store']] = visitor
        request.session[conf['first']] = visitor
        response.set_signed_cookie(conf['store'], visitor, salt=conf['salt'], max_age=conf['maxage'])
        response.set_signed_cookie(conf['first'], visitor, salt=conf['salt'], max_age=conf['maxage'])
    else:
        form = trackFormEvents()
    return HttpResponse('<form method="POST">%s<input type="submit"></form>' % form)

"""
-------------------------------------------------------------------
GET Ndatas*
-------------------------------------------------------------------
"""

@localcalloradminorstaff
def ndatasCSV(request):
    response = HttpResponse(content_type=conf['contenttype_csv'])
    response['Content-Disposition'] = 'attachment; filename="ndatas.csv"'
    writer = csv.writer(response)
    for track in Tracked.objects.reverse()[:conf['ndatas']]:
        writer.writerow([track.id, track.visitor, track.event, track.key, track.value, track.domain, track.url, track.title, track.create])
    return response

@localcalloradminorstaff
def ndatasJSON(request):
    datas = Tracked.objects.reverse()[:conf['ndatas']]
    return JsonResponse(serializers.serialize('json', datas, fields=('id', 'visitor', 'event', 'key','value','domain', 'url', 'title', 'create'), indent=2), safe=False)

@localcalloradminorstaff
def ndatasTXT(request):
    tpl = '{0} | {1} | {2} | {3} | {4} | {5} | {6} | {7}' 
    for track in Tracked.objects.reverse()[:conf['ndatas']]:
        try: datas = datas + '\n' +  tpl.format(track.id, track.visitor, track.event, track.key, track.value, track.domain, track.url, track.title, track.create)
        except NameError: datas = tpl.format(track.id, track.visitor, track.event, track.key, track.value, track.domain, track.url, track.title, track.create)
    return HttpResponse(datas, content_type=conf['contenttype_txt'])

"""
-------------------------------------------------------------------
ADD datas*
-------------------------------------------------------------------
"""
@localcalloradminorstaff
def addCSV(request, task):
    return addTask('csv', task)

@localcalloradminorstaff
def addJSON(request, task):
    return addTask('json', task)

@localcalloradminorstaff
def addTXT(request, task):
    return addTaskTXT('txt', task)

"""
-------------------------------------------------------------------
TASK MANAGER
-------------------------------------------------------------------
Scenario type:
1-order :    Task ordered
2-start :    Task started
3-running :  Task running
4-complete : Task complete

Error encountered
0-error:     Task in error
-------------------------------------------------------------------
"""

# ------------------------------------------- #
# task*
# ------------------------------------------- #
# task: ID task (1, 2, 3, 4, 0)
# command:
#    order
#    start
#    running
#    complete
#    error
# ------------------------------------------- #

@localcalloradminorstaff
def taskHTML(request, task, command, message=''):
    if command == 'order':    return order('html', task, message)
    if command == 'start':    return start('html', task, message)
    if command == 'running':  return running('html', task, message)
    if command == 'complete': return complete('html', task, message)
    if command == 'error':    return error('html', task, message)

@localcalloradminorstaff
def taskJSON(request, task, command, message=''):
    if command == 'order':    return order('json', task, message)
    if command == 'start':    return start('json', task, message)
    if command == 'running':  return running('json', task, message)
    if command == 'complete': return complete('json', task, message)
    if command == 'error':    return error('json', task, message)
        
@localcalloradminorstaff
def taskTXT(request, task, command, message=''):
    if command == 'order':    return order('txt', task, message)
    if command == 'start':    return start('txt', task, message)
    if command == 'running':  return running('txt', task, message)
    if command == 'complete': return complete('txt', task, message)
    if command == 'error':    return error('txt', task, message)