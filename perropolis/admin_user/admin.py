from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group

from admin_user.models import User


admin.site.register(User, UserAdmin)
