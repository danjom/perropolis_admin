from django.contrib import admin
from custom_users.models import *
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUser,CustomUserAdmin)