from django.contrib import admin

from smartmodels.admin.mixins import ResourceAdminMixin

from demo.accounts.models import Account


class AccountAdmin(ResourceAdminMixin, admin.ModelAdmin):
    pass


admin.site.register(Account, AccountAdmin)
