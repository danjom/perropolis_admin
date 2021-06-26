from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from perropolis.constants import WEEK_DAYS, ROOM_TYPES, PET_SIZES, SERVING_TYPES


class Location(models.Model):
    country = models.ForeignKey('core_data.Country', on_delete=models.PROTECT)
    name = models.CharField(_('Name'), max_length=30)
    email = models.EmailField(_('Email'))
    rooms_count = models.IntegerField(_('Rooms Count'), validators=[MinValueValidator(1)])
    daycare_capacity = models.IntegerField(_('Daycare Capacity'), validators=[MinValueValidator(1)])
    webcams_enabled = models.BooleanField(_('Webcams Enabled'), default=False)
    livestream_cost = models.DecimalField(_('Livestream Cost'), max_digits=10, decimal_places=2)
    phone_number = models.CharField(_('Phone Number'), max_length=24)
    city = models.CharField(_('City'), max_length=30)
    address = models.CharField(_('Address'), max_length=256)
    latitude = models.DecimalField(_('Latitude'), max_digits=10, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(_('Longitude'), max_digits=10, decimal_places=6, blank=True, null=True)
    is_active = models.BooleanField(_('is_active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='created_locations')
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='updated_locations')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'locations'
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
        indexes = [
            models.Index(fields=['country_id', 'name'], name='ix_location_name'),
        ]
        unique_together = ['country_id', 'name']


class OpenSchedule(models.Model):
    location = models.OneToOneField(Location, on_delete=models.PROTECT)
    start_week_day = models.IntegerField(_('Start Week Day'), choices=WEEK_DAYS)
    end_week_day = models.IntegerField(_('End Week Day'), choices=WEEK_DAYS)
    start_hour = models.IntegerField(_('Start Hour'), validators=[MinValueValidator(0), MaxValueValidator(23)])  # Daniel Please look at this
    end_hour = models.IntegerField(_('End Hour'), validators=[MinValueValidator(0), MaxValueValidator(23)])  # Daniel Please look at this
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='created_open_schedules')
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='updated_open_schedules')

    class Meta:
        db_table = 'open_schedules'
        verbose_name = _('Open Schedule')
        verbose_name_plural = _('Open Schedules')
        indexes = [
            models.Index(fields=['location_id'], name='ix_location_schedule'),
        ]


class HotelRoom(models.Model):
    location = models.OneToOneField(Location, on_delete=models.PROTECT)
    room_type = models.IntegerField(_('Room Type'), choices=ROOM_TYPES)
    details = models.CharField(_('Details'), max_length=512, blank=True, null=True)
    max_capacity = models.IntegerField(_('Max Capacity'), validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_active = models.BooleanField(_('Is Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='created_hotel_rooms')
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='updated_hotel_rooms')

    class Meta:
        indexes = [
            models.Index(fields=['location_id', 'room_type'], name='ix_location_room'),
            models.Index(fields=['room_type'], name='ix_room_hotel'),
        ]
        unique_together = ['location_id', 'room_type']


class Employee(models.Model):
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    user = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='employees')
    is_active = models.BooleanField(_('Is Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='created_employees')
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='updated_employees')

    @property
    def full_name(self):
        return self.user.get_full_name()

    def __str__(self):
        return f'{self.full_name}'

    class Meta:
        db_table = 'employees'
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

        indexes = [
            models.Index(fields=['location_id', 'user_id'], name='ix_location_roles')
        ]
        unique_together = ['location_id', 'user_id']


class LocationService(models.Model):
    service = models.ForeignKey('core_data.Service', on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    is_active = models.BooleanField(_('Is Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='created_location_services')
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='updated_location_services')

    def __str__(self):
        return f'{self.service.name} - {self.location.name}'

    class Meta:
        db_table = 'location_services'
        verbose_name = _('Location Service')
        verbose_name_plural = _('Location Services')

        indexes = [
            models.Index(fields=['service_id', 'location_id'], name='ix_service_location')
        ]
        unique_together = ['service_id', 'location_id']


class ServiceCapacity(models.Model):
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    service_type = models.IntegerField(_('Service Type'), choices=SERVING_TYPES)
    max_capacity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='created_service_capacities')
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='updated_service_capacities')

    class Meta:
        db_table = 'service_capacities'
        verbose_name = _('Service Capacity')
        verbose_name_plural = _('Service Capacities')

        indexes = [
            models.Index(fields=['location_id', 'service_type'], name='ix_service_capacity'),
            models.Index(fields=['service_type'], name='ix_service_type')
        ]
        unique_together = ['location_id', 'service_type']


class Pricing(models.Model):
    location_service = models.ForeignKey(LocationService, on_delete=models.PROTECT)
    service = models.ForeignKey('core_data.Service', on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    specie = models.ForeignKey('core_data.Specie', on_delete=models.PROTECT)
    pet_size = models.IntegerField(_('Pet Size'), choices=PET_SIZES)
    price = models.DecimalField(_('Price'), max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='created_pricings')
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='updated_pricings')

    def __str__(self):
        return f'{self.location.name} - {self.service.name} - {self.specie.name} - {self.price}'

    class Meta:
        db_table = 'pricing'
        verbose_name = _('Pricing')
        verbose_name_plural = _('Pricings')

        indexes = [
            models.Index(fields=['service_id', 'location_id'], name='ix_pricing_service_location')
        ]
        unique_together = ['service_id', 'location_id']


class Zone(models.Model):
    location_service = models.ForeignKey(LocationService, on_delete=models.PROTECT)
    service = models.ForeignKey('core_data.Service', on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    name = models.CharField(_('Name'), max_length=30)
    description = models.CharField(_('Description'), max_length=256, blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='created_zones')
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='updated_zones')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'zones'
        verbose_name = _('Zone')
        verbose_name_plural = _('Zones')

        indexes = [
            models.Index(fields=['location_id', 'name'], name='ix_zone_name')
        ]
        unique_together = ['location_id', 'name']


class Webcam(models.Model):
    location = models.ForeignKey(Location, on_delete=models.PROTECT, null=True, blank=True)
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT, null=True, blank=True)
    external_id = models.CharField(_('External ID'), max_length=64)
    code = models.CharField(_('Code'), max_length=20)
    alias = models.CharField(_('Alias'), max_length=30, unique=True)
    web_url = models.CharField(_('Web URL'), max_length=128, blank=True, null=True)
    app_url = models.CharField(_('APP URL'), max_length=128, blank=True, null=True)
    livestream_available = models.BooleanField(_('Livestream Available'), default=False)
    is_active = models.BooleanField(_('Is Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='created_webcams')
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='updated_webcams')

    def __str__(self):
        return f'{self.alias}'

    class Meta:
        db_table = 'webcams'
        verbose_name = _('Webcam')
        verbose_name_plural = _('Webcams')

        indexes = [
            models.Index(fields=['alias'], name='ix_webcam_alias')
        ]
