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
    return response = render(request, 'tracker/failed.html', context=datas)
def responseOKHTML(task, code, error):
    tpl = _('status: KO\ntask: {ntask}\nname: {name}\ntechnical: {technical}\ncode: {code}\nerror: {error}')
    datas = { 'task': task, 'name': conf['tasks'][int(task)][0], 'technical': conf['tasks'][int(task)][1], 'code': code, 'error': error}
    return response = render(request, 'tracker/success.html', context=datas)

# ------------------------------------------- #
# CONTENT TYPE - JSON
# ------------------------------------------- #
def responseKOJSON(task, code, error):
    datas = { 'task': task, 'name': conf['tasks'][int(task)][0], 'technical': conf['tasks'][int(task)][1], 'code': code, 'error': error}
    return JsonResponse(datas, safe=False)
def responseOKJSON(task, code, error):
    datas = { 'task': task, 'name': conf['tasks'][int(task)][0], 'technical': conf['tasks'][int(task)][1], 'code': code, 'error': error}
    return JsonResponse(datas, safe=False)

# ------------------------------------------- #
# CONTENT TYPE - TXT
# ------------------------------------------- #
def responseKOTXT(task, code, error):
    tpl = _('status: KO\ntask: {ntask}\nname: {name}\ntechnical: {technical}\ncode: {code}\nerror: {error}')
    datas = {'task': task, 'name': conf['tasks'][int(task)][0], 'technical': conf['tasks'][int(task)][1], 'code': code, 'error': error}
    return HttpResponse(tpl.format(**datas), status_code=code, content_type=conf['contenttype_txt'] )
def responseOKTXT(task, code, error):
    tpl = _('status: KO\ntask: {ntask}\nname: {name}\ntechnical: {technical}\ncode: {code}\nerror: {error}')
    datas = {'task': task, 'name': conf['tasks'][int(task)][0], 'technical': conf['tasks'][int(task)][1], 'code': code, 'error': error}
    return HttpResponse(tpl.format(**datas), status_code=code, content_type=conf['contenttype_txt'] )

# ------------------------------------------- #
# CONTENT TYPE - PROXY
# ------------------------------------------- #
# Content type orientation
# ------------------------------------------- #
def reponseKO(contenttype, task, code, error):
    if conttenttype == 'html': return responseKOHTML(task, code, error)
    if conttenttype == 'json': return responseKOJSON(task, code, error)
    return responseKOTXT(task, code, error)
def reponseOK(contenttype, task, code, error):
    if conttenttype == 'html': return responseOKHTML(task, code, error)
    if conttenttype == 'json': return responseOKJSON(task, code, error)
    return responseOKTXT(task, code, error)

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
    bgtask = '{0} {1} {2}/{3}.py {4}'.format(conf['backstart'], conf['python'], conf['taskdir'], conf['tasks'][int(task)][0], conf['backend'])
    try: subprocess.check_call(bgtask, shell=True)
    except subprocess.CalledProcessError: return False
    return True

# ------------------------------------------- #
# order
# ------------------------------------------- #
# Order a task
# ------------------------------------------- #
def order(task, message, contenttype):
    try:
        if isinstance(delta, int):
            if delta > 1000: delta = datetime.today() - timedelta(seconds=delta)
            else:            delta = datetime.today() - timedelta(days=delta)
            thetask = Task.objects.get(task=task, update__gte=delta)
        elif delta == 'Monthly':
            thetask = Task.objects.get(task=task, update__year=datetime.now().year, update__month=datetime.now().month)
        elif delta == 'Annually':
            thetask = Task.objects.get(task=task, update__year=datetime.now().year)
        else:
            return reponseKO(contenttype, task, 403, _('Delta not available'))
    except Task.DoesNotExist:
        thetask = Task(task=script)
        thetask.save()
    if thetask.status >= 1:
        if checkTask(script) is True:
            if startTask(task) is True:
                if contenttype == 'html': return render(request, 'tracker/success.html', context={'task': thetask, 'message': _('Task ordered')})
            return reponseKO(contenttype, task, 403, _('Task can\'t be started'))
        return reponseKO(contenttype, task, 403,  _('Task already running'))
    return reponseKO(contenttype, task, 403, _('Task can\'t be started'))