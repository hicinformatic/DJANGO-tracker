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