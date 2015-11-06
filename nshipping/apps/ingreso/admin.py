from django.contrib import admin

from .models import Branch, Client, DepositSlip, Dues

admin.site.register(Branch)
admin.site.register(Client)
admin.site.register(DepositSlip)
admin.site.register(Dues)
