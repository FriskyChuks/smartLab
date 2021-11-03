from django import forms

from .models import RadiologyService, RadiologyRequest


class RadiologyServiceForm(forms.ModelForm):
    class Meta:
        model = RadiologyService
        fields = ["radiology_service", "type","price"]

        widgets = {
                'radiology_service': forms.TextInput(attrs={'class': 'form-control'}),
                'type': forms.Select(attrs={'class': 'form-control'}),
                'price': forms.NumberInput(attrs={'class': 'form-control'}),
            }


class RaiseRadiologyServiceForm(forms.ModelForm):
    class Meta:
        model = RadiologyRequest
        fields = ["radiology_service", "unit", "clinical_info"]

        widgets = {
                'radiology_service': forms.Select(attrs={'class': 'form-control'}),
                'unit': forms.NumberInput(attrs={'class': 'form-control'}),
                'clinical_info': forms.TextInput(attrs={'class': 'form-control'}),
            }