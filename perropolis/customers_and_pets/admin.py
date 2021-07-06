from cloudinary.models import CloudinaryField
from django.contrib import admin

# Register your models here.
from django.contrib.admin import register
from django.contrib.admin.widgets import AdminFileWidget

from customers_and_pets.models import Customer, Pet, PetImage, PetVideo, PetFeeding, PetMedication, PetBelonging, \
    PetMedicalRecords, UserPet
from shared.admin import ModelAdminWithSaveOverrideForCreationAndUpdate


@register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    formfield_overrides = {
        CloudinaryField: {'widget': AdminFileWidget},
    }

    list_display = ['name', 'email', 'country', 'is_active', 'is_blocked', 'created_at', 'updated_at']
    list_display_links = list_display
    search_fields = ['name', 'email', 'country__name']
    sortable_by = ['name', 'country', 'created_at', 'updated_at']

    readonly_fields = ('profile_pic',)

    def save_model(self,  request, obj, form, change):
        if 'profile_pic_url' in form.changed_data:
            profile_pic = Customer.objects.values_list('profile_pic_url', flat=True).filter(pk=obj.pk).first()
            if profile_pic is not None:
                Customer.delete_profile_pic_from_cloudnary(profile_pic.public_id)
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        profile_pic = Customer.objects.values_list('profile_pic_url', flat=True).filter(pk=obj.pk).first()
        if profile_pic is not None:
            Customer.delete_logo_from_cloudnary(profile_pic.public_id)
        super().delete_model(request, obj)


class PetFeedingInline(admin.TabularInline):
    model = PetFeeding
    extra = 1
    readonly_fields = ('created_by', 'admin_created', 'updated_by', 'admin_updated')


class PetMedicationInline(admin.TabularInline):
    model = PetMedication
    extra = 1
    readonly_fields = ('created_by', 'admin_created', 'updated_by', 'admin_updated')


class PetBelongingInline(admin.TabularInline):
    model = PetBelonging
    extra = 1


class PetImageInline(admin.TabularInline):
    model = PetImage
    readonly_fields = ('version', 'image_small')
    extra = 1


class PetVideoInline(admin.TabularInline):
    model = PetVideo
    readonly_fields = ('version',)
    extra = 1


class PetMedicalRecordsInline(admin.TabularInline):
    model = PetMedicalRecords
    extra = 1
    readonly_fields = ('created_by', 'admin_created', 'updated_by', 'admin_updated')


class UserPetInline(admin.TabularInline):
    model = UserPet
    extra = 1
    readonly_fields = ('created_by', 'admin_created', 'updated_by', 'admin_updated')


@register(Pet)
class PetAdmin(ModelAdminWithSaveOverrideForCreationAndUpdate):
    list_display = ['name', 'breed', 'birth_date', 'created_at', 'updated_at']
    list_display_links = list_display
    search_fields = ['name', 'breed_name', 'birth_date']
    sortable_by = ['name', 'breed', 'birth_date', 'created_at']

    readonly_fields = ('created_by', 'admin_created', 'updated_by', 'admin_updated', 'last_service', 'profile_pic')

    inlines = [PetFeedingInline, PetMedicationInline, PetBelongingInline, PetMedicalRecordsInline, PetImageInline,
               UserPetInline]

    def save_model(self,  request, obj, form, change):
        """
        Override Pet's save method.
        Delete image from cloudinary when it is removed from the system!
        """
        if 'profile_pic_url' in form.changed_data:
            profile_pic = Customer.objects.values_list('profile_pic_url', flat=True).filter(pk=obj.pk).first()
            if profile_pic is not None:
                Customer.delete_profile_pic_from_cloudnary(profile_pic.public_id)

        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """
        Override Pet's delete method.
        Delete image from cloudinary when Pet is removed from the system!
        """
        profile_pic = Pet.objects.values_list('profile_pic_url', flat=True).filter(pk=obj.pk).first()
        if profile_pic is not None:
            Pet.delete_profile_pic_from_cloudnary(profile_pic.public_id)
        super().delete_model(request, obj)

    def save_formset(self, request, form, formset, change):
        """
        Given an inline formset save it to the database.
        """
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if instance.pk is None:
                instance.created_by = request.user
                instance.admin_created = request.user.is_superuser
            instance.updated_by = request.user
            instance.admin_updated = request.user.is_superuser
            instance.save()
        formset.save_m2m()


@register(PetImage)
class PetImageAdmin(admin.ModelAdmin):
    list_display = ['image_small', 'pet', 'created_at']
    list_display_links = list_display
    search_fields = ['pet__name']
    sortable_by = ['pet', 'created_at']

    readonly_fields = ('version', 'image')


@register(PetVideo)
class PetVideoAdmin(admin.ModelAdmin):
    list_display = ['name', 'pet', 'created_at']
    list_display_links = list_display
    search_fields = ['name', 'pet__name']
    sortable_by = ['name', 'pet', 'created_at']

    readonly_fields = ('version',)

    def delete_model(self, request, obj):
        video = Customer.objects.values_list('url', flat=True).filter(pk=obj.pk).first()
        if video is not None:
            Customer.delete_video_from_cloudnary(video.public_id)
        super().delete_model(request, obj)
