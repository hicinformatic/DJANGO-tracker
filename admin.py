
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from .models import Task, Tracked, Domain, Visitor, RouteAssociated, UserAgentAssociated, AcceptLanguageAssociated, DataAssociated, EventAssociated
from .settings import conf

@admin.register(Tracked)
class TrackedAdmin(admin.ModelAdmin):
    list_display = ( 'visitor', 'event', 'key', 'value', 'domain', 'url', 'title', )
    readonly_fields = ( 'visitor', 'event', 'key', 'value', 'domain', 'url', 'title', 'create', )

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ( 'domain', 'id', 'downloadJS', 'visitJS', 'visitSVG', 'status', 'counter', )
    readonly_fields = ( 'id', 'status', 'javascript', 'counter', 'create', 'update', )

    def downloadJS(self, obj):
        return u'<a href="%s">%s</a>' % (reverse('tracker:downloadJS', args=(str(obj.id),)), _('Download javascript'), )
    downloadJS.allow_tags = True
    downloadJS.short_description = _('Download')

    def visitJS(self, obj):
        return u'<a href="%s">%s</a>' % (reverse('tracker:trackerJS', args=(str(obj.id),)), _('Direct JS'), )
    visitJS.allow_tags = True
    visitJS.short_description = _('JS')

    def visitSVG(self, obj):
        return u'<a href="%s">%s</a>' % (reverse('tracker:trackerSVG', args=(str(obj.id),)), _('noscript SVG'), )
    visitSVG.allow_tags = True
    visitSVG.short_description = _('SVG')


class VisitorRouteInline(admin.TabularInline):
    model = RouteAssociated
    extra = 0
class VisitorUserAgentInline(admin.TabularInline):
    model = UserAgentAssociated
    extra = 0
class VisitorAcceptLanguagesInline(admin.TabularInline):
    model = AcceptLanguageAssociated
    extra = 0
class VisitorDatasInline(admin.TabularInline):
    model = DataAssociated
    extra = 0
class VisitorEventsInline(admin.TabularInline):
    model = EventAssociated
    extra = 0
@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ( 'visitor', 'domain', )
    readonly_fields = ( 'visitor', 'domain', )
    inlines = [ VisitorRouteInline, VisitorUserAgentInline, VisitorAcceptLanguagesInline, VisitorDatasInline, VisitorEventsInline ]
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ( 'task', 'info', 'status', 'dateupdate', )
    readonly_fields = ( 'task', 'info', 'status', 'error', 'updateby', 'datecreate', 'dateupdate', )
