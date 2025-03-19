from django.contrib import admin

from moss.store import models

admin.site.register(models.Tenant)
admin.site.register(models.User)
admin.site.register(models.File)
admin.site.register(models.Permission)
