# index.py

from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Country, Specie, Breed, MedicalSpeciality, Vet, Brand, PetFood, PetDrug, MedicalEvent, MedicalAction


@register(Country)
class CountryIndex(AlgoliaIndex):
    fields = ('id', 'name', 'code', 'phone_number_code', 'created_at')
    index_name = 'countries'


@register(Specie)
class SpecieIndex(AlgoliaIndex):
    fields = ('id', 'name', 'updated_at')
    index_name = 'species'


@register(Breed)
class BreedIndex(AlgoliaIndex):
    fields = ('id', 'name' 'species_id', 'updated_at')
    index_name = 'breeds'


@register(MedicalSpeciality)
class MedicalSpecialityIndex(AlgoliaIndex):
    fields = ('id', 'name', 'description', 'updated_at')
    index_name = 'medicalspecialities'


@register(Vet)
class VetIndex(AlgoliaIndex):
    fields = ('id', 'name', 'country_id', 'license_code', 'updated_at')
    index_name = 'vets'


@register(Brand)
class BrandIndex(AlgoliaIndex):
    fields = ('id', 'name', 'logo_url', 'brand_type', 'updated_at')
    index_name = 'brands'


@register(PetFood)
class PetFoodIndex(AlgoliaIndex):
    fields = ('id', 'name', 'brand_id', 'updated_at')
    index_name = 'petfoods'


@register(PetDrug)
class PetDrugIndex(AlgoliaIndex):
    fields = ('id', 'name', 'brand_id', 'updated_at')
    index_name = 'petdrugs'


@register(MedicalEvent)
class MedicalEventIndex(AlgoliaIndex):
    fields = ('id', 'name', 'updated_at')
    index_name = 'medicalevents'


@register(MedicalAction)
class MedicalActionIndex(AlgoliaIndex):
    fields = ('id', 'name', 'description', 'event_id', 'updated_at')
    index_name = 'medicalactions'
