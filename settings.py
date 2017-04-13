from django.conf import settings
from shutil import copyfile

conf = {}

# Global
conf['salt'] = 'y-;1n430^484ylwf$9@`4I1NZ.4xHK'
conf['store'] = 'folvis'
conf['first'] = 'firvis'

# Source
conf['host'] = 'localhost'
conf['ip'] = '127.0.0.1'

# Encoding
conf['charset'] = 'utf-8'

# Delta
conf['delta'] = 86400
conf['maxage'] = 86400

# Content Type
conf['contenttype_txt'] = 'text/plain; charset=%s' % conf['charset']
conf['contenttype_svg'] = 'image/svg+xml; charset=%s' % conf['charset']
conf['contenttype_js'] = 'application/javascript; charset=%s' % conf['charset']

# Default datas
conf['datas'] = [
    'connectEnd',
    'connectStart',
    'domComplete',
    'domContentLoadedEventEnd',
    'domContentLoadedEventStart',
    'domInteractive',
    'domLoading',
    'domainLookupEnd',
    'domainLookupStart',
    'fetchStart',
    'loadEventEnd',
    'loadEventStart',
    'navigationStart',
    'redirectCount',
    'redirectEnd',
    'redirectStart',
    'requestStart',
    'responseEnd',
    'responseStart',
    'timing',
    'navigation',
    'performance',
    'type',
    'unloadEventEnd',
    'unloadEventStart',
    'colorDepth',
    'pixelDepth',
    'height',
    'width',
    'availHeight',
    'availWidth',
    'innerWidth',
    'innerHeight',
    'outerWidth',
    'outerHeight',
    'Resize_innerWidth',
    'Resize_innerHeight',
    'Resize_outerWidth',
    'Resize_outerHeight',
]

for k,v in conf.items():
    try:
        conf[k] = MANAGER[k]
    except Exception:
        pass