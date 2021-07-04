from cloudinary.models import CloudinaryField
from django.contrib import admin

# Register your models here.
from django.contrib.admin import register
from django.contrib.admin.widgets import AdminFileWidget

from customers_and_pets.models import Customer, Pet, PetImage, PetVideo
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


@register(Pet)
class PetAdmin(ModelAdminWithSaveOverrideForCreationAndUpdate):
    list_display = ['name', 'owner', 'breed', 'birth_date', 'created_at', 'updated_at']
    list_display_links = list_display
    search_fields = ['name', 'owner__name', 'breed_name', 'birth_date']
    sortable_by = ['name', 'owner', 'breed', 'birth_date', 'created_at']

    readonly_fields = ('profile_pic',)

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


class FeedingAdmin(ModelAdminWithSaveOverrideForCreationAndUpdate):
    # TODO: Implement this
    pass


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
