from django.conf import settings
from django.db import models

from patients.models import Patient
from radiology.models import RadiologyRequest
from radiology.models import RadiologyRequest
from labs.models import LabRequest

User = settings.AUTH_USER_MODEL


BILL_STATUS = (
        ("pending","Pending"),
        ("billed","Billed"),
        ("paid","Paid")
    )


PAY_ACTION = (
        ("deposit","Deposit"),
        ("invoice","Invoice"),
        ("receipt","Receipt"),
    )


class Bill(models.Model):
    patient             = models.ForeignKey(Patient, on_delete=models.CASCADE)
    radiology_request   = models.ForeignKey(RadiologyRequest, on_delete=models.CASCADE, blank=True, null=True)
    lab_request         = models.ForeignKey(LabRequest, on_delete=models.CASCADE, blank=True, null=True)
    status              = models.CharField(max_length=10, choices=BILL_STATUS, default='pending')
    created_by          = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created        = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_updated        = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        if self.radiology_request:
            return f"{self.radiology_request}"
        else:
            return f"{self.lab_request}"


class Payment(models.Model):
    amount_paid     = models.DecimalField(decimal_places=2, default='00.00', max_digits=20)
    action          = models.CharField(max_length=20, choices=PAY_ACTION)
    created_by      = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created    = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return str(self.amount_paid)


class PaymentDetail(models.Model):
    bill            = models.ForeignKey(Bill, on_delete=models.CASCADE)
    payment         = models.ForeignKey(Payment, on_delete=models.CASCADE)
    created_by      = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created    = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_updated    = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        if self.bill.lab_request:
            return f"{self.bill.lab_request} {self.bill.lab_request.test.price}"
        else:
            return f"{self.bill.radiology_service} {self.bill.radiology_service.radiology_service.price}"


class Wallet(models.Model):
    patient         = models.OneToOneField(Patient, on_delete=models.CASCADE, null=True, blank=True)
    account_balance = models.DecimalField(decimal_places=2, default='00.00', max_digits=20)
    created_by      = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created    = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_updated    = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return f"N{self.account_balance} || {self.patient.id}"



