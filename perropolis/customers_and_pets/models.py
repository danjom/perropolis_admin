import hashlib

from cloudinary import uploader
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class Customer(models.Model):
    country = models.ForeignKey
    name = models.CharField(_('Name'), max_length=20)
    email = models.EmailField(_('Email'))
    email_validated = models.BooleanField(_('Email Validated'), default=False)
    phone_number = models.CharField(_('Phone Number'), max_length=24, blank=True, null=True)
    phone_validated = models.BooleanField(_('Phone Validated'), default=False)
    password = models.CharField(max_length=64)
    profile_pic_url =  CloudinaryField('logo', blank=True, null=True,
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
