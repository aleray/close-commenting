# *-* encoding: utf-8 *-*

## This file is part of Close Commenting.
## 
## Close Commenting is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## any later version.
## 
## Close Commenting is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with Close Commenting.  If not, see <http://www.gnu.org/licenses/>.


from django.db import models
from django.utils.translation import ugettext_lazy as _

from rights.models import Right
from geography.models import Language
from people.models import Person

from wmd.models import *
import md5
import re
import markdown
from BeautifulSoup import BeautifulSoup


class DocumentType(models.Model):
    """
    Describes a type of document.
    It can be a physical type or a digital format.
    Typical examples would be a Book, or an OGG file.
    """
    
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    
    def __unicode__(self):
        return u'%s' % self.name

class Document(models.Model):
    """
    Meta Class for any document type.
    It implements the Dublin Core Metadata Element Set, Version 1.1.
    See http://dublincore.org/documents/2008/01/14/dces/
    """
    
    help_texts = {
        'contributor' : _('An entity responsible for making contributions to the resource.'),
        'coverage'    : _('The spatial or temporal topic of the resource, the spatial applicability \
                           of the resource, or the jurisdiction under which the resource is relevant.'),
        'creator'     : _('An entity primarily responsible for making the resource.'),
        'date'        : _('A point or period of time associated with an event in the lifecycle of the resource.'),
        'description' : _('An account of the resource.'),
        'format'      : _('The file format, physical medium, or dimensions of the resource.'),
        'identifier'  : _('An unambiguous reference to the resource within a given context.'),
        'language'    : _('A language of the resource.'),
        'publisher'   : _('An entity responsible for making the resource available.'),
        'relation'    : _('A related resource.'),
        'rights'      : _('Information about rights held in and over the resource.'),
        'source'      : _('A related resource from which the described resource is derived.'),
        'subject'     : _('The topic of the resource.'),
        'title'       : _('A name given to the resource.'),
        'type'        : _('The nature or genre of the resource.'),
    }
    
    dc_contributor = models.ManyToManyField(Person, verbose_name=_('Contributors'), help_text=help_texts['contributor'])
    dc_coverage    = models.CharField(max_length=50, verbose_name=_('Coverage'), help_text=help_texts['coverage'])
    dc_creator     = models.ManyToManyField(Person, related_name='document_creator_set', verbose_name=_('Creators'), help_text=help_texts['creator'])
    dc_date        = models.DateField(verbose_name=_('Date'), help_text=help_texts['date'])
    dc_description = models.TextField(verbose_name=_('Description'), help_text=help_texts['description'])
    dc_format      = models.CharField(max_length=50, verbose_name=_('Format'), help_text=help_texts['format'])
    dc_identifier  = models.SlugField(verbose_name=_('Identifier'), help_text=help_texts['identifier'])
    dc_language    = models.ForeignKey(Language, verbose_name=_('Language'), help_text=help_texts['language'])
    dc_publisher   = models.ManyToManyField(Person, related_name='document_publisher_set', verbose_name=_('Publishers'), help_text=help_texts['publisher'])
    dc_relation    = models.CharField(max_length=50, verbose_name=_('Relation'), help_text=help_texts['relation'])
    dc_rights      = models.ManyToManyField(Right, related_name='document_right_set', verbose_name=_('Rights'), help_text=help_texts['rights'])
    dc_source      = models.CharField(max_length=50, verbose_name=_('Source'), help_text=help_texts['source'])
    dc_subject     = models.CharField(max_length=50, verbose_name=_('Subject'), help_text=help_texts['subject'])
    dc_title       = models.CharField(max_length=50, verbose_name=_('Title'), help_text=help_texts['title'])
    dc_type        = models.ForeignKey(DocumentType, verbose_name=_('Type'), help_text=help_texts['type'])
    
    # TODO
    # Define dublin core metadata using properties
    # for example:
    # @property
    # def dc_title(self): return self.title
    # or
    # @property
    # def dc_contributor(self): return u", ".join(["%s" % c for c in self.contributors.all()])
    
    def __unicode__(self):
        return u'%s' % self.dc_title
    
    # class Meta:
    #     abstract = True


class Text(Document):
    """
    Describes a text document.
    """
    
    body = MarkDownField(verbose_name=_('Body'))
        
    def save(self):
        """
        Saves the text and split it in pieces according to its paragraphs breaks.
        Compare the new paragraphs checksums with the existing ones, if any.
        Matching checksum paragraphs are preserved, allowing consistency in comment linking.
        Non-Matching checksum paragraphs are deleted.
        """
        
        super(Text, self).save()
        
        # # TODO: check Difflib and see how it could be integrated
        # existing_paragraphs = Paragraph.objects.filter(text=self)
        # output = markdown.markdown(self.body) 
        # pattern = re.compile(r'<p>(.*?)</p>', re.S)
        # new_paragraphs = [] # Creates a list of this form: [(paragraph_content , checksum), … ]
        # 
        # for match in pattern.findall(output):
        #     if not match.isspace():
        #         text = match.encode('utf-8')
        #         hash = md5.new()
        #         hash.update(text)
        #         new_paragraphs.append((text, hash.hexdigest()))
        #         
        # new_checksums = set(t[1] for t in new_paragraphs)
        # for p in existing_paragraphs:
        #     if not p.checksum in new_checksums:
        #         p.delete()
        # 
        # existing_checksums = set(p.checksum for p in existing_paragraphs)
        # for p, cs in new_paragraphs:
        #     if not cs in existing_checksums:
        #         paragraph = Paragraph()
        #         paragraph.text = self
        #         paragraph.content = p
        #         paragraph.checksum = cs
        #         paragraph.save()
        
        existing_paragraphs = Paragraph.objects.filter(text=self)
        output = markdown.markdown(self.body, ['footnotes'])
        
        new_paragraphs = [] # Creates a list of this form: [(paragraph_content , checksum), … ]
        # soup = BeautifulSoup(output)
        # for p in soup.findAll(text=True)
        for p in BeautifulSoup(output):
            if not unicode(p.string).encode('utf-8').isspace():
                text = unicode(p).encode('utf-8')
                hash = md5.new()
                hash.update(text)
                new_paragraphs.append((text, hash.hexdigest()))
        
        new_checksums = set(t[1] for t in new_paragraphs)
        for p in existing_paragraphs:
            if not p.checksum in new_checksums:
                p.delete()

        existing_checksums = set(p.checksum for p in existing_paragraphs)
        for p, cs in new_paragraphs:
            if not cs in existing_checksums:
                paragraph = Paragraph()
                paragraph.text = self
                paragraph.content = p
                paragraph.checksum = cs
                paragraph.save()


# TODO:
# Rename this class "Chunck" (or "section"?)
class Paragraph(models.Model):
    """
    Describes a paragraphs to comment on. Automatically created 
    after a Text when the paragraph comment option is checked.
    """
    
    text     = models.ForeignKey(Text)
    content  = models.TextField()
    checksum = models.CharField(max_length=32)
    
    def __unicode__(self):
        return u'%s' % self.content[0:100]


class ReadingList(models.Model):
    """
    Describes a collection of texts.
    """
    
    title = models.CharField(max_length=100)


class ReadingListItem(models.Model):
    """
    Describes a text entry in a reading list.
    """
    
    reading_list = models.ForeignKey(ReadingList)
    text         = models.ForeignKey(Text)
    order        = models.IntegerField(blank = True, null = True)
    
    def __unicode__(self):
        return self.issue
    
    class Meta:
        ordering = ('order',)
