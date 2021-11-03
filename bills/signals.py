from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver

from radiology.models import RadiologyRequest
from labs.models import LabRequest
from patients.models import Patient

from .models import Bill, Wallet


# Radiology Bill
@receiver(post_save, sender=RadiologyRequest)
def post_save_radiology_bill(sender, instance, created, **kwargs):
    if created:
        Bill.objects.create(
            patient_id = instance.patient_id,
            radiology_request_id = instance.id,
            status = "pending",
            created_by_id = instance.created_by_id           
        )


# LAB Bill
@receiver(post_save, sender=LabRequest)
def post_save_lab_request_bill(sender, instance, created, **kwargs):
    if created:
        Bill.objects.create(
            patient_id = instance.patient_id,
            lab_request_id = instance.id,
            status = "pending",
            created_by_id = instance.created_by_id           
        )


# AUTO CREATE WALLET AFTER REGISTERING PATIENT
@receiver(post_save, sender=Patient)
def post_save_create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(
                patient_id=instance.id,
                account_balance=float(0.00),
                created_by_id=instance.created_by_id
            )

