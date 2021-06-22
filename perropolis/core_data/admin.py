from django.contrib.admin import register
from django.contrib.admin.widgets import AdminFileWidget
from guardian.admin import GuardedModelAdmin

from core_data.forms import MedicalSpecialityForm, ServiceForm, MedicalActionForm
from core_data.models import *
from django.contrib import admin


@register(Country)
class CountryAdmin(GuardedModelAdmin):
    list_display = ('code', 'name', 'phone_number_code', 'created_at')
    list_display_links = list_display
    search_fields = ('name', 'code')
    sortable_by = ('code', 'name', 'created_at')


class BreedInline(admin.TabularInline):
    model = Breed
    extra = 1


@register(Specie)
class SpecieAdmin(GuardedModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    list_display_links = list_display
    search_fields = ('name',)
    sortable_by = ('name', 'created_at', 'updated_at')
    inlines = (BreedInline,)


@register(Breed)
class BreedAdmin(GuardedModelAdmin):
    list_display = ('name', 'species', 'size', 'created_at', 'updated_at')
    list_display_links = list_display
    search_fields = ('name', 'species__name')
    sortable_by = ('name', 'species__name', 'size', 'created_at', 'updated_at')
    autocomplete_fields = ('species', )


@register(Service)
class ServiceAdmin(GuardedModelAdmin):
    form = ServiceForm
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    list_display_links = list_display
    search_fields = ('name',)
    sortable_by = ('name', 'created_at', 'updated_at')


@register(MedicalSpeciality)
class MedicalSpecialityAdmin(GuardedModelAdmin):
    form = MedicalSpecialityForm

    list_display = ('name', 'created_at', 'updated_at')
    list_display_links = list_display
    search_fields = ('name',)
    sortable_by = ('name', 'created_at', 'updated_at')


class VetSpecialityInline(admin.TabularInline):
    model = VetSpeciality
    extra = 1


@register(Vet)
class VetAdmin(GuardedModelAdmin):
    list_display = ('country', 'name', 'license_code', 'receive_emergencies', 'created_at', 'updated_at')
    list_display_links = list_display
    search_fields = ('name','license_code', 'country__name')
    sortable_by = ('name', 'license_code', 'country__name', 'created_at', 'updated_at')
    inlines = (VetSpecialityInline,)
    autocomplete_fields = ('country',)


@register(Brand)
class BrandAdmin(GuardedModelAdmin):
    formfield_overrides = {
        CloudinaryField: {'widget': AdminFileWidget},
    }

    list_display = ('logo_small', 'name', 'brand_type', 'created_at', 'updated_at')
    list_display_links = list_display
    search_fields = ('name','brand_type')
    sortable_by = ('name', 'brand_type', 'created_at', 'updated_at')

    readonly_fields = ('logo',)

    def save_model(self,  request, obj, form, change):
        if 'logo_url' in form.changed_data:
            brand_logo = Brand.objects.values_list('logo_url', flat=True).filter(pk=obj.pk).first()
            if brand_logo is not None:
                Brand.delete_logo_from_cloudnary(brand_logo.public_id)
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        brand_logo = Brand.objects.values_list('logo_url', flat=True).filter(pk=obj.pk).first()
        if brand_logo is not None:
            Brand.delete_logo_from_cloudnary(brand_logo.public_id)
        super().delete_model(request, obj)


@register(PetFood)
class PetFoodAdmin(GuardedModelAdmin):
    list_display = ('name', 'brand', 'created_at', 'updated_at')
    list_display_links = list_display
    search_fields = ('name','brand__name')
    sortable_by = ('name', 'brand__name', 'created_at', 'updated_at')
    autocomplete_fields = ('brand',)


@register(PetDrug)
class PetDrugAdmin(GuardedModelAdmin):
    list_display = ('name', 'brand', 'drug_type', 'created_at', 'updated_at')
    list_display_links = list_display
    search_fields = ('name','brand__name', 'drug_type')
    sortable_by = ('name', 'drug_type', 'brand__name', 'created_at', 'updated_at')
    autocomplete_fields = ('brand',)


class MedicalActionInline(admin.TabularInline):
    form = MedicalActionForm
    model = MedicalAction
    extra = 1


@register(MedicalEvent)
class MedicalEventAdmin(GuardedModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    list_display_links = list_display
    search_fields = ('name',)
    sortable_by = ('name', 'created_at', 'updated_at')
    inlines = (MedicalActionInline,)
