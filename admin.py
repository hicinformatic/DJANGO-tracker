from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Domain, DataAuthorized, Tracked
from .settings import conf

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ( 'domain', 'id', 'status', 'counter', )
    readonly_fields = ( 'domain', 'id', 'create', 'update', )

def loadDatasAuthorized(modeladmin, request, queryset):
    with open(conf['appdir'] + '/moreconf.py', 'w') as f:
        f.write('more = [\r')
        for q in queryset:
            f.write(q.key + ',\n')
        f.write(']')
    f.closed
    modeladmin.message_user(request, _('Authorized data loaded'), 'success')
loadDatasAuthorized.short_description = _('Loads authorized data')
@admin.register(DataAuthorized)
class DataAuthorizedAdmin(admin.ModelAdmin):
    list_display = ( 'key', 'status', 'counter', )
    readonly_fields = ( 'create', 'update', 'counter', )
    actions = [ loadDatasAuthorized, ]

@admin.register(Tracked)
class TrackedAdmin(admin.ModelAdmin):
    list_display = ( 'visitor', 'key', 'value', 'domain', 'url', 'title',)
    readonly_fields = ( 'visitor', 'key', 'value', 'domain', 'url', 'title', )