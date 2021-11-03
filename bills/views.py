from django.http import request
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.decorators import allowed_users
from patients.models import Patient
from labs.models import LabRequest
from radiology.models import RadiologyRequest

from .models import Bill, Payment, PaymentDetail, Wallet


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','cashier'])
def billing_home_view(request):
    template = "bills/billing_home.html"
    context = {}
    return render(request, template, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','cashier'])
def pending_bills_view(request, pid): 
    rad_request_id = ""
    lab_request_id = ""
    bills = Bill.objects.filter(patient=pid, status="billed") | Bill.objects.filter(patient=pid, status="pending")
    radiology_bills = Bill.objects.filter(patient=pid, radiology_request__isnull=False, status='pending')
    lab_bills = Bill.objects.filter(patient=pid, lab_request__isnull=False, status='pending')

    # OUTSTANDING BILLS
    billed_rad_serv = Bill.objects.filter(patient=pid, radiology_request__isnull=False, status='billed')
    billed_lab_serv = Bill.objects.filter(patient=pid, lab_request__isnull=False, status='billed')
    
    # OUTSATANDING MEDICAL SERVICES
    outstanding_rad_serv = 0.00
    outstanding_lab_serv = 0.00

    # OUTSATANDING RADIOLOGY BILLS
    for billed_rad_serv in billed_rad_serv:
        rad_qty = billed_rad_serv.radiology_service.unit
        rad_price = billed_rad_serv.radiology_service.radiology_service.price
        outstanding_rad_serv = float(rad_price * rad_qty)
    # OUTSATANDING LAB BILLS
    for billed_lab_serv in billed_lab_serv:
        lab_price = billed_lab_serv.lab_request.test.price
        outstanding_lab_serv += float(lab_price)

    outstanding_bills = outstanding_rad_serv + outstanding_lab_serv

    radiology_total_bill = 0
    lab_total_bill = 0
            
    # Radiology Bill
    for obj in radiology_bills: 
        qty = obj.radiology_request.unit 
        radiology_subtotal = obj.radiology_request.radiology_service.price * qty
        radiology_total_bill += radiology_subtotal

     # LAB Bill
    for obj in lab_bills:
        lab_subtotal = obj.lab_request.test.price
        lab_total_bill += lab_subtotal 
    
    rad_total = radiology_total_bill
    lab_total = lab_total_bill
    total_bill = float(rad_total + lab_total)

    wallet = Wallet.objects.get(patient_id=pid)
    wallet_balance = wallet.account_balance

    pay_now = (float(total_bill) + float(outstanding_bills))

    patient = Patient.objects.get(id=pid)
    if request.method == "POST":
        if request.POST.get("bill_ID"):
            selected_bill = Payment()
            selected_bill.bill_id = request.POST.get("bill_ID")
            paid_amount = request.POST.get("pay_amount")
            if float(wallet_balance) < float(paid_amount):
                paid_amount = float(paid_amount) - float(wallet_balance)
                wallet = Wallet.objects.filter(patient_id=pid).update(account_balance=0.00)
            else:
                paid_amount = paid_amount
                wallet_balance = float(wallet_balance) - float(paid_amount)
                wallet = Wallet.objects.filter(patient_id=pid).update(account_balance=wallet_balance)
                
            pay_bill = selected_bill.bill_id
            pay_bill = str(pay_bill)
            # convert Comma separated string to a python list
            my_list = pay_bill.split(",")
           
            payment_obj = Payment.objects.create(amount_paid=paid_amount,action='receipt',created_by=request.user)
            if payment_obj:
                instance = payment_obj
                for item in my_list:
                    obj = PaymentDetail.objects.create(
                            bill_id         = item,
                            payment_id      = instance.id,
                            created_by      = request.user
                        )
                    obj.save()
                    Bill.objects.filter(id=item).update(status="paid")
                    bill = Bill.objects.get(id=item)
                
                    if bill.radiology_request:
                        rad_request_id=bill.radiology_request.id
                        print('Radio')
                        RadiologyRequest.objects.filter(id=rad_request_id).update(accepted=True)
                    if bill.lab_request:
                        lab_request_id=bill.lab_request.id
                        print('Lab')
                        LabRequest.objects.filter(id=lab_request_id).update(accepted=True)
                messages.success(request, "Payment processed successfully!")
                return redirect('pending_bills', pid=pid)
        
        else:
            messages.error(request, "Please check items to pay for!")

    template = "bills/bills.html"
    context = {
                "outstanding_bills":outstanding_bills,
                "bills":bills,
                "radiology_bills":radiology_bills,
                'lab_bills':lab_bills,
                'rad_total':rad_total,
                'lab_total':lab_total,
                'total_bill':total_bill,
                "pay_now":pay_now,
                'patient':patient,
                'wallet_balance':wallet_balance
              }
    return render(request, template, context)



@login_required(login_url="auth_login")
def load_wallet_view(request, pid):
    user = request.user
    patient = Patient.objects.get(id=pid)
    patient_wallet = Wallet.objects.get(patient_id=pid)
    initial_balance = patient_wallet.account_balance

    if request.method == 'POST':
        deposit_amount = request.POST.get('amount')
        if deposit_amount != '' and float(deposit_amount) > float(0):
            initial_balance = float(initial_balance) + float(deposit_amount)
            payment = Payment.objects.create(amount_paid=deposit_amount, action='deposit', created_by=user)
            object = Wallet.objects.filter(patient_id=pid).update(account_balance=initial_balance, created_by=request.user)
            messages.success(request, "Deposit was successful!")
            return redirect('wallet', pid=pid)
        else:
            messages.error(request, "Please enter POSITIVE VALUES only, Thanks!")

    template = "bills/wallet.html"
    context = {"patient":patient, "initial_balance":initial_balance}
    return render(request, template, context)


@login_required(login_url="auth_login")
def patient_account_info_view(request, pid):
    patient = Patient.objects.get(id=pid)
    patient_wallet = Wallet.objects.get(patient_id=pid)
    initial_balance = patient_wallet.account_balance

    template = "bills/patient_account_info.html"
    context = {"patient":patient, "initial_balance":initial_balance}
    return render(request, template, context)

    
    