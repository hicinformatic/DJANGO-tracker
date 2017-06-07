from django import forms
from .settings import conf

class trackFormDatas(forms.Form):
    def __init__(self, *args, **kwargs):
        super(trackFormDatas, self).__init__(*args, **kwargs)
        for field in conf['datas']:
            self.fields[field] = forms.CharField(required=False)

class trackFormEvents(forms.Form):
    def __init__(self, *args, **kwargs):
        super(trackFormEvents, self).__init__(*args, **kwargs)
        for field in conf['events']:
            self.fields[field] = forms.CharField(required=False)