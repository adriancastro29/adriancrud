from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'buyer_name',
            'buyer_contact',
            'buyer_address',
        ]
