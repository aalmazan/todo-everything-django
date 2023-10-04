from django.contrib import admin

from .models import Account, AccountProfile

admin.site.register(Account)
admin.site.register(AccountProfile)
