from django.contrib import admin
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from .models import Domain, DataAuthorized, Tracked
from .settings import conf


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ( 'domain', 'id', 'downloadJS', 'visitSVG', 'status', 'counter', )
    readonly_fields = ( 'id', 'status', 'javascript', 'counter', 'create', 'update', )

    def downloadJS(self, obj):
        return u'<a href="%s">%s</a>' % (reverse('tracker:downloadJS', args=(obj.id.hex,)), _('Download javascript'), )
    downloadJS.allow_tags = True
    downloadJS.short_description = _('JS')

    def visitSVG(self, obj):
        return u'<a href="%s">%s</a>' % (reverse('tracker:visitSVG', args=(obj.id.hex,)), _('noscript SVG'), )
    visitSVG.allow_tags = True
    visitSVG.short_description = _('SVG')

def loadDatasAuthorized(modeladmin, request, queryset):
    with open(conf['appdir'] + '/moreconf.py', 'w') as f:
        f.write('more = [\n')
        for q in queryset:
            if q.status is True:
                f.write("    '" + q.key + "',\n")
        f.write(']').closed
        queryset.filter(status=False).update(load=False)
        queryset.filter(status=True).update(load=True)
        DataAuthorized.objects.exclude(id__in=queryset).update(load=False)
        modeladmin.message_user(request, _('Authorized data loaded'), 'success')
loadDatasAuthorized.short_description = _('Loads authorized data')
def disableDatasAuthorized(modeladmin, request, queryset):
    with open(conf['appdir'] + '/moreconf.py', 'w') as f:
        queryset.update(status=False, load=True)
        DataAuthorized.objects.exclude(id__in=queryset).update(load=False)
        modeladmin.message_user(request, _('Authorized data disable'), 'success')
disableDatasAuthorized.short_description = _('Disable authorized data')
@admin.register(DataAuthorized)
class DataAuthorizedAdmin(admin.ModelAdmin):
    list_display = ( 'key', 'status', 'load', 'counter', )
    readonly_fields = ( 'create', 'update', 'load', 'counter', )
    actions = [ loadDatasAuthorized, disableDatasAuthorized, ]

@admin.register(Tracked)
class TrackedAdmin(admin.ModelAdmin):
    list_display = ( 'visitor', 'key', 'value', 'domain', 'url', 'title',)
    readonly_fields = ( 'visitor', 'key', 'value', 'domain', 'url', 'title', )