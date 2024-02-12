from django.contrib import admin

from . import models as org_models


class OrganizationAccountInline(admin.TabularInline):
    model = org_models.OrganizationAccount
    extra = 1


class OrganizationAdmin(admin.ModelAdmin):
    inlines = [
        OrganizationAccountInline,
    ]


admin.site.register(org_models.Organization, OrganizationAdmin)
