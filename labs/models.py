from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

from patients.models import Patient


class LabUnit(models.Model):
    title        = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description  = models.CharField(max_length=255, blank=True, null=True)
    created_by   = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated      = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title


class CompoundTest(models.Model):
    lab_unit            = models.ForeignKey(LabUnit, on_delete=models.CASCADE, blank=True, null=True)
    title               = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description         = models.CharField(max_length=255, blank=True, null=True)
    created_by          = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_created        = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated             = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title


class LabTest(models.Model):
    lab_unit            = models.ForeignKey(LabUnit, on_delete=models.CASCADE, blank=True, null=True)
    compound_test       = models.ForeignKey(CompoundTest, on_delete=models.CASCADE, blank=True, null=True)
    title               = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description         = models.CharField(max_length=255, blank=True, null=True)
    cost_price          = models.DecimalField(max_digits=65, decimal_places=2, default=00.00)
    price               = models.DecimalField(max_digits=65, decimal_places=2, default=00.00)
    active              = models.BooleanField(default=True)
    created_by          = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_created        = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated             = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title


class LabRequest(models.Model):
    patient             = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)
    test                = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    accepted            = models.BooleanField(default=False)
    decline             = models.BooleanField(default=False)
    done                = models.BooleanField(default=False)
    created_by          = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_created        = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated             = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.test)


class LabResult(models.Model):
    lab_request         = models.ForeignKey(LabRequest, on_delete=models.CASCADE, blank=True, null=True)
    result              = models.CharField(max_length=225)
    created_by          = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_created        = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated             = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.result)
