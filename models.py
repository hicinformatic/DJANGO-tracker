from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from .settings import conf
from uuid import uuid4

class Tracked(models.Model):
    visitor = models.CharField(max_length=36, editable=False, verbose_name=_('Unique ID'),)
    key = models.CharField(max_length=254, editable=False, verbose_name=_('Key'),)
    value = models.TextField(editable=False, verbose_name=_('Value'),)
    event = models.BooleanField(default=False, editable=False, verbose_name=_('Is an event'),)
    domain = models.CharField(max_length=32, editable=False, verbose_name=_('Domain associated'),)
    url = models.URLField(editable=False, verbose_name=_('URL momentary'),)
    title = models.CharField(max_length=254, blank=True, null=True, editable=False, verbose_name=_('Title momentary'),)
    create = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Creation date'),)

    class Meta:
        verbose_name        = _('#- Tracked data')
        verbose_name_plural = _('#- Tracked datas')

    def __str__(self):
        return self.visitor

class DataAuthorized(models.Model):
    key = models.CharField(max_length=254, unique=True, verbose_name=_('Data'),)
    status = models.BooleanField(default=True, verbose_name=_('Enable'),)
    event = models.BooleanField(default=False, verbose_name=_('Is an event'),)
    counter = models.BigIntegerField(default=0, verbose_name=_('Counter'),)
    load = models.BooleanField(default=False, verbose_name=_('Load'),)
    create = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Creation date'),)
    update = models.DateTimeField(auto_now=True, editable=False, verbose_name=_('Last modification date'),)

    class Meta:
        verbose_name        = _('Data authorized')
        verbose_name_plural = _('Datas authorized')

    def __str__(self):
        return self.key

class Domain(models.Model):
    id = models.CharField(primary_key=True, max_length=32, default=uuid4, editable=False, verbose_name=_('Unique ID'),)
    domain = models.URLField(verbose_name=_('Domain authorized'),)
    status = models.BooleanField(default=True, verbose_name=_('Enable'),)
    counter = models.BigIntegerField(default=0, verbose_name=_('Counter'),)
    javascript = models.TextField(blank=True, null=True, editable=False, verbose_name=_('Javascript integration'),
        help_text=_('Change [--URL_STATIC--] by your static files url and [--URL_TRACKER--] by tracker domain'))
    create = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Creation date'),)
    update = models.DateTimeField(auto_now=True, editable=False, verbose_name=_('Last modification date'),)

    class Meta:
        verbose_name        = _('Domain tracked')
        verbose_name_plural = _('Domains tracked')

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        self.javascript = conf['example'].format(reverse('tracker:trackerJS', args=(self.id.hex,)), reverse('tracker:trackerSVG', args=(self.id.hex,)),)
        super(Domain, self).save(*args, **kwargs)

class Visitor(models.Model):
    visitor = models.CharField(primary_key=True, max_length=60, verbose_name=_('Unique ID'),)
    domain = models.ForeignKey(Domain, blank=True, null=True, verbose_name=_('Domain associated'),)

    class Meta:
        verbose_name        = _('Visitor')
        verbose_name_plural = _('Visitors')

    def __str__(self):
        return self.visitor

class RouteAssociated(models.Model):
    visitor = models.ForeignKey(Visitor, verbose_name=_('Visitor associated'),)
    title = models.CharField(max_length=254, verbose_name=_('Title'),)
    url = models.URLField(max_length=254, verbose_name=_('URL'),)
    load = models.PositiveSmallIntegerField(blank=True, null=True, editable=False, verbose_name=_('Page Loading'),)
    create = models.DateTimeField(editable=False, verbose_name=_('Creation date'),)

    class Meta:
        verbose_name        = _('Route')
        verbose_name_plural = _('Routes')

    def __str__(self):
        return self.url

class UserAgentAssociated(models.Model):
    visitor = models.ForeignKey(Visitor, verbose_name=_('Visitor associated'),)
    useragent = models.TextField(editable=False, verbose_name=_('User-Agent'),)
    create = models.DateTimeField(editable=False, verbose_name=_('Creation date'),)

    class Meta:
        verbose_name        = _('User-Agent')
        verbose_name_plural = _('User-Agents')

    def __str__(self):
        return self.useragent

class AcceptLanguageAssociated(models.Model):
    visitor = models.ForeignKey(Visitor, verbose_name=_('Visitor associated'), )
    acceptlanguage = models.TextField(editable=False, verbose_name=_('AcceptLanguage'),)
    create = models.DateTimeField(editable=False, verbose_name=_('Creation date'),)

    class Meta:
        verbose_name        = _('Accepted Language')
        verbose_name_plural = _('Accepted Languages')

    def __str__(self):
        return self.acceptlanguage

class DataAssociated(models.Model):
    visitor = models.ForeignKey(Visitor, verbose_name=_('Visitor associated'), )
    key = models.CharField(max_length=254, verbose_name=_('Key'),)
    value = models.CharField(max_length=254, verbose_name=_('Value'),)
    title = models.CharField(max_length=254, verbose_name=_('Title'),)
    url = models.URLField(max_length=254, verbose_name=_('URL'),)
    create = models.DateTimeField(editable=False, verbose_name=_('Creation date'),)

    class Meta:
        verbose_name        = _('Data')
        verbose_name_plural = _('Datas')

    def __str__(self):
        return self.key

class EventAssociated(models.Model):
    visitor = models.ForeignKey(Visitor, verbose_name=_('Visitor associated'), )
    key = models.CharField(max_length=254, verbose_name=_('Key'),)
    value = models.CharField(max_length=254, verbose_name=_('Value'),)
    title = models.CharField(max_length=254, verbose_name=_('Title'),)
    url = models.URLField(max_length=254, verbose_name=_('URL'),)
    create = models.DateTimeField(editable=False, verbose_name=_('Creation date'),)

    class Meta:
        verbose_name        = _('Data')
        verbose_name_plural = _('Datas')

    def __str__(self):
        return self.key


class Task(models.Model):
    task = models.CharField(max_length=254, choices=conf['tasks'], editable=False, verbose_name=_('Task'), )
    info = models.TextField(blank=True, default=_('Ordered'), editable=False, null=True, verbose_name=_('Information about the task'),)
    status = models.PositiveSmallIntegerField(choices=conf['status'], default=1, editable=False, verbose_name=_('Status'), validators=[MinValueValidator(0),MaxValueValidator(5)], )
    error = models.TextField(blank=True, editable=False, null=True, verbose_name=_('Error encountered'),)
    updateby = models.CharField(blank=True, editable=False, max_length=254, null=True, verbose_name=_('Last update by'),)
    datecreate = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Creation date'),)
    dateupdate = models.DateTimeField(auto_now=True, editable=False, verbose_name=_('Last modification date'),)

    class Meta:
        verbose_name        = _('#- Task')
        verbose_name_plural = _('#- Tasks')

    def __str__(self):
        return self.get_task_display()