from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from core_data.models import Country


class User(AbstractUser):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    name = models.CharField(_('Name'), max_length=20)
    phone_number = models.CharField(_('Phone Number'), max_length=24, null=True, blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    is_blocked = models.BooleanField(default=True)
