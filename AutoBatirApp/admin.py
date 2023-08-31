from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(NationalID)
admin.site.register(UPI)
admin.site.register(Registration)
admin.site.register(Engineer)
admin.site.register(Permit)
# admin.site.register(Notifications)
admin.site.register(ArchivedPermit)
