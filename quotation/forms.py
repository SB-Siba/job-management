# quotation/forms.py

from django import forms
from .models import Quotation, QuotationItem, Invoice
from django.forms import modelformset_factory
from django.core.validators import RegexValidator
from .models import Item, Invoice, Client, Job, Employee


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['sr_no', 'name', 'description', 'quantity', 'amount']
        widgets = {
            'sr_no': forms.TextInput(attrs={'readonly': 'readonly'}),  # Set sr_no as read-only
            'description': forms.TextInput(attrs={'placeholder': 'Enter item description'}),
        }

ItemFormSet = modelformset_factory(
    Item, 
    fields=('sr_no', 'name', 'description', 'quantity', 'amount'), 
    extra=1, 
    can_delete=True
)


class QuotationForm(forms.ModelForm):
    TITLE_CHOICES = [
        ('Mr.', 'Mr.'),
        ('Mrs.', 'Mrs.'),
    ]

    title = forms.ChoiceField(choices=TITLE_CHOICES, required=True)

     # Enforce 10-digit phone number validation
    phone_number = forms.CharField(
        max_length=10,
        min_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit phone number.')],
        error_messages={'invalid': 'Enter a valid 10-digit phone number.'}
    )
    class Meta:
        model = Quotation
        fields = ['company_name', 'address', 'phone_number', 'title', 'first_name', 'middle_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_name'].widget.attrs.update({'placeholder': 'Enter company name'})
        self.fields['address'].widget.attrs.update({'placeholder': 'Enter address'})
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'Enter phone number'})
        self.fields['title'].widget.attrs.update({'placeholder': 'Select title'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter first name'})
        self.fields['middle_name'].widget.attrs.update({'placeholder': 'Enter middle name (optional)'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter last name'})


class QuotationItemForm(forms.ModelForm):
    class Meta:
        model = QuotationItem
        fields = ['item', 'quantity']


class InvoiceForm(forms.Form):
    company_name = forms.CharField(max_length=255)
    address = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)
    client = forms.ModelChoiceField(queryset=Client.objects.all(), required=False)
    job = forms.ModelChoiceField(queryset=Job.objects.all(), required=False)
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), required=False)
