from django.contrib import admin
from django.utils.translation import ugettext as _
from .models import Domain, DataAuthorized, Tracked

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ( 'domain', 'id', 'status', 'counter', )
    readonly_fields = ( 'domain', 'id', 'create', 'update', )


def loadDatasAuthorized(modeladmin, request, queryset):
    self.message_user(request, _('Authorized data loaded'), 'success')
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