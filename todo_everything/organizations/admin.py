from django.contrib import admin

from . import models as org_models


class OrganizationAdmin(admin.ModelAdmin):
    pass


admin.site.register(org_models.Organization, OrganizationAdmin)
