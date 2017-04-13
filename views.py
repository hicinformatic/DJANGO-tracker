from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .settings import conf
from .functions import isTrack
from .decorators import localcall, localcalloradmin, localcalloradminorstaff
from .forms import trackFormDatas

def downloadJS(request, domain):
    context = { 'domain': domain, 'url': request.META['HTTP_HOST'], }
    response = render(request, 'tracker/tracker.js', context=context, content_type=conf['contenttype_js'],)
    response['Content-Disposition'] = 'attachment; filename=visit.js'
    return response

def trackerSVG(request, visitor=''):
    visitor = isTrack(request, visitor)
    Tracked.objects.bulk_create([
        Tracked(visitor=visitor, key='User-Agent', value=request.META['HTTP_USER_AGENT'], domain=domain),
        Tracked(visitor=visitor, key='AcceptLanguage', value=request.META['HTTP_ACCEPT_LANGUAGE'], domain=domain),
    ])
    request.session[conf['store']] = visitor
    response.set_signed_cookie(conf['store'], visitor, salt=conf['salt'])
    return HttpResponse('<svg width="0" height="0"><text>%s</text></svg>' % visitor, content_type=conf['contenttype_svg'])

@csrf_exempt
def trackerDATAS(request, domain):
    response = HttpResponse('KO', content_type=conf['contenttype_txt'])
    if request.method == 'POST':
        form = trackFormDatas(request.POST)
        if form.is_valid():
            visitor = isTrack(request, form.clean_data['visitor'])
            datas = []
            if firsTrack(request):
                datas.append(Tracked(visitor=visitor, key='User-Agent', value=request.META['HTTP_USER_AGENT'], domain=domain))
                datas.append(Tracked(visitor=visitor, key='AcceptLanguage', value=request.META['HTTP_ACCEPT_LANGUAGE'], domain=domain))
            for key,value in form.clean_data.items():
                if value != '': datas.append(Tracked(visitor=visitor, key=key, value=value, domain=domain))
            Tracked.objects.bulk_create(datas)
        response = HttpResponse('OK', content_type=conf['contenttype_txt'])
        request.session[conf['store']] = visitor
        request.session[conf['first']] = visitor
        response.set_signed_cookie(conf['store'], visitor, salt=conf['salt'], max_age=conf['maxage'])
        response.set_signed_cookie(conf['first'], visitor, salt=conf['salt'], max_age=conf['maxage'])
    else:
        form = trackFormDatas()
    return HttpResponse('<form method="POST">%s<input type="submit"></form>' % form)
