from django.contrib import admin
from organizations.admin import OrganizationAccountInline

from . import models as accounts_models


class AccountAdmin(admin.ModelAdmin):
    fields = ("email", "password", "is_active", "is_staff", "is_superuser")
    inlines = [
        OrganizationAccountInline,
    ]


class AccountProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(accounts_models.Account, AccountAdmin)
admin.site.register(accounts_models.AccountProfile, AccountProfileAdmin)
