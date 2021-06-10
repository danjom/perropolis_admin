from perropolis.perropolis.constants import ANIMAL_SIZES
from django.contrib.auth.models import Group
from django.db import models
from datetime import datetime
from custom_users.models import CustomUser
from perropolis.constants import *


class Countries(models.Model):
    code = models.CharField("Code", null=False, max_length=6)
    name = models.CharField("Name", null=False, max_length=20)
    flag = models.CharField("Flag", null=True, max_length=256)
    created_at = models.DateTimeField("Created At", null=False, auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.code, self.name)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        db_table = 'countries'

class Locations(models.Model):
    country = models.ForeignKey(
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
        return "{} - {}, {}".format(self.name, self.address, self.city)

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        db_table = 'locations'

class UserRoles_Locations(models.Model):
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
        return "Location_id: {}- User_id: {}- Role_id: {}".format(self.location, self.user, self.role)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['location', 'user', 'role'], name='userrole_locations_index')
        ]
        verbose_name = 'Role by Location'
        verbose_name_plural = 'Roles by Locations'
        db_table = 'userrole_locations'


class SMS_Messages(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT
    )
    message_type = models.IntegerField("Type", null=False, choices=MESSAGE_TYPES)
    content = models.CharField("Content", null=True, max_length=100)
    phone_number = models.CharField("Phone Number", null=False, max_length=16)
    applied = models.BooleanField("Applied by user?", null=False, default=False)
    created_at = models.DateTimeField("Created At", null=False, auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", null=False, auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.phone_number, self.name)

    class Meta:
        verbose_name = 'SMS Message'
        verbose_name_plural = 'SMS Messages'
        db_table = 'sms_messages'

class Email_Messages(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT
    )
    message_type = models.IntegerField("Type", null=False, choices=MESSAGE_TYPES)
    subject = models.CharField("Subject", null=False, max_length=30)
    content = models.CharField("Content", null=True, max_length=100)
    email = models.CharField("Email", null=False, max_length=120)
    applied = models.BooleanField("Applied by user?", null=False, default=False)
    created_at = models.DateTimeField("Created At", null=False, auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", null=False, auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.email, self.subject)

    class Meta:
        verbose_name = 'Email Message'
        verbose_name_plural = 'Email Messages'
        db_table = 'email_messages'

class Medical_Specialties(models.Model):
    name = models.CharField("Name", null=False, max_length=30)
    description = models.CharField("Description", null=True, max_length=100)
    created_at = models.DateTimeField("Created At", null=False, auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", null=False, auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.email, self.subject)

    class Meta:
        verbose_name = 'Medical Specialty'
        verbose_name_plural = 'Medical Specialties'
        db_table = 'medical_specialties'

class Vets(models.Model):
    name = models.CharField("Name", null=False, max_length=50)
    phone_number = models.CharField("Phone Number", null=False, max_length=16)
    email = models.CharField("Email", null=True, max_length=120)
    attend_emergencies = models.BooleanField("Attends Emergencies?", null=False, default=False)
    address = models.CharField("Address", null=True, max_length=300)
    created_at = models.DateTimeField("Created At", null=False, auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", null=False, auto_now_add=True)

    def __str__(self):
        return "{}, Phone: {}, Email {}".format(self.name, self.phone_number, self.email)

    class Meta:
        verbose_name = 'Vet'
        verbose_name_plural = 'Vets'
        db_table = 'vets'

class Vet_Specialties(models.Model):
    vet = models.ForeignKey(
        Vets,
        on_delete=models.PROTECT
    )
    specialty = models.ForeignKey(
        Medical_Specialties,
        on_delete=models.PROTECT
    )
    created_at = models.DateTimeField("Created At", null=False, auto_now_add=True)

    def __str__(self):
        return "Location_id: {}- User_id: {}- Role_id: {}".format(self.location, self.user, self.role)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vet', 'specialty'], name='vet_specialties_index')
        ]
        verbose_name = 'Vet Specialty'
        verbose_name_plural = 'Vet Specialties'
        db_table = 'vet_specialties'

class Brands(models.Model):
    name = models.CharField("Name", null=False, max_length=50)
    logo_url = models.CharField("Logo", null=False, max_length=256)
    brand_type = models.IntegerField("Type", null=False, choices=BRAND_TYPES)
    quality_level = models.IntegerField("Quality Level", null=False, min=1, max=5)
    created_at = models.DateTimeField("Created At", null=False, auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", null=False, auto_now_add=True)

    def __str__(self):
        return "Name: {}, Logo Url: {}".format(self.name, self.logo_url)

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        db_table = 'brands'

class Breeds(models.Model):
    name = models.CharField("Name", null=False, max_length=50)
    life_expectancy = models.DecimalField("Life Expectancy", null=False, min=1, max=20, decimal_places=1, max_digits=3, max_length=4),
    animal_size = models.IntegerField("Adult Size", null=False, choices=ANIMAL_SIZES),
    health_score =  models.DecimalField("Health Score", null=False, min=1, max=10, decimal_places=1, max_digits=3, max_length=4),

    def __str__(self):
        return "Name: {}, Life Expectancy: {}, Health Score".format(self.name, self.life_expectancy, self.health_score)

    class Meta:
        verbose_name = 'Breed'
        verbose_name_plural = 'Breeds'
        db_table = 'breeds'



