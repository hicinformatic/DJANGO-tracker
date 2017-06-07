from django.utils.translation import ugettext as _
from django.conf import settings
import os, syslog

# ------------------------------------------- #
# CONFIGURATION
# ------------------------------------------- #

# Global
conf = {
    'appdir':     os.path.dirname(os.path.realpath(__file__)),
    'taskdir':    os.path.dirname(os.path.realpath(__file__))+'/tasks',
    'python':     '/bin/python3.6',
    'binary':     '/bin/bash',
    'backstart':  '/bin/nohup',
    'backend':    '&',
    'checkext':   '.sh',
    'syslog':     False,
    'sysloglvl':  5,
    'killscript': 3600,
    'host':       'localhost',
    'ip':         '127.0.0.1',
    'export':     30,
    'salt':       'y-;1n430^484ylwf$9@`4I1NZ.4xHK',
    'store':      'folvis',
    'first':      'firvis',
    'charset':    'utf-8',
    'maxage':     86400,
    'ndatas':     50,
    'port':       27080,
}

# Content Type
conf['contenttype_csv'] = 'text/csv; charset=%s' % conf['charset']
conf['contenttype_txt'] = 'text/plain; charset=%s' % conf['charset']
conf['contenttype_svg'] = 'image/svg+xml; charset=%s' % conf['charset']
conf['contenttype_js'] = 'application/javascript; charset=%s' % conf['charset']

# Tasks type
conf['tasks'] = (
    ('TRK_check_os',        _('check(OS)')),
    ('TRK_sort_recurring',  _('sort(Recurring)')),
    ('TRK_report_hourly',   _('report(Hourly)')),
    ('TRK_report_daily',    _('report(Daily)')),
    ('TRK_report_monthly',  _('report(Monthly)')),
    ('TRK_report_annually', _('report(Annually)')),
    ('TRK_purge_visit',     _('purge(Visit)')),
    ('TRK_purge_report',    _('purge(Report)')),
    ('TRK_purge_task',      _('purge(Task)')),
)

conf['subtasks'] = {
    'TRK_sort_recurring': ['addVisitors', 'addAllInfos', 'delTrackedSort'],
}

# Deltas tasks
conf['deltas'] = {
    'TRK_sort_recurring':  300,
    'TRK_report_hourly':   3600,
    'TRK_report_daily':    86400,
    'TRK_report_monthly':  'Monthly',
    'TRK_report_annually': 'Annually',
    'TRK_purge_visit':     300,
    'TRK_purge_report':    3600,
    'TRK_purge_task':      86400,
}

# Status
conf['status'] = (
    (0, _('In error')),
    (1, _('Ordered')),
    (2, _('Started')),
    (3, _('Running')),
    (4, _('Complete')),
)

# Default datas
conf['datas'] = [
    'visitor',
    'url',
    'title',
    'route',
    'connectEnd',
    'connectStart',
    'secureConnectionStart',
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
    'ResizeInnerWidth',
    'ResizeInnerHeight',
    'ResizeOuterWidth',
    'ResizeOuterHeight',
]

conf['events'] = [
    'visitor',
    'url',
    'title',
    'stay',
    'click',
    'scrolldown',
    'scrollup',
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

# ------------------------------------------- #
# LOGMETHIS
# ------------------------------------------- #
# Function de log system
def logmethis(lvl, msg):
    if conf['syslog'] is True and conf['sysloglvl'] >= lvl:
        syslog.openlog(logoption=syslog.LOG_PID)
        syslog.syslog(lvl, msg)
        syslog.closelog()