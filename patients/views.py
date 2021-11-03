import datetime
from django.db.models import Q
from django.db.models.aggregates import Count
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

from accounts.models import User
from accounts.decorators import allowed_users

from .models import Patient
from .forms import PatientBiodataForm, PatientImageForm


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','records','radiology','MLS','cashier'])
def search_patient_view(request):
	try:
		query = request.GET.get('q')
	except:
		query = None
	if query:
		# lookups = Q(title__icontains=query) | Q(description__icontains=query)
		# product = Product.objects.filter(lookups).distinct()
		patient = Patient.objects.search(query)
		context = {'query': query, 'patient': patient}
		template = 'patients/search_result.html'
	else:
		a = "Please enter a search parameter!"
		template = 'patients/search_result.html'
		context = {'query1': a}
	return render(request, template, context)



@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['records','admin','radiology','MLS','cashier'])
def patient_detail_view(request, id):
    patient = Patient.objects.filter(id=id, active=True)

    template = "patients/patient_info.html"
    context = {"patient":patient}
    return render(request, template, context)


@login_required
@allowed_users(alllowed_roles=['admin','records'])
def patient_registration_form(request):
    form = PatientBiodataForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = request.user
        obj.save()
        last_id = Patient.objects.last()
        pid = last_id.id
        messages.success(request, "Your registration was successful, your PID is: "+str(pid))
        return render(request, 'patients/success.html', {"pid":pid})                    

    template = "patients/registration.html"
    context = {"form": form}
    return render(request, template, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['records'])
def upload_patient_image_view(request, pid):
    patient_instance = Patient.objects.get(id=pid)
    pid = patient_instance.id
    form1 = PatientImageForm(instance=patient_instance) 
    if request.method == "POST":
        form1 = PatientImageForm(request.POST or None, request.FILES or None, instance=patient_instance)
        if form1.is_valid():
            form1.save()
            print("Uploaded Successfully")
            return redirect("patient_detail", id=pid)
        else:
            return redirect("patient_detail", id=pid)

    template = "patients/patient_foto.html"
    context = {"form": form1, "patient_instance":patient_instance}
    return render(request, template, context)
