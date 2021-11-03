from django import forms
from django.contrib.admin import options
from django.forms import widgets
from bootstrap_datepicker_plus import DatePickerInput

from .models import Patient#, PatientImage#,NextOfKin, Address


# for DateTime input use
class MyDateTimeInput(forms.DateTimeInput):
    input_type = 'date'

# for DateTime input use
class MyTimeInput(forms.TimeInput):
    input_type = 'date'


# for Date input use
class MyDateInput(forms.DateInput):
    input_type = 'date'


class PatientBiodataForm(forms.ModelForm):
    class Meta:
        model = Patient
        # fields = ["first_name", "last_name", "other_names", "gender", "date_of_birth", "marital_status"]
        exclude = ["date_created", "last_updated","active","created_by","new"]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['l_g_a'].queryset = LGA.objects.none()


        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'other_names': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': MyDateInput(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'phone_1': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone_2': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),         
        }


class PatientImageForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["foto"]



# class AddressForm(forms.ModelForm):
#     class Meta:
#         model = Patient
#         fields = ["phone_1", "phone_2", "country", "state", "l_g_a", "address"]


# class NextOfKinForm(forms.ModelForm):
#     class Meta:
#         model = Patient
#         fields = ["next_of_kin_relationship", "full_name", "phone", "next_of_kin_address"]


    # def clean(self):
    #     cleaned_data = super(PatientBiodataForm, self).clean()
    #     first_name = cleaned_data.get('first_name')
    #     last_name = cleaned_data.get('last_name')
    #     gender = cleaned_data.get('gender')
    #     date_of_birth = cleaned_data.get('date_of_birth')
    #     # message = cleaned_data.get('message')
    #     if not first_name and not last_name:
    #         raise forms.ValidationError('Firstname and Lastname fields cannot be blank!')
    #     elif not gender:
    #         raise forms.ValidationError('Specify your gender please!')
    #     elif not date_of_birth:
    #         raise forms.ValidationError('Please enter yout Date of birth!!')



