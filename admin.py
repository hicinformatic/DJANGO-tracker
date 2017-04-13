from django.contrib import admin
from .models import Domain, DataAuthorized, Tracked

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ( 'domain', 'id',  )
    readonly_fields = ( 'domain', 'id', 'create', 'update', )

@admin.register(DataAuthorized)
class DataAuthorizedAdmin(admin.ModelAdmin):
    list_display = ( 'key', 'create', 'update', )
    readonly_fields = ( 'create', 'update', )

@admin.register(Tracked)
class TrackedAdmin(admin.ModelAdmin):
    list_display = ( 'visitor', 'key', 'value', 'domain', 'url', 'title',)
    readonly_fields = ( 'visitor', 'key', 'value', 'domain', 'url', 'title', )