from datetime import datetime, timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
#from constants import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Email is required")
        else:
            user = self.model(
                email=self.normalize_email(email)
            )
            user.set_password(password)
            user.save()

            return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    country = models.ForeignKey(
        'core_data.Country',
        on_delete=models.PROTECT,
        null=True
    )
    name = models.CharField("Name",null=True,max_length=64)
    email = models.CharField("Email", unique=True, max_length=50)
    email_verified = models.BooleanField("Email Validated?",null=True,default=False)
    phone_number = models.CharField("Phone",null=True,max_length=16, default='-')
    phone_number_verified = models.BooleanField("Phone Verified?",null=True,default=False)
    profile_pic_url= models.CharField("Profile Pic", null=True, default='', max_length=256 )
    is_admin = models.BooleanField("Admin?", null=False, default=False)
    is_active = models.BooleanField("Active?", null=False, default=True)
    is_blocked = models.BooleanField("Blocked?", null=False, default=False)
    is_superuser = models.BooleanField("Super Admin?", default=False)
    created_at = models.DateTimeField("Created Date", auto_now_add=True)
    updatate_at = models.DateTimeField("Updated Date", auto_now=True)

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'users'

    USERNAME_FIELD = 'email'

    def full_name(self):
        return '{} {}'.format(self.name, self.last_name)

    def __str__(self):
        return '{}  {}'.format(self.name, self.last_name)

    @property
    def is_staff(self):
        return self.is_admin

