from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from perropolis.constants import WEEK_DAYS, ROOM_TYPES


class Location(models.Model):
    country = models.ForeignKey('core_data.Country', on_delete=models.POROTECT)
    name = models.CharField(_('Name'), max_length=30)
    email = models.EmailField(_('Email'))
    rooms_count = models.IntegerField(_('Rooms Count'), validators=[MinValueValidator(1)])
    daycare_capacity = models.IntegerField(_('Daycare Capacity'), validators=[MinValueValidator(1)])
    webcams_enabled = models.BooleanField(_('Webcams Enabled'), default=False)
    livestream_cost = models.DecimalField(_('Livestream Cost'), max_digits=10, decimal_places=2)
    phone_number = models.CharField(_('Phone Number'), max_length=24)
    city = models.CharField(_('City'), max_length=30)
    address = models.CharField(_('Address'), max_length=256)  # TODO: Text Area on ADMIN PORTAL
    latitude = models.DecimalField(_('Latitude'), max_digits=10, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(_('Longitude'), max_digits=10, decimal_places=6, blank=True, null=True)
    is_active = models.BooleanField(_('is_active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.ForeignKey('admin_user.User', on_delete=models.CASCADE, related_name='created_locations')
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey('admin_user.User', on_delete=models.CASCADE, related_name='updated_locations')

    class Meta:
        db_table = 'locations'
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
        indexes = [
            models.Index(fields=['country_id', 'name'], name='ix_location_name'),
        ]
        unique_together = ['country_id', 'name']


class OpenSchedule(models.Model):
    location = models.ForeignKey(Location, on_delete=models.PROTECT, unique=True)
    start_week_day = models.IntegerField(_('Start Week Day'), choices=WEEK_DAYS)
    end_week_day = models.IntegerField(_('End Week Day'), choices=WEEK_DAYS)
    start_hour = models.IntegerField(_('Start Hour'), validators=[MinValueValidator(0), MaxValueValidator(23)])  # Daniel Please look at this
    end_hour = models.IntegerField(_('End Hour'), validators=[MinValueValidator(0), MaxValueValidator(23)])  # Daniel Please look at this
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.ForeignKey('admin_user.User', on_delete=models.CASCADE, related_name='created_open_schedules')
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey('admin_user.User', on_delete=models.CASCADE, related_name='updated_open_schedules')

    class Meta:
        db_table = 'open_schedules'
        verbose_name = _('Open Schedule')
        verbose_name_plural = _('Open Schedules')
        indexes = [
            models.Index(fields=['location_id'], name='ix_location_schedule'),
        ]


class HotelRoom(models.Model):
    location = models.ForeignKey(Location, on_delete=models.PROTECT, unique=True)
    room_type = models.IntegerField(choices=ROOM_TYPES)
    details = models.CharField(max_length=512, blank=True, null=True, )  # TODO: 'Text Area in ADMIN PORTAL'
    max_capacity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.ForeignKey('admin_user.User', on_delete=models.CASCADE, related_name='created_hotel_rooms')
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey('admin_user.User', on_delete=models.CASCADE, related_name='updated_hotel_rooms')

    class Meta:
        indexes = [
            models.Index(fields=['location_id', 'room_type'], name='ix_location_room'),
            models.Index(fields=['room_type'], name='ix_room_hotel'),
        ]
        unique_together = ['location_id', 'room_type']
