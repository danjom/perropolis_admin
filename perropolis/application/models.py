from django.db import models
from datetime import datetime
from custom_users.models import CustomUser


class Countries(models.Model):
    code = models.CharField("Code", null=False, max_length=6)
    name = models.CharField("Name", null=False, max_length=20)
    flag = models.CharField("Flag", null=True, max_length=256)
    created_at = models.DateTimeField("Created At", null=False, auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.code, self.name)

    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'

class Locations(models.Model):
    country_id = models.ForeignKey(
        Countries,
        on_delete=models.PROTECT
    )
    name = models.CharField("Name", null=False, max_length=30)
    city = models.CharField("Name", null=False, max_length=30)
    address = models.CharField("Address", null=False, max_length=128)
    #latitude = models.DecimalField("Latitude", null=True, max_length=15)
    #latitude = models.DecimalField("Longitude", null=True, max_length=15)
    active = models.BooleanField("Activo?",null=False, default=True)
    open_schedule = models.CharField("Name", null=False, max_length=128)
    created_at = models.DateTimeField("Created At", null=False, auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.code, self.name)

    class Meta:
        verbose_name = 'Local'
        verbose_name_plural = 'Locales'

