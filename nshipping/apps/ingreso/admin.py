from django.contrib import admin

from .models import Branch, Client, DepositSlip, DetailDeposit, Dues

admin.site.register(Branch)
admin.site.register(Client)
admin.site.register(DepositSlip)
admin.site.register(DetailDeposit)
admin.site.register(Dues)

