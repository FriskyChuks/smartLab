from django.contrib import admin

from .models import Bill, Payment, PaymentDetail, Wallet


admin.site.register(Bill)
admin.site.register(Payment)
admin.site.register(PaymentDetail)
admin.site.register(Wallet)
