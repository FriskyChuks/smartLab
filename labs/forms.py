from django import forms
from django.contrib.admin import options
from django.forms import widgets
from bootstrap_datepicker_plus import DatePickerInput
from django.forms import modelformset_factory
from django.forms import ModelForm

from .models import LabResult, LabUnit


class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = ["lab_request", "result"]
        # exclude = []

        widgets = {
            'result': forms.TextInput(attrs={'class': 'form-control'}),           
        }

class ResultForm(ModelForm):
    class Meta:
      model = LabResult
      fields = ['lab_request', 'result']

LabResultFormSet = modelformset_factory(
    LabResult, fields=("lab_request", "result"), extra=1
)
