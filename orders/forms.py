from django import forms
from django.forms import ModelForm

from orders.models import Order


class CouponApplyForm(forms.Form):
    code = forms.CharField()
    

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','address', 'ostan', 'shahrestan', 'postalcode', 'description','email']
