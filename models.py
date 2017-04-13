from django.db import models
from django.utils.translation import ugettext as _

from uuid import uuid4

class Domain(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name=_('Unique ID'),)
    domain = models.URLField(editable=False, verbose_name=_('Domain authorized'),)
    status = models.BooleanField(default=True, verbose_name=_('Enable'),)
    counter = models.BigIntegerField(default=0, verbose_name=_('Counter'),)
    create = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Creation date'),)
    update = models.DateTimeField(auto_now=True, editable=False, verbose_name=_('Update date'),)

    class Meta:
        verbose_name        = _('Domain authorized')
        verbose_name_plural = _('Domains authorized')

    def __str__(self):
        return self.domain

class DataAuthorized(models.Model):
    key = models.CharField(max_length=254, unique=True, verbose_name=_('Data'),)
    status = models.BooleanField(default=True, verbose_name=_('Enable'),)
    counter = models.BigIntegerField(default=0, verbose_name=_('Counter'),)
    create = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Creation date'),)
    update = models.DateTimeField(auto_now=True, editable=False, verbose_name=_('Update date'),)

    class Meta:
        verbose_name        = _('Data authorized')
        verbose_name_plural = _('Datas authorized')

    def __str__(self):
        return self.key

class Tracked(models.Model):
    visitor = models.CharField(max_length=32, editable=False, verbose_name=_('Unique ID'),)
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
