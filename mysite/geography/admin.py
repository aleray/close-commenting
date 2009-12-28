# *-* encoding: utf-8 *-*

from geography.models import *
from django.contrib import admin

class CountryAdmin(admin.ModelAdmin):
    list_display =  ('name_en', 'iso_code')
    prepopulated_fields = {"slug": ('name_en',)}
admin.site.register(Country, CountryAdmin)

class CityAdmin(admin.ModelAdmin):
    list_display =  ('name_en', 'country')
    list_filter = ('country',)
    search_fields = ['name_en', 'name_fr', 'country', 'iso_code']
    prepopulated_fields = {"slug": ('name_en', "country")}
    pass
admin.site.register(City, CityAdmin)

class LanguageAdmin(admin.ModelAdmin):
    list_display =  ('name_en', 'iso_code')
    prepopulated_fields = {"slug": ('name_en',)}
    pass
admin.site.register(Language, LanguageAdmin)

