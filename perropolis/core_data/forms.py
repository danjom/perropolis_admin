from django import forms

from core_data.models import MedicalSpeciality, Service, MedicalAction


class MedicalSpecialityForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = MedicalSpeciality
        fields = '__all__'


class ServiceForm(forms.ModelForm):
    details = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Service
        fields = '__all__'


class MedicalActionForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = MedicalAction
        fields = '__all__'

