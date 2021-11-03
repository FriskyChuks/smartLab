from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from formtools.preview import FormPreview
from .models import Patient#, Foto


class PatientBiodataFormPreview(FormPreview):
  # login_url="auth_login"
  form_template = 'patients/registration.html'
  preview_template = 'patients/preview.html'

  def done(self, request, cleaned_data):
    Patient.objects.create(**cleaned_data)
    
    return HttpResponseRedirect('patients/success.html')