from django import forms
from .settings import conf

try:
    from .moredatas import datas
    DatasAuthorized = conf['datas']+datas
except Exception:
    DatasAuthorized = conf['datas']

try:
    from .moreevents import events
    EventsAuthorized = conf['events']+events
except Exception:
    EventsAuthorized = conf['events']

class trackFormDatas(forms.Form):
    def __init__(self, *args, **kwargs):
        super(trackFormDatas, self).__init__(*args, **kwargs)
        for field in DatasAuthorized:
            self.fields[field] = forms.CharField(required=False)

class trackFormEvents(forms.Form):
    def __init__(self, *args, **kwargs):
        super(trackFormEvents, self).__init__(*args, **kwargs)
        for field in EventsAuthorized:
            self.fields[field] = forms.CharField(required=False)