from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import *


class ParagraphAdmin(admin.ModelAdmin):
    pass
admin.site.register(Paragraph, ParagraphAdmin)


class ParagraphInline(admin.StackedInline):
    model = Paragraph
    extra = 0


class TextAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('body',),
        }),
        (_('Metadata'), {
            'fields': (
                'dc_contributor', 'dc_coverage', 'dc_creator', 'dc_date', 'dc_description', 
                'dc_format', 'dc_identifier', 'dc_language', 'dc_publisher', 'dc_relation', 
                'dc_rights', 'dc_source', 'dc_subject', 'dc_title', 'dc_type'
            ),
        }),
    )
admin.site.register(Text, TextAdmin)


class DocumentTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(DocumentType, DocumentTypeAdmin)


from django.contrib import admin
from django import forms

from models import ReadingList, ReadingListItem

class ReadingListForm(forms.ModelForm):
    model = ReadingList
    class Media:
        js = (
            '/static/js/jquery-1.3.2.min.js',
            '/static/js/jquery-ui-1.7.2.custom.min.js',
            '/static/js/menu-sort.js',
        )


class ReadingListItemInline(admin.StackedInline):
    model = ReadingListItem

admin.site.register(ReadingList, inlines=[ReadingListItemInline], form=ReadingListForm)
