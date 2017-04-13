from django import forms
from .settings import conf

try:
    from .moreconf import more
    DatasAuthorized = conf['datas']+more
except Exception:
    DatasAuthorized = conf['datas']

class trackFormDatas(forms.Form):
    def __init__(self, *args, **kwargs):
        super(trackFormDatas, self).__init__(*args, **kwargs)
        for field in DatasAuthorized:
            self.fields[field] = forms.CharField(required=False)