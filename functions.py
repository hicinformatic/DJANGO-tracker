from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .settings import conf
import uuid

def isTrack(request, visitor):
    try: return request.session[conf['store']]
    except Exception: pass
    try: return request.get_signed_cookie(conf['store'], salt=conf['salt'])
    except Exception: pass
    return visitor if visitor != '' else str(uuid.uuid4())

def firsTrack(request):
    try: 
        request.session[conf['first']]
        return False
    except Exception: pass
    try: 
        request.get_signed_cookie(conf['first'], salt=conf['salt'])
        return False
    except Exception: pass
    return True

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _

from .models import Task, Visitor, RouteAssociated, UserAgentAssociated, AcceptLanguageAssociated, DataAssociated
from .settings import conf

from datetime import datetime, timedelta
import subprocess

"""
-------------------------------------------------------------------
RESPONSE BY CONTENT TYPE
-------------------------------------------------------------------
Content type authorized:
    - .html: Success/Failed
    - .txt:  Success/Failed
    - .json: Success/Failed
    - .csv:  Success/Failed
-------------------------------------------------------------------
"""

# ------------------------------------------- #
# CONTENT TYPE - HTML
# ------------------------------------------- #
def responseKOHTML(task, code, error):
    tpl = _('status: KO\ntask: {ntask}\nname: {name}\ntechnical: {technical}\ncode: {code}\nerror: {error}')
    datas = { 'task': task, 'name': conf['tasks'][int(task)][0], 'technical': conf['tasks'][int(task)][1], 'code': code, 'error': error}
    return render(request, 'SendinBlue/failed.html', context=datas)
def responseOKHTML(task, message):
    tpl = _('status: KO\ntask: {ntask}\nname: {name}\ntechnical: {technical}\nmessage: {message}')
    datas = { 'task': task, 'name': conf['tasks'][int(task)][0], 'technical': conf['tasks'][int(task)][1], 'code': code, 'error': error}
    return render(request, 'SendinBlue/success.html', context=datas)

# ------------------------------------------- #
# CONTENT TYPE - JSON
# ------------------------------------------- #
def responseKOJSON(task, code, error):
    datas = { 'task': task, 'name': conf['tasks'][int(task)][0], 'technical': conf['tasks'][int(task)][1], 'code': code, 'error': error}
    return JsonResponse(datas, safe=False)
def responseOKJSON(task, message):
    datas = { 'task': task, 'name': conf['tasks'][int(task)][0], 'technical': conf['tasks'][int(task)][1], 'message': message}
    return JsonResponse(datas, safe=False)

# ------------------------------------------- #
# CONTENT TYPE - TXT
# ------------------------------------------- #
def responseKOTXT(task, code, error):
    tpl = _('status: KO\ntask: {ntask}\nname: {name}\ntechnical: {technical}\ncode: {code}\nerror: {error}')
    datas = {'task': task, 'name': conf['tasks'][int(task)][0], 'technical': conf['tasks'][int(task)][1], 'code': code, 'error': error}
    return HttpResponse(tpl.format(**datas), status_code=code, content_type=conf['contenttype_txt'] )
def responseOKTXT(task, message):
    tpl = _('status: KO\ntask: {task}\nname: {name}\ntechnical: {technical}\nmessage: {message}')
    datas = {'task': task, 'name': conf['tasks'][int(task)][0], 'technical': conf['tasks'][int(task)][1], 'message': message}
    return HttpResponse(tpl.format(**datas), content_type=conf['contenttype_txt'] )

# ------------------------------------------- #
# CONTENT TYPE - PROXY
# ------------------------------------------- #
# Content type orientation
# ------------------------------------------- #
def responseKO(contenttype, task, code, error):
    if contenttype == 'html': return responseKOHTML(task, code, error)
    if contenttype == 'json': return responseKOJSON(task, code, error)
    return responseKOTXT(task, code, error)
def responseOK(contenttype, task, message):
    if contenttype == 'html': return responseOKHTML(task, message)
    if contenttype == 'json': return responseOKJSON(task, message)
    return responseOKTXT(task, message)

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
# checkTask
# ------------------------------------------- #
# Check if the task can be ordered or started
# ------------------------------------------- #
def checkTask(task):
    check = '{0} {1}/{2}{3} {4} {5}'.format(conf['binary'], conf['taskdir'], conf['tasks'][0][0], conf['checkext'], task, conf['killscript'])
    try: subprocess.check_call(check, shell=True)
    except subprocess.CalledProcessError: return False
    return True

# ------------------------------------------- #
# startTask
# ------------------------------------------- #
# Try to start the task
# ------------------------------------------- #
def startTask(task):
    bgtask = '{0} {1} {2}/{3}.py {4} {5}'.format(conf['backstart'], conf['python'], conf['taskdir'], conf['tasks'][int(task)][0], conf['port'], conf['backend'])
    try: subprocess.check_call(bgtask, shell=True)
    except subprocess.CalledProcessError: return False
    return True

# ------------------------------------------- #
# error
# ------------------------------------------- #
# Task in error
# ------------------------------------------- #
def error(contenttype, task, error):
    try: script = conf['tasks'][int(task)][0]
    except NameError: return responseKO('html', task, 404, _('Task not found'))
    try: thetask = Task.objects.filter(task=script, status__in=[1, 2, 3]).latest('dateupdate')
    except Task.DoesNotExist: return responseKO(contenttype, task, 403,  _('No task'))
    thetask.status = 0
    if error is None or error == '': thetask.error = _('Error')
    else: thetask.error = error
    thetask.save()
    return responseOK(contenttype, task, error)

# ------------------------------------------- #
# order
# ------------------------------------------- #
# Order a task
# ------------------------------------------- #
def order(contenttype, task, message):
    try: script = conf['tasks'][int(task)][0]
    except NameError: return responseKO('html', task, 404, _('Task not found'))
    try: delta = conf['deltas'][script]
    except NameError: return responseKO('html', task, 404, _('Delta not found'))
    try:
        if isinstance(delta, int):
            if delta > 40: delta = datetime.today() - timedelta(seconds=delta)
            else:            delta = datetime.today() - timedelta(days=delta)
            thetask = Task.objects.get(task=script, status__in=[1,2,3], dateupdate__gte=delta)
        elif delta == 'Monthly':
            thetask = Task.objects.get(task=script, status__in=[1,2,3], dateupdate__year=datetime.now().year, dateupdate__month=datetime.now().month)
        elif delta == 'Annually':
            thetask = Task.objects.get(task=script, status__in=[1,2,3], dateupdate__year=datetime.now().year)
        else:
            return responseKO(contenttype, task, 403, _('Delta not available'))
    except Task.DoesNotExist:
        thetask = Task(task=script)
        if message is not None or message != '': thetask.info = message
        thetask.save()
    if thetask.status >= 1:
        if checkTask(script) is True:
            if startTask(task) is True:
                return responseOK(contenttype, task, message)
            return responseKO(contenttype, task, 403, _('Task can\'t be started'))
        return responseKO(contenttype, task, 403,  _('Task already running'))
    else:
        return responseKO(contenttype, task, 403, _('Delta too short please wait'))    
    return responseKO(contenttype, task, 403, _('Task can\'t be started'))

# ------------------------------------------- #
# start
# ------------------------------------------- #
# Start a task
# ------------------------------------------- #
def start(contenttype, task, message):
    try: script = conf['tasks'][int(task)][0]
    except NameError: return responseKO('html', task, 404, _('Task not found'))
    try: thetask = Task.objects.filter(task=script, status=1).latest('dateupdate')
    except Task.DoesNotExist: return responseKO(contenttype, task, 403,  _('No task to start'))
    thetask.status = 2
    if message is None or message == '': thetask.info = _('Started')
    else: thetask.info = message
    thetask.save()
    return responseOK(contenttype, task, message)

# ------------------------------------------- #
# running
# ------------------------------------------- #
# Task running
# ------------------------------------------- #
def running(contenttype, task, message):
    try: script = conf['tasks'][int(task)][0]
    except NameError: return responseKO('html', task, 404, _('Task not found'))
    try: thetask = Task.objects.filter(task=script, status__in=[2, 3]).latest('dateupdate')
    except Task.DoesNotExist: return responseKO(contenttype, task, 403,  _('No task running'))
    thetask.status = 3
    if message is None or message == '': thetask.info = _('Running')
    else: thetask.info = message
    thetask.save()
    return responseOK(contenttype, task, message)

# ------------------------------------------- #
# complete
# ------------------------------------------- #
# Task completed
# ------------------------------------------- #
def complete(contenttype, task, message):
    try: script = conf['tasks'][int(task)][0]
    except NameError: return responseKO('html', task, 404, _('Task not found'))
    try: thetask = Task.objects.filter(task=script, status__in=[2, 3]).latest('dateupdate')
    except Task.DoesNotExist: return responseKO(contenttype, task, 403,  _('No task to complete'))
    thetask.status = 4
    if message is None or message == '': thetask.info = _('Complete')
    else: thetask.info = message
    thetask.save()
    return responseOK(contenttype, task, message)


"""
-------------------------------------------------------------------
TASK INTEGRATOR
-------------------------------------------------------------------
"""

def addTRK_sort_recurring(contenttype, script):
    try:
        open(conf['appdir'] + script + '.json')
    except IOError as e:
        return responseKO(contenttype, task, 404, e)
    return responseOK(contenttype, task, 'Success')

def addTask(contenttype, task):
    try: script = conf['tasks'][int(task)][0]
    except NameError: return responseKO(contenttype, task, 404, _('Task not found'))
    if script == 'TRK_sort_recurring':
        return addTRK_sort_recurring(contenttype, script)

    return responseKO(contenttype, task, 404, _('Task unavailable'))