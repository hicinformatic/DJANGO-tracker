from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from .settings import conf
from uuid import uuid4

class Tracked(models.Model):
    visitor = models.CharField(max_length=36, editable=False, verbose_name=_('Unique ID'),)
    key = models.CharField(max_length=254, editable=False, verbose_name=_('Key'),)
    value = models.TextField(editable=False, verbose_name=_('Value'),)
    domain = models.URLField(editable=False, verbose_name=_('Domain associated'),)
    url = models.URLField(editable=False, verbose_name=_('URL momentary'),)
    title = models.CharField(max_length=254, blank=True, null=True, editable=False, verbose_name=_('Title momentary'),)
    create = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Creation date'),)

    class Meta:
        verbose_name        = _('Tracked data')
        verbose_name_plural = _('Tracked datas')

    def __str__(self):
        return self.visitor

class DataAuthorized(models.Model):
    key = models.CharField(max_length=254, unique=True, verbose_name=_('Data'),)
    status = models.BooleanField(default=True, verbose_name=_('Enable'),)
    counter = models.BigIntegerField(default=0, verbose_name=_('Counter'),)
    load = models.BooleanField(default=False, verbose_name=_('Load'),)
    create = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Creation date'),)
    update = models.DateTimeField(auto_now=True, editable=False, verbose_name=_('Update date'),)

    class Meta:
        verbose_name        = _('Data authorized')
        verbose_name_plural = _('Datas authorized')

    def __str__(self):
        return self.key

class Domain(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name=_('Unique ID'),)
    domain = models.URLField(verbose_name=_('Domain authorized'),)
    status = models.BooleanField(default=True, verbose_name=_('Enable'),)
    counter = models.BigIntegerField(default=0, verbose_name=_('Counter'),)
    javascript = models.TextField(blank=True, null=True, editable=False, verbose_name=_('Javascript integration'),
        help_text=_('Change [--URL_STATIC--] by your static files url and [--URL_TRACKER--] by tracker domain'))
    create = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Creation date'),)
    update = models.DateTimeField(auto_now=True, editable=False, verbose_name=_('Update date'),)

    class Meta:
        verbose_name        = _('Domain authorized')
        verbose_name_plural = _('Domains authorized')

    def __str__(self):
        return self.domain

    def save(self, *args, **kwargs):
        self.javascript = conf['example'].format(reverse('tracker:trackerJS', args=(self.id.hex,)), reverse('tracker:trackerSVG', args=(self.id.hex,)),)
        super(Domain, self).save(*args, **kwargs)

class Visitor(models.Model):
    visitor = models.CharField(max_length=36, editable=False, verbose_name=_('Unique ID'), )
    domain = models.ForeignKey(Domain, verbose_name=_('Domain associated'), )

class DataAssociated(models.Model):
    visitor = models.ForeignKey(Visitor, verbose_name=_('Visitor associated'), )
    key = models.CharField(max_length=254, unique=True, verbose_name=_('Key'),)
    value = models.CharField(max_length=254, unique=True, verbose_name=_('Data'),)
    status = models.BooleanField(default=True, verbose_name=_('Enable'),)
    create = models.DateTimeField(editable=False, verbose_name=_('Creation date'),)