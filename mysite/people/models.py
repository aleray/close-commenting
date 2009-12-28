# *-* encoding: utf-8 *-*

from django.db import models
from geography.models import *
from django.utils.translation import ugettext_lazy as _
from wmd.models import *

class Occupation(models.Model):
    """
    Describes an occupation
    """
    name_en = models.CharField(max_length=50, verbose_name=_('Name (EN)'))
    name_fr = models.CharField(max_length=50, verbose_name=_('Name (FR)'))
    slug    = models.SlugField(verbose_name=_('Slug'), unique=True, 
                            help_text=_('Unique identifier. Allows a constant targeting of an occupation'))
    
    @property
    def name(self): return self.name_en
    
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        ordering = ['name_en']

class Person(models.Model):
    """
    Base class for a Person, be it/him/her an organization or a human being
    """
    slug           = models.SlugField(verbose_name=_('Slug'), unique=True, 
                                      help_text=_('Unique identifier. Allows a constant targeting of the person'))
    address        = models.CharField(max_length=60, verbose_name=_('Address'), blank=True)
    zip_code       = models.CharField(max_length=10, verbose_name=_('Zip Code'), blank=True)
    city           = models.ForeignKey(City, verbose_name=_('City'), null=True, blank=True)
    phone_prefix   = models.PositiveIntegerField(max_length=2, null=True, blank=True, verbose_name=_('Phone Number Prefix'),
                                                 help_text=_('2 digits without the + sign. Eg.: "31", "32" or "33"'))
    phone          = models.PositiveIntegerField(max_length=12, null=True, blank=True, verbose_name=_('Phone Number'), 
                                                 help_text=_('Phone Number without any Prefix (digits only). Eg.: "0475436789" or "0608674534" '))    
    email          = models.EmailField(verbose_name=_('Email'), blank=True)
    link           = models.URLField(verbose_name=_('Hyperlink'), verify_exists=False, blank=True)
    occupations    = models.ManyToManyField(Occupation, verbose_name=_("Occupations"), null=True, blank=True)
    description_en = MarkDownField(verbose_name=_('Description (EN)'), 
                                      help_text=_('Fill with a free description of the person'), blank=True)
    description_fr = MarkDownField(verbose_name=_('Description (FR)'), 
                                      help_text=_('Fill with a free description of the person'), blank=True)
    mood           = models.CharField(max_length=3, verbose_name=_('Mood'), blank=True)
    @property
    def all_occupations(self): return u", ".join(["%s" % k for k in self.occupations.all()])
    
    @property
    def get_person(self): 
        try:
            return u'%s' % (self.humanbeing)
        except:
            return u'%s' % (self.corporation)
        
    @property
    def link_person(self): 
        if self.link:
            return u'<a href="%s" target="_blank" class="hyperlink">%s</a>' % (self.link, self)
        else: 
            return u'%s' % self
    
    def __unicode__(self):
        try:
            return u'%s' % (self.humanbeing)
        except:
            return u'%s' % (self.corporation)
    
    class Meta:
        pass

class HumanBeing(Person):
    """
    Describes a Human being
    """
    firstname  = models.CharField(max_length=30, verbose_name=_('First Name'), blank=True)
    middlename = models.CharField(max_length=30, verbose_name=_('middle Name'), blank=True)
    lastname   = models.CharField(max_length=30, verbose_name=_('Last Name'), blank=True)
    nickname   = models.CharField(max_length=30, verbose_name=_('Nick name'), blank=True)
    is_team    = models.BooleanField(verbose_name=_('Is part of the team?'))
    
    def __unicode__(self):
        return u'%s %s %s' % (self.firstname, self.middlename, self.lastname)
        
    @property
    def last_cv_orderby_when(self): 
        return self.cventry_set.all().order_by('-beginning_date', '-ending_date')[0]
    @property
    def last_cv_orderby_what_fr(self): 
        return self.cventry_set.all().order_by('description_fr')[0].description_fr
    @property
    def last_cv_orderby_what_en(self): 
        return self.cventry_set.all().order_by('description_en')[0].description_en
    @property
    def last_cv_orderby_where(self): 
        return self.cventry_set.all().order_by('corporation', 'city')[0].cv_where
    
    @property
    def last_cventry(self): 
        try:
            return self.cventry_set.all().order_by('-beginning_date', '-ending_date')[0]
        except:
            return 0
    
    @property
    def last_cventry_beginning_date(self): 
        try:
            return self.cventry_set.all().order_by('-beginning_date', '-ending_date')[0].beginning_date
        except:
            return ""
    
    @property
    def last_cventry_cv_where(self):
        try:
            return self.cventry_set.all().order_by('-beginning_date', '-ending_date')[0].cv_where
        except:
            return ""
    
    @property
    def last_cventry_description_fr(self):
        try:
            return self.cventry_set.all().order_by('-beginning_date', '-ending_date')[0].description_fr
        except:
            return ""
    
    @property
    def last_cventry_description_en(self):
        try:
            return self.cventry_set.all().order_by('-beginning_date', '-ending_date')[0].description_en
        except:
            return ""
    
    class Meta:
        ordering = ['slug']
        verbose_name_plural = _('Human Beings')

class Corporation(Person):
    """
    Describes an corporation
    """
    name   = models.CharField(max_length=100, verbose_name=_('Name'))
    prefix = models.CharField(max_length=100, verbose_name=_('Prefix'), blank=True)
    
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        ordering = ['name']

class CVEntry(models.Model):
    """
    Describes a line in a CV
    """
    human_being    = models.ForeignKey(HumanBeing, verbose_name=_('Human Being'))
    beginning_date = models.DateField(verbose_name=_('Beginning Date'))
    ending_date    = models.DateField(verbose_name=_('Ending Date'), null=True, blank=True)
    city           = models.ForeignKey(City, verbose_name=_('City'), null=True, blank=True)
    description_en = models.CharField(max_length=60, verbose_name=_('Description (EN)'), 
                                      help_text=_('Fill with a free description of the person'))
    description_fr = models.CharField(max_length=60, verbose_name=_('Description (FR)'), 
                                      help_text=_('Fill with a free description of the person'))
    corporation    = models.ForeignKey(Corporation, verbose_name=_('Corporation'), null=True, blank=True)
    
    @property
    def description(self): return self.description_en
        
    @property
    def cv_where(self): 
        if self.corporation and self.city:
            return u'%s, %s' % (self.corporation, self.city)
        else:
            if self.corporation:
                return u'%s' % self.corporation
            else:
                return u'%s' % self.city
    
    def __unicode__(self):
        return u'%s' % self.description
    
    class Meta:
        ordering = ['-beginning_date', '-ending_date']
        verbose_name = _('CV Entry')
        verbose_name_plural = _('CV Entries')
        
