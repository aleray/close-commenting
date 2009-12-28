# *-* encoding: utf-8 *-*

from models import *
from django.contrib import admin

class CVEntryInline(admin.TabularInline):
    model = CVEntry
    extra = 1

class OccupationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name_en",)}
admin.site.register(Occupation, OccupationAdmin)

class HumanBeingAdmin(admin.ModelAdmin):
    inlines = [CVEntryInline,]
    prepopulated_fields = {"slug": ('firstname', "middlename", 'lastname', 'nickname')}
    list_filter = ('is_team', 'occupations', 'city')
    list_display =  ('__unicode__', 'link', 'city', "all_occupations", 'is_team')
    filter_horizontal = ['occupations']
    fieldsets = (
        (None, {
            'fields': (('firstname', 'middlename', 'lastname'), 'nickname', 'slug', 'is_team', 'occupations', 'mood')
        }),
        ('Coordinates', {
            'classes': ('collapse',),
            'fields': (('address', 'zip_code', 'city'), ('phone_prefix', 'phone'), ('email', 'link'))
        }),
        ('Description', {
            'classes': ('collapse',),
            'fields': ('description_en', 'description_fr')
        }),
    )
admin.site.register(HumanBeing, HumanBeingAdmin)

class CorporationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('prefix', "name",)}
    list_filter = ('occupations', 'city')
    list_display =  ('name', 'link', 'city', "all_occupations")
    fieldsets = (
        (None, {
            'fields': (('name', 'prefix'), 'slug', 'occupations', 'mood')
        }),
        ('Coordinates', {
            'classes': ('collapse',),
            'fields': (('address', 'zip_code', 'city'), ('phone_prefix', 'phone'), ('email', 'link'))
        }),
        ('Description', {
            'classes': ('collapse',),
            'fields': ('description_en', 'description_fr')
        }),
    )    
admin.site.register(Corporation, CorporationAdmin)

