from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import RadiologyRequest


@receiver(post_save, sender=RadiologyRequest)
def post_save_update_sub_total(sender, instance, created, **kwargs):
    if created:
        print('CREATED')
        price = instance.radiology_service.price
        qty = instance.unit
        new_subtotal = price * qty
        print(price)
        print(qty)
        print('subtotal', new_subtotal)
        obj=RadiologyRequest.objects.filter(id=instance.id).update(subtotal=new_subtotal)
        
