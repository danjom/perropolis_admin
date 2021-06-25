from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Location


@register(Location)
class LocationIndex(AlgoliaIndex):
    fields = ('id', 'name', 'country_id', 'rooms_count', 'daycare_capacity', 'webcams_enabled', 'address', 'city'
              'latitude', 'longitude', 'updated_at')
    index_name = 'locations'


