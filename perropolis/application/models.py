from django.db import models
from datetime import datetime
from custom_users.models import CustomUser
from django.contrib.auth.models import Group


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
        db_table = 'countries'

class Locations(models.Model):
    country_id = models.ForeignKey(
        Countries,
        on_delete=models.PROTECT
    )
    name = models.CharField("Name", null=False, max_length=30)
    city = models.CharField("Name", null=False, max_length=30)
    address = models.CharField("Address", null=False, max_length=128)
    latitude = models.DecimalField("Latitude", null=True, decimal_places=6, max_digits=10, max_length=15)
    longitude = models.DecimalField("Longitude", null=True, decimal_places=6, max_digits=10,  max_length=15)
    active = models.BooleanField("Activo?",null=False, default=True)
    open_schedule = models.CharField("Name", null=False, max_length=128)
    created_at = models.DateTimeField("Created At", null=False, auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.code, self.name)

    class Meta:
        verbose_name = 'Local'
        verbose_name_plural = 'Locales'
        db_table = 'locations'

class UserRolesLocations(models.Model):
    location = models.ForeignKey(
        Locations,
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT
    )
    role = models.ForeignKey(
        Group,
        on_delete=models.PROTECT
    )
    created_at = models.DateTimeField("Created At", null=False, auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.code, self.name)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['location', 'user', 'role'], name='userroleslocation_index')
        ]
        verbose_name = 'Rol por Local'
        verbose_name_plural = 'Roles por Local'
        db_table = 'userroles_locations'



