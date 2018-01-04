from django import forms
from django.forms import ModelForm, inlineformset_factory
from django.core.exceptions import ValidationError
import datetime

from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(label='Username:', required=True)
    password = forms.CharField(label='Password:', required=True, widget=forms.PasswordInput)

"""
class AddStoreForm(forms.Form):
    store_code = forms.CharField(label='Store Code:', max_length=3, required=True)
    store_name = forms.CharField(label='Store Name:', max_length=100, required=True)
    store_region = forms.CharField(label='Store Region:', max_length=70, required=True)
    store_address = forms.CharField(label='Store Address', max_length=255, required=True, widget=forms.Textarea)
"""

class AddItemForm(forms.Form):
    item_SKU = forms.CharField(label='Item SKU:', required=True, help_text='000000')
    item_name = forms.CharField(label='Item Name:', required=True)
    item_unit_price = forms.CharField(label='Unit Price:', required=True, help_text='Kindly round up to nearest tens i.e. 43.5 -> 44')
    item_retail_price = forms.CharField(label='Retail Price:', required=True)

class AdviceCreator(forms.Form):
    #store_code = forms.CharField(label='Store Code:', max_length=3, required=True)
    #invoice_number = forms.CharField(label='Invoice Number: ', max_length=11, required=True)
    #invoice_date = forms.DateField(label='Invoice Date: ', required=True, help_text='YYYY-MM-DD')
    #payment_due = forms.DateField(label='Payment Due:', required=True, help_text='YYYY-MM-DD')
    #adviceCreateDate = forms.DateField(label='To be created on', required=True, initial=datetime.date.today)
    adviceCreator = forms.CharField(label='To be created by', required=True)

class EditAdvItemsForm(forms.Form):
    item_qty = forms.CharField(widget=forms.TextInput(attrs={}))

"""
class EditAdviceForm(ModelForm):
    class Meta:
        model = SalesAdvice
        fields = '__all__'
        exclude = ()
"""

class AddAdviceForm(ModelForm):
    adviceCreator = forms.CharField(widget=forms.TextInput(attrs={'readonly':'True'}))
    adviceCreateDate = forms.CharField(widget=forms.TextInput(attrs={'readonly':'True'}))
    class Meta:
        model = SalesAdvice
        fields = ['invoiceNumber', 'invoiceDate', 'paymentDueDate', 'store', 'adviceCreator', 'adviceCreateDate']

class AddStoreForm(ModelForm):
    store_name = forms.CharField(widget=forms.TextInput(attrs={'size':50}))
    store_region = forms.CharField(widget=forms.TextInput(attrs={'size':50}))
    class Meta:
        model = Store
        fields = ['store_code', 'store_name', 'store_region', 'store_address',]

class EditStoreForm(ModelForm):
    store_name = forms.CharField(widget=forms.TextInput(attrs={'size':50}))
    store_region = forms.CharField(widget=forms.TextInput(attrs={'size':50}))
    class Meta:
        model = Store
        fields = ['store_name', 'store_region', 'store_address',]
        exclude = ['store_code']

class EditAdviceItemsForm(ModelForm):
    itemQty = forms.CharField(widget=forms.TextInput(attrs={'id':'True'}))
    class Meta:
        model = SalesAdviceItems
        fields = ['itemQty']
        exclude =['itemUnitCost', 'item_id', 'invoiceNumber_id', 'itemCost']

class AddReceivingAdviceForm(ModelForm):
    adviceCreator = forms.CharField(widget=forms.TextInput(attrs={'readonly':'True'}))
    adviceCreateDate = forms.CharField(widget=forms.TextInput(attrs={'readonly':'True'}))
    class Meta:
        model = ReceivingAdvice
        fields = ['receiptNumber', 'receiptDate', 'store', 'adviceCreator', 'adviceCreateDate']

class EditItem(ModelForm):
    item_name = forms.CharField(widget=forms.TextInput(attrs={'size':50}))
    class Meta:
        model = Product
        fields = ['item_name', 'item_unit_price', 'item_retail_price']
        exclude = ['item_SKU']
