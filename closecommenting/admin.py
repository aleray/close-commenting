from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import *
from django import forms
from markedit.admin import MarkEditAdmin

class ParagraphAdmin(admin.ModelAdmin):
    pass
admin.site.register(Paragraph, ParagraphAdmin)


class ParagraphInline(admin.StackedInline):
    model = Paragraph
    extra = 0

class TextForm(forms.ModelForm):
    model = Text
    class Media:
        css = {
            'all': ('/static/css/markedit/jquery-ui-1.7.2.custom.css',),
        }

class TextAdmin(MarkEditAdmin):
    fieldsets = (
        (None, {
            'fields': ('body',),
        }),
    )
    class MarkEdit:
        fields = ['body',]
        options = {
            'toolbar': {
                'backgroundMode': 'light',
            }
        }
admin.site.register(Text, TextAdmin, form=TextForm)


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
