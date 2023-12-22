from django.contrib import admin

from . import models as org_models


class OrganizationAccountsInline(admin.TabularInline):
    model = org_models.OrganizationAccounts
    extra = 1


class OrganizationAdmin(admin.ModelAdmin):
    inlines = [
        OrganizationAccountsInline,
    ]


admin.site.register(org_models.Organization, OrganizationAdmin)
