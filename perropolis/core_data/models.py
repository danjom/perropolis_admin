from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from  perropolis import constants


class Country(models.Model):
    code = models.CharField(_('Code'), max_length=5)
    name = models.CharField(_('Name'), max_length=30, unique=True)
    taxes_percentage = models.DecimalField(_('Taxes Percentage'), max_digits=4, decimal_places=2)
    phone_number_code = models.CharField(_('Phone Number Code'), max_length=5)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    def __str__(self):
        return f'{self.code}-{self.name}'

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        db_table = 'countries'
        indexes = [
            models.Index(fields=['name'], name='ix_country_name'),
        ]


class Specie(models.Model):
    name = models.CharField(_('Name'), max_length=30, unique=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Specie')
        verbose_name_plural = _('Species')
        db_table = 'species'
        indexes = [
            models.Index(fields=['name'], name='ix_species_name'),
        ]


class Breed(models.Model):
    species = models.ForeignKey(Specie, on_delete=models.PROTECT)
    name = models.CharField(_('Name'), max_length=30)
    life_expectancy = models.DecimalField(_('Life Expectancy'), max_digits=3, decimal_places=1)
    # size = models.IntegerField(_('Size'), validators=[MaxValueValidator(99), MinValueValidator(0)])
    size = models.CharField(max_length=32, choices=constants.ANIMAL_SIZES)
    health_score = models.DecimalField(_('Healt Score'), max_digits=3, decimal_places=1,
                                       validators=[MaxValueValidator(10), MinValueValidator(0)])
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Breed')
        verbose_name_plural = _('Breeds')
        db_table = 'breeds'
        indexes = [
            models.Index(fields=['species_id', 'name'], name='ix_breed_name'),
        ]


class Service(models.Model):
    name = models.CharField(_('Name'), max_length=20)
    details = models.TextField(_('Details'), max_length=256)
    is_active = models.BooleanField(_('Is Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.IntegerField(_('Created By'))
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.IntegerField(_('Updated By'))

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        db_table = 'services'
        indexes = [
            models.Index(fields=['name'], name='ix_service_name'),
        ]


class MedicatSpeciality(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    description = models.TextField(_('Description'), max_length=256)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Medical Speciality')
        verbose_name_plural = _('Medical Specialities')
        db_table = 'medical_specialities'
        indexes = [
            models.Index(fields=['name'], name='ix_specialty_name'),
        ]


class Vet(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    name = models.CharField(_('Name'), max_length=50)
    license_code = models.CharField(_('License Code'), max_length=30, blank=True, null=True)
    email = models.EmailField(_('Email'))
    phone_number = models.CharField(_('Phone Number'), max_length=24)
    has_facility = models.BooleanField(_('Has Facility'), default=False)
    home_visits = models.BooleanField(_('Home Visits'), default=False)
    receive_emergencies = models.BooleanField(_('Receive Emergencies'), default=False)
    address = models.TextField(_('Address'))

    class Meta:
        verbose_name = _('Vet')
        verbose_name_plural = _('Vets')
        db_table = 'vets'
        indexes = [
            models.Index(fields=['name'], name='ix_vet_name'),
            models.Index(fields=['country_id', 'license_code'], name='ix_vet_license'),
        ]
        unique_together = ['country_id', 'license_code']


class VetSpeciality(models.Model):
    vet = models.ForeignKey(Vet, on_delete=models.PROTECT)
    speciality = models.ForeignKey(MedicatSpeciality, on_delete=models.PROTECT)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Vet Speciality')
        verbose_name_plural = _('Vet specialities')
        db_table = 'vet_specialities'
        indexes = [
            models.Index(fields=['vet_id', 'speciality_id'], name='ix_specialty_vet'),
        ]
        unique_together = ['vet_id', 'speciality_id']


class Brand(models.Model):
    name = models.CharField(_('Name'), max_length=30, unique=True)
    logo_url = models.URLField(_('Logo URL'), blank=True, null=True)
    brand_type = models.IntegerField(_('Brand Type'), max_length=32, choices=constants.BRAND_TYPES)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')
        db_table = 'brands'
        indexes = [
            models.Index(fields=['name'], name='ix_brand_name'),
        ]


class PetFood(models.Model):
    name = models.CharField(_('Name'), max_length=20)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Pet Food')
        verbose_name_plural = _('Pet fods')
        db_table = 'pet_foods'
        indexes = [
            models.Index(fields=['brand_id', 'name'], name='ix_food_name'),
        ]
        unique_together = ['brand_id', 'name']


class PetDrug(models.Model):
    name = models.CharField(_('Name'), max_length=20)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    drug_type = models.CharField(_('Drug Type'), max_length=32, choices=constants.DRUG_TYPES)
    admin_created = models.BooleanField(_('Admin Created'), default=False)
    admin_updated = models.BooleanField(_('Admin Updated'), default=False)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.IntegerField(_('Created By'))
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.IntegerField(_('Updated By'))

    class Meta:
        verbose_name = _('Pet Drug')
        verbose_name_plural = _('Pet Drugs')
        db_table = 'pet_drugs'
        indexes = [
            models.Index(fields=['brand_id', 'name'], name='ix_drug_name'),
        ]
        unique_together = ['brand_id', 'name']


class MedicalEvent(models.Model):
    name = models.CharField(_('Name'), max_length=20, unique=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Medical Event')
        verbose_name_plural = _('Medical events')
        db_table = 'medical_events'
        indexes = [
            models.Index(fields=['name'], name='ix_med_event_name'),
        ]


class MedicalAction(models.Model):
    event = models.ForeignKey(MedicalEvent, on_delete=models.PROTECT)
    name = models.CharField(_('Name'), max_length=20)
    description = models.TextField(_('Description'))
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Medical Action')
        verbose_name_plural = _('Medical Actions')
        db_table = 'medical_actions'
        indexes = [
            models.Index(fields=['event_id', 'name'], name='ix_med_action_name'),
        ]
        unique_together = ['event_id', 'name']
