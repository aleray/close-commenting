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
from dcdocuments.models import Document

import md5, re, markdown
from BeautifulSoup import BeautifulSoup


class Text(Document):
    """
    Describes a text document.
    """
    
    body = models.TextField(verbose_name=_('Body'))
        
    def save(self):
        """
        Saves the text and split it in pieces according to its paragraphs breaks.
        Compare the new paragraphs checksums with the existing ones, if any.
        Matching checksum paragraphs are preserved, allowing consistency in comment linking.
        Non-Matching checksum paragraphs are deleted.
        """
        
        super(Text, self).save()
        
        ## TODO: check Difflib and see how it could be integrated
        
        existing_paragraphs = Paragraph.objects.filter(text=self)
        md = markdown.Markdown(extensions=['meta', 'footnotes'])
        output = md.convert(self.body)
        
        # Populates the metadata
        self.dc_contributor = md.Meta.get('contributor', [''])[0]
        self.dc_coverage    = md.Meta.get('coverage', [''])[0]
        self.dc_creator     = md.Meta.get('creator', [''])[0]
        self.dc_date        = md.Meta.get('date', [''])[0]
        self.dc_description = md.Meta.get('description', [''])[0]
        self.dc_format      = md.Meta.get('format', [''])[0]
        self.dc_identifier  = md.Meta.get('identifier', [''])[0]
        self.dc_language    = md.Meta.get('language', [''])[0]
        self.dc_publisher   = md.Meta.get('publisher', [''])[0]
        self.dc_relation    = md.Meta.get('relation', [''])[0]
        self.dc_rights      = md.Meta.get('rights', [''])[0]
        self.dc_source      = md.Meta.get('source', [''])[0]
        self.dc_subject     = md.Meta.get('subject', [''])[0]
        self.dc_title       = md.Meta.get('title', [''])[0]
        self.dc_type        = md.Meta.get('type', [''])[0]
        
        super(Text, self).save()
        
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

