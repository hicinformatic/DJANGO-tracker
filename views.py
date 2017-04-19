from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from django.contrib.auth.decorators import permission_required
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from .settings import conf
from .functions import isTrack, firsTrack
from .decorators import localcall, localcalloradmin, localcalloradminorstaff
from .forms import trackFormDatas
from .models import Tracked, Visitor, DataAssociated, Task

from datetime import datetime, timedelta

@localcalloradminorstaff
def downloadJS(request, domain):
    context = { 'domain': domain, 'url': request.META['HTTP_HOST'], }
    response = render(request, 'tracker/tracker.js', context=context, content_type=conf['contenttype_js'],)
    response['Content-Disposition'] = 'attachment; filename=visit.js'
    return response

def trackerJS(request, domain):
    context = { 'domain': domain, 'url': request.META['HTTP_HOST'], }
    return render(request, 'tracker/tracker.js', context=context, content_type=conf['contenttype_js'],)

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

@csrf_exempt
def trackerDATAS(request, domain):
    response = HttpResponse('KO', content_type=conf['contenttype_txt'])
    if request.method == 'POST':
        form = trackFormDatas(request.POST)
        if form.is_valid():
            url = title = None
            visitor = isTrack(request, form.cleaned_data.pop('visitor'))
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

def NjsonDATAS(request):
    datas = Tracked.objects.reverse()[:conf['ndatas']]
    return JsonResponse(serializers.serialize('json', datas), safe=False)

@localcalloradminorstaff
def Order(request, task):
    if any(int(task) in code for code in conf['tasks']):
        name = conf['tasks'][int(task)][1]
        delta = conf['deltas'][name]
        try:
            if isinstance(delta, int):
                delta = datetime.today() - timedelta(seconds=delta)
                Task.objects.get(task=task, create__gte=delta)
            elif delta == 'Monthly':
                now = datetime.datetime.now()
                month = now.month-1 if now.month > 1 else 12
                year = now.year-1 if month == 12 else now.year
                Task.objects.get(task=task, create__year=year, create__month=month)
            elif delta == 'Annually':
                year = datetime.datetime.now().year-1
                Task.objects.get(task=task, create__year=year)
            else:
                return HttpResponseServerError(_('KO | Task delta unavailable: {} - {}'.format(task, name)), content_type='text/plain')
        except Task.DoesNotExist:
            newtask = Task(task=task)
        return HttpResponse(_('OK | Task ordered: {} - {}'.format(task, name)), content_type='text/plain')
    else:
        return HttpResponseServerError(_('KO | Task unavailable: %s' %task), content_type='text/plain')


@localcalloradminorstaff
def Start(request, task):
    #delta = datetime.today() - timedelta(hours=Activity_Delta)
    #try:
    #    delta = datetime.today() - timedelta(hours=Activity_Delta)
    #    sbactivity = SendinBlueActivity.objects.get(activity=activity, status=True, datecreate__gte=delta)
    #    canlaunch = True if sbactivity.datecreate < delta else False
    #except Exception:
    #    canlaunch = True  
    #if canlaunch is True:
    #    if os.name == 'posix': task = 'nohup {0} {1} > /dev/null 2>&1&'
    #    if os.name == 'nt': task = 'start {0} {1} > NUL'
    #    try:
    #        os.popen(task.format( conf['binary'], conf['scripts'][int(activity)]) )
    #        return HttpResponse(_('OK | Task started: '), content_type='text/plain')
    #    except Exception as e:
    #        pass
    return HttpResponseServerError(_('KO | Unable to start task'), content_type='text/plain')

@localcalloradminorstaff
def Running(request, task):
    return HttpResponseServerError(_('KO | Unable to start task'), content_type='text/plain')

@localcalloradminorstaff
def Complete(request, task):
    return HttpResponseServerError(_('KO | Unable to start task'), content_type='text/plain')

@localcalloradminorstaff
def Error(request, task):
    return HttpResponseServerError(_('KO | Unable to start task'), content_type='text/plain')
       
# ------------------------------------------- #
# START
# ------------------------------------------- #
# Enregistre le démarrage d'une activité
#@localcall
#@csrf_exempt
#@login_required(login_url='/authentication/failure/401')
#@permission_required('SendinBlue.can_start')
#def start(request, activity):
#    running = False
#    try:
#        delta = timezone.now() - timedelta(hours=Activity_Delta)
#        activities = SendinBlueActivity.objects.filter(activity=activity, status=True)
#        for activity in activities:
#            if activity.datecreate < delta:
#                activity.status = False
#                activity.updateby = request.user.username
#                activity.save()
#            else:
#                running = True
#    except SendinBlueActivity.DoesNotExist:
#        pass
#    if running is False:
#        try:
#            activity = SendinBlueActivity(activity=activity, updateby=request.user.username)
#            activity.full_clean()
#            activity.success()
#        except Exception:
#            return HttpResponse(ko(106), content_type='text/plain')
#    else:
#        return HttpResponse(ko(108), content_type='text/plain')
#    return HttpResponse(ok(activity.id), content_type='text/plain')

# ------------------------------------------- #
# STOP
# ------------------------------------------- #
# Enregistre la fin d'une activité
#@localcall
#@csrf_exempt
#@login_required(login_url='/authentication/failure/401')
#@permission_required('SendinBlue.can_stop')
#def stop(request, activity):
#    try:
#        activity = SendinBlueActivity.objects.get(activity=activity, status=True)
#        activity.status = False
#        activity.updateby = request.user.username
#        activity.save()
#    except Exception:
#        return HttpResponse(ko(107), content_type='text/plain')
#    return HttpResponse(ok(False), content_type='text/plain')