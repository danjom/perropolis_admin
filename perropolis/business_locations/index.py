from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Location, Webcam


@register(Location)
class LocationIndex(AlgoliaIndex):
    fields = ('id', 'name', 'country_id', 'rooms_count', 'daycare_capacity', 'webcams_enabled', 'address', 'city',
              'latitude', 'longitude', 'updated_at')
    index_name = 'locations'



@register(Webcam)
class WebcamIndex(AlgoliaIndex):
    fields = ('id', 'location_id', 'alias', 'livestream_available', 'updated_at')
    index_name = 'webcams'
