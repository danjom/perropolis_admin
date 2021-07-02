import hashlib

from cloudinary import uploader
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from perropolis.constants import GENDERS


class Customer(models.Model):
    country = models.ForeignKey
    name = models.CharField(_('Name'), max_length=20)
    email = models.EmailField(_('Email'))
    email_validated = models.BooleanField(_('Email Validated'), default=False)
    phone_number = models.CharField(_('Phone Number'), max_length=24, blank=True, null=True)
    phone_validated = models.BooleanField(_('Phone Validated'), default=False)
    password = models.CharField(max_length=64)
    profile_pic_url = CloudinaryField('profile_pic', blank=True, null=True,
                                      folder=f'/platform/{settings.ENVIRONMENT}/customer_profile_pics/')
    is_active = models.BooleanField(default=True)
    is_blacked = models.BooleanField(default=False)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    def profile_pic_small(self):
        try:
            return mark_safe(self.profile_pic_url.image(width=60, height=60))
        except AttributeError:
            return 'No Profile Pic'

    def profile_pic(self):
        try:
            return mark_safe(self.profile_pic_url.image(height=100))
        except AttributeError:
            return 'No Profile Pic'

    profile_pic_small.short_description = _('Profile Picture')
    profile_pic.short_description = _('Profile Picture Preview')
    profile_pic.allow_tags = profile_pic_small.allow_tags = True

    @staticmethod
    def delete_profile_pic_from_cloudnary(public_id=None):
        if public_id is None:
            return
        uploader.destroy(public_id, invalidate=True)

    class Meta:
        db_table = 'customers'
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

        indexes = [
            models.Index(fields=['email'], name='ix_user_email')
        ]

    def save(self, *args, **kwargs):
        if self.pk is None:
            sha256_hash = hashlib.sha256(self.password.encode('utf-8'))
            self.password = sha256_hash.hexdigest()
        super().save(*args, **kwargs)


class Pet(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.PROTECT)
    vet_id = models.ForeignKey('core_data.Vet', on_delete=models.PROTECT)
    breed_id = models.ForeignKey('core_data.Breed', on_delete=models.PROTECT)
    name = models.CharField(max_length=20)
    gender = models.IntegerField(choices=GENDERS)
    birth_date = models.DateTimeField(blank=True, null=True)
    profile_pic_url = CloudinaryField('profile_pic', blank=True, null=True,
                                      folder=f'/platform/{settings.ENVIRONMENT}/pet_profile_pics/')
    castrated = models.BooleanField()
    last_service = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='created_pets')
    admin_created = models.BooleanField()
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='updated_pets')
    admin_updated = models.BooleanField()

    def __str__(self):
        return f'{self.name} - {self.owner.name}'

    def profile_pic_small(self):
        try:
            return mark_safe(self.profile_pic_url.image(width=60, height=60))
        except AttributeError:
            return 'No Profile Pic'

    def profile_pic(self):
        try:
            return mark_safe(self.profile_pic_url.image(height=100))
        except AttributeError:
            return 'No Profile Pic'

    profile_pic_small.short_description = _('Profile Picture')
    profile_pic.short_description = _('Profile Picture Preview')
    profile_pic.allow_tags = profile_pic_small.allow_tags = True

    @staticmethod
    def delete_profile_pic_from_cloudnary(public_id=None):
        if public_id is None:
            return
        uploader.destroy(public_id, invalidate=True)

    class Meta:
        db_table = 'pets'
        verbose_name = _('Pet')
        verbose_name_plural = _('Pets')

        indexes = [
            models.Index(fields=['name'], name='ix_pet_name')
        ]
