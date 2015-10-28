from django.contrib import admin

from .models import Car, Driver, Manifest
# Register your models here.


admin.site.register(Car)
admin.site.register(Driver)
admin.site.register(Manifest)
