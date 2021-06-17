from django.contrib.admin import register

from core_data.models import *
from django.contrib import admin


@register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    list_display_links = list_display
    search_fields = ('name', 'code')
    sortable_by = ('name', 'created_at')


class BreedInline(admin.TabularInline):
    model = Breed
    extra = 1


@register(Specie)
class SpecieAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    list_display_links = list_display
    search_fields = ('name',)
    sortable_by = ('name', 'created_at', 'updated_at')
    inlines = (BreedInline,)


@register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'created_at', 'updated_at')
    list_display_links = list_display
    search_fields = ('name', 'species__name')
    sortable_by = ('name', 'species__name', 'created_at', 'updated_at')


@register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    list_display_links = list_display
    search_fields = ('name',)
    sortable_by = ('name', 'created_at', 'updated_at')


@register(MedicalSpeciality)
class MedicalSpecialityAdmin(admin.ModelAdmin):
    # TODO: Description need text widget
    list_display = ('name', 'created_at', 'updated_at')
    list_display_links = list_display
    search_fields = ('name',)
    sortable_by = ('name', 'created_at', 'updated_at')


class VetSpecialityInline(admin.TabularInline):
    model = VetSpeciality
    extra = 1


@register(Vet)
class VetAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_code', 'country')
    list_display_links = list_display
    search_fields = ('name','license_code', 'country__name')
    sortable_by = ('name', 'license_code', 'country__name', 'created_at', 'updated_at')
    inlines = (VetSpecialityInline,)


@register(Brand)
class BrandAdmin(admin.ModelAdmin):
    # TODO: caledonia API integration!
    list_display = ('name', 'created_at', 'updated_at')
    list_display_links = list_display
    search_fields = ('name',)
    sortable_by = ('name', 'created_at', 'updated_at')


@register(PetFood)
class PetFoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    list_display_links = list_display
    search_fields = ('name','brand__name')
    sortable_by = ('name', 'created_at', 'updated_at')


@register(PetDrug)
class PetDrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'drug_type', 'brand', 'created_at', 'updated_at')
    list_display_links = list_display
    search_fields = ('name','brand__name', 'drug_type')
    sortable_by = ('name', 'drug_type', 'brand__name', 'created_at', 'updated_at')


class MedicalActionInline(admin.TabularInline):
    model = MedicalAction
    extra = 1


@register(MedicalEvent)
class MedicalEventAdmin(admin.ModelAdmin):
    # TODO: Description need text widget
    list_display = ('name', 'created_at', 'updated_at')
    list_display_links = list_display
    search_fields = ('name',)
    sortable_by = ('name', 'created_at', 'updated_at')
    inlines = (MedicalActionInline,)
