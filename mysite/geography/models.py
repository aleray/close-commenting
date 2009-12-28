# *-* encoding: utf-8 *-*

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Country(models.Model):
    """
    Describes a country
    """
    name_en  = models.CharField(max_length=100, verbose_name=_('Name (EN)'))
    name_fr  = models.CharField(max_length=100, verbose_name=_('Name (FR)'))
    slug     = models.SlugField(verbose_name=_('Slug'), unique=True, 
                                help_text=_('Unique identifier. Allows a constant targeting of the country'))
    iso_code = models.CharField(max_length=2, verbose_name=_('ISO Code'), help_text=_('2 letters ISO code'))    
    
    @property
    def name(self): return self.name_en
        
    def save(self):
        try:
            self.iso_code = self.iso_code.upper()
            super(Country, self).save()
        except:
            super(Country, self).save()
    
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ['name_en']


class City(models.Model):
    """
    Describes a city
    """
    name_en = models.CharField(max_length=100, verbose_name=_('Name (EN)'))
    name_fr = models.CharField(max_length=100, verbose_name=_('Name (FR)'))
    slug    = models.SlugField(verbose_name=_('Slug'), unique=True, 
                               help_text=_('Unique identifier. Allows a constant targeting of the city'))
    country = models.ForeignKey(Country, verbose_name=_('Country'))
    
    @property
    def name(self): return self.name_en
    
    def __unicode__(self):
        return u'%s' % (self.name)
    
    class Meta:
        ordering = ['name_en', 'country']
        verbose_name_plural = 'Cities'


class Language(models.Model):
    """
    Describes a language
    """
    name_en  = models.CharField(max_length=100, verbose_name=_('Name (EN)'))
    name_fr  = models.CharField(max_length=100, verbose_name=_('Name (FR)'))
    slug = models.SlugField(verbose_name=_('Slug'), unique=True, 
                            help_text=_('Unique identifier. Allows a constant targeting of the language'))
    iso_code = models.CharField(max_length=2, verbose_name=_('ISO Code'), help_text=_('2 letters ISO code'))
    
    @property
    def name(self): return self.name_en
    
    def save(self):
        try:
            self.iso_code = self.iso_code.upper()
            super(Language, self).save()
        except:
            super(Language, self).save()
    
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        ordering = ['name_en']
        
