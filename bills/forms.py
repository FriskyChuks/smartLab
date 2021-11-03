from django import forms
from django.db import models

from .models import Bill, Payment, Wallet


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['amount']

        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),           
        } 