# *-* encoding: utf-8 *-*

from django.db import models
from django.utils.translation import ugettext_lazy as _

class License(models.Model):
    """
    Describes a licence.
    """
    name       = models.CharField(max_length=50, verbose_name=_('Name'))
    body       = models.TextField(verbose_name=_('Body'))
    identifier = models.SlugField(verbose_name=_('Slug'), unique=True, help_text=_('Unique identifier. Allows a constant targeting of an occupation'))
    
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        ordering = ['name']
    
class Right(models.Model):
    """
    Describes an Right.
    """
    copyright = models.CharField(max_length=200, verbose_name=_('Name'))
    licence   = models.ManyToManyField(License, verbose_name=_('Name'), null=True, blank=True)
    
    def __unicode__(self):
        return u'%s' % self.copyright
    
    class Meta:
        ordering = ['copyright']
