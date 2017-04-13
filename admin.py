from django.contrib import admin

from .models import Domain, DataAuthorized, Tracked


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ( 'visitor', 'key', 'value', 'domain', 'create', 'update', )
    readonly_fields = ( 'visitor', 'key', 'value', 'domain', 'create', 'update', )

@admin.register(DataAuthorized)
class DataAuthorizedInline(admin.TabularInline):
    list_display = ( 'key', 'create', 'update', )
    readonly_fields = ( 'key', 'create', 'update', )

@admin.register(Tracked)
class TrackedAdmin(admin.ModelAdmin):
    list_display = ( 'visitor', 'key', 'value', 'domain', 'url', 'title',)
    readonly_fields = ( 'visitor', 'key', 'value', 'domain', 'url', 'title', )