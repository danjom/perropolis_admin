from django import forms

from customers_and_pets.models import PetFeeding, PetMedication, PetMedicalRecords, PetBelonging


class PetFeedingForm(forms.ModelForm):
    details = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = PetFeeding
        fields = '__all__'


class PetMedicationForm(forms.ModelForm):
    details = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = PetMedication
        fields = '__all__'


class PetMedicalRecordsForm(forms.ModelForm):
    details = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = PetMedicalRecords
        fields = '__all__'


class PetBelongingForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = PetBelonging
        fields = '__all__'
