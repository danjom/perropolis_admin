from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Pet


@register(Pet)
class PetIndex(AlgoliaIndex):
    fields = ['id', 'vet_id', 'name', 'updated_at']
    index_name = 'pets'
