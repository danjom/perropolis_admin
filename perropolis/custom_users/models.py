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
    email = models.CharField("Email", unique=True, max_length=50)
    user_name = models.CharField("Username",null=True,max_length=256)
    name = models.CharField("Name",null=True,max_length=64)
    last_name = models.CharField("Lastname",null=True,max_length=64)
    phone = models.CharField("Phone",null=True,max_length=12)
    is_admin = models.BooleanField("Admin", null=False, default=False)
    is_active = models.BooleanField("Activo", null=False, default=True)
    is_superuser = models.BooleanField("SuperAdmin", null=False, default=False)
    
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'email'

    def full_name(self):
        return '{} {}'.format(self.name, self.last_name)

    def __str__(self):
        return '{}  {}'.format(self.name, self.last_name)

    #def has_perm(self, perm, obj=None):
    #    return False

    #def has_module_perms(self, app_label):
    #    return True

    @property
    def is_staff(self):
        return self.is_admin

