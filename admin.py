from django.contrib import admin

from .models import Domain, DataAuthorized, Tracked

class DataAuthorizedInline(admin.TabularInline):
    model = DataAuthorized
    readonly_fields = ( 'key', 'create', 'update', )
    extra = 0
@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ( 'visitor', 'key', 'value', 'domain', 'create', 'update', )
    readonly_fields = ( 'visitor', 'key', 'value', 'domain', 'create', 'update', )
    inlines = [ DataAuthorizedInline, ]

@admin.register(Tracked)
class TrackedAdmin(admin.ModelAdmin):
    list_display = ( 'visitor', 'key', 'value', 'domain', 'url', 'title',)
    readonly_fields = ( 'visitor', 'key', 'value', 'domain', 'url', 'title', )