from django import forms
from .models import Quotation, Invoice, Item, Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'address']

class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['client', 'due_date', 'total_amount']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['description', 'quantity', 'unit_price']

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['quotation', 'due_date', 'paid']

