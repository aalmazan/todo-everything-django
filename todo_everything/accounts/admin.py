from django.contrib import admin

from . import models as accounts_models


class AccountAdmin(admin.ModelAdmin):
    pass


class AccountProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(accounts_models.Account, AccountAdmin)
admin.site.register(accounts_models.AccountProfile, AccountProfileAdmin)
