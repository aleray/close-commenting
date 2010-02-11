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

