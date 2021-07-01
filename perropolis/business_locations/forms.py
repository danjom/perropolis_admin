from django import forms

from business_locations.models import HotelRoom, Location, Zone


class HotelRoomForm(forms.ModelForm):
    details = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = HotelRoom
        fields = '__all__'


class LocationForm(forms.ModelForm):
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Location
        fields = '__all__'


class ZoneForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Zone
        fields = '__all__'
        exclude = ('location', 'service')
