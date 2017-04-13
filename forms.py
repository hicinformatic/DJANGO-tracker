from django import forms

from .settings import conf
try:
    from .more import more
    conf['data'] = conf['data']+more
except Exception:
    pass

class trackFormDatas(forms.Form):
    def __init__(self, *args, **kwargs):
        super(trackFormDatas, self).__init__(*args, **kwargs)
        for field in conf['datas']:
            self.fields[field] = forms.CharField(required=False)