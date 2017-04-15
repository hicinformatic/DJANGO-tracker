from django.conf import settings
import os

conf = {'appdir': os.path.dirname(os.path.realpath(__file__)), }

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
conf['ndatas'] = 50

# Content Type
conf['contenttype_txt'] = 'text/plain; charset=%s' % conf['charset']
conf['contenttype_svg'] = 'image/svg+xml; charset=%s' % conf['charset']
conf['contenttype_js'] = 'application/javascript; charset=%s' % conf['charset']

# Default datas
conf['datas'] = [
    'visitor',
    'url',
    'title',
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

conf['example'] = """<!--
[--URL_STATIC--]  -> Static URL hosting the javascript file
[--URL_TRACKER--] -> URL of the tracker | Leave empty if the host is the same
-->

<!-- Own host JS | better -->
<script src="[--URL_STATIC--]/visit.js"></script>
<!-- Direct host JS -->
<script src="[--URL_TRACKER--]{0}"></script>

<!-- Use example -->
<script>
(function() {
    visit = new visit('[--URL_TRACKER--]');
    visit.add('height', window.screen.height);
    visit.add('width', window.screen.width);
    visit.visit();
})();
</script>
<noscript><img width=0 height=0 src="[--URL_TRACKER--]{1}"></noscript>
"""

for k,v in conf.items():
    try:
        conf[k] = MANAGER[k]
    except Exception:
        pass