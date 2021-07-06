import hashlib

from cloudinary import uploader
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from perropolis.constants import GENDERS, MEASURE_UNITS, BELONGING_TYPES, IMAGE_TYPES


class Customer(models.Model):
    country = models.ForeignKey('core_data.Country', on_delete=models.PROTECT)
    name = models.CharField(_('Name'), max_length=20)
    email = models.EmailField(_('Email'))
    email_validated = models.BooleanField(_('Email Validated'), default=False)
    phone_number = models.CharField(_('Phone Number'), max_length=24, blank=True, null=True)
    phone_validated = models.BooleanField(_('Phone Validated'), default=False)
    password = models.CharField(max_length=64)
    profile_pic_url = CloudinaryField('profile_pic', blank=True, null=True,
                                      folder=f'/platform/{settings.ENVIRONMENT}/customer_profile_pics/')
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    def __str__(self):
        return f'{self.name}'

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
    vet = models.ForeignKey('core_data.Vet', blank=True, null=True, on_delete=models.PROTECT)
    breed = models.ForeignKey('core_data.Breed', on_delete=models.PROTECT)
    name = models.CharField(_('Name'), max_length=20)
    gender = models.IntegerField(_('Gender'), choices=GENDERS)
    birth_date = models.DateField(_('Birth Date'), blank=True, null=True)
    profile_pic_url = CloudinaryField('profile_pic', blank=True, null=True,
                                      folder=f'/platform/{settings.ENVIRONMENT}/pet_profile_pics/')
    castrated = models.BooleanField(_('Castrated'))
    last_service = models.DateField(_('Last Service'), blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='created_pets')
    admin_created = models.BooleanField(_('Admin Created'))
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='updated_pets')
    admin_updated = models.BooleanField(_('Admin Updated'))

    def __str__(self):
        return f'{self.name}'

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


class UserPet(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.PROTECT)
    pet = models.ForeignKey(Pet, on_delete=models.PROTECT)
    linked = models.BooleanField(default=False)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='created_user_pets')
    admin_created = models.BooleanField(_('Admin Created'))
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='updated_user_pets')
    admin_updated = models.BooleanField(_('Admin Updated'))

    def __str__(self):
        return f'{self.user.name} - {self.pet.name}'

    class Meta:
        db_table = 'users_pets'
        verbose_name = _('User Pet')
        verbose_name_plural = _('Users Pets')
        indexes = [
            models.Index(fields=['user_id', 'pet_id'], name='ix_user_pets')
        ]
        unique_together = ['user_id', 'pet_id']


class PetFeeding(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.PROTECT)
    food = models.ForeignKey('core_data.PetFood', on_delete=models.PROTECT)
    times_per_day = models.IntegerField(_('Times Per Day'), validators=[MinValueValidator(1), MaxValueValidator(10)])
    food_portion = models.DecimalField(_('Food Portion'), max_digits=6, decimal_places=2)
    measure_unit = models.IntegerField(_('Measure Unit'), choices=MEASURE_UNITS)
    is_active = models.BooleanField(_('Is Active'), default=True)
    details = models.CharField(_('Details'), max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='created_pet_feedings')
    admin_created = models.BooleanField(_('Admin Created'))
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='updated_pet_feedings')
    admin_updated = models.BooleanField(_('Admin Updated'))

    def __str__(self):
        return f'{self.pet.name} - {self.food.name}'

    class Meta:
        db_table = 'pet_feedings'
        verbose_name = _('Pet Feeding')
        verbose_name_plural = _('Pet Feedings')

        indexes = [
            models.Index(fields=['pet_id', 'food_id'], name='ix_pet_feed')
        ]
        unique_together = ['pet_id', 'food_id']


class PetMedication(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.PROTECT)
    drug = models.ForeignKey('core_data.PetDrug', on_delete=models.PROTECT)
    dose = models.DecimalField(max_digits=6, decimal_places=2)
    measure_unit = models.IntegerField(choices=MEASURE_UNITS)
    is_active = models.BooleanField(_('Is Active'), default=True)
    start_date = models.DateField(_('Start Date'))
    end_date = models.DateField(_('End Date'))
    lifetime_required = models.BooleanField(_('Lifetime Required'), default=False)
    details = models.CharField(_('Details'), max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='created_pet_medications')
    admin_created = models.BooleanField(_('Admin Created'))
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='updated_pet_medications')
    admin_updated = models.BooleanField(_('Admin Updated'))

    def __str__(self):
        return f'{self.pet.name} - {self.drug.name}'

    class Meta:
        db_table = 'pet_medications'
        verbose_name = _('Pet Medication')
        verbose_name_plural = _('Pet Medications')

        indexes = [
            models.Index(fields=['pet_id', 'drug_id'], name='ix_pet_drug')
        ]
        unique_together = ['pet_id', 'drug_id']


class PetBelonging(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.PROTECT)
    name = models.CharField(_('Name'), max_length=20)
    description = models.CharField(_('Description'), max_length=256, blank=True, null=True)
    belongings_type = models.IntegerField(_('Belongigs Type'), choices=BELONGING_TYPES)
    favorite = models.BooleanField(_('Favorite'), default=False)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.pet.name}'

    class Meta:
        db_table = 'pet_belongings'
        verbose_name = _('Pet Belonging')
        verbose_name_plural = _('Pet Belongings')

        indexes = [
            models.Index(fields=['pet_id', 'name'], name='ix_belonging_name')
        ]


class PetMedicalRecords(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.PROTECT)
    event = models.IntegerField(_('Event ID'))
    action = models.ForeignKey('core_data.MedicalAction', on_delete=models.PROTECT)
    event_date = models.DateTimeField(_('Event Date'))
    details = models.CharField(_('Details'), max_length=512, blank=True, null=True)
    has_files = models.BooleanField(_('Has Files'), null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='created_pet_medical_records')
    admin_created = models.BooleanField(_('Admin Created'))
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey('admin_user.User', on_delete=models.PROTECT, related_name='updated_pet_medical_records')
    admin_updated = models.BooleanField(_('Admin Updated'))

    def __str__(self):
        return f'{self.pet.name} - {self.action.name}'

    class Meta:
        db_table = 'pet_medical_records'
        verbose_name = _('Pet Medical Record')
        verbose_name_plural = _('Pet Medical Records')
        indexes = [
            models.Index(fields=['pet_id', 'action_id'], name='ix_pet_med_action')
        ]


class PetImage(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.PROTECT)
    url = CloudinaryField('image', folder=f'/platform/{settings.ENVIRONMENT}/images/')
    version = models.IntegerField(_('Version'), blank=True, null=True)
    height = models.IntegerField(_('Height'))
    width = models.IntegerField(_('Width'))
    reference_type = models.IntegerField(_('Reference Type'), choices=IMAGE_TYPES)
    reference_id = models.IntegerField(_('Reference ID'))
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    def image_small(self):
        try:
            return mark_safe(self.url.image(width=60, height=60))
        except AttributeError:
            return 'No Image'

    def image(self):
        try:
            return mark_safe(self.url.image(height=100))
        except AttributeError:
            return 'No Image'

    image_small.short_description = _('Image')
    image.short_description = _('Image Preview')
    image.allow_tags = image_small.allow_tags = True

    @staticmethod
    def delete_image_from_cloudnary(public_id=None):
        if public_id is None:
            return
        uploader.destroy(public_id, invalidate=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.version = self.url.version
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        public_id = getattr(self.url, 'public_id', None)
        super().delete(using, keep_parents)
        if public_id:
            self.delete_image_from_cloudnary(public_id=public_id)

    def __str__(self):
        return f'{self.pet.name} - {self.get_reference_type_display()} - {self.version}'

    class Meta:
        db_table = 'pet_images'
        verbose_name = _('Pet Image')
        verbose_name_plural = _('Pet Images')


class PetVideo(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.PROTECT)
    url = CloudinaryField('video', resource_type='video', folder=f'/platform/{settings.ENVIRONMENT}/videos/')
    name = models.CharField(_('Name'), max_length=20)
    version = models.IntegerField(_('Version'), blank=True, null=True)
    height = models.IntegerField(_('Height'))
    width = models.IntegerField(_('Width'))
    reference_type = models.IntegerField(_('Reference Type'), choices=IMAGE_TYPES)
    reference_id = models.IntegerField(_('Reference ID'))
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    def __str__(self):
        return f'{self.pet.name} - {self.name} - {self.get_reference_type_display()} - {self.version}'

    @staticmethod
    def delete_video_from_cloudnary(public_id=None):
        if public_id is None:
            return
        uploader.destroy(public_id, invalidate=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.version = self.url.version
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        public_id = getattr(self.url, 'public_id', None)
        super().delete(using, keep_parents)
        if public_id:
            self.delete_video_from_cloudnary(public_id=public_id)

    class Meta:
        db_table = 'pet_videos'
        verbose_name = _('Pet Video')
        verbose_name_plural = _('Pet Videos')
