from .models import Task, Domain, Visitor, RouteAssociated, UserAgentAssociated, AcceptLanguageAssociated, DataAssociated
from .settings import conf


class subtaskStore:

    def addVisitors(contenttype, task, script):
        try:
            visitorsJSON = '{}/{}_visitors.json'.format(conf['taskdir'], script)
            with open(visitorsJSON) as json_data:
                visitors = []
                listtest = []
                domains = json.load(json_data)
                for domain in domains:
                    try:
                        domobj = Domain.objects.get(id=domain)
                        for k,v in domains[domain].items():
                            visitors.append(Visitor(visitor=k, domain=domobj))
                    except Domain.DoesNotExist:
                        for k,v in domains[domain].items():
                            visitors.append(Visitor(visitor=k)) 
                existing = [e for e in Visitor.objects.filter(visitor__in=visitors).values_list('visitor', flat=True)]
                visitors = [v for v in visitors if v.visitor not in existing ]
                Visitor.objects.bulk_create(visitors)
        except Exception as e:
            return str(e)
        return True