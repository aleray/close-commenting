# *-* encoding: utf-8 *-*

from models import *
from django.contrib import admin

class RightAdmin(admin.ModelAdmin):
    pass
admin.site.register(Right, RightAdmin)

class LicenseAdmin(admin.ModelAdmin):
    pass
admin.site.register(License, LicenseAdmin)