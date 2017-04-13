from .settings import conf
import uuid

def isTrack(request, visitor):
    try: return request.session[conf['store']]
    except Exception: pass
    try: return request.get_signed_cookie(conf['store'], salt=conf['salt'])
    except Exception: pass
    return visitor if visitor != '' else str(uuid.uuid4)

def firsTrack(request):
    try: return request.session[conf['first']]
    except Exception: pass
    try: return request.get_signed_cookie(conf['first'], salt=conf['salt'])
    except Exception: pass
    return False