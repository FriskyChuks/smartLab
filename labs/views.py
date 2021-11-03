import datetime
from django.views.generic import ListView, TemplateView
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Count
from django.contrib import messages
import string

from patients.models import Patient

from accounts.decorators import allowed_users

from .models import LabRequest, LabTest, LabUnit, LabResult
from .forms import LabResultForm, LabResultFormSet


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','doctor','MLS','lab_front_desk','records'])
def lab_request_view(request, pid):
    patient = Patient.objects.get(id=pid, active=True)
    microbiology_tests = LabTest.objects.filter(lab_unit=3).order_by('-compound_test_id')
    chem_path_tests = LabTest.objects.filter(lab_unit=2).order_by('-compound_test_id')
    hermatology_tests = LabTest.objects.filter(lab_unit=1).order_by('-compound_test_id')
    
    if request.method == "POST":
        if request.POST.get("test_id"):
            selected_test = LabRequest()
            selected_test.test_id = request.POST.get("test_id")
            test_request = selected_test.test_id

            test_request = str(test_request)
            # convert Comma separated string to a python list
            request_list = test_request.split(",")

            for item in request_list:
                obj = LabRequest.objects.create(
                    patient_id      = pid,
                    test_id         = item,
                    created_by      = request.user
                )
                obj.save()
        messages.success(request, "Lab investigation request successful!.")
        return redirect('/labs/request_list_view')
        
    template = "labs/lab_request2.html"
    context = {
                "patient":patient,
                "microbiology_tests":microbiology_tests,
                "chem_path_tests":chem_path_tests,
                "hermatology_tests":hermatology_tests
            }
    return render(request, template, context)


# View for all Pending Request || CENTRAL LAB
@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','MLS','records'])
def request_list_view(request):
    patient_request = LabRequest.objects.filter(done=False, accepted=True).values\
                ('patient').annotate(total=Count('id'))
    # patient_request = LabRequest.objects.filter(done=False, date_created__gte=datetime.date.today()).distinct('patient')
    
    template = 'labs/display_request.html'
    context = {"patient_request":patient_request}
    return render(request, template, context)


# Details of all Pending Request
@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','MLS'])
def request_detail_view(request, pid):
    request_detail = LabRequest.objects.filter(patient_id=pid,accepted=True,decline=False, done=False).order_by('-date_created')   

    template = 'labs/request_detail.html'
    context = {"request_detail":request_detail}
    return render(request, template, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['MLS'])
def send_lab_results_view(request, pid):
    lab_request = LabRequest.objects.filter(patient_id=pid,accepted=True, done=False, decline=False)
    result = request.POST
    result_trimmed = dict(result.lists())
    # del result_trimmed['csrfmiddlewaretoken']
    result_trimmed.pop('csrfmiddlewaretoken', None)

    for i, j in result_trimmed.items():
        # remove unwanted characters
        bad_chars = ['[', ']', "'"]
        # initializing test string
        cleaned_result = j 
        cleaned_result = ''.join((filter(lambda x: x not in bad_chars, cleaned_result)))
        # print(i, cleaned_result) 
        if cleaned_result:
            lab_result = LabResult.objects.create(
                    lab_request_id = i,
                    result      = cleaned_result,
                    created_by  = request.user
                )
            lab_result.save()
            # Update LabResuest table and mark sent results as done
            LabRequest.objects.filter(id=i).update(done=True)

    template = "labs/lab_results.html"
    context = {"lab_request":lab_request}
    return render(request, template, context)




